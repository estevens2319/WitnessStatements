import json
import openai
import ast
import mongo 

from openai_response import get_openai_response
from openai import OpenAI


def get_answers_dynamic(case_no, crime):
    # user_prompt = request.args.get('user_prompt')
    # crime = request.args.get('crime')
    statements=mongo.show_mongodb_statements(case_no)
    user_prompt = ""
    for key in statements.keys():
        user_prompt+=statements[key]
        user_prompt+='\n'

    answers = []
    system_prompt = "You will be given a few witness statements about a " + crime + "identify a comprehensive set of questions that can be answered from the statements and that will be benificial to the investigators. Return a python list of questions."
    questions = get_openai_response("", system_prompt)
    part_2 = """
    [{question:,
      answer:}, ]"
    If the answer to that question is not in the passage, leave it empty:

    """
    
    system_prompt = "I will be giving you a few witness statements about a crime. Your task is to answer the follow up questions in a clear and concise manner. The accuracy of this task is important and so, refrain from answering the questions whose answers are not mentioned in the statement. These are the questions that you must answer based on the witness statements. Please limit your answer to 3 words or less." + questions + "return the answer as a json of questions and answers in the following format: " + part_2
   

    answers = get_openai_response(user_prompt, system_prompt)
    answers = ast.literal_eval(answers)
    return answers

print(get_answers_dynamic('1234', 'kidnapping'))