### service for query generation and query execution.
from typing import List, Dict
import os
import json
from groq import Groq
import concurrent.futures
from dotenv import load_dotenv
import asyncio


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
async def generate_queries_for_step(step: str, description: str) -> Dict:
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
    




async def execute_queries(step_queries: Dict[str, List[str]]) -> Dict:
    """Execute search queries concurrently using asyncio and return results."""
    search_results = {"queries": {}}
    query_tasks = []

    # Step 1: Prepare tasks for all queries
    for step, queries in step_queries.items():
        for query in queries:
            query_tasks.append((step, query, web_search_wrapper(query)))

    # Step 2: Run all web searches concurrently
    responses = await asyncio.gather(*(task[2] for task in query_tasks), return_exceptions=True)

    # Step 3: Build the structured response
    for i, (step, query, _) in enumerate(query_tasks):
        response = responses[i]
        if isinstance(response, Exception):
            search_results["queries"][query] = {
                "error": str(response)
            }
        else:
            answer = response.get("answer", "No answer found")
            citations = response.get("citations", [])[:1]

            search_results["queries"][query] = {
                "answer": answer,
                "top_citations": citations
            }

    return search_results
