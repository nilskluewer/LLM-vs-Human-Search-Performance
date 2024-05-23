import main_for_evaluation as main

queries = [
    # Easy Questions
    "What is the capital of Italy?",
    "Best laptops for students 2023",

    # Moderate Complexity Questions
    "Details of the Treaty of Versailles",
    "Results of the 2022 FIFA World Cup final",
    "How does blockchain technology work?",

    # Complex Questions
    "What are the pros and cons of keto diet?",
    "Impact of Brexit on UK economy",
    "Which is better for home use: solar panels or wind turbines?",

    # Highly Complex and Ambiguous Questions
    "Is artificial intelligence beneficial to society?",
    "What is the best way to achieve a work-life balance?"
]

# Evaluate queries and save results to JSON file
main.evaluate_queries(queries)


