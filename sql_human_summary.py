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
PRAGMA foreign_keys = ON;

CREATE TABLE "publication" (
"Publication_ID" int,
"Book_ID" int,
"Publisher" text,
"Publication_Date" text,
"Price" real,
PRIMARY KEY ("Publication_ID"),
FOREIGN KEY ("Book_ID") REFERENCES "book"("Book_ID")
);

CREATE TABLE "book" (
"Book_ID" int,
"Title" text,
"Issues" real,
"Writer" text,
PRIMARY KEY ("Book_ID")
);

The tables publication and book are connected using Book_ID.
"""
example_question = """
Question: List the publisher of the publication with the lowest price.
Explanation: We need to list the publisher with the lowest price belonging to any publication. The list of publishers with the minimum value of price can be fetched from the publication table.
"""
input = table_desc+ example_question
#print(input)

#question_bank = json.load('grouped_questions.json')
with open('grouped_questions.json') as json_file:
    data = json.load(json_file)
#print(data)
db_name = 'book_2'
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
		if i == 15:
			break
		#i = i+ 1
		question = questionIt['question']
		 
		with open('gold.txt' , 'a') as f:
			f.write(questionIt['query']+'\t'+db_name +'\n')

		inputNew = input+"Question: "+question+'\n'+"Explanation:"
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
		time.sleep(15)
		#catch the exception 
		ret = response['choices'][0]['text']
		my_list = ret.splitlines()
		output = table_desc+'\n'+"Question: "+question+'\n'+"Explanation:" + my_list[0]+'\n' + "SELECT"
		#print(output)
		with open('book_2_summary_prompt_%s.txt' % j , 'w') as f:
			f.write(output)
		j = j + 1

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


