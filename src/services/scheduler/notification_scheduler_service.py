import asyncio
import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from src.configs.runtime_config import RuntimeConfig
from src.logics.scheduler.scheduler_logic import SchedulerLogic

logger = logging.getLogger(__name__)


class NotificationSchedulerService:
    def __init__(self, scheduler_logic: SchedulerLogic) -> None:
        self._scheduler_logic = scheduler_logic
        self._scheduler = AsyncIOScheduler()

    def start(self) -> None:
        self._scheduler.add_job(
            self._scheduler_logic.create_notifications_for_upcoming_expenses,
            # RuntimeConfig.SCHEDULER_TRIGGER_TYPE,
            # hour=RuntimeConfig.SCHEDULER_HOUR,
            # minute=RuntimeConfig.SCHEDULER_MINUTE,
            "interval",
            seconds=60,
            id="daily_notification_check",
        )
        self._scheduler.start()
        logger.info("Notification scheduler started")

    async def run(self) -> None:
        self.start()
        logger.info("Scheduler running, press Ctrl+C to stop")
        try:
            while True:
                await asyncio.sleep(60)
        except (KeyboardInterrupt, SystemExit):
            self._scheduler.shutdown()
            logger.info("Scheduler stopped")
