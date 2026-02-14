from archipy.adapters.postgres.sqlalchemy.adapters import AsyncPostgresSQLAlchemyAdapter
from archipy.adapters.redis.adapters import AsyncRedisAdapter
from dependency_injector import containers, providers

from src.configs.runtime_config import RuntimeConfig
from src.logics.admin.admin_logic import AdminLogic
from src.logics.auth.auth_logic import AuthLogic
from src.logics.balance.balance_logic import BalanceLogic
from src.logics.expense.expense_logic import ExpenseLogic
from src.logics.file.file_logic import FileLogic
from src.logics.income.income_logic import IncomeLogic
from src.logics.notification.notification_logic import NotificationLogic
from src.logics.referral.referral_logic import ReferralLogic
from src.logics.scheduler.scheduler_logic import SchedulerLogic
from src.logics.storage.storage_logic import StorageLogic
from src.logics.user.user_logic import UserLogic
from src.repositories.admin.adapters.admin_postgres_adapter import AdminPostgresAdapter
from src.repositories.admin.admin_repository import AdminRepository
from src.repositories.auth.adapters.auth_redis_adapter import AuthRedisAdapter
from src.repositories.auth.auth_repository import AuthRepository
from src.repositories.expense.adapters.expense_postgres_adapter import ExpensePostgresAdapter
from src.repositories.expense.expense_repository import ExpenseRepository
from src.repositories.file.adapters.file_postgres_adapter import FilePostgresAdapter
from src.repositories.file.file_repository import FileRepository
from src.repositories.income.adapters.income_postgres_adapter import IncomePostgresAdapter
from src.repositories.income.income_repository import IncomeRepository
from src.repositories.notification.adapters.notification_postgres_adapter import NotificationPostgresAdapter
from src.repositories.notification.notification_repository import NotificationRepository
from src.repositories.referral.adapters.referral_postgres_adapter import ReferralPostgresAdapter
from src.repositories.referral.referral_repository import ReferralRepository
from src.repositories.storage.adapters.system_storage_adapter import SystemStorageAdapter
from src.repositories.storage.storage_repository import StorageRepository
from src.repositories.user.adapters.user_postgres_adapter import UserPostgresAdapter
from src.repositories.user.user_repository import UserRepository
from src.services.scheduler.notification_scheduler_service import NotificationSchedulerService


class ServiceContainer(containers.DeclarativeContainer):
    # region base adapters
    _config: RuntimeConfig = RuntimeConfig.global_config()
    _postgres_adapter: AsyncPostgresSQLAlchemyAdapter = providers.ThreadSafeSingleton(AsyncPostgresSQLAlchemyAdapter)
    _redis_adapter: AsyncRedisAdapter = providers.ThreadSafeSingleton(AsyncRedisAdapter)
    # endregion

    # region storage
    _storage_system_adapter = providers.ThreadSafeSingleton(SystemStorageAdapter, config=_config)
    _storage_repository = providers.ThreadSafeSingleton(
        StorageRepository,
        system_adapter=_storage_system_adapter,
    )
    storage_logic = providers.ThreadSafeSingleton(
        StorageLogic,
        repository=_storage_repository,
    )
    # endregion

    # region file
    _file_postgres_adapter = providers.ThreadSafeSingleton(FilePostgresAdapter, adapter=_postgres_adapter)
    _file_repository = providers.ThreadSafeSingleton(
        FileRepository,
        postgres_adapter=_file_postgres_adapter,
    )
    file_logic = providers.ThreadSafeSingleton(
        FileLogic,
        storage_logic=storage_logic,
        repository=_file_repository,
    )
    # endregion

    # region referral
    _referral_postgres_adapter = providers.ThreadSafeSingleton(
        ReferralPostgresAdapter,
        adapter=_postgres_adapter,
    )
    _referral_repository = providers.ThreadSafeSingleton(
        ReferralRepository,
        postgres_adapter=_referral_postgres_adapter,
    )
    referral_logic = providers.ThreadSafeSingleton(
        ReferralLogic,
        repository=_referral_repository,
    )
    # endregion

    # region user
    _user_postgres_adapter = providers.ThreadSafeSingleton(
        UserPostgresAdapter,
        adapter=_postgres_adapter,
    )
    _user_repository = providers.ThreadSafeSingleton(
        UserRepository,
        postgres_adapter=_user_postgres_adapter,
    )
    user_logic = providers.ThreadSafeSingleton(UserLogic, repository=_user_repository, referral_logic=referral_logic)
    # endregion

    # region auth
    _auth_redis_adapter = providers.ThreadSafeSingleton(
        AuthRedisAdapter,
        adapter=_redis_adapter,
    )
    _auth_repository = providers.ThreadSafeSingleton(
        AuthRepository,
        redis_adapter=_auth_redis_adapter,
    )
    auth_logic = providers.ThreadSafeSingleton(
        AuthLogic,
        repository=_auth_repository,
        user_logic=user_logic,
        referral_logic=referral_logic,
    )
    # endregion

    # region admin
    _admin_postgres_adapter = providers.ThreadSafeSingleton(
        AdminPostgresAdapter,
        adapter=_postgres_adapter,
    )
    _admin_repository = providers.ThreadSafeSingleton(
        AdminRepository,
        postgres_adapter=_admin_postgres_adapter,
    )
    admin_logic = providers.ThreadSafeSingleton(
        AdminLogic,
        repository=_admin_repository,
    )
    # endregion

    # region expense
    _expense_postgres_adapter = providers.ThreadSafeSingleton(
        ExpensePostgresAdapter,
        adapter=_postgres_adapter,
    )
    _expense_repository = providers.ThreadSafeSingleton(
        ExpenseRepository,
        postgres_adapter=_expense_postgres_adapter,
    )
    expense_logic = providers.ThreadSafeSingleton(
        ExpenseLogic,
        repository=_expense_repository,
    )
    # endregion

    # region income
    _income_postgres_adapter = providers.ThreadSafeSingleton(
        IncomePostgresAdapter,
        adapter=_postgres_adapter,
    )
    _income_repository = providers.ThreadSafeSingleton(
        IncomeRepository,
        postgres_adapter=_income_postgres_adapter,
    )
    income_logic = providers.ThreadSafeSingleton(
        IncomeLogic,
        repository=_income_repository,
    )
    # endregion

    # region notification
    _notification_postgres_adapter = providers.ThreadSafeSingleton(
        NotificationPostgresAdapter,
        adapter=_postgres_adapter,
    )
    _notification_repository = providers.ThreadSafeSingleton(
        NotificationRepository,
        postgres_adapter=_notification_postgres_adapter,
    )
    notification_logic = providers.ThreadSafeSingleton(
        NotificationLogic,
        repository=_notification_repository,
    )
    # endregion

    # region balance
    balance_logic = providers.ThreadSafeSingleton(
        BalanceLogic,
        expense_logic=expense_logic,
        income_logic=income_logic,
    )
    # endregion

    # region scheduler
    scheduler_logic = providers.ThreadSafeSingleton(
        SchedulerLogic,
        expense_logic=expense_logic,
        notification_logic=notification_logic,
        user_logic=user_logic,
    )

    scheduler_service = providers.ThreadSafeSingleton(
        NotificationSchedulerService,
        scheduler_logic=scheduler_logic,
    )
    # endregion
