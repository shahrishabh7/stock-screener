import pytest
from openai_completions import OpenAIService


@pytest.fixture
async def test_openai_service():
    return OpenAIService(api_key="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", model="gpt-3.5-turbo")


@pytest.mark.asyncio
async def test_completion_response(openai_service):
    response = await openai_service.completion("Hello, world!")
    assert response is not None
