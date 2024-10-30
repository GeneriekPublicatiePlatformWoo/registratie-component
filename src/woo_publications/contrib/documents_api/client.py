from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from uuid import UUID

from furl import furl
from zgw_consumers.client import build_client
from zgw_consumers.models import Service
from zgw_consumers.nlx import NLXClient

from .typing import EIOCreateBody, EIOCreateResponseBody

__all__ = ["get_client"]


def get_client(service: Service) -> DocumentenClient:
    return build_client(service, client_factory=DocumentenClient)


@dataclass
class FilePart:
    uuid: UUID
    order: int
    size: int


@dataclass
class Document:
    uuid: UUID
    lock: str
    file_parts: list[FilePart]


def _extract_uuid(url: str) -> UUID:
    path = furl(url).path
    last_part = path.segments[-1]
    return UUID(last_part)


class DocumentenClient(NLXClient):
    """
    Implement interactions with a Documenten API.

    Requires Documenten API 1.1+ since we use the large file uploads mechanism.
    """

    def create_document(
        self,
        *,
        identification: str,
        source_organisation: str,
        document_type_url: str,
        creation_date: date,
        title: str,
        filesize: int,
        filename: str,
        author: str = "WOO registrations",
        content_type: str = "application/octet-stream",
        description: str = "",
    ) -> Document:
        data: EIOCreateBody = {
            "identificatie": identification,
            "bronorganisatie": source_organisation,
            "informatieobjecttype": document_type_url,
            "creatiedatum": creation_date.isoformat(),
            "titel": title,
            "auteur": author,
            "status": "definitief",
            "formaat": content_type,
            "taal": "dut",
            "bestandsnaam": filename,
            # do not post any data, we use the "file parts" upload mechanism
            "inhoud": None,
            "bestandsomvang": filesize,
            "beschrijving": description[:1000],
            "indicatieGebruiksrecht": False,
        }

        response = self.post("enkelvoudiginformatieobjecten", json=data)
        response.raise_for_status()

        response_data: EIOCreateResponseBody = response.json()

        # translate into the necessary metadata for us to track everything
        file_parts = [
            FilePart(
                uuid=_extract_uuid(part_data["url"]),
                order=part_data["volgnummer"],
                size=part_data["omvang"],
            )
            for part_data in response_data["bestandsdelen"]
        ]

        return Document(
            uuid=_extract_uuid(response_data["url"]),
            lock=response_data["lock"],
            file_parts=file_parts,
        )
