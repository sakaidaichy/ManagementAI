from reports.weekly import make_weekly_report
from app.chatwork import post_to_chatwork


def main():
    message = make_weekly_report()

    print("=== 週報プレビュー ===")
    print(message)

    post_to_chatwork(message)


if __name__ == "__main__":
    main()