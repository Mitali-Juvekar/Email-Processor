import asyncio
import json
from processor import EmailProcessor

async def test_full_process():
    processor = EmailProcessor()
    results = await processor.process_new_emails(limit=3)
    
    for result in results:
        print(f"\nProcessing email: {result['subject']}")
        print("Extracted data:", json.dumps(result['processed_data'], indent=2))

if __name__ == "__main__":
    asyncio.run(test_full_process())