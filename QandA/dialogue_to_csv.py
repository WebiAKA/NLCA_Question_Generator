import csv
import os

csv_filename = 'dialogue_data.csv'
dialoguedir = '/Users/webby/Desktop/aka-files/working-dir/NLCA_Question_Generator/dialogues/'

dialogues = os.listdir(dialoguedir)

def get_data(filename):
    with open(dialoguedir + filename, 'r') as file:
        data = file.read().strip()
        data = data.replace("\n", ' ')
        data = data.split("Musio:")
        clean_data = []
        for sent in data:
            if sent:
                if "user:" in sent:
                    sents = sent.split("user:")
                    for clean_sent in sents:
                        if clean_sent:
                            clean_data.append(clean_sent.strip())
                    continue
                elif "User:" in sent:
                    sents = sent.split("User:")
                    for clean_sent in sents:
                        if clean_sent:
                            clean_data.append(clean_sent.strip())
                    continue
                else:
                    clean_data.append(sent.strip())

    return clean_data

with open(csv_filename, 'a+') as file:
    writer = csv.writer(file, delimiter=';')
    dialogue_num = 1
    for dialogue in dialogues:
        for_csv = get_data(dialogue)
        ind = 0

        while ind + 1 < len(for_csv):
            writer.writerow([dialogue_num] + for_csv[ind: ind+2])
            ind += 2

        dialogue_num += 1

