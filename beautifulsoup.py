import re
import os
from typing import List
import requests
from bs4 import BeautifulSoup
from anthropicService import ClaudeService, HumanAssistantPrompt
from dotenv import load_dotenv
import pdfkit

load_dotenv()

ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')


class BeautifulSoupService:
    def __init__(self, url: str, generate_content: bool =  False):
        self.headers = {'User-Agent': "rohith.mandavilli@gmail.com"}
        self.pdf_path = "10k.pdf"
        self.url = url
        self.page_content = None
        self.html = None
        self.claude = ClaudeService(api_key=ANTHROPIC_API_KEY)

        if generate_content:
            page = requests.get(url, headers=self.headers)
            assert page.status_code, 200
            self.page_content = page.content
            self.html = BeautifulSoup(self.page_content, "html.parser")

    async def generate_pdf(self) -> None:
        try:
            # need to run brew install Caskroom/cask/wkhtmltopdf to use successfully
            pdfkit.from_url(self.url, self.pdf_path)
            print(f"PDF generated and saved at {self.pdf_path}")
        except Exception as e:
            print(f"PDF generation failed: {e}")

    async def get_page_content(self) -> str:
        pgraphs = await self.get_article_from_html()

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

    async def get_text_from_sec_html(self) -> str:
        elements = []
        
        for span in self.html.find_all("span"):
            if span.find_parent("table"):
                continue
            elements.append(span)

        if not elements:
            return "No <span> tags found on page"
        
        formatted_elements = []
        for i, element in enumerate(elements):
            # remove extra whitespaces \s+ matches multiple spaces in a row
            text = re.sub(r"\s+", " ", element.text).strip()
            prefix = f"{i + 1}. "
            formatted_elements.append(f"{prefix}{text}")

        return "\n".join(formatted_elements)
    
    async def get_tables_from_sec_html(self) -> str:
        table_elements = []

        for table in self.html.find_all("table"):
            table_elements.append(table)
        
        if not table_elements:
            return "No <table> tags found on page"
    
        formatted_elements = []
        for i, element in enumerate(table_elements):
            # remove extra whitespaces \s+ matches multiple spaces in a row
            text = re.sub(r"\s+", " ", element.text).strip()
            prefix = f"{i + 1}. "
            formatted_elements.append(f"{prefix}{text}")

        return "\n".join(formatted_elements)

    async def get_article_from_html(self) -> str:
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

    @staticmethod
    def extract_content_from_line_nums(self, pgraphs: str, line_nums: str) -> List[str]:
        pgraph_elements = pgraphs.split("\n")
        content = []
        for line_num in line_nums.split(","):
            if "-" in line_num:
                start, end = self.extract_initial_line_numbers(line_num)
                if start and end:
                    for i in range(start, min(end + 1, len(pgraph_elements) + 1)):
                        text = ".".join(
                            pgraph_elements[i - 1].split(".")[1:]).strip()
                        content.append(text)
            elif line_num.isdigit():
                text = ".".join(
                    pgraph_elements[int(line_num) - 1].split(".")[1:]
                ).strip()
                content.append(text)
        return content
