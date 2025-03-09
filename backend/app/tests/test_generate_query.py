from services.query_execution import generate_queries_for_step

def test_generate_queries():
    # tc1 : a single step with description
    step = "step 1"
    description = "Analyse trends,consumer habits and behavior in quick food service like zepto cafe/swish." 

    result = generate_queries_for_step(step,description)
    print("Test Case 1 - Normal Input:")
    print(result)


if __name__ == "__main__":
    test_generate_queries()

