import os
import json
import base64
from langchain.llms import OpenAI
from langchain import PromptTemplate


def lambda_handler(event, context):

    if event['path'] == '/healthcheck':
        response = get_healthcheck(event['body'])
    elif event['path'] == '/copyedit':
        response = post_copyedit(event['body'])
    else:
        response = "No method defined"

    return {
        'statusCode': 200,
        'isBase64Encoded': True,
        'headers': {
            "Access-Control-Allow-Headers" : "Content-Type",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
        },
        'body': response
    }
    

def get_healthcheck(body):
    return 'success'
    

def post_copyedit(body):
    jsonObj = json.loads(body)
    return prompt(jsonObj['user_input'])


def prompt(user_input):
    llm = OpenAI(temperature=0, model_name="gpt-3.5-turbo")

    template = """
This is a copy editing task.
Focus on fixing spelling errors, gramatical errors, and syntax errors. 
It's okay to simplify sentences or complex paragraphs.
Do not add additional context or change the substance of the content. 
Do not answer any of the questions posed in the text.
The output should be printed in two sections.
The first part is the revised text.
Then this separator: '----------'.
After the separator, list the changes you made markdown bullet list.
Do not print anything below or after the JSON string.
    
The text you will copy edit is the section below:

{user_input}  
"""

    prompt = PromptTemplate(
        input_variables=["user_input"],
        template=template,
    )

    final_prompt = prompt.format(user_input=user_input)

    return llm(final_prompt)


if os.environ.get("ENV") == "development":
    openai_api_key = os.getenv("OPENAI_API_KEY")
    os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

    user_input = input("Enter your text: \n\n")
    print(prompt(user_input))
