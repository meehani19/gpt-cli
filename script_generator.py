from openai import OpenAI
import os
import argparse
import datetime

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
        {'role': 'system', 'content': "You are a software engineer who writes python scripts. In your response, only provide the content of the script. Do not include anything else. Do not format the response with markdown."},
        {'role': 'user', 'content': prompt}
    ],
    temperature=0
)

content = "placeholder"

# Extract the content from the response
if response.choices and len(response.choices) > 0:
    content = response.choices[0].message.content                                                                                                                                         
                                                                                                                                                                                                    
# Define the file name with the date                                                                                                                                                                   
file_name = f"gpt_script_{datetime.datetime.now().strftime("%Y-%m-%d")}.py"                                                                                                                                                                 
                                                                                                                                                                                                    
# Create and write to the file                                                                                                                                                                         
with open(file_name, 'w') as file:                                                                                                                                                                     
    file.write(content)                                                                                                                                             
                                                                                                                                                                                                        
print(f"File '{file_name}' created successfully.")