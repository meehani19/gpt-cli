import os
from openai import OpenAI

prompt = input("prompt: ")

with open('config.txt', 'r') as file:
    lines = [line for line in file]
    org_id = str(lines[0])
    proj_id = str(lines[1])
    api_key = str(lines[2])


# print(os.environ.get('OPENAI_API_KEY'))

client = OpenAI(
    # organization=org_id,
    # project=proj_id,
    api_key=os.environ.get('OPENAI_API_KEY')
)

try:
    stream = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        model="gpt-4o-mini",
        stream=True,
    )

    for chunk in stream:
        print(chunk.choices[0].delta.content or "", end="")

except Exception as e:
    print("Query Failed")
    print(e)