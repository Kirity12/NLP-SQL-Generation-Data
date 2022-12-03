# import openai

# def generate_sql_query(prompt, max_tokens=100, temperature=0.5, top_p=1.0, frequency_penalty=0.0, presence_penalty=0.0):
#     response = openai.Completion.create(
#         engine="davinci-codex",
#         #model="code-davinci-002",
#         prompt=prompt,
#         max_tokens=max_tokens,
#         temperature=temperature,
#         top_p=top_p,
#         frequency_penalty=frequency_penalty,
#         presence_penalty=presence_penalty,
#     )
#     return response.choices[0].text

# prompt = input("Enter your prompt - What data do you need?: ")
# print(generate_sql_query(prompt))

import os
import openai
import time
import json

#openai.api_key = "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"
openai.api_key = "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"

table_desc = """
CREATE TABLE "battle" (
"id" int,
"name" text,
"date" text,
"bulgarian_commander" text,
"latin_commander" text,
"result" text,
primary key("id")
);

CREATE TABLE "ship" (
"lost_in_battle" int,
"id" int,
"name" text,
"tonnage" text,
"ship_type" text,
"location" text,
"disposition_of_ship" text,
primary key("id"),
foreign key (`lost_in_battle`) references `battle`("id") 
);


CREATE TABLE "death" (
"caused_by_ship_id" int,
"id" int,
"note" text,
"killed" int,
"injured" int,
primary key("id"),
foreign key ("caused_by_ship_id") references `ship`("id") 
);


--Using valid SQLite, answer the following questions for the tables provided above.
"""
example_question = """
Easy: List the name and tonnage ordered by in descending alphaetical order for the names.
SELECT name ,  tonnage FROM ship ORDER BY name DESC

Medium: How many battles did not lose any ship with tonnage '225'?
SELECT count(*) FROM battle WHERE id NOT IN ( SELECT lost_in_battle FROM ship WHERE tonnage  =  '225' );

Hard: What is the ship id and name that caused most total injuries?
SELECT T2.id ,  T2.name FROM death AS T1 JOIN ship AS t2 ON T1.caused_by_ship_id  =  T2.id GROUP BY T2.id ORDER BY count(*) DESC LIMIT 1
"""
input = table_desc+ example_question
#print(input)

#question_bank = json.load('grouped_questions.json')
with open('grouped_questions_dev.json') as json_file:
    data = json.load(json_file)
#print(data)
db_name = 'battle_death'
j = 0
levels = ['easy','medium','hard','extra']
for level in levels:
	question_bank = data[db_name][level]
	i = 0 
	for questionIt in question_bank:
		#print(question_bank)
		i = i+ 1
		if i%2==0:

			continue
		if i == 2:
			break
		#i = i+ 1
		question = questionIt['question']
		 
		with open('gold_sakshi.txt' , 'a') as f:
			f.write(questionIt['query']+'\t'+db_name +'\n')

		inputNew = input+"\n"+"--Using valid SQLite, create easy, medium and hard questions and corresponding sql queries."
		print(inputNew)
		response = openai.Completion.create(
		  model="code-davinci-002",
		  prompt=inputNew,
		  
		  temperature=0.7, #The temperature controls how much randomness is in the output.
		  max_tokens=1024,
		  top_p=1.0,
		  frequency_penalty=2.0,
		  presence_penalty=2.0,
		)
		#time.sleep(15)
		#catch the exception 
		ret = response['choices'][0]['text']
		print(ret)
		# my_list = ret.splitlines()
		# output = table_desc+'\n'+"Question: "+question+'\n'+"Explanation:" + my_list[0]+'\n' + "SELECT"
		# #print(output)
		# with open('book_2_summary_prompt_%s.txt' % j , 'w') as f:
		# 	f.write(output)
		# j = j + 1

		# response = openai.Completion.create(
		#   model="code-davinci-002",
		#   prompt=output,
		# from openai.error import RateLimitError
		  
		#   temperature=0.7, #The temperature controls how much randomness is in the output.
		#   max_tokens=1024,
		#   top_p=1.0,
		#   frequency_penalty=2.0,
		#   presence_penalty=2.0,
		# )
# 		try:
# call_model(prompt, db_name, dataset_name, itr)
# except RateLimitError as e:
# if str(e) == "You exceeded your current quota, please check your plan and billing details.":
# logger.error('We ran out of tokens :(')
# raise e
# logger.error('We have hit our rate limit. Writing output then sleeping.') 
		# ret = response['choices'][0]['text']
		# my_list = ret.splitlines()
		# with open('pred.txt'  , 'a') as f:
		# 	f.write("SELECT"+my_list[0]+'\n')

		# print(my_list[0])


