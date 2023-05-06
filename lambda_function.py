import os
import json
from langchain.llms import OpenAI
from langchain import PromptTemplate

if os.environ.get("ENV") == "development":
    openai_api_key = os.getenv("OPENAI_API_KEY")
    os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")


def copyedit():
    llm = OpenAI(model_name="text-davinci-003")

    template = """
    Please lightly copy edit the following text: {user_input}

    After you print the output text, add a line break, and then print a bulleted list of what you changed.
    """
    user_input = input("Enter your text: \n")


    prompt = PromptTemplate(
        input_variables=["user_input"],
        template=template,
    )
    final_prompt = prompt.format(user_input=user_input)

    return (f"Output text:\n {llm(final_prompt)}")

def lambda_handler():
    
    return {
        'statusCode': 200,
        'body': json.dumps( copyedit() )
    }


if os.environ.get("ENV") == "development":
    print( lambda_handler() )