import json
import logging

import jdatetime
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
from src.models.types.enums import NotificationStatusType, NotificationType

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
        self._redis = redis.from_url(RuntimeConfig.global_config().REDIS_URL)
        self._user_logic = user_logic

    async def create_notifications_for_upcoming_expenses(self) -> None:
        logger.info("Starting notification creation for upcoming expenses")

        shamsi_today = jdatetime.date.today()
        today_day = shamsi_today.day
        # week_later_day = (shamsi_today + jdatetime.timedelta(days=7)).day
        week_later_day = shamsi_today.day + 7

        search_dto = SearchExpenseInputDTOV1.create(
            user_uuid=None,
            status_type=ExpenseStatusType.UNPAID,
            is_active=True,
            days=(today_day, week_later_day),
            page=1,
            page_size=100,
        )

        expenses_result = await self._expense_logic.search_expenses(input_dto=search_dto)
        logger.info(f"Found {expenses_result.total} unpaid expenses in next 7 days")

        for expense in expenses_result.expenses:
            await self._process_expense(expense=expense, today_day=today_day)

        logger.info("Notification creation completed")

    async def _process_expense(self, expense, today_day: int) -> None:
        days_until_due = expense.day_of_month - today_day

        # notification_type = None
        # title = ""
        # message = ""
        user = await self._user_logic.get_user(input_dto=GetUserInputDTOV1(user_uuid=expense.user_uuid))

        notification_type = NotificationType.PAYMENT_DUE_TODAY
        title = f"Payment Due Today: {expense.title}"
        message = f"Your payment of {expense.amount} for {expense.title} is due today."

        # if days_until_due == 0 and expense.notify_on_day:
        #     notification_type = NotificationType.PAYMENT_DUE_TODAY
        #     title = f"Payment Due Today: {expense.title}"
        #     message = f"Your payment of {expense.amount} for {expense.title} is due today."
        #
        # elif days_until_due == 1 and expense.notify_day_before:
        #     notification_type = NotificationType.PAYMENT_DUE_DAY_BEFORE
        #     title = f"Payment Due Tomorrow: {expense.title}"
        #     message = f"Reminder: Your payment of {expense.amount} for {expense.title} is due tomorrow."
        #
        # elif days_until_due == 7 and expense.notify_week_before:
        #     notification_type = NotificationType.PAYMENT_DUE_WEEK
        #     title = f"Payment Due in 7 Days: {expense.title}"
        #     message = f"Reminder: Your payment of {expense.amount} for {expense.title} is due in one week."

        if not notification_type:
            return

        notification_input = CreateNotificationInputDTOV1.create(
            user_uuid=expense.user_uuid,
            input_dto=CreateNotificationRestInputDTOV1(
                expense_uuid=expense.expense_uuid,
                title=title,
                message=message,
                notification_type=notification_type,
                status=NotificationStatusType.PENDING,
                is_read=False,
            ),
        )

        notification = await self._notification_logic.create_notification(input_dto=notification_input)

        payload = json.dumps(
            {
                "notification_id": str(notification.notification_uuid),
                "telegram_id": user.telegram_id,
                "message": message,
            },
        )
        self._redis.rpush("notification_queue", payload)

        logger.info(f"Queued notification {notification.notification_uuid} for expense {expense.expense_uuid}")
