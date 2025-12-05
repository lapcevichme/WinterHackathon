from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime, timedelta


def example_scheduler():
    pass

def init_scheduler():
    """
    Add all jobs to scheduler
    """
    scheduler = AsyncIOScheduler()
    
    scheduler.add_job(
        func=example_scheduler,
        trigger="cron",
        minute="*/10",
        id="example",
        next_run_time=datetime.now() + timedelta(seconds=3),
        max_instances=1,
        coalesce=True,
        misfire_grace_time=60,
    )
    
    # scheduler.start()

    return scheduler
