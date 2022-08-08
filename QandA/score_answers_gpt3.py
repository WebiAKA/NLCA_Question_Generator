import openai
from random import seed
import pandas
import numpy as np


with open('../openaiapikey.txt', 'r') as infile:
    open_ai_api_key = infile.read()
openai.api_key = open_ai_api_key


seed(42)
csv_file_dir = '/Users/webby/Desktop/aka-files/working-dir/NLCA_Question_Generator/QandA/'
prompt_dir = "/Users/webby/Desktop/aka-files/working-dir/NLCA_Question_Generator/QandA/"
csv_filename = 'dialogue_data_scored.csv'
out_filename = 'dialogue_data_scored.csv'
prompt_name = 'score_answer_prompt.txt'



def load_prompt(filename, payload1, payload2):
    with open(prompt_dir + filename, 'r', encoding='utf-8') as infile:
        body = infile.read()
        body = body.replace('<<QUESTION>>', payload1)
        body = body.replace('<<ANSWER>>', payload2)
        return body


def completion(prompt, engine='text-davinci-002', temp=0.7, top_p=1, tokens=10, freq_pen=0.5, pres_pen=0.5,  stop=None):
    try:
        response = openai.Completion.create(
            engine=engine,
            prompt=prompt,
            temperature=temp,
            max_tokens=tokens,
            top_p=top_p,
            frequency_penalty=freq_pen,
            presence_penalty=pres_pen,
            stop=stop)
        text = response['choices'][0]['text'].strip()
        if text.isdigit():
            return text
        elif "Score:" in text:
            return text[-1]
        else:
            print(f"Response from GPT-3: {text}")
            raise ValueError("The returned score is not an integer. Please check the Prompt.")
    except Exception as oops:
        print('ERROR in completion function:', oops)



df = pandas.read_csv(csv_file_dir + csv_filename, delimiter=';')

num_data = len(df)
for row_num in range(num_data):

    if np.isnan(df.loc[row_num, " Score"]):
        question = df.loc[row_num, " Question"]
        answer = df.loc[row_num, " Answer"]

        prompt_body = load_prompt(prompt_name, question, answer)
        score = completion(prompt_body)

        df.loc[row_num, " Score"] = score
        print(f"{row_num}/{num_data} Completed")
    # else:
    #     print(f"{row_num} - Already scored!")


df.to_csv(csv_file_dir + out_filename, sep = ';', index=False)
   
