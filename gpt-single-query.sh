#!/bin/bash

if [ -t 0 ]; then
  PROMPT="$*"
else
  FILE_CONTENT=$(cat)
  PROMPT="$*\n\n--- BEGIN FILE CONTENT ---\n$FILE_CONTENT\n--- END FILE CONTENT ---"
fi

python3 /opt/gpt-cli/md_stream_response.py --prompt "$(echo -e "$PROMPT")"
