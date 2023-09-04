from typing import List
from asyncio import Semaphore, create_task, gather

from app.infra.playwright.get_page_dynamic_content import async_get_page_html_content
from app.infra.postgres.pg_upsert import AsyncPostgresDB
from app.infra.selectolax.magalu_parser import MagaluItemParser


class Magalu:
    @staticmethod
    async def exec(urls: List[str], concurrency_limit: Semaphore):
        tasks = []
        for url in urls:
            scraper = MagaluScraper()
            task = create_task(scraper.scrap(url, concurrency_limit))
            tasks.append(task)
        result = await gather(*tasks)
        return result
    

class MagaluScraper:
    async def scrap(self, url: str, concurrency_limit: Semaphore) -> None:
        async with concurrency_limit:
            try:
                html_content = await async_get_page_html_content(url)
                magalu_item_parser = MagaluItemParser(url, html_content)
                item = magalu_item_parser.get_item()
                await AsyncPostgresDB.upsert_item(item)
            except Exception as e:
                print(e)
