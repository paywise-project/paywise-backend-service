from archipy.helpers.utils.base_utils import BaseUtils
import jdatetime


class DateUtils(BaseUtils):
    @classmethod
    def get_today_day_in_jalali(cls) -> int:
        shamsi_day = jdatetime.date.today().day
        return shamsi_day
