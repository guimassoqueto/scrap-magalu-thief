from os import getenv
from dotenv import load_dotenv


load_dotenv()

RABBITMQ_DEFAULT_USER = getenv("RABBITMQ_DEFAULT_USER") or "user"
RABBITMQ_DEFAULT_PASS = getenv("RABBITMQ_DEFAULT_PASS") or "password"
RABBITMQ_DEFAULT_HOST = getenv("RABBITMQ_DEFAULT_HOST") or "localhost"
RABBITMQ_RECEIVER_QUEUE = getenv("RABBITMQ_RECEIVER_QUEUE") or "magalu-item"
POSTGRES_PORT = getenv("POSTGRES_PORT") or "5432"
POSTGRES_HOST = getenv("POSTGRES_HOST") or "localhost"
POSTGRES_DB = getenv("POSTGRES_DB") or "postgres"
POSTGRES_USER = getenv("POSTGRES_USER") or "postgres"
POSTGRES_PASSWORD = getenv("POSTGRES_PASSWORD") or "password"
MAX_CONCURRENCY = int(getenv("MAX_CONCURRENCY") or "8") 