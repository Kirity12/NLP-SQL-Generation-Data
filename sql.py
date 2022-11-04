# import openai

# openai.api_key = "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"

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

openai.api_key = "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"

response = openai.Completion.create(
  model="code-davinci-002",
  #prompt="### Postgres SQL tables, with their properties:\n#\n# Employee(id, name, department_id)\n# Department(id, name, address)\n# Salary_Payments(id, employee_id, amount, date)\n#\n### A query to list the names of the departments which employed more than 10 employees in the last 3 months\nSELECT",
  #prompt="/*\n3 example rows from table Highschooler:\nSELECT * FROM Highschooler LIMIT 3;\nTable: Highschooler\n  ID    name  grade\n1510  Jordan      9\n1689 Gabriel      9\n1381 Tiffany      9\n*/\n/*\n3 example rows from table Friend:\nSELECT * FROM Friend LIMIT 3;\nTable: Friend\n student_id  friend_id\n       1510       1381\n        1510       1689\n        1689       1709\n */\n /*\n 3 example rows from table Likes:\n SELECT * FROM Likes LIMIT 3;\n Table: Likes\n  student_id  liked_id\n        1689      1709\n        1709      1689\n        1782      1709\n */\n -- Using valid SQLite, answer the following questions for the tables provided above.\n -- What are Kyle's friends ids?\n SELECT",
  prompt="CREATE TABLE Highschooler(\n       ID int primary key,\n       name text,\n       grade int)\nCREATE TABLE Friend( \n       student_id int,\n)\nfriend_id int,\nprimary key (student_id,friend_id),\nforeign key(student_id) references Highschooler(ID),\nforeign key (friend_id) references Highschooler(ID)\nCREATE TABLE Likes( \n student_id int,\nliked_id int,\nprimary key (student_id, liked_id),\nforeign key (liked_id) references Highschooler(ID),\nforeign key (student_id) references Highschooler(ID)\n)\n-- Using valid SQLite, answer the following questions for the tables provided above.\n-- What is Kyle’s id?\nSELECT",
  
  temperature=0, #The temperature controls how much randomness is in the output.
  max_tokens=4096,
  top_p=1.0,
  frequency_penalty=0.0,
  presence_penalty=0.0,
)
print(response.choices[0].text)