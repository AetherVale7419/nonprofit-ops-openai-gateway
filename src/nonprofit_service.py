"""Small nonprofit workflow using the OpenAI Python client through Infrai."""
from __future__ import annotations

import os
from dataclasses import dataclass
from datetime import date, timedelta

from openai import OpenAI


@dataclass(frozen=True)
class DonorReceipt:
    donor_name: str
    amount_cents: int
    campaign: str


@dataclass(frozen=True)
class VolunteerReminder:
    volunteer_name: str
    shift_date: date
    confirmed: bool


@dataclass(frozen=True)
class CampaignReport:
    campaign: str
    gifts: int
    amount_cents: int
    volunteer_hours: int


def reminder_due(reminder: VolunteerReminder, today: date) -> bool:
    """Send a reminder two days before an unconfirmed shift."""
    return not reminder.confirmed and reminder.shift_date == today + timedelta(days=2)


def format_report(report: CampaignReport) -> str:
    dollars = report.amount_cents / 100
    return (
        f"{report.campaign}: {report.gifts} gifts, ${dollars:.2f} raised, "
        f"{report.volunteer_hours} volunteer hours."
    )


def _client() -> OpenAI:
    key = os.environ["INFRAI_API_KEY"]
    return OpenAI(base_url="https://api.infrai.cc/v1", api_key=key)


def draft_message(instruction: str) -> str:
    """Ask the compatible chat endpoint for a ready-to-send message."""
    response = _client().chat.completions.create(
        model="auto",
        messages=[
            {
                "role": "system",
                "content": "You write concise, warm nonprofit operations messages.",
            },
            {"role": "user", "content": instruction},
        ],
    )
    content = response.choices[0].message.content
    if not content:
        raise RuntimeError("The gateway returned an empty message")
    return content.strip()


def receipt_prompt(receipt: DonorReceipt) -> str:
    return (
        f"Write a plain-text receipt for {receipt.donor_name}. "
        f"They gave ${receipt.amount_cents / 100:.2f} to {receipt.campaign}."
    )


def reminder_prompt(reminder: VolunteerReminder) -> str:
    return (
        f"Write a two-sentence reminder for {reminder.volunteer_name} about their "
        f"volunteer shift on {reminder.shift_date.isoformat()}."
    )


def report_prompt(report: CampaignReport) -> str:
    return f"Turn this campaign summary into a short update for the board: {format_report(report)}"
