import openai
from random import seed, sample
import os
import re


with open('openaiapikey.txt', 'r') as infile:
    open_ai_api_key = infile.read()
openai.api_key = open_ai_api_key


seed()
topicsdir = '/Users/webby/Desktop/aka-files/working-dir/NLCA_Question_Generator/topics/'
outdir = '/Users/webby/Desktop/aka-files/working-dir/NLCA_Question_Generator/dialogues/'
files = os.listdir(topicsdir)
# files = [i for i in files if 'news' in i]    # filter list: dialog, medical, reddit, stack, news
prompt_name = 'dialogue_prompt.txt'
# files = sample(files, 1)
print(files)

# davinci-instruct
# temp = 0.9
# top_p = 0.95
# freq pen = 0.5
# pres pen = 0.5


def load_prompt(filename, payload):
    with open('/Users/webby/Desktop/aka-files/working-dir/NLCA_Question_Generator/%s' % filename, 'r', encoding='utf-8') as infile:
        body = infile.read()
        body = body.replace('<<TOPIC>>', payload)
        return body


def completion(prompt, engine='text-davinci-002', temp=0.7, top_p=1, tokens=600, freq_pen=0.5, pres_pen=0.5,  stop=None):
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
        text = response['choices'][0]['text'].strip().splitlines()
        print("text:",text)
        questions = ''
        for t in text:
            questions += re.sub('^\-', '', t).strip() + '\n'
        questions = questions.strip()
        return questions
    except Exception as oops:
        print('ERROR in completion function:', oops)

for f in files:
    try:
        with open(topicsdir + f, 'r', encoding='utf-8') as infile:
            topics = infile.read()
            topics = topics.split('\n')
        for topic in topics:
            topic = topic.strip()
            if not topic or '#' in topic: # skip over topics that are already used
                continue
            try:
                prompt = load_prompt(prompt_name, topic)
                print('\n---------------------\n', prompt)
                questions = completion(prompt)
                print('\n---------------------\n', questions)
                with open(outdir + topic, 'w', encoding='utf-8') as outfile:
                    outfile.write('Musio: ')
                    outfile.write(questions)
            except Exception as oops1:
                print("Error while requesting GPT-3", f, oops1)
    except Exception as oops:
        print('ERROR in main loop:', f, oops)