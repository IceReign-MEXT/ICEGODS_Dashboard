# ICEGODS Dashboard — Command Portal

This branch adds the first responsive public/customer-facing interface foundation for ICEGODS.

## Preview
Open `portal/index.html` in a browser, or deploy the `portal` folder as a static site.

## Important status
This is an interface prototype, not a production-connected application. It intentionally labels itself PREVIEW MODE. No real customer accounts, payment verification, revenue ledger, bot heartbeats, blockchain monitoring, AI model, owner authentication or automatic repair agent are connected yet. Do not collect payments or promise paid monitoring from this static build.

## Included
- Responsive public portal and navigation
- Platform, bot catalogue, intelligence, plans, documentation and community pages
- Restricted owner command-centre placeholder
- Clear labels preventing demo content from being mistaken for live records
- Mobile navigation and accessible semantic page structure

## Next engineering milestones
1. Build backend API, PostgreSQL schema, migrations and secure authentication/roles.
2. Connect public and customer views to permission-checked API data.
3. Build owner-only revenue ledger, bot registry, service health and incident console.
4. Implement verified, idempotent payment orders and subscription entitlements.
5. Integrate supported chain data sources and Telegram delivery workers.
6. Add documentation-grounded customer AI and policy-limited owner operations agent.
7. Add automated tests, staging, security review, backups and restore tests.

## Configuration
See `.env.example` for the planned environment-variable contract. Most integrations are not implemented by this static portal, so do not enter secrets until their backend adapters exist. Never commit real tokens, API keys, database credentials, private keys or seed phrases.
