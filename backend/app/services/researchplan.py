import json
from typing import Dict , Any
from openai import OpenAI
from dotenv import load_dotenv
import os
from groq import Groq
from app.services.query_execution import generate_queries_for_step , execute_queries

from app.prompts import RESEARCH_PLAN_PROMPT
from app.utils.events import send_event

# Load environment variables
load_dotenv()

# Initialize OpenAI client
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
openai_client = Groq(api_key=GROQ_API_KEY)

RESEARCH_PLAN_PROMPT = RESEARCH_PLAN_PROMPT


#  function to generate a research plan based on user query + follow-up QnA context 
async def generate_research_plan(initial_query: str, followup_context: str) -> Dict:
    """Generate a research plan based on the query and follow-up context."""
    try:
        combined_context = initial_query + followup_context
        completion = openai_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": RESEARCH_PLAN_PROMPT},
                {"role": "user", "content": combined_context}
            ],
            response_format={"type": "json_object"},
        )
        research_plan = json.loads(completion.choices[0].message.content)
        # Write the research plan to the output file
        # write_output_to_file("### Research Plan\n" + json.dumps(research_plan, indent=2))
        
        return research_plan
    except json.JSONDecodeError:
        return {"plan": "Could you clarify further?"}
    


# plan_steps = {'plan': {'step 1': 'Identify the primary effects of climate change on agriculture, including rising temperatures, extreme weather events, and changes in precipitation patterns', 'step 2': 'Research the specific impacts of rising temperatures on crop yields, including heat stress, altered growing seasons, and reduced productivity', 'step 3': 'Examine the consequences of extreme weather events, such as floods, droughts, and storms, on farming infrastructure, soil quality, and crop damage', 'step 4': 'Investigate the effects of climate change on soil quality and water availability, including soil moisture reduction, nutrient degradation, and water scarcity', 'step 5': 'Analyze the economic and social implications of climate change on agriculture, including economic losses for farmers, food security concerns, and potential adaptation strategies'}}


### function to execute a research plan (generating queries -> executing queries -> getting the results and content).
### execute_research_plan() dependent on -> generate_queries_for step and execute_queries.
async def execute_research_plan(plan_steps: Dict[str, str] , websocket) -> Dict:
    """ Execute each step of the research plan and fetch search results. """
    search_queries_and_responses = {"plan": {}}

    for step, description in plan_steps.items():

        # Generate search queries for the step
        search_queries = await generate_queries_for_step(step, description)
        
        if step in search_queries:
            queries = search_queries[step].get("search_queries", [])
        else:
            queries = ["No queries generated"]
        
        search_results = await execute_queries({step:queries})

        plan_exec_step = {
            "plan_step" : description,
            "search_queries" : queries,
            "search_results" : search_results
        }

        print(plan_exec_step)
        await send_event(websocket , "plan_execution_steps" ,  plan_exec_step)

        # Store results
        search_queries_and_responses["plan"][step] = plan_exec_step


    return search_queries_and_responses



# if __name__ == "__main__":
#     execute_research_plan(plan_steps["plan"])