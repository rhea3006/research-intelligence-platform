from apscheduler.schedulers.background import BackgroundScheduler
from ingestion.ingest_paper import run_ingestion

scheduler = BackgroundScheduler()

def scheduled_ingestion():
    print("🚀 Running scheduled ingestion...")

    stats = run_ingestion(verbose=False)

    print(
        f"✅ Finished | Inserted: {stats['inserted']} | "
        f"Skipped: {stats['skipped']}"
    )

scheduler.add_job(
    scheduled_ingestion,
    trigger="interval",
    hours=6,
    id="paper_ingestion",
    replace_existing=True,
)

def start_scheduler():
    if not scheduler.running:
        scheduler.start()
        print("📅 Scheduler started.")

def stop_scheduler():
    if scheduler.running:
        scheduler.shutdown()
        print("🛑 Scheduler stopped.")