import redis
from rq import Queue

redis_connection = redis.Redis(host="redis", port=6379, db=0)
task_queue = Queue("whatsapp_message_queue", connection=redis_connection)
send_queue = Queue("send_message_queue", connection=redis_connection)
