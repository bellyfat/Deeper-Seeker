from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import os
import json
from google import genai
from google.genai import types
from dotenv import load_dotenv
import logging

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


gemini_client = genai.Client(api_key=GEMINI_API_KEY)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s' ,force = True)
logger = logging.getLogger(__name__)


# Pydantic model for structured Gemini response
class ReportResponse(BaseModel):
    reportMarkdownContent: str

# class ReportResponseModel(BaseModel):
#     status : str
#     report : str | None
#     message : str

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


def save_report_to_file(report_content: str, filename="final_report.md"):
    try:
        if not isinstance(report_content, str):
            raise ValueError("Report content must be a string")

        with open(filename, "w", encoding="utf-8") as file:
            file.write(report_content)

        print(f"Report saved successfully to {filename}")
    except Exception as e:
        print(f"Error saving report: {e}")




# Report generation function - LLM used - gemini2.0
async def generate_report(prompt: str, learnings: str) -> dict:
    """Generate a detailed markdown report using Google Gemini."""
    sys_instruct = "You are a professional research analyst. Your task is to generate a detailed 3-page markdown report based on the provided research data."
    try:
        response = gemini_client.models.generate_content(
            model="gemini-2.0-flash",
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=ReportResponse,
            ),
            contents=[
                f"Given the following prompt from the user, write a final report on the topic using "
                f"the learnings from research. Return a JSON object with a 'reportMarkdown' field "
                f"containing a detailed markdown report (aim for 3+ pages). Include ALL the learnings. use the text field corresponding to the query.The report should be very detailed with inline citations in markdown format :- (text)[source link] in each subsection "
                f"from research:\n\n<prompt>{prompt}</prompt>\n\n"
                f"Here are all the learnings from research:\n\n<learnings>\n{learnings}\n</learnings>"
            ]
        )
        # response parsing using pydantic model
        #  reportResponse is a pydantic model 
        report_response = ReportResponse.model_validate_json(response.text)
        logger.info(f"generated_report: {report_response.reportMarkdownContent[:50]}")
        # save_report_to_file(report)
        report_markdown = str(report_response.reportMarkdownContent)

        save_report_to_file(report_markdown)
        return {
            "status" : "success",
            "final_report_content" : report_response.reportMarkdownContent,
            "message" : "report generated successfully",
        }
    except Exception as e:
        logger.error(f"Error generating report: {e}")
        return {
            "status" : "error",
            "final_report_content" : None,
            "message" : f"failed to generate report: {e}",
        }