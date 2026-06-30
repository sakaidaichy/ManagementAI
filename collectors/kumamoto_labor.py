from collectors.common import extract_links


def collect():
    return extract_links(
        source_name="熊本労働局",
        base_url="https://jsite.mhlw.go.jp/kumamoto-roudoukyoku/",
        keywords=["助成金", "雇用", "労働", "最低賃金", "求人"],
    )