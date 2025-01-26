from kafka import KafkaConsumer
import json
from datetime import datetime

def main():
   print(f"Starting consumer at {datetime.now()}")
   consumer = KafkaConsumer(
       'email_topic',
       bootstrap_servers=['localhost:9092'],
       auto_offset_reset='earliest',
       value_deserializer=lambda x: json.loads(x.decode('utf-8')),
       group_id='email_group'
   )
   print("Consumer initialized, waiting for messages...")
   try:
        for message in consumer:
            data = message.value
            print(f"\nReceived message:")
            print(f"Subject: {data.get('subject', 'No subject')}")
            print("-" * 50)
   except Exception as e:
        print(f"Error: {e}")

   seen_messages = set()
   for message in consumer:
       msg_id = f"{message.value['subject']}_{message.value['content'][:50]}"
       if msg_id not in seen_messages:
          seen_messages.add(msg_id)
          print(f"Received email:")
          print(f"Subject: {message.value['subject']}")
          print(f"Content: {message.value['content'][:100]}...")
          print("-" * 50)

if __name__ == "__main__":
   main()