# Augmented vs. traditional usage of search-engine

## Setup API Key
Insert your API Key from OpenAI into the .env file / create a .env file as shown in .env_example. 

## main.py
Execute and find out how the different search strategies perform on your query! 
Enter your question in the **"query"** variable. 

Change the **model** and **temperatur** parameter how you like, but keep in mind that only models are supported which 
support function calling!"

## main_for_evaluation.py
Is used to conduct the evaluation, inputing a list of multiple queries! For experimenting please use the main.py and
input your queries at the top of the script!

## multiple_requests.py 
This is used to evaluate multiple queries. Use this to let the main.py run over multiple requests and save them in 
the "./output/" folder. 

## evaluation_by_model.py 
This runs an evaluation over the results from "multiple_requests.py" and rates them. It will output an .xlsx file in
"./outputs/" where you can see the results. 


## OUTPUT
Check the output folder to see your results.

