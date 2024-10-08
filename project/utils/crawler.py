import aiohttp
import asyncio
from bs4 import BeautifulSoup
import re

class Crawler:
    async def fetch_webpage(self, session, url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        async with session.get(url, headers=headers) as response:
            response.raise_for_status()
            return await response.text()

    def clean_text(self, text):
        return re.sub(r'[\s]+', ' ', text).strip()

    def convert_to_markdown(self, html_content):
        soup = BeautifulSoup(html_content, 'html.parser')
        text = soup.get_text()
        clean_text_content = self.clean_text(text)
        return clean_text_content

    async def main(self, urls):
        async with aiohttp.ClientSession() as session:
            tasks = [self.fetch_webpage(session, url) for url in urls]
            html_contents = await asyncio.gather(*tasks)
            content = ''
            for html_content in html_contents:
                content += self.convert_to_markdown(html_content) + '\n\n'
            return content

    def run(self, urls):
        return asyncio.run(self.main(urls))


# if __name__ == '__main__':
#     # Example usage
#     cw = Crawler()
#     print(cw.run(urls=['https://quotes.toscrape.com/random' for _ in range(2)]))
#     # print(cw.run(urls=['https://www.makeoverarena.com/2024/10/07/murdoch-university-rtp-scholarships/' for _ in range(2)]))