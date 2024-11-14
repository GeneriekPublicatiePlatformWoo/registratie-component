.. _admin_publicaties_index:

Publicaties
============

Onder het menu-item "Publicaties" en op het dashboard onder het kopje "Publicaties" wordt toegang geboden tot het beheer van:

* Documenten
* Publicaties

Door hierop te klikken wordt het desbetreffende beheerscherm geopend.

Documenten
-----------

Een *document* bestaat uit een bestand (bijvoorbeeld een PDF) en metadata. Een *document* hoort altijd bij een publicatie.

In het beheerscherm van de *documenten* wordt een lijst getoond van alle *document*-registraties, die zijn opgeslagen in het "WOO Publicaties"-component.
Op dit scherm zijn de volgende acties mogelijk:

* Rechtboven zit een knop **document toevoegen** waarmee een registratie toegevoegd kan worden.
* Bovenaan zit een zoekveld met en knop **Zoeken** waarmee in de registraties gezocht kan worden.
* Direct onder de zoekbalk zit de mogelijkheid om de lijst te **filteren op een specifieke registratiedatum**.
* Daaronder zit de mogelijkheid om **eenzelfde actie uit te voeren over meerdere documentregistraties**. Op dit moment wordt alleen de actie **Geselecteerde documenten verwijderen** ondersteund. Merk op dat het mogelijk is om in de lijst één of meerdere *document*-regsitraties aan te vinken.
* Onder de (bulk-)actie staat de lijst met *document*-registraties. Door op de kolomtitels te klikken kan de lijst **alfabetisch of chronologisch geordend** worden.
* Rechts naast de lijst bestaat de mogelijkheid om deze te **filteren op registratiedatum en/of creatiedatum**.
* Bij een *document*-registratie kan op de `officiële titel` geklikt worden om **de details in te zien** en deze eventueel **te wijzigen**.
* Bij een *document*-registratie kan op **Show logs** (rechter kolom) geklikt worden om direct de :ref:`audit trail<admin_logging_index>` in te zien.

Wanneer bij een *document*-registratie op  de `officiële titel` wordt geklikt, wordt een scherm geopend met de *document*-details.
Hierop zien we:

* **Alle metadatavelden**. Deze lichten we hieronder toe.
* Rechtsboven een knop **Show logs**. Deze toont de volledige :ref:`audit trail<admin_logging_index>` van de *document*-registratie.
* Rechtsboven een knop **Geschiedenis**. Deze toont de beheer-handelingen die vanuit de Admin-interface zijn uitgevoerd op de registratie.
* Linksonder de mogelijkheid om **wijzigingen op te slaan**. Er kan voor gekozen worden om na het opslaan direct een nieuwe registratie aan te maken of om direct de huidige registratie nogmaals te wijzigen.
* Rechtsonder de mogelijkheid om de registratie te **verwijderen**.

Op een *document*-registratie zijn de volgende metadata beschikbaar. Op het scherm wordt verplichte velden **dikgedrukt** weergegeven.

**Algemene velden**

* ``Publicatie``. Het *document* moet hier gekoppeld worden aan een bestaande of nieuwe *publicatie*
* ``Identificatie``. Het unieke kenmerk dat intern aan het *document* is toegekend, bijvoorbeeld door het zaaksysteem of het DMS. (DiWoo : ``identifier``)
* ``Officiële titel``. De (mogelijk uitgebreide) officiële titel van het document. (DiWoo : ``officieleTitel``)
* ``Verkorte titel``. De verkorte titel / citeertitel van het document. (DiWoo : ``verkorteTitel``)
* ``Omschrijving``. Een beknopte omschrijving / samenvatting van de inhoud van het document. (DiWoo : ``omschrijving``)
* ``Creatiedatum``. De datum waarop het document gecreëerd is. Deze ligt doorgaans voor of op de registratiedatum.  (DiWoo : ``creatiedatum``)
* ``Bestandsformaat``. *In ontwikkeling* (DiWoo : ``format``)
* ``Bestandsnaam``. Naam van het bestand zoals deze op de harde schijf opgeslagen wordt.
* ``Bestandsomvang`` Bestandsgrootte, in aantal bytes.
* ``Status``. De publicatiestatus van het document (DiWoo : ``publicatiestatus``)
* ``Geregistreerd op``. De niet-wijzigbare datum en tijd waarop het document nieuw is toegevoegd.
* ``Laatst gewijzigd op``. De niet-wijzigbare datum en tijd waarop het document voor het laatst gewijzigd was.
* ``UUID``. Een niet-wijzigbaar, automatisch toegekend identificatiekenmerk. (DiWoo : ``identifier``)

**Documenthandelingen**

Documenthandelingen zijn verplichte gegevens in de DiWoo-standaard.

* ``Soort handeling``. De soort documenthandeling die op dit document plaatsgevonden heeft. Dit wordt nu automatisch gezet.
* ``Vanaf``. Het gerapporteerde moment van de documenthandeling, deze is gelijk aan de documentregistratiedatum.
* ``Was geassocieerd met``. De organisatie die deze handeling heeft uitgevoerd, afgeleid uit de verantwoordelijke
  organisatie van de gerelateerde publicatie.

**Documenten-API-koppeling**

* ``Documents API Service``. Systeemveld, bevat de verwijzing naar het bestand in de Documenten API.
* ``Document UUID``. Systeemveld, bevat de verwijzing naar het bestand in de Documenten API.
* ``Documentvergrendelingscode``. systeemveld, bevat de vergrendelingscode van een bestand in de Documenten API.

Publicaties
------------

Een *publicatie* bestaat uit een aantal gegevens met doorgaans een of meerdere *documenten* (zie hierboven).

.. tip::

    Het toevoegen van een document aan een *publicatie* is niet verplicht. Daarmee kan
    voldaan worden aan:

        (...) Van een gehele niet-openbaarmaking doet het bestuursorgaan mededeling op
        de wijze en het tijdstip waarop het niet-openbaar gemaakte stuk openbaar zou
        zijn gemaakt.

        -- `Wet open overheid, art. 3.3, lid 8`_

    In het veld ``Omschrijving`` kan de mededeling opgenomen worden.

In het beheerscherm van de *publicaties* wordt een lijst getoond van alle *publicatie*-registraties, die zijn opgeslagen in het "WOO Publicaties"-component.
Op dit scherm zijn de volgende acties mogelijk:

* Rechtboven zit een knop **publicatie toevoegen** waarmee een registratie toegevoegd kan worden.
* Bovenaan zit een zoekveld met en knop **Zoeken** waarmee in de registraties gezocht kan worden.
* Direct onder de zoekbalk zit de mogelijkheid om de lijst te **filteren op een specifieke registratiedatum**.
* Daaronder zit de mogelijkheid om **eenzelfde actie uit te voeren over meerdere publicaties**. Op dit moment wordt alleen de actie **Geselecteerde publicaties verwijderen** ondersteund. Merk op dat het mogelijk is om in de lijst één of meerdere *publicatie*-regsitraties aan te vinken.
* Onder de (bulk-)actie staat de lijst met *publicatie*-registraties. Door op de kolomtitels te klikken kan de lijst **alfabetisch of chronologisch geordend** worden.
* Rechts naast de lijst bestaat de mogelijkheid om deze te **filteren op registratiedatum**.
* Bij een *publicatie*-registratie kan op de `officiële titel` geklikt worden om **de details in te zien** en deze eventueel **te wijzigen**.
* Bij een *publicatie*-registratie kan op **Show documents** (rechter kolom) geklikt worden om direct de gekoppelde *documenten* in te zien.
* Bij een *publicatie*-registratie kan op **Show logs** (rechter kolom) geklikt worden om direct de :ref:`audit trail<admin_logging_index>` in te zien.

Wanneer bij een *publicatie*-registratie op  de `officiële titel` wordt geklikt, wordt een scherm geopend met de *publicatie*-details.
Hierop zien we:

* **Alle metadatavelden**. Deze lichten we hieronder toe.
* Rechtsboven een knop **Show logs**. Deze toont de volledige :ref:`audit trail<admin_logging_index>` van de *publicatie*-registratie.
* Rechtsboven een knop **Geschiedenis**. Deze toont de beheer-handelingen die vanuit de Admin-interface zijn uitgevoerd op de registratie.
* Onder de metadatavelden de gekoppelde *documenten*. De metadata die getoond en gewijzigd kan worden komt overeen met zoals hierboven beschreven. Een *document* kan ook verwijderd worden door dit aan de rechterzijde aan te vinken. Let op, dit betreft niet alleen het ontkoppelen van een *document*, maar de volledige verwijdering!
* Onder de *documenten* de mogelijkheid om **een nieuw document** toe te voegen aan de *publicatie*.
* Linksonder de mogelijkheid om **wijzigingen op te slaan**. Er kan voor gekozen worden om na het opslaan direct een nieuwe registratie aan te maken of om direct de huidige registratie nogmaals te wijzigen.
* Rechtsonder de mogelijkheid om de registratie te **verwijderen**.

Op een *publicatie*-registratie zijn de volgende metadata beschikbaar. Op het scherm wordt verplichte velden **dikgedrukt** weergegeven.

* ``Informatiecategorieën`` De informatiecategorieën die het soort informatie verduidelijken binnen de publicatie (DiWoo : ``informatieCategorieen``)
* ``Publisher`` De organisatie die de publicatie heeft gepubliceerd. (DiWoo : ``publisher``)
* ``Verantwoordelijke`` De organisatie die de verantwoordelijk is voor de publicatie. (DiWoo : ``verantwoordelijke``)
* ``Opsteller`` De organisatie die de publicatie opgesteld heeft. (DiWoo : ``opsteller``)
* ``Officiële titel``. De (mogelijk uitgebreide) officiële titel van de publicatie. (DiWoo : ``officieleTitel``)
* ``Verkorte titel``. De verkorte titel / citeertitel van de publicatie. (DiWoo : ``verkorteTitel``)
* ``Omschrijving``. Een beknopte omschrijving / samenvatting van de publicatie. (DiWoo : ``omschrijving``)
* ``Status``. De publicatiestatus van de publicatie **LET OP**: wanneer de publicatie ingetrokken wordt, worden de gepubliceerde documenten ook ingetrokken. (DiWoo : ``publicatiestatus``)
* ``Publicatie``. Het *document* moet hier gekoppeld worden aan een bestaande of nieuwe *publicatie*
* ``UUID``. Een niet-wijzigbaar, automatisch toegekend identificatiekenmerk. (DiWoo : ``identifier``)
* ``Geregistreerd op``. De niet-wijzigbare datum en tijd waarop de publicatie nieuw is toegevoegd.
* ``Laatst gewijzigd op``. De niet-wijzigbare datum en tijd waarop de publicatie voor het laatst gewijzigd was.

.. _Wet open overheid, art. 3.3, lid 8: https://wetten.overheid.nl/BWBR0045754/2024-10-01#Hoofdstuk3_Artikel3.3
