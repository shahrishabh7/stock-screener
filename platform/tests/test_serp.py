import os
from serp import SerpService


def test_search_returns_dict():
    # serp_service = SerpService(api_key=os.environ.get("SERP_KEY"))
    serp_service = SerpService(
        api_key=os.environ.get("SERP_KEY"), engine="google_news")
    query = "Apple market news"

    result = serp_service.search(query)

    assert isinstance(result, dict)
