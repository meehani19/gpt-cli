from openai import OpenAI
import os
import argparse
from rich.console import Console
from rich.markdown import Markdown

# Initialize Rich Console
console = Console()

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--prompt", type=str, help="Enter a prompt")
args = parser.parse_args()

prompt = args.prompt

if not os.environ.get("OPENAI_API_KEY"):
    raise Exception("Missing OPENAI_API_KEY environment variable... Exiting.")

client = OpenAI()

response = client.chat.completions.create(
    model='gpt-4o-mini',
    messages=[
        {'role': 'system', 'content': "You are a helpful and concise dev ops engineer, who is helping to build out Ubuntu as a development hobby server on a raspberry pi 5."},
        {'role': 'user', 'content': prompt}
    ],
    temperature=0
)

# Extract the content from the response
if response.choices and len(response.choices) > 0:
    content = response.choices[0].message.content
    # Render the Markdown content
    console.print(Markdown(content))

# Print token usage if available
if response.usage:
    console.print('\n')
    console.print('****************END OF RESPONSE****************')
    console.print(f'Completion Tokens: {response.usage.completion_tokens}')
    console.print(f'Prompt Tokens: {response.usage.prompt_tokens}')
    console.print(f'Total Tokens: {response.usage.total_tokens}')
    console.print(f'Total Price: Coming soon...')
