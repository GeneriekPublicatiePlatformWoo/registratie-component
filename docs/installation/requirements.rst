.. _installation_requirements:

Requirements
============

Documents API
-------------

The Woo Publications component uses the VNG
`Documents API <https://vng-realisatie.github.io/gemma-zaken/standaard/documenten/>`_
standard for the actual persisting of (published) documents. This means that you must
provide or provision an API provider that implements this standard. You must also
configure some authorization aspects in the
`Authorisations API <https://vng-realisatie.github.io/gemma-zaken/standaard/autorisaties/>`_
used by the chosen Documents API.

What you'll need
~~~~~~~~~~~~~~~~

* Access to the admin environment of the Woo Publications component, e.g.
  ``https://woo-publications.example.com/admin/``.
* The API root URL, e.g. ``https://api.example.com/documenten/api/v1/``
* API credentials: a client ID and secret
* RSIN of the organisation that will own the documents in the Documents API. Typically
  this will be the RSIN of your municipality.

Configuration in the registration component
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Navigate to the **Admin** environment.
2. In the menu, navigate to **Configuration** > **Services**.
3. Click the **Add service** button in the top right of the screen.
4. Fill out the form fields:

    - ``Label``: a label so you can recognize the service in a choice list, e.g. "Documents API".
    - ``Type``: select "DRC (Informatieobjecten)"
    - ``API root URL``: enter the obtained base URL of the API, e.g.
      ``https://api.example.com/documenten/api/v1/`` from the examples in the previous
      section.
    - ``Client ID`` and ``Secret``: enter the credentials obtained from the reuqirements
      in the previous section.
    - ``Authorization type``: select "ZGW client_id + secret"

5. Save the changes.
6. Now, we must instruct the application to use this service. Navigate to
   **Configuration** > **General configuration**.
7. Fill out the form fields:

    - ``Documents API service``: select the service that you created in step 4.
    - ``RSIN organisation``: enter the RSIN obtained from the requirements in the
      previous section.

8. Save the changes.

Configuration for the Authorisations API
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The Woo Publications component uses the
:ref:`information categories <admin_metadata_index_information_categories>` to describe
the document type ("informatieobjecttype") for the Documents API. The permissions to the
Documents API are based on these document types.

**Permission scopes**

* ``documenten.aanmaken``
* ``documenten.bijwerken``

Woo Publications requires the scopes listed above, for all information categories.

The API resource URLs for all information categories are available on a page in the
admin. Navigate to **Admin** > **Metadata** > **Information categories**. In the top
right, click the **View API resource URLs** button.

The list page displays all information categories, grouped by their origin with the
fully qualified resource URLs required by the Authorisations API.

Known applications/products providing a Documents API
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* `Open Zaak <https://open-zaak.readthedocs.io/>`_

.. tip:: If you're a vendor, please create a PR to add your product to this list.

Reverse proxy
-------------

It's recommended to set up a reverse proxy (like nginx or a Kubernetes ingress/gateway)
before the application container, as these pieces of software are designed to scale
well. They can prevent the application containers from becoming overloaded.

Configuring a reverse proxy or Kubernetes cluster is out of scope for this project, but
some implementation details are relevant and they are listed below.

Allow streaming of document downloads
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Uploaded documents in the API are also downloaded again - especially by the National
Search Index (DiWoo) which indexes the documents, but ultimately also by interested
parties like citizens, journalists...

Our download API endpoint (``/api/v1/documenten/:uuid/download``) sends a response
header ``X-Accel-Buffering: off`` to the reverse proxy to promote synchronous streaming
to the client. Certain nginx (or possibly other reverse proxy implementations)
configuration can lead to this header being ignored.

Most of the time (small files, fast networks...) this shouldn't be a problem, but
especially with larger files (1GB+) being downloaded over slow connections it's possible
the internal nginx buffers fill up and the application container times out when trying
to write the response back to nginx. This results in downloads getting aborted after
about 1GB. Disabling buffering prevents this problem by writing/streaming directly to
the client.

Alternative configurations could be to disable buffering for these endpoints in
particular, in which case the response header can be safely ignored too.

.. seealso:: For all the gritty details, you can read more in
   `github issue 164 <https://github.com/GPP-Woo/GPP-publicatiebank/issues/164>`_.
