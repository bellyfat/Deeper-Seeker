# code for agent orchestration and agent execution

from app.services.followup import run_followup_loop
from app.services.researchplan import generate_research_plan, execute_research_plan
from app.services.web_search import extract_learnings
from app.services.report import generate_report
import json
from typing import Any, Dict
from app.utils.events import send_event


class Agent:
    def __init__(self, websocket):
        self.websocket = websocket

    async def agent_executor(self):
        """function defining the orchestration and execution flow of the agent"""
        try:
                await self.websocket.send_text("Agent executor started. Please enter your query")
                initial_query = await self.websocket.receive_text()

                await self.websocket.send_text(f"Query received: {initial_query}")

                # Follow-up questions
                followup_result = await run_followup_loop(initial_query, 3, self.websocket)
                await send_event(self.websocket,"followup_result" , followup_result)

                # Plan generation
                # await self.websocket.send_text("Generating a research plan...")
                research_plan = await generate_research_plan(
                    followup_result["initial_query"],
                    followup_result["final_context"]
                )
                # await self.websocket.send_text("Research plan generated")

                plan_steps = research_plan["plan"]
                await send_event(self.websocket,"research_plan_generated"  , plan_steps)

                # Plan exec
                # await self.websocket.send_text("Executing research plan...")
                result = await execute_research_plan(plan_steps , self.websocket)
                await send_event(self.websocket,"research_execution_complete"  , result)

                # Extract learning
                # await self.websocket.send_text("Extracting learnings...")
                learnings_string = await extract_learnings(result)
                await send_event(self.websocket,"learnings_extracted" , learnings_string)

                # Final report
                await send_event(self.websocket,"final_report_compilation" , "")
                report_response = await generate_report(initial_query, learnings_string)
                if report_response["status"] == "success":
                    report_content = report_response["final_report_content"]
                    await send_event(self.websocket,"report_generated_saved" , report_content)
                else:
                    await self.websocket.send_text("Error generating report. Please try again.")

                await self.websocket.send_text("You can ask another question or type 'exit' to leave.")

        except Exception as e:
                await self.websocket.send_text(f"Error processing query: {str(e)}")
