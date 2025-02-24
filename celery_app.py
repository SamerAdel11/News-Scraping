from celery import Celery
import subprocess

# Initialize Celery
celery = Celery(
    "tasks",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0",
)

celery.conf.task_routes = {"tasks.run_spider": {"queue": "scrapy_queue"}}
celery.conf.task_default_queue = "scrapy_queue"

@celery.task
def run_spider(spider_name: str):
    """Runs a Scrapy spider asynchronously."""
    try:
        subprocess.run(["scrapy", "crawl", spider_name], check=True)
        return f"Spider {spider_name} started successfully!"
    except subprocess.CalledProcessError:
        return f"Failed to start spider {spider_name}!"
