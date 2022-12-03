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
        "max_tokens": 1024,
        "presence_penalty": 2.0,
        "frequency_penalty": 2.0,
        #"echo": True,
}

num_completions = 30

def main():
    global num_completions
    output = "Question:\n\n"

    databases = os.listdir(PARENT_DIR/'data\database')


    do = ['hard','medium','easy']

    keywords = ['ADD', 'DISTINCT', "SET", 'TRUNCATE', 'ORDER BY', 'ASC', 
                'DESC', 'BETWEEN', 'LIMIT', 'IS NULL', 'GROUP BY ', 'HAVING', 
                'INNER JOIN', 'LEFT JOIN', 'RIGHT JOIN', 'OUTER JOIN', 
                'UNION', 'UNION ALL', 'EXISTS', 'LIKE', 'CASE', 'JOIN', 'count']

    with open(Path('few_shot_prompts\grouped_questions.json')) as f:
        grouped_questions = json.load(f)

    i=0
    if not os.path.exists('predicted_prompt3'):
        os.makedirs('predicted_prompt3')

    while i<50:

        database = databases[random.randint(0,len(databases)-1)]

        try:

            with open(Path('data\database\{}\schema.sql'.format(database)), 'r') as f:
                schema = f.read()

            schema = schema[:schema.find('INSERT')]
            difficulty = do[random.sample(range(0, len(do)), 1)[0]]
            questions = grouped_questions[database][difficulty] 
            idx =  random.sample(range(0, len(questions)), 1)[0]
            question, query = questions[idx]['question'], questions[idx]['query']

            keys = ''
            for k in keywords:
                if k in query:
                    keys += k +', '


            prompt = "Using valid SQLite, answer the following question for the tables provided above by writing the SQL query for the question below using "+keys+" and SELECT terms."

            qq = question

            prompt = schema + '\n' + prompt + '\nQuestion:' + qq + '\n'+ 'Query: '

            response = openai.Completion.create(
                prompt=prompt,
                **api_cfg
            )
            output = ' '.join(response['choices'][0]['text'].split('\n'))
            output = output if ';' in output else output+';'
            print(output)

            pp = {'databases': database, 'prompt': prompt, 'complexity':difficulty, 'question': question, 'given_query': query, 'predicted_answer': output}

            with open(Path('predicted_prompt3\{}_example.json'.format(i+1)),'w') as file:

                json.dump(pp, file, indent=4)

            i+=1
        except Exception as e:
            print('Error:', str(e))



        

if __name__ == '__main__':
    main()