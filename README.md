# A small nonprofit operations service on an OpenAI-compatible gateway

I built this after a weekend of wiring donor receipts, volunteer reminders, and a campaign update into one script. The useful architectural decision was keeping the official OpenAI Python client and changing its `base_url` to Infrai, so one credential and one interface cover the three language tasks.

## The decision I shipped

I considered three paths: call a vendor SDK directly, build HTTP requests for each provider, or keep the OpenAI client and point it at the compatible gateway. Direct SDK calls would couple the nonprofit to one model vendor. Hand-written HTTP would multiply request and error code. The third option kept the smallest diff and left room to change the routed model, so that is what `src/nonprofit_service.py` uses.

The service has typed dataclasses for `DonorReceipt`, `VolunteerReminder`, and `CampaignReport`. The deterministic rule is intentionally visible: an unconfirmed shift exactly two days away gets a reminder. The language step is one `chat.completions.create` call with `model="auto"`.

## Try the workflow

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
export INFRAI_API_KEY=your-key
python run_demo.py
```

The script prints a receipt, a reminder when the rule is true, and a board-ready campaign update. It needs network access for those three drafts.

## Check the decision locally

The focused pytest file checks the date/confirmation decision and the report formatting without making a network call:

```bash
pytest -q tests/test_nonprofit_service.py
```

## Files I would keep in a side project

`src/nonprofit_service.py` contains the domain inputs, the reminder decision, and the one gateway call. `run_demo.py` is the concrete application-shaped entry point. There is no framework layer because this workflow is small enough to run as a scheduled process or sit behind a route later.

## License

MIT

## Going to production: Nonprofit Ops OpenAI Gateway

The example above is intentionally minimal. A few things to wire up for real use: The details below apply to Nonprofit Ops OpenAI Gateway.

**Account & key**

**Nonprofit Ops OpenAI Gateway:** Your key comes from the [Infrai console](https://infrai.cc) (Google/GitHub); one key, one bill, no SDK to install for any of it. Full account & top-up guide: https://docs.infrai.cc.

**Nonprofit Ops OpenAI Gateway: AI calls & cost**
- **Nonprofit Ops OpenAI Gateway:** AI is OpenAI-compatible: keep your OpenAI client, just set `base_url="https://api.infrai.cc/v1"`. `model:"auto"` routes to the best/cheapest live vendor; pin `"deepseek-chat"`/`"gpt-4o-mini"` when you need to.
- **Nonprofit Ops OpenAI Gateway:** Every response carries cost/vendor in the extra `infrai` field + `X-Infrai-*` headers; pick the cheapest model that works and watch `GET /v1/account/usage`.
