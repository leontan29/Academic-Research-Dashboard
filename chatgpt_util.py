import os
from openai import OpenAI

mocking = os.getenv('MOCKING')

if not mocking:
    client = OpenAI(
        # This is the default and can be omitted
        # api_key=os.environ.get("OPENAI_API_KEY"),
    )

def get_summary(item):
    if mocking: return '# Summary of {item}'
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system",
             "content": "You are a database professor at a reknowned university."},
            {"role": "user", "content": f'''
                Summarize the paper: {item}.
                Provide result directly in Markdown format without prolog or epilog.
            '''}
        ]
    )
    return completion.choices[0].message.content
