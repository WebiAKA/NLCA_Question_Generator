# Dialogue Generator for Musio interview

After installing the requirements by `pip install -r requirements.txt` command, edit the prompt text in `dialogue_prompt.txt` and paths, if needed.


1. `python3 generate_dialogues.py` will generate the dialogues according to the list of topics in `topics` folder (the topics can be added to different files). The dialogues are saved in the `dialogues` folder under the filename of their respective topics.

2. `python3 generate_summaries.py` generates summaries for each dialogue saved in `dialogues` folder.

3. `python3 QandA/dialogue_to_csv.py` collects every Q and A pairs between Musio and the student and save it in a csv (`delimiter = ';'`) file. Sample data in csv format:
  <p align="center">
    <img width="800" align = 'center' alt="Screen Shot 2022-08-08 at 8 08 40 PM" src="https://user-images.githubusercontent.com/108511037/183404723-b27f68ab-fb9b-46cd-b993-ba6c25a23e06.png">
  </p>

4. `python3 QandA/score_answers_gpt3.py` will score the answers from the students. The script reads Q and A pair from the csv file and scores the answer using OpenAI's api and writes it to another csv file.
