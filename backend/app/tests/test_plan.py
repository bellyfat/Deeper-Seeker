# tests/test_plan.py

from services.researchplan import generate_research_plan, execute_research_plan

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

def test_generate_research_plan():
    """Test the research plan generation based on the context."""
    topic = "What are the impacts of climate change on agriculture?"
    result = generate_research_plan(topic, context)

    print("\nTest - Generate Research Plan:")
    print(result)



def test_execute_research_plan():
    """Test executing the generated research plan."""
    topic = "What are the impacts of climate change on agriculture?"
    research_plan = generate_research_plan(topic, context)  # Generate a plan first
    final_result = execute_research_plan(research_plan["plan"])  # Execute the plan

    print("\nTest - Execute Research Plan:")
    print(final_result)

  
if __name__ == "__main__":
    test_generate_research_plan()
    test_execute_research_plan()
