import re
import requests
from bs4 import BeautifulSoup
from anthropic import ClaudeService, HumanAssistantPrompt


class BeautifulSoupService:
    def __init__(self, html):
        self.html = html

    async def get_page_content(self, url: str) -> str:
        page = requests.get(url)
        if page.status_code != 200:
            page = self.scraper.get(url)

        html = BeautifulSoup(page.content, "html.parser")
        pgraphs = self.get_article_from_html(html)

        prompt = HumanAssistantPrompt(
            human_prompt=f"Below is a numbered list of the text in all the <p> and <li> tags on a web page: {pgraphs} Within this list, some lines may not be relevant to the primary content of the page (e.g. footer text, advertisements, etc.). Please identify the range of line numbers that correspond to the main article's content (i.e. article's paragraphs). Your response should only mention the range of line numbers, for example: 'lines 5-25'.",
            assistant_prompt="Given the extracted text, the main content's line numbers are:",
        )

        line_nums = await self.claude.completion(
            prompt=prompt,
            max_tokens_to_sample=500,
            temperature=0,
        )

        if len(line_nums) == 0:
            return ""

        content = self.extract_content_from_line_nums(pgraphs, line_nums)
        return "\n".join(content)

    def get_article_from_html(self) -> str:
        elements = []
        processed_lists = set()
        for p in self.html.find_all("p"):
            elements.append(p)
            next_sibling = p.find_next_sibling(["ul", "ol"])
            if next_sibling and next_sibling not in processed_lists:
                elements.extend(next_sibling.find_all("li"))
                processed_lists.add(next_sibling)

        if not elements:
            return "No <p> or <li> tags found on page"

        formatted_elements = []
        for i, element in enumerate(elements):
            text = re.sub(r"\s+", " ", element.text).strip()
            prefix = f"{i + 1}. "
            if element.name == "li":
                prefix += "• "
            formatted_elements.append(f"{prefix}{text}")

        return "\n".join(formatted_elements)