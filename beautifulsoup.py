import re
import os
from typing import List
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import pdfkit

load_dotenv()

ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')


class BeautifulSoupService:
    def __init__(self, url: str):
        self.headers = {'User-Agent': "rohith.mandavilli@gmail.com"}
        self.pdf_path = "10k.pdf"
        page = requests.get(url, headers=self.headers)
        assert page.status_code, 200
        self.page_content = page.content
        self.html = BeautifulSoup(self.page_content, "html.parser")

        try:
            pdfkit.from_url(url, self.pdf_path)
            print(f"PDF generated and saved at {self.pdf_path}")
        except Exception as e:
            print(f"PDF generation failed: {e}")

    async def get_page_content(self) -> str:
        pgraphs = await self.get_article_from_html()
        return pgraphs

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
