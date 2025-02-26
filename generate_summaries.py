import openai
from random import seed,sample
import os
import re


with open('openaiapikey.txt', 'r') as infile:
    open_ai_api_key = infile.read()
openai.api_key = open_ai_api_key


seed()
dialoguedir = '/Users/webby/Desktop/aka-files/working-dir/NLCA_Question_Generator/dialogues/'
outdir = '/Users/webby/Desktop/aka-files/working-dir/NLCA_Question_Generator/summaries/'
promptdir = '/Users/webby/Desktop/aka-files/working-dir/NLCA_Question_Generator/summary_prompt.txt'
files = os.listdir(dialoguedir)
# files = [i for i in files if 'stack' in i]  # filter list: dialog, medical, reddit, stack, news
# files = sample(files, 16)
print(files)

# davinci-instruct
# temp = 0.9
# top_p = 0.95
# freq pen = 0.5
# pres pen = 0.5


def load_prompt(filename, payload):
    with open(filename, 'r', encoding='utf-8') as infile:
        body = infile.read()
        body = body.replace('<<DIALOGUE>>', payload)
        return body


def completion(prompt, engine='davinci-instruct-beta', temp=0.8, top_p=0.95, tokens=600, freq_pen=0.5, pres_pen=0.5, stop=None):
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
        return text
    except Exception as oops:
        print('ERROR in completion function:', oops)

for f in files:
    try:
        with open(dialoguedir + f, 'r', encoding='utf-8') as infile:
            context = infile.read()
        prompt = load_prompt(promptdir, context)
        print('\n---------------------\n', prompt)
        summary = completion(prompt)
        print('\n', summary)
        with open(outdir + f, 'w', encoding='utf-8') as outfile:
            outfile.write(summary)
    except Exception as oops:
        print('ERROR in main loop:', f, oops)