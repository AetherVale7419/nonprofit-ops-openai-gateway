from datetime import date, timedelta

from src.nonprofit_service import CampaignReport, VolunteerReminder, format_report, reminder_due


def test_unconfirmed_shift_two_days_away_is_due() -> None:
    today = date(2026, 9, 5)
    reminder = VolunteerReminder("Ari", today + timedelta(days=2), False)
    assert reminder_due(reminder, today) is True


def test_confirmed_or_other_date_is_not_due() -> None:
    today = date(2026, 9, 5)
    assert reminder_due(VolunteerReminder("Ari", today + timedelta(days=2), True), today) is False
    assert reminder_due(VolunteerReminder("Ari", today + timedelta(days=1), False), today) is False


def test_report_is_readable_for_board_prompt() -> None:
    report = CampaignReport("Pantry", 2, 1250, 4)
    assert format_report(report) == "Pantry: 2 gifts, $12.50 raised, 4 volunteer hours."
