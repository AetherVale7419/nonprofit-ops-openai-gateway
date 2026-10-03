from datetime import date

from src.nonprofit_service import (
    CampaignReport,
    DonorReceipt,
    VolunteerReminder,
    draft_message,
    receipt_prompt,
    reminder_due,
    reminder_prompt,
    report_prompt,
)


def main() -> None:
    today = date.today()
    receipt = DonorReceipt("Mina Chen", 7500, "Community Pantry")
    reminder = VolunteerReminder("Luis", today.replace(day=today.day) , False)
    report = CampaignReport("Community Pantry", 18, 143500, 62)

    print("Receipt:\n", draft_message(receipt_prompt(receipt)))
    if reminder_due(reminder, today):
        print("Reminder:\n", draft_message(reminder_prompt(reminder)))
    print("Report:\n", draft_message(report_prompt(report)))


if __name__ == "__main__":
    main()
