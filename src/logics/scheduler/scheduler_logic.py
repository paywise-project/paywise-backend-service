import json
import logging
from datetime import datetime, timedelta

import redis

from src.configs.runtime_config import RuntimeConfig
from src.logics.notification.notification_logic import NotificationLogic
from src.logics.payment.payment_logic import PaymentLogic
from src.logics.user.user_logic import UserLogic
from src.models.dtos.notification.domain.v1.notification_domain_interface_dtos import (
    CreateNotificationInputDTOV1,
    CreateNotificationRestInputDTOV1,
)
from src.models.dtos.user.domain.v1.user_domain_interface_dtos import GetUserInputDTOV1
from src.models.types.enums import NotificationStatusType, NotificationType, PaymentOccurrenceStatusType

logger = logging.getLogger(__name__)


class SchedulerLogic:
    def __init__(
        self,
        payment_logic: PaymentLogic,
        notification_logic: NotificationLogic,
        user_logic: UserLogic,
    ) -> None:
        self._payment_logic = payment_logic
        self._notification_logic = notification_logic
        self._user_logic = user_logic
        self._redis = redis.from_url(RuntimeConfig.global_config().REDIS_URL)

    async def process_due_occurrences(self) -> None:
        logger.info("Job 1: processing overdue occurrences")
        processed = await self._payment_logic.process_overdue_occurrences()
        logger.info(f"Job 1: processed {len(processed)} occurrences")
        return processed

    async def extend_infinite_occurrences(self, processed) -> None:
        logger.info("Job 2: extending infinite occurrences")
        await self._payment_logic.extend_infinite_occurrences(processed=processed)
        logger.info("Job 2: done")

    async def create_due_notifications(self) -> None:
        logger.info("Job 3: creating notifications")
        today = datetime.now().date()
        tomorrow = today + timedelta(days=1)
        week_later = today + timedelta(days=7)

        occurrences = await self._payment_logic.get_occurrences_for_notifications()
        logger.info(f"Job 3: found {len(occurrences)} occurrences to evaluate")

        for occ in occurrences:
            due_date = occ.due_datetime.date()

            if due_date == today and occ.notify_on_day:
                notification_type = NotificationType.PAYMENT_DUE_TODAY
                title = f"سررسید پرداخت امروز: {occ.title}"
                message = f"پرداخت {occ.amount} تومان بابت {occ.title} امروز سررسید دارد."
            elif due_date == tomorrow and occ.notify_day_before:
                notification_type = NotificationType.PAYMENT_DUE_DAY_BEFORE
                title = f"سررسید پرداخت فردا: {occ.title}"
                message = f"یادآوری: پرداخت {occ.amount} تومان بابت {occ.title} فردا سررسید دارد."
            elif due_date == week_later and occ.notify_week_before:
                notification_type = NotificationType.PAYMENT_DUE_WEEK
                title = f"سررسید پرداخت در ۷ روز آینده: {occ.title}"
                message = f"یادآوری: پرداخت {occ.amount} تومان بابت {occ.title} یک هفته دیگر سررسید دارد."
            else:
                continue

            try:
                notification_input = CreateNotificationInputDTOV1.create(
                    user_uuid=occ.user_uuid,
                    input_dto=CreateNotificationRestInputDTOV1(
                        payment_occurrence_uuid=occ.payment_occurrence_uuid,
                        title=title,
                        message=message,
                        notification_type=notification_type,
                        status_type=NotificationStatusType.PENDING,
                        is_read=False,
                    ),
                )
                notification = await self._notification_logic.create_notification(input_dto=notification_input)

                if notification is None:
                    logger.info(f"Duplicate notification skipped for occurrence {occ.payment_occurrence_uuid}")
                    continue

                user = await self._user_logic.get_user(input_dto=GetUserInputDTOV1(user_uuid=occ.user_uuid))
                payload = json.dumps(
                    {
                        "notification_id": str(notification.notification_uuid),
                        "telegram_id": user.telegram_id,
                        "message": message,
                    },
                )
                self._redis.rpush("notification_queue", payload)
                logger.info(f"Queued notification for occurrence {occ.payment_occurrence_uuid}")

            except Exception as e:
                logger.error(f"Failed to create notification for occurrence {occ.payment_occurrence_uuid}: {e}")
                continue

        logger.info("Job 3: done")

    async def run_all_jobs(self) -> None:
        processed = await self.process_due_occurrences()
        await self.extend_infinite_occurrences(processed=processed)
        await self.create_due_notifications()
