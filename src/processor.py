import ollama
import time
import json
import hashlib
import asyncio
import redis
from email_fetcher import EmailFetcher
from database import Database
from kafka_handler import EmailKafkaHandler

class EmailProcessor:
   def __init__(self):
       self.db = Database()
       self.fetcher = EmailFetcher()
       self.model = "mistral"
       self.redis = redis.Redis(host='localhost', port=6379)
       self.cache_ttl = 3600  
       self.kafka_handler = EmailKafkaHandler()

   async def process_emails_batch(self, emails):
       tasks = []
       for email in emails:
           tasks.append(self.process_email(email['content']))
       return await asyncio.gather(*tasks)

   async def process_new_emails(self, limit=10):
        try:
            print(f"Fetching {limit} emails...")
            emails = await self.fetcher.fetch_recent_emails(limit)
            print(f"Processing batch of {len(emails)} emails...")
            start_time = time.time()
            processed_results = await self.process_emails_batch(emails)
            results = []
            for email, processed in zip(emails, processed_results):
                # Send to Kafka queue
                self.kafka_handler.send_email({
                    'subject': email['subject'],
                    'content': email['content']
                })

                results.append({
                    'subject': email['subject'],
                    'source_account': email['source_account'],
                    'processed_data': processed
                })
            print(f"Batch processing completed in {time.time() - start_time} seconds")
            return {"results": results}
        except Exception as e:
            raise Exception(f"Error processing emails: {e}")


   async def process_email(self, email_content: str):
       cache_key = hashlib.md5(email_content.encode()).hexdigest()
       cached = self.redis.get(cache_key)
       if cached:
           return json.loads(cached)

       start_time = time.time()
       
       try:
           response = ollama.chat(model=self.model, messages=[{
               'role': 'user',
               'content' : """First identify phrases about dates and classify them:
                - "I need it to arrive by X" = Required by Date
                - "hoping the package arrives by X" = Required by Date  
                - "need to send by X" = Package Ready Date
                - "must send out by X" = Package Ready Date
                - "gone by X" = Package Ready Date

                Do NOT make assumptions about dates not mentioned in the email.
                Do NOT infer dates based on other information.
                Mark as "Not specified" if date type isn't clearly stated.

                Extract information:
                Name: <name>
                Age: <age if stated, otherwise Not specified>
                Source Address: <pickup location>
                Destination Address: <delivery location>
                Package Ready Date: <only if explicitly stated as send/pickup/ready date>
                Required by Date: <only if explicitly stated as arrival/delivery date>
                Price Range: <budget>
                Is Price Negotiable: <yes/no/Not specified>

                Email: """ + email_content
           }])
           
           extracted = self.parse_llm_response(response['message']['content'])
           processing_time = time.time() - start_time
           
           result = {
               "extracted_info": extracted,
               "processing_time": processing_time
           }
           
           self.redis.setex(cache_key, self.cache_ttl, json.dumps(result))
           
           return result
           
       except Exception as e:
           print(f"Error processing email: {e}")
           raise
   async def get_all_emails(self):
        emails = await self.fetcher.fetch_recent_emails(limit=50)
        results = []
        for email in emails:
            processed = await self.process_email(email['content'])
            results.append({
                'subject': email['subject'],
                'source_account': email['source_account'],
                'processed_data': processed
        })
        return results

   def parse_llm_response(self, response_text):
       info = {}
       lines = response_text.strip().split('\n')
       for line in lines:
           if ':' in line:
               key, value = line.split(':', 1)
               info[key.strip()] = value.strip()
       return info