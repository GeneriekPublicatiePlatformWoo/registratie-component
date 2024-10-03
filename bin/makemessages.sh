#!/bin/bash
cwd="${PWD}"
toplevel=$(git rev-parse --show-toplevel)

cd "${toplevel}/src"

echo "Extracting messages for Python code..."

# Some constants are generated and can be ignored.
python manage.py makemessages \
  --all \
  --ignore="test_*"

echo "You can now update the translations catalog. Afterwards, make sure to run"
echo "src/manage.py compilemessages."

cd "${cwd}"
