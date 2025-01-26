from database import Database

def test_database():
    db = Database()
    
    # Create tables
    print("Setting up database...")
    db.setup()
    
    # Test insertion
    print("Testing insertion...")
    test_email = "Hi, my name is John, age 25. Shipping from NYC to LA."
    test_data = {
        "name": "John",
        "age": 25,
        "source": "NYC",
        "destination": "LA"
    }
    
    email_id = db.save_email(
        raw_content=test_email,
        extracted_info=test_data,
        model_used="test",
        processing_time=0.5
    )
    
    print(f"Inserted email with ID: {email_id}")
    
    # Test retrieval
    result = db.get_email(email_id)
    print(f"Retrieved email: {result}")

if __name__ == "__main__":
    test_database()