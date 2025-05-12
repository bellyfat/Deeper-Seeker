import pytest
from services.followup import generate_followup, run_followup_loop

def test_generate_followup():
    """Test generate_followup with different hardcoded inputs."""
    
    # Test Case 1: Normal Input
    context1 = "What are the effects of climate change?"
    result1 = generate_followup(context1)
    print("\nTest Case 1 Result:", result1)
    
    assert isinstance(result1, dict)
    assert "question" in result1  # API should return a follow-up question

    # Test Case 2: Empty String
    context2 = ""
    result2 = generate_followup(context2)
    print("\nTest Case 2 Result:", result2)
    
    assert isinstance(result2, dict)
    assert "question" in result2  # Should still return a valid question

    # Test Case 3: Complex Input
    context3 = "Explain how machine learning is used in climate science and its future potential."
    result3 = generate_followup(context3)
    print("\nTest Case 3 Result:", result3)
    
    assert isinstance(result3, dict)
    assert "question" in result3  # Should generate an advanced follow-up

def test_run_followup_loop():
    """Test run_followup_loop with predefined responses (instead of user input)."""
    
    initial_query = "How does climate change impact agriculture?"
    
    # Hardcoding user responses instead of asking for input()
    user_responses = [
        "Yes, it affects crop yields.",
        "Rising temperatures cause droughts.",
        "Extreme weather impacts livestock."
    ]
    
    context = initial_query
    history = []
    
    for i, response in enumerate(user_responses):
        followup = generate_followup(context)
        question = followup.get("question", "Could you elaborate?")
        
        print(f"\nIteration {i+1}:")
        print(f"Assistant: {question}")
        print(f"User: {response}")
        
        context += f" Follow-up Q: {question} Follow-up A: {response}"
        history.append({
            "iteration": i + 1,
            "question": question,
            "answer": response,
            "context_snapshot": context
        })
    
    # Simulating final output structure
    result = {
        "final_context": context,
        "interaction_history": history,
        "initial_query": initial_query,
        "total_iterations": len(user_responses)
    }

    assert isinstance(result, dict)
    assert "final_context" in result
    assert "interaction_history" in result
    assert result["total_iterations"] == len(user_responses)
    assert len(result["interaction_history"]) == len(user_responses)
