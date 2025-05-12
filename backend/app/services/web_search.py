from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import os
import requests
import json
from openai import OpenAI
from groq import Groq
from colorama import Fore, Style, init
import time
import pyfiglet
import concurrent.futures
from exa_py import Exa
import httpx

from dotenv import load_dotenv
from app.prompts import GEN_QUERY_PROMPT




# Load environment variables
load_dotenv()

# Initialize OpenAI client
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
EXA_API_KEY = os.getenv("EXA_API_KEY")
EXA_BASE_URL = os.getenv("EXA_BASE_URL")
openai_client = Groq(api_key=GROQ_API_KEY)


GEN_QUERY_PROMPT = GEN_QUERY_PROMPT


async def web_search_wrapper(query: str) -> Dict:
    """Async wrapper around Exa Answer API using httpx."""
    data = {"query": query, "text": True}
    headers = {
        "Authorization": f"Bearer {EXA_API_KEY}",
        "Content-type": "application/json"
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(EXA_BASE_URL, json=data, headers=headers)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPError as error:
        return {"error": str(error)}


# extract learning from the search results
async def extract_learnings(output: dict) -> str:
    """Extract learnings from the search results."""
    learnings = []
    for step, data in output["plan"].items():
        plan_step = data["plan_step"]
        search_results = data["search_results"]["queries"]
        for query, result in search_results.items():
            answer = result["answer"]
            citations = result["top_citations"]
            learnings.append(f"### {plan_step}\n**Query:** {query}\n**Answer:** {answer}\n**Citations:** {json.dumps(citations, indent=2)}")
    return "\n\n".join(learnings)