import asyncio
import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from src.configs.runtime_config import RuntimeConfig
from src.logics.scheduler.scheduler_logic import SchedulerLogic

logger = logging.getLogger(__name__)


class SchedulerService:
    def __init__(self, scheduler_logic: SchedulerLogic) -> None:
        self._scheduler_logic = scheduler_logic
        self._scheduler = AsyncIOScheduler()

    def start(self) -> None:
        self._scheduler.add_job(
            self._scheduler_logic.run_all_jobs,
            RuntimeConfig.global_config().SCHEDULER_TRIGGER_TYPE,
            hour=RuntimeConfig.global_config().SCHEDULER_HOUR,
            minute=RuntimeConfig.global_config().SCHEDULER_MINUTE,
            misfire_grace_time=300,
        )
        self._scheduler.start()
        logger.info("Scheduler started — runs daily at 00:05")

    async def run(self) -> None:
        self.start()
        try:
            while True:
                await asyncio.sleep(60)
        except (KeyboardInterrupt, SystemExit):
            self._scheduler.shutdown()
            logger.info("Scheduler stopped")
