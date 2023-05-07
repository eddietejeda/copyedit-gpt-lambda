import os
import json
import base64
# from html_sanitizer import Sanitizer

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
        'body': base64.b64encode(response) 
    }
    

def get_healthcheck(body):
    return bytes('success {}!'.format(body), "utf-8")
    

def post_copyedit(body):

    jsonString = base64.b64decode(body)
    jsonObj = json.loads(jsonString)
    
    return prompt(jsonObj['user_input'])
    


def prompt(user_input):

    llm = OpenAI(model_name="text-davinci-003")

    template = """
Lightly copy edit the section below, but do not change the substance of the content. Keep track of the changes you made. The output will be in a JSON string format.The JSON will include the revised text in the "revision" field and the changes you made will be the "changes" field using markdown bullet lists. Do not print any other text below or after the JSON string.
    
Here is the text:
{user_input}  
    """

    prompt = PromptTemplate(
        input_variables=["user_input"],
        template=template,
    )

    final_prompt = prompt.format(user_input=user_input)

    return bytes(llm(final_prompt), "utf-8")
    


if os.environ.get("ENV") == "development":
    openai_api_key = os.getenv("OPENAI_API_KEY")
    os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

    user_input = input("Enter your text: \n\n")
    response = json.loads(prompt(user_input))
    
    print(f"\n\nRevised text:\n\n{response['revision']}\n\nChanges:\n\n{response['changes']}")


    # sanitizer = Sanitizer({
    #     'tags': ('h1', 'h2', 'p'),
    #     'attributes': {},
    #     'empty': set(),
    #     'separate': set(),
    # })
