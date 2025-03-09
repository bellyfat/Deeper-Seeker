from services.web_search import web_search_wrapper , extract_learnings

def test_websearch():
    #tc1 : normal input
    query = "key players in indian vape market 2025?"
    result = web_search_wrapper(query)
    print("testcase 1 - normal input")
    print(result)

    # final_result = extract_learnings(result.get("output"))
    # print(final_result)



if __name__ == "__main__":
    test_websearch()