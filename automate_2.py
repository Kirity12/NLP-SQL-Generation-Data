import json
import openai
from pathlib import Path
import os
openai.api_key = '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'
import random

api_cfg = {
        "engine": "text-davinci-002",
        "top_p": 1.0,
        "temperature": 0.7,
        "max_tokens": 1024,
        "presence_penalty": 2.0,
        "frequency_penalty": 2.0,
        #"echo": True,
}

num_completions = 30

def main():
    global num_completions
    output = "Question:\n\n"

    databases = os.listdir(r'C:\Users\sganugap\Documents\Kirity Projects\sql_generation-c39846c9d76f296857017c3d7cf9ffb958a4c6ec\data\database')


    do = ['hard','medium','easy']

    keywords = ['ADD', 'DISTINCT', "SET", 'TRUNCATE', 'ORDER BY', 'ASC', 
                'DESC', 'BETWEEN', 'LIMIT', 'IS NULL', 'GROUP BY ', 'HAVING', 
                'INNER JOIN', 'LEFT JOIN', 'RIGHT JOIN', 'OUTER JOIN', 
                'UNION', 'UNION ALL', 'EXISTS', 'LIKE', 'CASE', 'JOIN']

    with open(Path('few_shot_prompts\grouped_questions.json')) as f:
        grouped_questions = json.load(f)

    i=0

    while i<10:

        database = databases[random.randint(0,len(databases)-1)]

        try:

            with open(Path('data\database\{}\schema.sql'.format(database)), 'r') as f:
                schema = f.read()

            schema = schema[:schema.find('INSERT')]
            questions = grouped_questions[database]['extra']
            idx =  random.sample(range(0, len(questions)), 1)[0]
            question, query = questions[idx]['question'], questions[idx]['query']

            keys = ''
            for k in keywords:
                if k in query:
                    keys += k +', '

            easy_ = grouped_questions[database]['easy'][random.randint(0,len(grouped_questions[database]['easy'])-1)]
            hard_ = grouped_questions[database]['hard'][random.randint(0,len(grouped_questions[database]['hard'])-1)]
            medium_ = grouped_questions[database]['medium'][random.randint(0,len(grouped_questions[database]['medium'])-1)]

            qq = 'Question: ' + easy_['question'] + '\nQuery: ' + easy_['query'] + '\nQuestion: ' + medium_['question'] + '\nQuery: ' + medium_['query'] + '\nQuestion: ' + hard_['question'] + '\nQuery: ' + hard_['query'] + '\nQuestion: ' + question
        


            prompt = "Using valid SQLite, answer the following questions for the tables provided above."


            prompt = schema + '\n' + prompt + '\n' + qq + '\n'+ 'Query: '

            response = openai.Completion.create(
                prompt=prompt,
                **api_cfg
            )
            output = response['choices'][0]['text']

            pp = {'databases': database, 'pompt': prompt, 'qustions': question, 'given_query': query, 'predicted_answer': output}

            with open(Path('predicted_prompt3\{}_example.json'.format(i+1)),'w') as file:

                json.dump(pp, file, indent=4)

            print('---------completed---------', 'example', i)
            i+=1
        except Exception:
            pass 



        

if __name__ == '__main__':
    main()