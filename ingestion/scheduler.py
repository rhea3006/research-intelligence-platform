from apscheduler.schedulers.asyncio import AsyncIOScheduler
from ingestion.ingest_paper import run_ingestion
from datetime import datetime

scheduler = None


def scheduled_ingestion():
    print("=" * 60)
    print(f"🚀 Scheduler fired at {datetime.now()}")

    try:
        stats = run_ingestion(verbose=True)

        print(
            f"Inserted: {stats['inserted']}"
        )

    except Exception as e:
        print(e)

def start_scheduler():
    global scheduler

    if scheduler is None:
        scheduler = AsyncIOScheduler()

        scheduler.add_job(
            scheduled_ingestion,
            trigger="interval",
            hours=6,
            next_run_time=datetime.now(),
            id="paper_ingestion",
            replace_existing=True,
        )

    if not scheduler.running:
        scheduler.start()

    print("📅 Scheduler started.")
    print("Scheduler running:", scheduler.running)
    print("Jobs:", scheduler.get_jobs())

def stop_scheduler():
    global scheduler

    if scheduler and scheduler.running:
        scheduler.shutdown()