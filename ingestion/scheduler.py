from apscheduler.schedulers.asyncio import AsyncIOScheduler
from ingestion.ingest_paper import run_ingestion
from datetime import datetime

scheduler = AsyncIOScheduler()

def scheduled_ingestion():
    print("=" * 60)
    print(f"🚀 Scheduler fired at {datetime.now()}")

    try:
        stats = run_ingestion(verbose=True)

        print(
            f"✅ Finished | Inserted: {stats['inserted']} | "
            f"Skipped: {stats['skipped']}"
        )

    except Exception as e:
        print(f"❌ Scheduler failed: {e}")

    print("=" * 60)


scheduler.add_job(scheduled_ingestion,trigger="interval",minutes=1,next_run_time=datetime.now(),
    id="paper_ingestion",replace_existing=True,)

def start_scheduler():
    if not scheduler.running:
        scheduler.start()
        print("📅 Scheduler started.")
        print("Scheduler running:", scheduler.running)
        print("Jobs:", scheduler.get_jobs())

def stop_scheduler():
    if scheduler.running:
        scheduler.shutdown()
        print("🛑 Scheduler stopped.")