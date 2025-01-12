from openai import OpenAI
from pprint import pprint
client = OpenAI()

completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are an helpful and consise dev ops engineer, who is helping to build out Ubuntu as a development hobby server on a raspberry pi 5."},
        {
            "role": "user",
            "content": "How can I set up my network on this pi so I can ssh in from another device."
        }
    ]
)

pprint(completion.choices[0].message.content)
