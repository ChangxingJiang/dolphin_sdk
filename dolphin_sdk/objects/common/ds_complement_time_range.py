"""
海豚调度的调度时间范围
"""

import dataclasses
import datetime

__all__ = [
    "DSComplementTimeRange"
]


@dataclasses.dataclass(slots=True)
class DSComplementTimeRange:
    """海豚调度的补数时间范围"""

    complement_start_date: datetime.datetime = dataclasses.field(kw_only=True)
    complement_end_date: datetime.datetime = dataclasses.field(kw_only=True)

    @staticmethod
    def create_as_default():
        """根据默认值构造，即当日 0 点"""
        today = datetime.datetime.combine(datetime.datetime.now(), datetime.time.min)
        return DSComplementTimeRange(
            complement_start_date=today,
            complement_end_date=today
        )

    def to_json(self) -> dict:
        return {
            "complementStartDate": self.complement_start_date.strftime("%Y-%m-%d %H:%M:%S"),
            "complementEndDate": self.complement_end_date.strftime("%Y-%m-%d %H:%M:%S"),
        }
