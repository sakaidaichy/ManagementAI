from collectors.common import extract_links


def collect():
    return extract_links(
        source_name="厚生労働省",
        base_url="https://www.mhlw.go.jp/",
        keywords=["助成金", "雇用", "労働", "育児", "介護", "法改正", "賃金"],
    )