.. _configuration_services:

Services
========

GPP-Publicatiebank is designed to operate in a micro-service environment, which broadly
means that it talks to other APIs to be able to function correctly - see
:ref:`installation_requirements` for some more background information and things that
need to be arranged in those external services.

The services configuration in GPP-Publicatiebank stores the connection and
authentication details for those external services.

General instructions
--------------------

To view and manage services, navigate to **Admin** > **Configuration** > **Services**.

The list shows an overview of configured services, displaying the label/name, the kind
of service and the base URL where it is hosted.

In the top right of the page, you can click the **Service toevoegen** button to add a
new service. To edit an existing service, click its label, which takes you to the
edit page.

.. _configuration_services_documents_api:

Documents API configuration
---------------------------

Currently, GPP-Publicatiebank depends on one required service: the
`Documents API <https://vng-realisatie.github.io/gemma-zaken/standaard/documenten/>`_.

What you'll need
~~~~~~~~~~~~~~~~

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
    - ``Client ID`` and ``Secret``: enter the credentials obtained from the requirements
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
