# Email Processing Dashboard

Automated email processor that extracts shipping information using LLMs and displays in a dashboard.

## Features
- Email processing with Mistral LLM
- Multi-account support
- Real-time processing with Kafka
- Redis caching
- PostgreSQL storage

## Prerequisites
- Python 3.10+
- PostgreSQL
- Redis
- Kafka & Zookeeper
- Ollama

## Setup
1. Install dependencies:
```bash
pip install -r requirements.txt

2. Configure environment:
- Copy .env.example to .env
- Add Gmail account credentials (requires 2FA and App Password)
- Configure database settings

3. Start services (each in separate terminal):
```bash
redis-server
zookeeper-server-start /opt/homebrew/etc/kafka/zookeeper.properties
kafka-server-start /opt/homebrew/etc/kafka/server.properties
ollama serve

4. Add email accounts:
```bash
curl -X POST "http://localhost:8000/add-email-account?email=your_email@gmail.com&password=your_app_password&imap_server=imap.gmail.com"

5. Run application:
```bash
cd src
uvicorn main:app --reload

Visit http://localhost:8000/dashboard