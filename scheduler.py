"""
Eli's Research Scheduler

A lightweight task scheduler that runs research cycles on configurable intervals:
- Hourly: News scan
- Every 6 hours: Opportunity detection
- Daily: System improvement scan
- Weekly: Full research journal synthesis

Uses threading and time.sleep (no cron dependency).
"""

import logging
import threading
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Callable, Dict, List, Optional

from researcher import (
    NewsScanner,
    OpportunityDetector,
    SystemImprover,
    ResearchJournal,
    ResearchPipeline,
)


# ============================================================================
# Configuration
# ============================================================================

ELI_RESEARCH_ROOT = Path("/eli/research")
LOG_FILE = ELI_RESEARCH_ROOT / "scheduler.log"

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)


# ============================================================================
# ScheduledTask Class
# ============================================================================

class ScheduledTask:
    """Represents a scheduled research task."""

    def __init__(
        self,
        name: str,
        interval_seconds: int,
        task_func: Callable,
        description: str = "",
    ):
        self.name = name
        self.interval_seconds = interval_seconds
        self.task_func = task_func
        self.description = description
        self.last_run: Optional[datetime] = None
        self.next_run: Optional[datetime] = None
        self.run_count = 0
        self.error_count = 0
        self.logger = logging.getLogger(f"Task[{name}]")

    def should_run(self) -> bool:
        """Check if task should run now."""
        now = datetime.now()
        if self.last_run is None:
            return True
        elapsed = (now - self.last_run).total_seconds()
        return elapsed >= self.interval_seconds

    def execute(self) -> bool:
        """Execute the task."""
        try:
            self.logger.info(f"Executing {self.name}...")
            self.task_func()
            self.last_run = datetime.now()
            self.next_run = self.last_run + timedelta(seconds=self.interval_seconds)
            self.run_count += 1
            self.logger.info(f"✓ {self.name} completed (run #{self.run_count})")
            return True
        except Exception as e:
            self.error_count += 1
            self.logger.error(f"✗ {self.name} failed: {e}", exc_info=True)
            return False

    def get_status(self) -> Dict:
        """Get task status."""
        return {
            "name": self.name,
            "description": self.description,
            "interval_seconds": self.interval_seconds,
            "last_run": self.last_run.isoformat() if self.last_run else None,
            "next_run": self.next_run.isoformat() if self.next_run else None,
            "run_count": self.run_count,
            "error_count": self.error_count,
        }


# ============================================================================
# ResearchScheduler Class
# ============================================================================

class ResearchScheduler:
    """Orchestrates scheduled research tasks."""

    def __init__(self):
        self.logger = logging.getLogger("ResearchScheduler")
        self.tasks: List[ScheduledTask] = []
        self.running = False
        self._setup_tasks()

    def _setup_tasks(self):
        """Configure all scheduled tasks."""
        # Hourly news scan
        self.add_task(
            ScheduledTask(
                name="news_scan",
                interval_seconds=3600,  # 1 hour
                task_func=self._task_news_scan,
                description="Scan all news feeds for relevant articles",
            )
        )

        # Every 6 hours: opportunity detection
        self.add_task(
            ScheduledTask(
                name="opportunity_detection",
                interval_seconds=21600,  # 6 hours
                task_func=self._task_opportunity_detection,
                description="Detect business and monetization opportunities",
            )
        )

        # Daily: system improvement scan
        self.add_task(
            ScheduledTask(
                name="improvement_scan",
                interval_seconds=86400,  # 24 hours
                task_func=self._task_improvement_scan,
                description="Scan projects for improvement opportunities",
            )
        )

        # Weekly: research journal synthesis
        self.add_task(
            ScheduledTask(
                name="journal_synthesis",
                interval_seconds=604800,  # 7 days
                task_func=self._task_journal_synthesis,
                description="Generate weekly research journal entry",
            )
        )

        # Daily: full-cycle (comprehensive research)
        self.add_task(
            ScheduledTask(
                name="full_cycle",
                interval_seconds=86400,  # 24 hours
                task_func=self._task_full_cycle,
                description="Run complete research pipeline (all tasks)",
            )
        )

    def add_task(self, task: ScheduledTask):
        """Register a scheduled task."""
        self.tasks.append(task)
        self.logger.info(
            f"Task registered: {task.name} (every {task.interval_seconds}s) - {task.description}"
        )

    def _task_news_scan(self):
        """Task: Scan news feeds."""
        scanner = NewsScanner()
        articles = scanner.scan()
        scanner.save_digest()

    def _task_opportunity_detection(self):
        """Task: Detect opportunities."""
        scanner = NewsScanner()
        articles = scanner.scan()
        detector = OpportunityDetector(articles)
        detector.detect()
        detector.save_opportunities()

    def _task_improvement_scan(self):
        """Task: Scan projects for improvements."""
        improver = SystemImprover()
        improver.scan()
        improver.save_improvements()

    def _task_journal_synthesis(self):
        """Task: Generate research journal entry."""
        scanner = NewsScanner()
        articles = scanner.scan()
        detector = OpportunityDetector(articles)
        opportunities = detector.detect()
        journal = ResearchJournal(articles, opportunities)
        entry = journal.generate_entry()
        journal.save_entry(entry)

    def _task_full_cycle(self):
        """Task: Run complete research pipeline."""
        pipeline = ResearchPipeline()
        pipeline.run_full_cycle()

    def run(self, poll_interval: int = 60):
        """Run the scheduler in an infinite loop."""
        self.running = True
        self.logger.info("=" * 70)
        self.logger.info("RESEARCH SCHEDULER STARTED")
        self.logger.info("=" * 70)
        self.logger.info(f"Polling interval: {poll_interval}s")
        self.logger.info(f"Registered tasks: {len(self.tasks)}")
        for task in self.tasks:
            self.logger.info(f"  - {task.name}: every {task.interval_seconds}s")
        self.logger.info("=" * 70)

        try:
            while self.running:
                for task in self.tasks:
                    if task.should_run():
                        task.execute()

                time.sleep(poll_interval)

        except KeyboardInterrupt:
            self.logger.info("\nScheduler interrupted. Shutting down gracefully...")
            self.stop()

    def run_threaded(self, poll_interval: int = 60) -> threading.Thread:
        """Run scheduler in a background thread."""
        thread = threading.Thread(target=self.run, args=(poll_interval,), daemon=True)
        thread.start()
        self.logger.info("Scheduler started in background thread")
        return thread

    def stop(self):
        """Stop the scheduler."""
        self.running = False
        self.logger.info("Scheduler stopped")

    def get_status(self) -> Dict:
        """Get overall scheduler status."""
        return {
            "running": self.running,
            "timestamp": datetime.now().isoformat(),
            "tasks": [task.get_status() for task in self.tasks],
        }

    def print_status(self):
        """Print scheduler status to console."""
        status = self.get_status()
        print("\n" + "=" * 70)
        print("RESEARCH SCHEDULER STATUS")
        print("=" * 70)
        print(f"Running: {status['running']}")
        print(f"Timestamp: {status['timestamp']}")
        print(f"\nTasks ({len(status['tasks'])} total):")
        print("-" * 70)

        for task_status in status["tasks"]:
            print(f"\n{task_status['name'].upper()}")
            print(f"  Description: {task_status['description']}")
            print(f"  Interval: {task_status['interval_seconds']}s")
            print(f"  Run count: {task_status['run_count']}")
            print(f"  Errors: {task_status['error_count']}")
            if task_status["last_run"]:
                print(f"  Last run: {task_status['last_run']}")
            if task_status["next_run"]:
                print(f"  Next run: {task_status['next_run']}")

        print("\n" + "=" * 70)


# ============================================================================
# Demo and Testing
# ============================================================================

def run_demo():
    """Run a demo of the scheduler."""
    logger.info("Starting scheduler demo...")
    scheduler = ResearchScheduler()

    # Run in background thread
    thread = scheduler.run_threaded(poll_interval=30)

    # Print status after some time
    time.sleep(5)
    scheduler.print_status()

    # Keep running for demo
    try:
        while True:
            time.sleep(10)
            print("\n[DEMO] Scheduler is running in background...")
    except KeyboardInterrupt:
        logger.info("Demo interrupted")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "--demo":
        run_demo()
    else:
        # Run scheduler normally
        scheduler = ResearchScheduler()
        scheduler.run(poll_interval=60)
