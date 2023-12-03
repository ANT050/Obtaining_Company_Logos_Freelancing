import requests
from bs4 import BeautifulSoup


def fetch_html_content(url: str) -> BeautifulSoup | None:
    try:
        response = requests.get(url)

        if response.status_code == 200:
            html_content = response.text
            soup = BeautifulSoup(html_content, 'lxml')

            return soup
        else:
            print(f"Ошибка: {response.status_code}")

            return None

    except Exception:
        print("Ошибка: Неправильно указан URL")

        return None


def get_links_to_categories(url: str) -> list:
    soup = fetch_html_content(url)

    categories = soup.find_all('a', class_='alphabet logo')
    category_links = [category['href'] for category in categories]

    return category_links


def go_to_another_page(url: str) -> str | None:
    soup = fetch_html_content(url)
    next_links = soup.find_all('a', class_='button fullwidth')

    for next_btn in next_links:
        if 'Next' in next_btn.get_text():
            return next_btn.get('href')

    return None


def getting_links_to_svg_files(start_url: str) -> list:
    url = start_url
    svg_links = []

    count = 1

    while url:
        soup = fetch_html_content(url)
        company_logos = soup.find_all(class_='logo__container')

        for logo in company_logos:
            img_tag = logo.find('img')

            if img_tag:
                svg_links.append(img_tag['src'])
                print(f"{count}. {img_tag['src']}")
                count += 1

        url = go_to_another_page(url)

    return svg_links


def main() -> None:
    # url = 'https://worldvectorlogo.com/alphabetical'
    # links_to_categories = get_links_to_categories(url)

    url = 'https://worldvectorlogo.com/alphabetical/a'
    getting_links_to_svg_files(url)


if __name__ == '__main__':
    main()
