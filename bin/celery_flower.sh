#!/bin/bash
exec celery flower --app woo_publications --workdir src
