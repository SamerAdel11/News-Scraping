from celery.schedules import crontab
from celery_app import celery

celery.conf.beat_schedule = {
    "run_scraper_every_6_hours": {
        "task": "celery_app.run_spider",  # ✅ Corrected task name
        "schedule": crontab(minute='*/1',
                    # hour="*/6"
                    ),  # ✅ Runs every 6 hours
        "args": ("cnnarabic",),  # ✅ Use correct spider name
    },
}

if __name__ == "__main__":
    celery.start()
