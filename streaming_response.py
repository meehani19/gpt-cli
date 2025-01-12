from openai import OpenAI
import os
import argparse

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
        {'role': 'system', 'content': "You are an helpful and consise dev ops engineer, who is helping to build out Ubuntu as a development hobby server on a raspberry pi 5."},
        {'role': 'user', 'content': prompt}
    ],
    temperature=0,
    stream=True,
    stream_options={"include_usage": True}
)

print('')
for chunk in response:
    if len(chunk.choices) > 0 and chunk.choices[0].delta.content is not None:
        print(chunk.choices[0].delta.content, end='')
    if chunk.usage is not None:
        print('\n')
        print('****************END OF RESPOSNE****************')
        print(f'Completion Tokens: {chunk.usage.completion_tokens}')
        print(f'Prompt Tokens: {chunk.usage.prompt_tokens}')
        print(f'Total Tokens: {chunk.usage.total_tokens}')
        print(f'Total Price: Coming soon...')

print('')
