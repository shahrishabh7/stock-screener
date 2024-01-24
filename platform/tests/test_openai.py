import pytest
from openai_completions import OpenAIService


@pytest.fixture
def openai_service():
    return OpenAIService(model="gpt-3.5-turbo", api_key='')


@pytest.mark.asyncio
async def test_completion_real_request(openai_service):
    test_prompt = "What is the capital of France?"
    response = await openai_service.completion(prompt=test_prompt)
    print(response["choices"][0]["message"]["content"])

    assert response is not None
    assert "Paris" in response["choices"][0]["message"]["content"]
