from collectors.common import extract_links


def collect():
    return extract_links(
        source_name="熊本市",
        base_url="https://www.city.kumamoto.jp/",
        keywords=["高齢者", "介護", "事業者", "補助金", "助成金"],
    )