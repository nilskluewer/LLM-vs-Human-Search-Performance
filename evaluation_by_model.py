import json
import os
import re
import pandas as pd
from openai import OpenAI
from dotenv import load_dotenv

# Example usage
input_file = 'outputs/evaluation_results.json'
output_file = 'outputs/comparative_evaluation_results_used_in_report.xlsx'

model = "gpt-4o"
temperatur = 0.0

load_dotenv()
client = OpenAI(
    organization=os.environ.get("OPENAI_ORG_KEY_1"),
    api_key=os.environ.get("OPENAI_API_KEY_1"),
)

template = """
{
    "REASONING": "text with reasoning",
    "A": {
        "Coherence": "<rating>",
        "Relevance": "<rating>",
        "Completeness": "<rating>"
    },
    "B": {
        "Coherence": "<rating>",
        "Relevance": "<rating>",
        "Completeness": "<rating>"
    }
}
"""

def sanitize_json_response(response):
    """
    Sanitizes and fixes the raw JSON response to ensure it's compliant.
    Strips control characters that could break JSON parsing.
    """
    sanitized = re.sub(r'[\x00-\x1F]+', '', response)
    return sanitized

def comparative_evaluation(query, enhanced_results, regular_results, repetitions=5):
    evaluation_data = []

    for _ in range(repetitions):
        evaluation_prompt = f"""
        <query>
        {query}
        </query>

        <result_A>
        {json.dumps(enhanced_results, indent=2)}
        </result_A>

        <result_B>
        {json.dumps(regular_results, indent=2)}
        </result_B>

        First, reason out the differences between both results and why one could be better, or if they are both good. This should be in the "REASONING" field. Then, evaluate each set of results based on the following criteria:
            - Coherence: Logical consistency and fluency of text. How well does the results maintains a coherent and meaningful response. Give a rating from 1-10.
            - Relevance: How well the responses address the query specific information need. Give a rating from 1-10.
            - Completeness: Does the response cover all the essential information required to adequately answer the query? Give a rating from 1-10

        Use the template below to provide your evaluation. Not using this template will result in an ERROR. Please use the template strictly. Do not include the XML Tags.

        {template}
        """

        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": evaluation_prompt}],
            temperature=temperatur
        )
        print("Raw API Message:\n", evaluation_prompt)
        evaluation_response = response.choices[0].message.content
        print("Raw API Response:\n", evaluation_response)  # Print the raw response for debugging

        try:
            sanitized_response = sanitize_json_response(evaluation_response)
            evaluation_json = json.loads(sanitized_response)
            evaluation_json['query'] = query
            evaluation_data.append(evaluation_json)
        except json.JSONDecodeError as e:
            print(f"Failed to parse JSON for query: {query}. Error: {e}")
            print(f"Sanitized API Response:\n", sanitized_response)

    return evaluation_data

def create_dataframe(evaluation_data):
    rows = []

    for entry in evaluation_data:
        row = {
            'query': entry['query'],
            'reasoning': entry['REASONING'],
            'A_Coherence (AUGMENTED)': entry['A']['Coherence'],
            'A_Relevance (AUGMENTED)': entry['A']['Relevance'],
            'A_Completeness (AUGMENTED)': entry['A']['Completeness'],
            'B_Coherence (REGULAR)': entry['B']['Coherence'],
            'B_Relevance (REGULAR)': entry['B']['Relevance'],
            'B_Completeness (REGULAR)': entry['B']['Completeness'],
        }
        rows.append(row)

    df = pd.DataFrame(rows)
    df[['A_Coherence (AUGMENTED)', 'A_Relevance (AUGMENTED)', 'A_Completeness (AUGMENTED)', 'B_Coherence (REGULAR)', 'B_Relevance (REGULAR)', 'B_Completeness (REGULAR)']] = df[['A_Coherence (AUGMENTED)', 'A_Relevance (AUGMENTED)', 'A_Completeness (AUGMENTED)', 'B_Coherence (REGULAR)', 'B_Relevance (REGULAR)', 'B_Completeness (REGULAR)']].apply(pd.to_numeric)
    return df

def evaluate_results_from_file(input_file, output_file):
    with open(input_file, 'r') as f:
        evaluation_data = json.load(f)

    all_responses = []

    for entry in evaluation_data:
        query = entry['query']
        enhanced_results = entry['enhanced_search']['summary']
        regular_results = entry['regular_search']['summary']

        evaluation_responses = comparative_evaluation(query, enhanced_results=enhanced_results,
                                                      regular_results=regular_results, repetitions=5)
        all_responses.extend(evaluation_responses)

    df = create_dataframe(all_responses)

    with pd.ExcelWriter(output_file) as writer:
        df.to_excel(writer, index=False, sheet_name='Raw Data')

        summary_stats = df.groupby('query').agg({
            'A_Coherence (AUGMENTED)': ['mean', 'std'],
            'A_Relevance (AUGMENTED)': ['mean', 'std'],
            'A_Completeness (AUGMENTED)': ['mean', 'std'],
            'B_Coherence (REGULAR)': ['mean', 'std'],
            'B_Relevance (REGULAR)': ['mean', 'std'],
            'B_Completeness (REGULAR)': ['mean', 'std'],
        }).reset_index()

        summary_stats.columns = ['_'.join(col).strip() for col in summary_stats.columns.values]
        summary_stats.to_excel(writer, index=False, sheet_name='Summary Stats')

    print(f"Evaluation completed and results saved to {output_file}")

evaluate_results_from_file(input_file, output_file)