### service ro generate followup questions based on the user query.
import json
from typing import Dict , Any
from openai import OpenAI
from dotenv import load_dotenv
import os
from groq import Groq

from prompts import FOLLOWUP_PROMPT

# Load environment variables
load_dotenv()

# Initialize OpenAI client
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
openai_client = Groq(api_key=GROQ_API_KEY)


# Follow-up prompt
FOLLOWUP_PROMPT = FOLLOWUP_PROMPT

def generate_followup(context: str) -> Dict:
    """Generate follow-up questions based on the user query and context."""
    try:
        completion = openai_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": FOLLOWUP_PROMPT},
                {"role": "user", "content": context}
            ],
            response_format={"type": "json_object"},
        )
        return json.loads(completion.choices[0].message.content)
    except json.JSONDecodeError:
        return {"question": "Could you clarify further?", "query_context": context}
    

def run_followup_loop(initial_query: str, iterations: int = 3) -> Dict[str, Any]:
    """Iteratively generate follow-up questions and collect user responses."""
    context = initial_query
    history = []
    for i in range(iterations):
        followup = generate_followup(context)
        question = followup.get("question", "Could you elaborate?")
        print(f"\nAssistant: {question}")
        user_answer = input("Your response: ")
        context += f" Follow-up Q: {question} Follow-up A: {user_answer}"
        history.append({
            "iteration": i + 1,
            "question": question,
            "answer": user_answer,
            "context_snapshot": context
        })
        # Write each interaction to the output file
        # write_output_to_file(f"### Follow-up Interaction {i + 1}\n**Question:** {question}\n**Answer:** {user_answer}\n**Context Snapshot:** {context}")
    return {
        "final_context": context,
        "interaction_history": history,
        "initial_query": initial_query,
        "total_iterations": iterations
    }