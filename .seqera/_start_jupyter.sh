#!/usr/bin/env bash

export SHELL=/usr/bin/bash

source /usr/local/bin/_activate_current_env.sh

if [ -n "$CONNECT_TOOL_PATH_PREFIX" ]; then
  JUPYTER_BASE_PATH="--NotebookApp.base_url=$CONNECT_TOOL_PATH_PREFIX"
else
  JUPYTER_BASE_PATH=""
fi

exec jupyter lab \
     --port $CONNECT_TOOL_PORT \
     --IdentityProvider.token='' \
     --allow-root \
     --ServerApp.allow_remote_access=True \
     --no-browser \
     --NotebookApp.allow_origin=* \
     $JUPYTER_BASE_PATH
