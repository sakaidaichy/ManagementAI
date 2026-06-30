import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

from app.config import USER_AGENT, REQUEST_TIMEOUT
from app.logger import logger


def fetch_html(url):
    headers = {
        "User-Agent": USER_AGENT
    }

    response = requests.get(
        url,
        headers=headers,
        timeout=REQUEST_TIMEOUT
    )

    response.raise_for_status()
    response.encoding = response.apparent_encoding

    return response.text


def extract_links(source_name, base_url, keywords):
    try:
        html = fetch_html(base_url)

    except Exception as e:
        logger.error(f"{source_name} の取得に失敗: {e}")
        print(f"{source_name} の取得に失敗: {e}")
        return []

    soup = BeautifulSoup(html, "html.parser")
    links = soup.find_all("a")

    results = []
    seen_urls = set()

    for link in links:
        title = link.get_text(strip=True)
        href = link.get("href")

        if not title or not href:
            continue

        if not any(keyword in title for keyword in keywords):
            continue

        full_url = urljoin(base_url, href)

        if full_url in seen_urls:
            continue

        seen_urls.add(full_url)

        results.append({
            "source": source_name,
            "title": title,
            "url": full_url,
        })

    logger.info(f"{source_name}: {len(results)}件取得")
    return results