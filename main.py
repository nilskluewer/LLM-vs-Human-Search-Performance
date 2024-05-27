from openai import OpenAI
from dotenv import load_dotenv
import os
import json
import functions_duckduckgo
import config_prompts
import warnings
from colorama import init, Fore, Style
import time
import datetime

# Set custom query -> press run if API Keys are set.
custom_query = ("How did the socio-political context of 17th-century Netherlands "
                "influence the evolution of still life paintings, particularly with"
                " respect to symbolism and everyday objects depicted?")

model = "gpt-3.5-turbo"
temperatur = 0.0

# Warnungen von curl_cffi unterdrücken
warnings.filterwarnings("ignore", category=RuntimeWarning, module="curl_cffi")
warnings.filterwarnings("ignore", category=UserWarning, module="curl_cffi")

init()  # Initialisiere Colorama

load_dotenv()
client = OpenAI(
    #organization=os.environ.get("OPENAI_ORG_KEY_1"),
    api_key=os.environ.get("OPENAI_API_KEY_1")
)

def print_section_header(title):
    print(Fore.CYAN + "=" * 150)
    print(title)
    print("=" * 150 + Style.RESET_ALL)

def print_search_result(search_result):
    query = search_result["query"]
    results = search_result["results"]
    error = search_result["error"]

    print(Fore.YELLOW + "Search Query: " + Style.RESET_ALL + query)
    if error:
        print(Fore.RED + " Error: " + Style.RESET_ALL + error)
    else:
        print(" Search Results:")
        for i, result in enumerate(results, start=1):
            title = result.get("title", "No title available")
            body = result.get("body", "No description available")
            url = result.get("href", "No URL available")
            print(f" Result #{i}")
            print(f" Title: {title}")
            print(f" Description: {body}")
            print(f" URL: {url}")
            print(" " + "-" * 20)
    print()

def enhanced_search(query, all_generated_queries, max_results=2):
    user_message = f"Führe 5 Suchanfrage durch zu dieser Anfrage: {query}."

    print_section_header(f"Start of enhanced search with query of user. \n Query:{query}")

    # Configure & construct system message
    system_message = config_prompts.system_message
    messages = [{"role": "system", "content": user_message},
                {"role": "user", "content": system_message}]
    tools = config_prompts.tools
    # Start of time keeping
    response = client.chat.completions.create(
        model=model,
        temperature=temperatur,
        messages=messages,
        tools=tools,
        # auto is default, required leads to a forced function call
        tool_choice="required",
    )
    query_generation_response_message = response.choices[0].message

    print_section_header("""Response from model where the model produces alternative search queries and 
    suggests and execution of functions (5 are suggested) """)
    print(query_generation_response_message)

    print_section_header("""Start of executing functions and summarizing results...""")
    tool_calls = query_generation_response_message.tool_calls
    if tool_calls:
        available_functions = {
            "duckduckgo_text_search": functions_duckduckgo.duckduckgo_text_search,
        }
        messages.append(query_generation_response_message)
        search_results = []
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_to_call = available_functions[function_name]
            function_args = json.loads(tool_call.function.arguments)
            try:
                function_response, results_obj = function_to_call(
                    keywords=function_args.get("keywords"),
                    region=function_args.get("region"),
                    max_results=max_results
                )
                print("FUNCTION RESPOSE", function_response)
                messages.append({
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": function_response,
                })
                search_results.append({
                    "query": function_args.get("keywords"),
                    "results": results_obj,
                    "error": None
                })
                # Add generated query to the all_generated_queries list
                all_generated_queries.append({"initial_query": query, "generated_query": function_args.get("keywords")})
            except Exception as e:
                error_message = f"An error occurred while calling the function '{function_name}': {str(e)}"
                messages.append({
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": error_message,
                })
                search_results.append({
                    "query": function_args.get("keywords"),
                    "results": None,
                    "error": error_message
                })
                # Add generated query with error
                all_generated_queries.append({"initial_query": query, "generated_query": function_args.get("keywords"), "error": error_message})

        messages.append({
            "role": "user",
            "content": f"Beantworte nun die ursprüngliche Frage oder Query step by step. Begründe mit Quellen wie zu dem Ergebnis kommst,"
                       f"gebe deine Quellen vollständig mit URL an! Und schlage die 5 relevantesten Webseiten vor!"
                       f"\n"
                       f"{query}"
        })

        response = client.chat.completions.create(
            model=model, temperature=temperatur,
            messages=messages,
        )
        summarizing_results_response = response.choices[0].message

        print_section_header("Search conducted and summary generated.")
        print("Enhanced Summary:", summarizing_results_response)

        # Return the search results of the enhanced search. Consists of query, search results entries and errors if an error occurred.
        return search_results, summarizing_results_response

def regular_search(query):
    # Make the same request with the results of the regular search
    print_section_header(f"Start of regular search with query of user. \n Query:{query}")

    result_str, results_obj = functions_duckduckgo.duckduckgo_text_search(query, max_results=10)

    messages = [{"role": "user", "content": f"Führe eine Suchanfrage durch zu dieser Anfrage: {query}"},
                {"role": "user", "content": f"Search Results from DuckduckGo function call: \n \n {result_str}"},
                {"role": "user",
                 "content": f"Beantworte nun die ursprüngliche Frage oder Query step by step. Begründe mit Quellen wie zu dem Ergebnis kommst,"
                            f"gebe deine Quellen vollständig mit URL an! Und schlage die 5 relevantesten Webseiten vor!"
                            f"\n"
                            f"{query}"}]
    response = client.chat.completions.create(
        model="gpt-3.5-turbo", temperature=0.7,
        messages=messages,
    )

    summarizing_results_response = response.choices[0].message

    print_section_header("Regular Search with LLM Summarization finished.")
    print(summarizing_results_response)
    return results_obj, summarizing_results_response

def display_results(query, enhanced_query_search_results, enhanced_query_summarized_answer, regular_query_search_results, regular_query_summarized_answer,
                    time_enhanced, time_regular):
    print(Fore.RED + "=" * 150)
    print(" START OF EVALUATION OF RESULTS ")
    print("=" * 150 + Style.RESET_ALL)

    print_section_header(f"Original Query: {query}")

    print_section_header("LLM-Enhanced Search Results")
    for search_result in enhanced_query_search_results:
        print_search_result(search_result)

    print_section_header("Regular Search Results")
    for i, result in enumerate(regular_query_search_results, start=1):
        title = result.get("title", "No title available")
        body = result.get("body", "No description available")
        url = result.get("href", "No URL available")
        print(f"Result #{i}")
        print(f" Title: {title}")
        print(f" Description: {body}")
        print(f" URL: {url}")
        print(" " + "-" * 20)
    print()

    print_section_header("LLM-Enhanced Answer Summary")
    print(enhanced_query_summarized_answer.content)
    print()

    print_section_header("Regular Search Answer Summary")
    print(regular_query_summarized_answer.content)
    print()

    print_section_header("Time needed to complete query")
    print("Time in seconds needed for the ENHANCED query with summary", time_enhanced)
    print()
    print("Time in seconds needed for the REGULAR query with summary", time_regular)

def run_single_query(query):
    start = time.time()
    all_generated_queries = []  # Ensure this is defined
    enhanced_query_search_results, enhanced_query_summarized_answer = enhanced_search(query, all_generated_queries)
    end = time.time()
    time_enhanced_query = end - start

    start = time.time()
    regular_query_search_results, regular_query_summarized_answer = regular_search(query)
    end = time.time()
    time_regular_query = end - start

    # Use for a simple query
    display_results(query, enhanced_query_search_results, enhanced_query_summarized_answer, regular_query_search_results,
                    regular_query_summarized_answer, time_enhanced_query, time_regular_query)


#For a single query
run_single_query(custom_query)