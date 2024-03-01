#!/bin/bash
set -o errexit
set -o pipefail
set -o nounset

export ENV=test

# Prepare system
make build
make start START_SERVICES="frs-app1 frs-app2 frs-app3"
sleep 10

# Run tests
set +o errexit
make run RUN_SERVICE=test
return_code=$?
set -o errexit

# Down system
make stop

# Exit script
exit $return_code
