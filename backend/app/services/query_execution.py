### service for query generation and query execution.
from typing import List, Dict
import os
import json
from groq import Groq
import concurrent.futures
from dotenv import load_dotenv
from app.prompts import GEN_QUERY_PROMPT


from app.services.web_search import web_search_wrapper



# Load environment variables
load_dotenv()

# Initialize OpenAI client
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
openai_client = Groq(api_key=GROQ_API_KEY)


GEN_QUERY_PROMPT = GEN_QUERY_PROMPT


# step - step no. in string
# description - description of the step.
def generate_queries_for_step(step: str, description: str) -> Dict:
    """Generate search queries for a specific research step."""
    try:
        completion = openai_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": GEN_QUERY_PROMPT},
                {"role": "user", "content": description}
            ],
            response_format={"type": "json_object"},
        )
        queries = json.loads(completion.choices[0].message.content)
        # Write the generated queries to the output file
        # write_output_to_file(f"### Generated Queries for {step}\n" + json.dumps(queries, indent=2))
        return {step: queries}
    except json.JSONDecodeError:
        return {step: {"error": "Failed to generate queries"}}
    


### function to execute each search query and get results.
def execute_queries(step_queries: Dict[str, List[str]]) -> Dict:
    """Execute search queries in parallel and return the top 3 citations from each result."""
    search_results = {"queries": {}}

    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        future_to_query = {executor.submit(web_search_wrapper, query): query for query in step_queries}

        for future in concurrent.futures.as_completed(future_to_query):
            query = future_to_query[future]
            try:
                response = future.result()
                answer = response.get("answer", "No answer found")
                citations = response.get("citations", [])[:1]  # Get top 3 citations

                search_results["queries"][query] = {
                    "answer": answer,
                    "top_citations": citations
                }
            except Exception as exc:
                search_results["queries"][query] = {
                    "error": str(exc)
                }

    return search_results