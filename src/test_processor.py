from processor import EmailProcessor
import asyncio
import json

async def test_processor():
    processor = EmailProcessor()
    
    test_email = """
    Hello,
    My name is Sarah Johnson, I'm 28 years old.
    I need to ship a package from 123 Main St, Boston MA to 456 Park Ave, New York NY.
    The delivery date should be January 25th, 2025.
    My budget is $100-150, and I'm open to negotiation.
    Best regards,
    Sarah
    """
    
    try:
        result = await processor.process_email(test_email)
        print("Processing successful!")
        print("Extracted information:", json.dumps(result, indent=2))
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_processor())