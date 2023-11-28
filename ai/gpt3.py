import json
import os
import pandas as pd
from openai import OpenAI

GPT3 = "gpt-3.5-turbo-1106"

input_datapath = "../data/testdata1.csv"


def load_dataset():
    print('Loading dataset.')
    df = pd.read_csv(input_datapath, index_col=0)
    df = df[["comment"]]
    df = df.dropna()
    return df


def get_sentiment(txt):
    messages = [
        {"role": "system", "content": "dopasuj sentyment komentarza do jednej z kategorii: "
                                      "\"komentarz jest pozytywny\","
                                      " \"Komentarz jest obraźliwy i niekonstruktywny\", "
                                       "\"neutralny\", "
                                      "\"wyraża niezadowolenie\""},
        # {"role": "system", "content": "krótko podsumuj komentarz z youtube"},
        {"role": "user", "content": txt.lower()}]

    # functions = [{
    #             "name": "dopasuj_sentyment_do_komentarza",
    #             "parameters": {
    #                 "type": "object",
    #                 "properties": {
    #                     "sentyment": {
    #                         "type": "string",
    #                         "items": {
    #                             "type": "string",
    #                             "enum": ["pozytywny", "obraźliwy", "neutralny"]
    #                         }
    #                     }
    #                 },
    #                 "required": ["sentyment"],
    #             }
    #         }]

    client = OpenAI(api_key=os.environ['GPT_KEY'])

    completion = client.chat.completions.create(
        model=GPT3,
        messages=messages,
        # functions=functions,
        # function_call={"name": "dopasuj_sentyment_do_komentarza"},
        temperature=0.3,
        timeout=15
    )

    # print(completion)
    response_message = completion.choices[0].message
    # print(f'response_message: {response_message}')
    return response_message.content
    # function_call = response_message.function_call
    # if function_call:
    #     name = function_call.name
    #     if name:
    #         arguments = function_call.arguments
    #         if arguments:
    #             arg_dict = json.loads(arguments)
    #             # print(f'arg_dict: {arg_dict}')
    #             return arg_dict


if __name__ == '__main__':
    df = load_dataset()
    print(type(df.comment))
    for comment in df.comment:
        print(f'{get_sentiment(comment)}: {comment}')
