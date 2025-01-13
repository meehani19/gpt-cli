# gpt-cli

## Python Requirements
- `python3-openai`
- `rich`
- `dotenv`

## Usage
- Use with or without quotations:
  ```
  gpt "How to center a div?"
  ```
  or
  ```
  gpt How to center a div?
  ```
- Pipe in file contents:
  ```
  gpt Does my script have any errors? < app.py
  ```

## TODO
- Session management: preserve context, list sessions, set active session, age off sessions
- Set instruction prompt
- Script generator for any script type (not just Python)
- README setup instructions
- Configure packaging into RPM and build from it