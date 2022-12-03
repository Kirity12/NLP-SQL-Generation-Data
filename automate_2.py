import sys
import json
import openai
from pathlib import Path
import os
openai.api_key = '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'
import random

PARENT_DIR = Path(__file__, '..').resolve()
sys.path.append(str(PARENT_DIR))

api_cfg = {
        "engine": "text-davinci-002",
        "top_p": 1.0,
        "temperature": 0.7,
        "max_tokens": 2047,
        "presence_penalty": 2.0,
        "frequency_penalty": 2.0,
        #"echo": True,
}


PARENT_DIR = Path(__file__, '..').resolve()
sys.path.append(str(PARENT_DIR))

num_completions = 30

def main():
    global num_completions
    output = "Question:\n\n"

    databases = os.listdir(PARENT_DIR/'data\database')
    do = ['hard','medium','easy']


    with open(Path('few_shot_prompts\grouped_questions.json')) as f:
        grouped_questions = json.load(f)

    i=0

    while i<10:

        database = databases[random.randint(0,len(databases)-1)]

        try:

            with open(Path('data\database\{}\schema.sql'.format(database)), 'r') as f:
                schema = f.read()

            schema = schema[:schema.find('INSERT')]
            difficulty = do[random.sample(range(0, len(do)), 1)[0]]
            questions = grouped_questions[database][difficulty]
            idx =  random.sample(range(0, len(questions)), 1)[0]
            question, query = questions[idx]['question'], questions[idx]['query']

            easy_ = grouped_questions[database]['easy'][random.randint(0,len(grouped_questions[database]['easy'])-1)]
            while easy_ == questions[idx]:
                easy_ = grouped_questions[database]['easy'][random.randint(0,len(grouped_questions[database]['easy'])-1)]


            hard_ = grouped_questions[database]['hard'][random.randint(0,len(grouped_questions[database]['hard'])-1)]
            while hard_ == questions[idx]:
                hard_ = grouped_questions[database]['hard'][random.randint(0,len(grouped_questions[database]['hard'])-1)]

            medium_ = grouped_questions[database]['medium'][random.randint(0,len(grouped_questions[database]['medium'])-1)]
            while medium_ == questions[idx]:
                medium_ = grouped_questions[database]['medium'][random.randint(0,len(grouped_questions[database]['medium'])-1)]

            qq = 'Question: ' + easy_['question'] + '\nQuery: ' + easy_['query'] + '\nQuestion: ' + medium_['question'] + '\nQuery: ' + medium_['query'] + '\nQuestion: ' + hard_['question'] + '\nQuery: ' + hard_['query'] + '\nQuestion: ' + question
        


            prompt = "Using valid SQLite, answer the following questions for the tables provided above."


            prompt = schema + '\n' + prompt + '\n' + qq + '\n'+ 'Query: '

            response = openai.Completion.create(
                prompt=prompt,
                **api_cfg
            )
            output = response['choices'][0]['text']

            pp = {'databases': database, 'prompt': prompt, 'complexity':difficulty, 'question': question, 'given_query': query, 'predicted_answer': output}

            with open(Path('predicted_prompt2\{}_example.json'.format(i+1+40)),'w') as file:

                json.dump(pp, file, indent=4)

            print('---------completed---------', 'example', i+40)
            i+=1
        except Exception as e:
            pass 



        

if __name__ == '__main__':
    main()