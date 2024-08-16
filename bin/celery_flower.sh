#!/bin/bash
exec celery flower --app odrc --workdir src
