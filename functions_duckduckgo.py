from typing import List, Dict, Optional, Annotated, Tuple, Any
from duckduckgo_search import DDGS

def duckduckgo_text_search(
        keywords: Annotated[
            str,
            "Keywords for the search query. Enter the search terms you want to query. "
            "You can use various search operators to refine your search: "
            "1. 'cats dogs' - Results about cats or dogs. "
            "2. '\"cats and dogs\"' - Results for the exact term 'cats and dogs'. "
            "3. 'cats -dogs' - Fewer dogs in results. "
            "4. 'cats +dogs' - More dogs in results. "
            "5. 'cats filetype:pdf' - PDFs about cats. Supported file types: pdf, doc(x), xls(x), ppt(x), html. "
            "6. 'dogs site:example.com' - Pages about dogs from example.com. "
            "7. 'cats -site:example.com' - Pages about cats, excluding example.com. "
            "8. 'intitle:dogs' - Page title includes the word 'dogs'. "
            "9. 'inurl:cats' - Page URL includes the word 'cats'."
        ],
        region: Annotated[
            str,
            "Region for the search. Specifies the language and country for the search results. "
            "The region is represented by a two-part code: 'language-country'. "
            "For example: 'en-us' represents English language and United States country. "
            "Some common regions include: "
            "- 'wt-wt': Global (default) "
            "- 'us-en': United States (English) "
            "- 'uk-en': United Kingdom (English) "
            "- 'fr-fr': France (French) "
            "- 'de-de': Germany (German) "
            "- 'es-es': Spain (Spanish) "
            "- 'ru-ru': Russia (Russian) "
            "- 'ja-jp': Japan (Japanese) "
            "The first part of the code represents the language, and the second part represents the country. "
            "You can specify the desired language and country to get localized search results. "
            "If you provide an invalid or unsupported region code, the search will default to the global region."
        ] = "wt-wt",
        safesearch: Annotated[
            str,
            "Safe search setting. Controls the level of filtering for adult content. "
            "Available options: 'on' (strict filtering), 'moderate' (default filtering), 'off' (no filtering)."
        ] = "moderate",
        timelimit: Annotated[
            Optional[str],
            "Time limit for the search. Restricts the search results to a specific time period. "
            "Available options: 'd' (past day), 'w' (past week), 'm' (past month), 'y' (past year). "
            "Leave as None for no time limit."
        ] = None,
        max_results: Annotated[
            Optional[int],
            "Maximum number of search results to retrieve. Specifies the maximum number of search results to return. "
            "Enter a positive integer value. Leave as None to retrieve all available results."
        ] = 5,
) -> tuple[str, Any]:
    ddgs = DDGS()
    results = ddgs.text(
        keywords=keywords,
        region=region,
        safesearch=safesearch,
        timelimit=timelimit,
        max_results=max_results,
    )
    return str(results), results


"""
results = duckduckgo_text_search(keywords="TU Wien, Lobeshymnen")
print(results)

print("Search Results:")
print("---------------")

for i, result in enumerate(results, start=1):
    title = result.get("title", "No title available")
    body = result.get("body", "No description available")
    url = result.get("href", "No URL available")

    print(f"Result #{i}")
    print(f"Title: {title}")
    print(f"Description: {body}")
    print(f"URL: {url}")
    print("---------------")
"""