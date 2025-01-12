# !/bin/bash
PROMPT="$*"
python3 /opt/gpt-cli/streaming_response.py --prompt "$PROMPT"

