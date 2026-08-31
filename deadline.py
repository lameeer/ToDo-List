from PyQt6.QtCore import QDate

DATE_FORMAT = "dd.MM.yyyy"

COLOR_NORMAL = "#7f8c8d"
COLOR_OVERDUE = "#e74c3c"
COLOR_SOON = "#f39c12"
COLOR_COMPLETED = "#b0b0b0"


def days_until_deadline(date_str: str) -> int | None:
    date = QDate.fromString(date_str, DATE_FORMAT)
    if not date.isValid():
        return None
    return QDate.currentDate().daysTo(date)


def _days_word(n: int) -> str:
    n = abs(n)
    if 11 <= n % 100 <= 14:
        return "дней"
    rem = n % 10
    if rem == 1:
        return "день"
    if rem in (2, 3, 4):
        return "дня"
    return "дней"


def _remaining_phrase(days: int) -> str:
    if days == 1:
        return "остался 1 день"
    return f"осталось {days} {_days_word(days)}"


def format_date_with_deadline(date_str: str, completed: bool = False) -> tuple[str, str]:
    if not date_str:
        return "", COLOR_NORMAL

    days = days_until_deadline(date_str)
    if days is None:
        return date_str, COLOR_NORMAL

    if completed:
        return date_str, COLOR_COMPLETED

    if days < 0:
        overdue = abs(days)
        suffix = f" · просрочена на {overdue} {_days_word(overdue)}"
        return date_str + suffix, COLOR_OVERDUE

    if days == 0:
        return date_str + " · срок сегодня", COLOR_SOON

    if days <= 3:
        return date_str + f" · {_remaining_phrase(days)}", COLOR_SOON

    return date_str + f" · {_remaining_phrase(days)}", COLOR_NORMAL
