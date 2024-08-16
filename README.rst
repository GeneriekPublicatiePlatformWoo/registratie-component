==================
odrc
==================

:Version: 0.1.0
:Source: https://github.com/maykinmedia/odrc
:Keywords: ``<keywords>``

|docs| |docker|

``<oneliner describing the project>``
(`English version`_)

Ontwikkeld door `Maykin B.V.`_ in opdracht ``<client>``.


Introductie
===========

``<describe the project in a few paragraphs and briefly mention the features>``


API specificatie
================

|lint-oas| |generate-sdks| |generate-postman-collection|

==============  ==============  =============================
Versie          Release datum   API specificatie
==============  ==============  =============================
latest          n/a             `ReDoc <https://redocly.github.io/redoc/?url=https://raw.githubusercontent.com/maykinmedia/odrc/master/src/odrc/api/openapi.yaml>`_,
                                `Swagger <https://petstore.swagger.io/?url=https://raw.githubusercontent.com/maykinmedia/odrc/master/src/odrc/api/openapi.yaml>`_,
                                (`verschillen <https://github.com/maykinmedia/odrc/compare/0.1.0..master#diff-b9c28fec6c3f3fa5cff870d24601d6ab7027520f3b084cc767aefd258cb8c40a>`_)
0.1.0           YYYY-MM-DD      `ReDoc <https://redocly.github.io/redoc/?url=https://raw.githubusercontent.com/maykinmedia/odrc/0.1.0/src/odrc/api/openapi.yaml>`_,
                                `Swagger <https://petstore.swagger.io/?url=https://raw.githubusercontent.com/maykinmedia/odrc/0.1.0/src/odrc/api/openapi.yaml>`_
==============  ==============  =============================

Vorige versies worden nog 6 maanden ondersteund nadat de volgende versie is 
uitgebracht.

Zie: `Alle versies en wijzigingen <https://github.com/maykinmedia/odrc/blob/master/CHANGELOG.rst>`_


Ontwikkelaars
=============

|build-status| |coverage| |black| |docker| |python-versions|

Deze repository bevat de broncode voor odrc. Om snel aan de slag
te gaan, raden we aan om de Docker image te gebruiken. Uiteraard kan je ook
het project zelf bouwen van de broncode. Zie hiervoor
`INSTALL.rst <INSTALL.rst>`_.

Quickstart
----------

1. Download en start odrc:

   .. code:: bash

      wget https://raw.githubusercontent.com/maykinmedia/odrc/master/docker-compose.yml
      docker-compose up -d --no-build
      docker-compose exec web src/manage.py loaddata demodata
      docker-compose exec web src/manage.py createsuperuser

2. In de browser, navigeer naar ``http://localhost:8000/`` om de beheerinterface
   en de API te benaderen.


Links
=====

* `Documentatie <https://TODO>`_
* `Docker image <https://hub.docker.com/r/maykinmedia/odrc>`_
* `Issues <https://github.com/maykinmedia/odrc/issues>`_
* `Code <https://github.com/maykinmedia/odrc>`_
* `Community <https://TODO>`_


Licentie
========

Copyright © Maykin 2024

Licensed under the EUPL_


.. _`English version`: README.EN.rst

.. _`Maykin B.V.`: https://www.maykinmedia.nl

.. _`Objecttypen API`: https://github.com/maykinmedia/objecttypes-api

.. _`EUPL`: LICENSE.md

.. |build-status| image:: https://github.com/maykinmedia/odrc/workflows/ci/badge.svg?branch=master
    :alt: Build status
    :target: https://github.com/maykinmedia/odrc/actions?query=workflow%3Aci

.. |docs| image:: https://readthedocs.org/projects/odrc-and-objecttypes-api/badge/?version=latest
    :target: https://odrc-and-objecttypes-api.readthedocs.io/
    :alt: Documentation Status

.. |coverage| image:: https://codecov.io/github/maykinmedia/odrc/branch/master/graphs/badge.svg?branch=master
    :alt: Coverage
    :target: https://codecov.io/gh/maykinmedia/odrc

.. |black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :alt: Code style
    :target: https://github.com/psf/black

.. |docker| image:: https://img.shields.io/docker/v/maykinmedia/odrc?sort=semver
    :alt: Docker image
    :target: https://hub.docker.com/r/maykinmedia/odrc

.. |python-versions| image:: https://img.shields.io/badge/python-3.11%2B-blue.svg
    :alt: Supported Python version

.. |lint-oas| image:: https://github.com/maykinmedia/odrc/workflows/lint-oas/badge.svg
    :alt: Lint OAS
    :target: https://github.com/maykinmedia/odrc/actions?query=workflow%3Alint-oas

.. |generate-sdks| image:: https://github.com/maykinmedia/odrc/workflows/generate-sdks/badge.svg
    :alt: Generate SDKs
    :target: https://github.com/maykinmedia/odrc/actions?query=workflow%3Agenerate-sdks

.. |generate-postman-collection| image:: https://github.com/maykinmedia/odrc/workflows/generate-postman-collection/badge.svg
    :alt: Generate Postman collection
    :target: https://github.com/maykinmedia/odrc/actions?query=workflow%3Agenerate-postman-collection
