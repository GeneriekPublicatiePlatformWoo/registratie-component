.. _installation_docker_compose:

Install using Docker Compose
============================

This installation is meant for people who want to just try out WOO Publications on
their own machine.

A `Docker Compose`_ file is available to get the app up and running in minutes.
It contains 'convenience' settings, which means that no additional
configuration is needed to run the app. Therefore, it should **not** be used
for anything other than testing. For example, it includes:

* A default ``SECRET_KEY`` environment variable
* A predefined database with the environment variable
  ``POSTGRES_HOST_AUTH_METHOD=trust``. This lets us connect to the database
  without using a password.
* Debug mode is enabled.
* Admin superuser credentials (``admin`` / ``admin``).
* An API key ``insecure-ea1a8d297e3b2d3313b8a30b18959c3``.

.. _`WSL`: https://docs.microsoft.com/en-us/windows/wsl/

Prerequisites
-------------

You will only need Docker tooling and nothing more:

* `Docker Engine`_ (Desktop or Server)
* `Docker Compose`_ (sometimes comes bundled with Docker Engine)

.. _`Docker Engine`: https://docs.docker.com/engine/install/
.. _`Docker Compose`: https://docs.docker.com/compose/install/


Getting started
---------------

1. Download the project as ZIP-file:

   .. code:: bash

      wget https://github.com/GPP-Woo/GPP-publicatiebank/archive/refs/heads/main.zip
      unzip main.zip
      cd registratie-component-main

2. Start the docker containers with ``docker compose``. If you want to run the
   containers in the background, add the ``-d`` option to the command below:

   .. code:: bash

      docker compose up


   The output should look similar to:

   .. code-block:: none

      [+] Running 12/12
       ✔ Network registratie-component-main_default              Created       0.1s
       ✔ Volume "registratie-component-main_oz-media"            Created       0.0s
       ✔ Volume "registratie-component-main_oz-private-media"    Created       0.0s
       ✔ Volume "registratie-component-main_media"               Created       0.0s
       ✔ Volume "registratie-component-main_log"                 Created       0.0s
       ✔ Volume "registratie-component-main_db"                  Created       0.0s
       ✔ Volume "registratie-component-main_redis-data"          Created       0.0s
       ✔ Container registratie-component-main-redis-1            Created       0.2s
       ✔ Container registratie-component-main-db-1               Created       0.2s
       ✔ Container registratie-component-main-web-1              Created       0.1s
       ✔ Container registratie-component-main-openzaak-celery-1  Created       0.1s
       ✔ Container registratie-component-main-openzaak-web-1     Created       0.1s
      Attaching to db-1, openzaak-celery-1, openzaak-web-1, redis-1, web-1
      Gracefully stopping... (press Ctrl+C again to force)

4. Navigate to ``http://127.0.0.1:8000/admin/``, where you can log in with the
   ``admin`` username and ``admin`` password.

5. You can authenticate to the API endpoints with the
   ``Authorization: Token insecure-ea1a8d297e3b2d3313b8a30b18959c3`` HTTP request header.

6. To stop the containers, press *CTRL-C* or if you used the ``-d`` option:

   .. code:: bash

      docker compose stop

7. If you want to get newer versions, you need to ``pull`` because the
   ``docker-compose.yml`` contains no explicit versions:

   .. code:: bash

      docker compose pull
