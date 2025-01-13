from openai import OpenAI
import os
import argparse
from rich.console import Console
from rich.markdown import Markdown
from rich.live import Live
from dotenv import load_dotenv
import logging
import datetime
import uuid

load_dotenv()

def get_pricing():
    input_price = float(os.getenv("MODEL_INPUT_PRICE", 0.15)) / 1_000_000
    cached_input_price = float(os.getenv("MODEL_CACHED_INPUT_PRICE", 0.075)) / 1_000_000
    output_price = float(os.getenv("MODEL_OUTPUT_PRICE", 0.60)) / 1_000_000

    return input_price, cached_input_price, output_price

def calculate_charge(usage):
    input_tokens = usage.prompt_tokens 
    output_tokens = usage.completion_tokens
    cached_tokens = usage.prompt_tokens_details.get('cached_tokens')
    input_price, cached_input_price, output_price = get_pricing()
    input_charge = (input_tokens - cached_tokens) * input_price
    cached_input_charge = cached_tokens * cached_input_price
    output_charge = output_tokens * output_price
    total_charge = input_charge + cached_input_charge + output_charge
    return total_charge, input_charge, cached_input_charge, total_charge

console = Console()

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--prompt", type=str, help="Enter a prompt")
args = parser.parse_args()

prompt = args.prompt

if not os.getenv("OPENAI_API_KEY"):
    raise Exception("Missing OPENAI_API_KEY environment variable... Exiting.")

client = OpenAI()

log_file_name = f"/opt/gpt-cli/logs/gpt_query_{str(uuid.uuid4())}_{datetime.datetime.now().strftime("%Y-%m-%d")}.log"
logging.basicConfig(filename=log_file_name, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logging.info(prompt)

response = client.chat.completions.create(
    model=os.getenv("MODEL", "gpt-4o-mini"),
    messages=[
        {'role': 'system', 'content': "You are a helpful and concise dev ops engineer, who is helping to build out Ubuntu as a development hobby server on a raspberry pi 5. Your answers should require all necessary detail but minimize extra words, and use the least amount of words possible."},
        {'role': 'user', 'content': prompt}
    ],
    temperature=0,
    stream=True,
    stream_options={"include_usage": True}
)

markdown_content = ""
summary = f"""
No usage info received.
"""

with Live(Markdown(markdown_content), console=console, vertical_overflow='crop', refresh_per_second=10) as live:
    for chunk in response:
        if len(chunk.choices) > 0 and chunk.choices[0].delta.content is not None:
            markdown_content += chunk.choices[0].delta.content
            live.update(Markdown(markdown_content))

        # Print token usage details when the stream ends
        if chunk.usage is not None:
            total_charge, input_charge, cached_input_charge, total_charge = calculate_charge(chunk.usage)
            markdown_content += f"\n\n**Query Price:** ${total_charge:.8f}\n\n"
            live.update(Markdown(markdown_content))

logging.info(markdown_content) 