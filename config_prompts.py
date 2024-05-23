tools = [
    {
        "type": "function",
        "function": {
            "name": "duckduckgo_text_search",
            "description": "Queries Duckduckgo search engine and responses with the top pages showing up!",
            "parameters": {
                "type": "object",
                "properties": {
                    "keywords": {
                        "type": "string",
                        "description": """Keywords for the search query. Enter the search terms you want to query.
                                                      Du kannst verschiedene Suchoperatoren verwenden, um deine Suche zu verfeinern:
                                                        1. 'Katzen Hunde' - Ergebnisse über Katzen oder Hunde.
                                                        2. \„Katzen und Hunde\“ - Ergebnisse für den genauen Begriff „Katzen und Hunde“.
                                                        3. 'Katzen -Hunde' - Weniger Hunde in den Ergebnissen.
                                                        4. 'Katzen +Hunde' - Mehr Hunde in den Ergebnissen.""",
                    },
                    "region": {
                        "type": "string",
                        "description": """Region for the search. Specifies the language and country for the search results.
                                                The region is represented by a two-part code: 'language-country'.
                                                For example: 'en-us' represents English language and United States country.
                                                Some common regions include:
                                                - 'wt-wt': Global (default)
                                                - 'us-en': United States (English)
                                                - 'uk-en': United Kingdom (English)
                                                - 'fr-fr': France (French)
                                                - 'de-de': Germany (German)
                                                - 'es-es': Spain (Spanish)
                                                - 'ru-ru': Russia (Russian)
                                                - 'ja-jp': Japan (Japanese)
                                                The first part of the code represents the language, and the second part represents the country.
                                                You can specify the desired language and country to get localized search results.
                                                If you provide an invalid or unsupported region code, the search will default to the global region.
                                                """
                    },
                },
                "required": ["keywords"],
            },
        },
    }
]
system_message = f"""Du bist ein search query / keywords expert. Du musst 5 Suchanfragen durchführen. Die fünf
    suchanfragen sollten so aufgebaut sein, das es dir gelingt eine möglichst umfassenden Antwort zu bekommen für die
     gegeben Suchanfrage. Nutze dafür die Tools des function calling und nutze die möglichkeit Keywords mit operatoren zu verändern. 
     Folgenden optionen gibt es:
        Du kannst verschiedene Suchoperatoren verwenden, um deine Suche zu verfeinern:
        1. 'Katzen Hunde' - Ergebnisse über Katzen oder Hunde.
        2. \„Katzen und Hunde\“ - Ergebnisse für den genauen Begriff „Katzen und Hunde“.
        3. 'Katzen -Hunde' - Weniger Hunde in den Ergebnissen.
        4. 'Katzen +Hunde' - Mehr Hunde in den Ergebnissen.
        WICHTIG: Du bekommst einen Strafpunkt, sollten gleiche Ergebnisse bei dem Ergebnisse der Suche rauskommen.
    """