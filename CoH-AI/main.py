#CoH-AIChatbot - main
from vanna.chromadb import ChromaDB_VectorStore
from vanna.google import GoogleGeminiChat

# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import mysql 

class MyVanna(ChromaDB_VectorStore, GoogleGeminiChat):
    def __init__(self, config=None):
        ChromaDB_VectorStore.__init__(self, config=config)
        GoogleGeminiChat.__init__(self, config={'api_key': 'AIzaSyDMih0nrHNoJqPcKtsaJJUoUtNKfFaIa7I', 'model': 'gemini-2.5-Flash-lite'})

vn = MyVanna()



# Connection to DB
vn.connect_to_mysql(host='localhost', dbname='CoH', user='root', password='et1138RWU', port=3306)



# TRAINING CODE FOR DATABASE ------------------------------------------------------------------------------------------

# df_information_schema = vn.run_sql("SELECT * FROM INFORMATION_SCHEMA.COLUMNS")
# plan = vn.get_training_plan_generic(df_information_schema)
# plan
# vn.train(ddl="""
#     CREATE TABLE IF NOT EXISTS my-table (
#         id INT PRIMARY KEY,
#         name VARCHAR(100),
#         age INT
#     )
# """)
# vn.train(documentation="Our business defines OTIF score as the percentage of orders that are delivered on time and in full")

# vn.train(sql="SELECT * FROM my-table WHERE name = 'John Doe'")
# training_data = vn.get_training_data()
# training_data
# vn.remove_training_data(id='1-ddl')
# TRAINING CODE FOR DATABASE ------------------------------------------------------------------------------------------





# Asking the AI
response = vn.ask(question="What mental health resources are available?")
print(response)



# Vanna Flask website
# from vanna.flask import VannaFlaskApp
# app = VannaFlaskApp(vn)
# app.run()