# tests/test_followup.py

from services.followup import generate_followup

def test_generate_followup():
    # Test case 1: Normal input
    context = "What are the impacts of climate change on agriculture?"
    result = generate_followup(context)
    print("Test Case 1 - Normal Input:")
    print(result)

    # Test case 2: Empty input
    # context = ""
    # result = generate_followup(context)
    # print("Test Case 2 - Empty Input:")
    # print(result)

    # Test case 3: Invalid input (non-string)
    context = 12345
    try:
        result = generate_followup(context)
        print("Test Case 3 - Invalid Input:")
        print(result)
    except Exception as e:
        print(f"Test Case 3 - Invalid Input Error: {e}")

if __name__ == "__main__":
    test_generate_followup()