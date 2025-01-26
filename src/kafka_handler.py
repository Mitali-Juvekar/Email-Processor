from kafka import KafkaProducer, KafkaConsumer
import json

class EmailKafkaHandler:
   def __init__(self):
       self.producer = KafkaProducer(
           bootstrap_servers=['localhost:9092'],
           value_serializer=lambda x: json.dumps(x, default=str).encode('utf-8')
       )

   def send_email(self, email_data):
       try:
           self.producer.send('email_topic', value=email_data)
           self.producer.flush()
       except Exception as e:
           print(f"Error sending to Kafka: {e}")