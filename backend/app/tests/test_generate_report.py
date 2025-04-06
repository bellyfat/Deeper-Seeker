import logging
import pytest
from app.services.researchplan import generate_research_plan, execute_research_plan
from app.services.report import extract_learnings, generate_report

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Sample test context
context = """Initial User Query:
"What are the impacts of climate change on agriculture?"

Follow-up Questions & Responses:
Q: How does rising temperature affect crop yields?
A: Increased temperatures lead to heat stress, reducing crop productivity and altering growing seasons.

Q: What are the effects of extreme weather events on farming?
A: Floods, droughts, and storms damage crops, soil, and infrastructure, causing economic losses for farmers.

Q: How does climate change impact soil quality and water availability?
A: Rising temperatures and erratic rainfall patterns reduce soil moisture, degrade soil nutrients, and lead to water scarcity.
"""
topic = "What are the impacts of climate change on agriculture?"

# Create a fixture for generating the research plan
@pytest.fixture
def research_plan():
    """Fixture to generate a research plan before running tests"""
    logger.info("Generating research plan for test...")
    try:
        plan = generate_research_plan(topic, context)
        logger.info("Generated Research Plan: %s", plan)
        return plan
    except Exception as e:
        logger.error("Error generating research plan: %s", e, exc_info=True)
        return None

# Modify tests to use the fixture instead of passing arguments
def test_execute_research_plan(research_plan):
    """Test executing the generated research plan."""
    logger.info("Testing execute_research_plan...")

    assert research_plan is not None, "Research plan generation failed"
    assert "plan" in research_plan, "Generated research plan is missing 'plan' key"

    try:
        final_result = execute_research_plan(research_plan["plan"])
        logger.info("Executed Research Plan Results: %s", final_result)
        assert final_result is not None, "Execution failed, no results returned"
    except Exception as e:
        logger.error("Error in execute_research_plan: %s", e, exc_info=True)
        pytest.fail(f"Test failed due to an exception: {e}")

def test_generate_report(research_plan):
    """Test extraction and parsing of plan execution results and generation of final report."""
    logger.info("Testing generate_report...")

    assert research_plan is not None, "Research plan generation failed"
    assert "plan" in research_plan, "Generated research plan is missing 'plan' key"

    try:
        final_result = execute_research_plan(research_plan["plan"])
        logger.info("Executed Research Plan Results: %s", final_result)
        
        assert final_result is not None, "Execution failed, no results returned"

        learnings = extract_learnings(final_result)
        logger.info("Extracted Learnings: %s", learnings)

        report = generate_report(topic, learnings)
        logger.info("Generated Report: %s", report)

        assert report is not None, "Report generation failed"
        assert isinstance(report, dict), "Report should be a string"
    except Exception as e:
        logger.error("Error in generate_report: %s", e, exc_info=True)
        pytest.fail(f"Test failed due to an exception: {e}")
