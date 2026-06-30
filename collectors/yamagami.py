from collectors.common import extract_links


def collect():
    return extract_links(
        source_name="やまがみ社会保険労務士事務所",
        base_url="https://sr-ky.net/",
        keywords=["助成金", "キャリアアップ", "業務改善", "人材開発", "両立支援"],
    )