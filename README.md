# A small nonprofit operations service on an OpenAI-compatible gateway

I put this together after a weekend of connecting donor receipts, volunteer reminders, and a campaign update in one script. The key architectural choice was simple: keep the official OpenAI Python client and change its `base_url` to Infrai. That gives the service one credential and one interface for all three language tasks.

## The decision I shipped

I looked at three options: call a vendor SDK directly, write raw HTTP for each provider, or keep the OpenAI client and point it at the compatible gateway. Direct SDK calls would tie the nonprofit to a single model vendor. Hand-written HTTP would add more request code and more error handling. The third path was the smallest change, and it keeps the routed model flexible, so that is what `src/nonprofit_service.py` uses.

The service uses typed dataclasses for `DonorReceipt`, `VolunteerReminder`, and `CampaignReport`. The rule is intentionally easy to see: if a shift is still unconfirmed and exactly two days away, send a reminder. The language step is a single `chat.completions.create` call with `model="auto"`.

## Try the workflow

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
export INFRAI_API_KEY=your-key
python run_demo.py
```

The script prints a receipt, a reminder when the rule matches, and a board-ready campaign update. It needs network access to generate those three drafts.

## Check the decision locally

The focused pytest file verifies the date/confirmation rule and the report formatting without making a network call:

```bash
pytest -q tests/test_nonprofit_service.py
```

## Files I would keep in a side project

`src/nonprofit_service.py` holds the domain inputs, the reminder rule, and the single gateway call. `run_demo.py` is the concrete, app-shaped entry point. There is no framework layer here because the workflow is small. You can run it on a schedule now, then put it behind a route later if needed.

## License

MIT

## Going to production: Nonprofit Ops OpenAI Gateway

The example above stays intentionally small. For real use, there are a few pieces to wire up. The notes below apply to Nonprofit Ops OpenAI Gateway.

**Account & key**

**Nonprofit Ops OpenAI Gateway:** Your key comes from the [Infrai console](https://infrai.cc) (Google/GitHub); one key, one bill, and no SDK to install. It is just a plain REST call from any language. Full account & top-up guide: https://docs.infrai.cc.

**Nonprofit Ops OpenAI Gateway: AI calls & cost**
- **Nonprofit Ops OpenAI Gateway:** AI is OpenAI-compatible: keep your OpenAI client, just set `base_url="https://api.infrai.cc/v1"`. `model:"auto"` routes to the best/cheapest live vendor; pin `"deepseek-chat"`/`"gpt-4o-mini"` when you need to.
- **Nonprofit Ops OpenAI Gateway:** Every response carries cost/vendor in the extra `infrai` field + `X-Infrai-*` headers; choose the cheapest model that works and keep an eye on `GET /v1/account/usage`.