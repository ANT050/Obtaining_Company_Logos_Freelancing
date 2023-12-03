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


def main() -> None:
    url = 'https://worldvectorlogo.com/alphabetical'
    links_to_categories = get_links_to_categories(url)

    count = 1
    for link in links_to_categories:
        print(f'{count}. {link}')
        count += 1


if __name__ == '__main__':
    main()
