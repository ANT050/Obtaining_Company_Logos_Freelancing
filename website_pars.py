import asyncio
import aiohttp
import pandas as pd
from bs4 import BeautifulSoup
from typing import List, Optional


async def fetch_html_content(session: aiohttp.ClientSession, url: str) -> Optional[BeautifulSoup]:
    try:
        async with session.get(url) as response:

            if response.status == 200:
                html_content = await response.text()
                soup = BeautifulSoup(html_content, 'lxml')

                return soup

            else:
                print(f"Ошибка: {response.status}")

                return None

    except Exception:
        print("Ошибка: Неправильно указан URL")

        return None


async def get_links_to_categories(session: aiohttp.ClientSession, url: str) -> List[str]:
    soup = await fetch_html_content(session, url)

    categories = soup.find_all('a', class_='alphabet logo')
    category_links = [category['href'] for category in categories]

    return category_links


async def go_to_another_page(session: aiohttp.ClientSession, url: str) -> Optional[str]:
    soup = await fetch_html_content(session, url)
    next_links = soup.find_all('a', class_='button fullwidth')

    for next_btn in next_links:
        if 'Next' in next_btn.get_text():
            return next_btn.get('href')

    return None


async def get_links_to_svg_files_one_category(session: aiohttp.ClientSession, start_url: str) -> List[str]:
    url = start_url
    svg_links = []

    while url:
        soup = await fetch_html_content(session, url)
        company_logos = soup.find_all(class_='logo__container')

        for logo in company_logos:
            img_tag = logo.find('img')

            if img_tag:
                svg_links.append(img_tag['src'])

        url = await go_to_another_page(session, url)

    return svg_links


async def get_all_links_svg_files(session: aiohttp.ClientSession, url: str) -> List[List[str]]:
    links_to_categories = await get_links_to_categories(session, url)
    all_links_svg_files = []

    count = 1
    for link in links_to_categories:
        svg_file = await get_links_to_svg_files_one_category(session, link)

        all_links_svg_files.append(svg_file)
        print(f'{count} категория алфавита')
        count += 1

    return all_links_svg_files


async def save_links_to_csv(links: list, path_csv: str) -> None:
    flat_links = [link for sublist in links for link in sublist]
    df = pd.DataFrame({"Ссылки на svg логотипы компаний": flat_links})
    df.to_csv(path_csv, index=False, encoding='utf-8')

    print(f"Ссылки сохранены в файл: {path_csv}")


async def main() -> None:
    url = 'https://worldvectorlogo.com/alphabetical'
    path_csv_file = "links_to_svg_files.csv"

    async with aiohttp.ClientSession() as session:
        all_links_svg_files = await get_all_links_svg_files(session, url)

        await save_links_to_csv(all_links_svg_files, path_csv_file)


if __name__ == '__main__':
    asyncio.run(main())
