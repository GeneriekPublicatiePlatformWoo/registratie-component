.. _developers_troubleshooting:

Troubleshooting
===============

Some common problems can occur during (local) development. We've summarized those here
with a description of the problem and solution.

Can't bind to port 8000 (``docker compose`` or ``runserver``)
-------------------------------------------------------------

**Likely solution**

Ensure you only bring up the Open Zaak service:

.. code-block:: bash

    docker compose up openzaak-web

**Cause**

The ``docker-compose.yml`` also includes the Woo-Publications service itself, which is
mutually exclusive with running it via ``runserver`` on the default port (8000).

You can also run ``runserver`` on a different port instead of the default.


Creating documents fails with with ``HTTPError`` (1)
----------------------------------------------------

**Likely solution**

Ensure that you're making API calls to ``host.docker.internal`` and not ``localhost``
or ``127.0.0.1``. You also need to have this entry in your ``/etc/hosts`` file - see
:ref:`install_etc_hosts`.

**Cause**

When POST-ing a document to the Woo-Publications API endpoint exposed via ``runserver``,
you can get an HTTP 400 error from Open Zaak if the wrong host is used (``localhost``
or ``127.0.0.1``). This is because those hosts point to the Open Zaak container itself
rather than the development server on the host system. You must use the
``host.docker.internal`` hostname so that Open Zaak uses the Docker gateway instead.

In the docker compose logs this looks similar to:

.. code-block:: none

    openzaak-web-1  | rest_framework.exceptions.ValidationError: {'informatieobjecttype': [ErrorDetail(string='De service voor deze URL is niet bekend.', code='unknown-service')]}


Creating documents fails with with ``HTTPError`` (2)
----------------------------------------------------

**Likely solution**

Check that you are binding to all ports with ``runserver``:

.. code-block:: bash

    src/manage.py runserver 0.0.0.0:8000

**Cause**

When POST-ing a document to the Woo-Publications API endpoint exposed via ``runserver``,
you can get an HTTP 400 error from Open Zaak. In the docker compose logs this looks
similar to:

.. code-block:: none

    openzaak-web-1  | rest_framework.exceptions.ValidationError: {'informatieobjecttype': [ErrorDetail(string='Bad URL "http://host.docker.internal:8000/catalogi/api/v1/informatieobjecttypen/b84c3b0d-a471-48f5-915f-7fbd8b94188f" - object could not be fetched. This *may* be because you have insufficient read permissions.', code='bad-url')]}

