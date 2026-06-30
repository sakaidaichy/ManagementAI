from collectors.common import extract_links


def collect():
    return extract_links(
        source_name="玉名市",
        base_url="https://www.city.tamana.lg.jp/",
        keywords=["高齢介護", "介護", "高齢者", "事業者", "補助金"],
    )