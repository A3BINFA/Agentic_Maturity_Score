# Branding Setup

Default colors:
- Primary: `#16BAC5`
- Accent: `#1A1D2E`

To brand the PDF report with your logo:
- Use the `/report/file` endpoint with payload including `"brand": {"primary":"#16BAC5","accent":"#1A1D2E","logo_b64":"<base64 png>"}`
- Example payload in `samples/report_request_brand.json` uses the RiteUPAi logo.
