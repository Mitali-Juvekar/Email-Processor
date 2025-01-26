import redis

r = redis.Redis()
try:
    r.ping()
    print("Redis connection successful")
except Exception as e:
    print(f"Redis error: {e}")