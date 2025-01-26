from email_fetcher import EmailFetcher
import asyncio

async def test_fetch():
    fetcher = EmailFetcher()
    emails = await fetcher.fetch_recent_emails(limit=5)
    for email in emails:
        print(f"\nSubject: {email['subject']}")
        print(f"From: {email['from']}")
        print(f"Date: {email['date']}")
        print("Content:", email['content'][:100], "...")

if __name__ == "__main__":
    asyncio.run(test_fetch())