# ICEGODS Unified Platform Blueprint

Status: architecture proposal; not a claim that the features are already implemented or tested.

## 1. Product promise

ICEGODS is a web-first blockchain visibility and alerting service with Telegram access. It provides monitoring and evidence-based signals for explicitly supported networks and data sources. It does not promise detection of every event, prevention of every exploit, investment returns, or guaranteed token safety.

### Customer deliverables
- Account and secure sign-in.
- Add/remove public wallet addresses; never request seed phrases or private keys.
- Solana and Ethereum wallet activity monitoring, introduced in tested stages.
- Transaction and balance-activity alerts, with event type, chain, address, timestamp, explorer link and source.
- Token/market indicators where reliable data sources support them; label signals and confidence/limitations.
- Alert history, watchlist management, usage limits and subscription status.
- Telegram bot linking and alert delivery.
- Subscription purchase, payment status, receipts and renewal/expiry information.
- Help, privacy, terms, supported-network matrix and service status.

### Admin deliverables
- Customer/account and subscription management.
- Revenue ledger: verified gross receipts, currency, network, transaction reference, refunds, fees and net totals.
- Bot/service inventory with heartbeat, version, last successful job, queue depth and errors.
- Monitoring coverage, provider health, alert delivery outcomes and incident log.
- Plan/entitlement controls, customer support tools, audit log and operational-cost tracking.
- No customer secrets or private wallet keys.

## 2. Platform layout

1. Public website and pricing pages.
2. Customer dashboard.
3. Admin dashboard (role-protected).
4. API/backend: authentication, account ownership, entitlements and rate limits.
5. Core database: users, wallets, subscriptions, payment orders, verified transactions, events, alerts, bot registry, audit events.
6. Background workers: chain ingestion, normalization, detection rules, notification delivery, payment reconciliation, subscription lifecycle and scheduled maintenance.
7. Provider adapters: Solana RPC/indexer, Ethereum RPC/indexer, market-data providers, Telegram and payment data.
8. Observability: structured logs, metrics, health checks, error reporting, backups and alerts.

All services use one documented API and shared durable database. Bots are workers/clients of the platform, not independent sources of truth. Each bot registers its identity, version, capabilities and heartbeat.

## 3. Event flow

### Wallet activity
Provider event/poll -> validate network and address -> normalize event -> deduplicate by chain + transaction/event identity -> persist -> evaluate enabled rules -> check user entitlement -> enqueue alert -> deliver Telegram/dashboard notification -> record delivery result.

### Subscription payment
Customer selects plan -> backend creates a unique pending order -> checkout displays the exact chain, asset, amount, recipient and expiry -> verifier independently checks the on-chain transaction -> validate chain/cluster, recipient, asset, amount, successful/finalized status, order association and replay protection -> atomically mark payment verified -> activate entitlement -> issue receipt -> record immutable ledger entry.

Never activate from a screenshot, client-side claim, unconfirmed transfer, wrong network, wrong token contract, wrong recipient or reused transaction. Define handling for underpayment, overpayment, late payment, wrong asset and refunds. Do not silently credit ambiguous payments.

### Bot lifecycle
Worker starts -> validates configuration -> connects to database/providers -> registers heartbeat -> processes durable jobs -> records success/failure -> retries transient failures with bounded backoff -> exposes health status. Uptime checks only verify reachability; they do not keep a sleeping worker reliably processing jobs.

## 4. Dashboard information architecture

### Customer navigation
Overview | My Wallets | Alerts | Token Signals | Telegram | Subscription & Billing | Help & Status | Account & Privacy

Overview cards must be computed from real database records, never demo/sample activity in production. Empty states should explain how to connect a wallet. Show last data update and provider status.

### Admin navigation
Command Center | Customers | Subscriptions | Revenue Ledger | Wallet Activity | Detection Rules | Bots & Workers | Integrations | Incidents & Logs | Plans | Settings

Admin-only metrics must be protected by server-side roles, not merely hidden in the interface. Financial totals must reconcile to verified ledger entries and clearly separate pending payments, refunds and fees.

## 5. Configuration contract

The application must have one canonical configuration schema and validate it at startup. This is a proposed inventory, not a statement that every current code module already reads these names. Implement only variables required by a specific enabled integration; fail closed with clear errors when required settings are absent.

### Core
- APP_ENV=development|staging|production
- APP_BASE_URL=
- API_BASE_URL=
- SECRET_KEY= (secret; generate a strong random value)
- DATABASE_URL= (secret; managed durable PostgreSQL URL for production)
- LOG_LEVEL=INFO
- TIMEZONE=UTC
- CORS_ALLOWED_ORIGINS=
- SESSION_COOKIE_SECURE=true (production)
- ENCRYPTION_KEY= (secret; only if field encryption is implemented)

### Admin and identity
- ADMIN_USER_IDS= (server-side allowlist; never trust a client-supplied admin flag)
- AUTH_PROVIDER= (only if external identity provider is implemented)
- AUTH_CLIENT_ID=
- AUTH_CLIENT_SECRET= (secret; only if required)

### Telegram
- TELEGRAM_BOT_TOKEN= (secret)
- TELEGRAM_WEBHOOK_SECRET= (secret; webhook mode only)
- TELEGRAM_WEBHOOK_URL=
- TELEGRAM_ADMIN_CHAT_ID=
- TELEGRAM_PUBLIC_CHANNEL_ID= (optional)
- TELEGRAM_BOT_USERNAME=

### Solana
- SOLANA_CLUSTER=mainnet-beta
- SOLANA_RPC_URL= (secret if provider key is embedded)
- SOLANA_RECEIVE_ADDRESS= (public receiving address)
- SOLANA_INDEXER_API_KEY= (secret; only for chosen provider)
- SOLANA_CONFIRMATION_POLICY=finalized

### Ethereum
- ETHEREUM_CHAIN_ID=1
- ETHEREUM_RPC_URL= (secret if provider key is embedded)
- ETHEREUM_RECEIVE_ADDRESS= (public receiving address)
- ETHEREUM_INDEXER_API_KEY= (secret; only for chosen provider)
- ETHEREUM_CONFIRMATION_POLICY= (define safe finality policy)

### Market data and detection
- MARKET_DATA_PROVIDER=
- MARKET_DATA_API_KEY= (secret; only if required)
- DEX_DATA_PROVIDER=
- DETECTION_POLL_INTERVAL_SECONDS=
- ALERT_SCORE_THRESHOLD=
- ENABLE_EXPERIMENTAL_DETECTIONS=false

### Billing and operations
- SUPPORTED_PAYMENT_ASSETS=
- PAYMENT_ORDER_TTL_MINUTES=
- PAYMENT_MIN_CONFIRMATIONS=
- SUBSCRIPTION_GRACE_PERIOD_HOURS=
- SUPPORT_CONTACT=
- STATUS_PAGE_URL=
- ERROR_REPORTING_DSN= (secret; optional)
- BACKUP_POLICY= (document provider and retention outside this variable)

### Deployment
- PORT= (platform-provided where applicable)
- WORKER_CONCURRENCY=
- JOB_MAX_RETRIES=
- JOB_RETRY_BACKOFF_SECONDS=
- HEALTHCHECK_TOKEN= (secret if health endpoint needs protection)

Do not commit actual tokens, API keys, database passwords, private keys, seed phrases, or secret webhook values. Commit only placeholders in .env.example. Receiving addresses are public but should be configured in the deployment environment and validated against the intended chain. The two receiving addresses supplied by the owner must be checked for correctness and chain compatibility before enabling payment collection.

## 6. Security and privacy requirements

- Public wallet addresses only; no custody, signing, seed phrase or private-key collection.
- Separate customer and admin roles; enforce ownership in every API query.
- Secrets in hosting environment variables/secret manager, never Git.
- HTTPS, secure cookies, CSRF protection where applicable, input validation and rate limits.
- Database constraints and transactions for payment idempotency and entitlement activation.
- Audit admin actions and sensitive account changes.
- Minimize personal data; define retention, export and deletion processes.
- Protect webhook endpoints with signature/secret validation and replay protection.
- Restrict CORS and validate redirect/callback URLs.
- Backups with documented restore tests.
- No automated fund transfers, swaps, trading or treasury investment in the initial release.

## 7. Reliability and operations

- Durable queue or database-backed job table; do not rely on in-memory queues for critical work.
- Provider timeouts, bounded retries, circuit breakers and provider health indicators.
- Deduplication and idempotent processing for chain events, payments and alerts.
- Alert delivery retries, user mute/opt-out controls and delivery receipts.
- Structured logs with correlation IDs; never log secrets.
- Health endpoints distinguish web/API readiness from worker/provider health.
- Monitor database availability, queue age, last chain cursor, last successful poll, bot heartbeat and notification failures.
- Production needs a durable database and continuously running worker. Free/sleeping hosts may be suitable for a demo, not a paid 24/7 monitoring promise.

## 8. Existing bot integration policy

Inventory every repository and identify its real function, runtime, dependencies, data store, credentials, deployment, owner and status. Do not display a bot as online until it reports a recent heartbeat. Do not connect unknown or duplicate bots blindly. Migrate each bot behind a common adapter/API and retire duplicated payment, user and wallet databases after verified migration.

## 9. Phased delivery and acceptance gates

### Phase 0 — audit and inventory
- Inspect dashboard, website, MEX-WarSystem and all candidate bot repositories.
- Map duplicate functionality, configuration names, databases, APIs and existing deployment.
- Produce a capability matrix: working, partial, placeholder, broken, unknown.
- No production claims before runtime evidence.

### Phase 1 — foundation
- Canonical config validation, PostgreSQL schema/migrations, authentication, roles, audit log and API.
- CI, linting, unit tests, staging environment and secret scanning.
- Acceptance: clean startup with valid config; clear failure with missing config; tenant isolation tests pass.

### Phase 2 — first paid service
- Solana public-wallet watchlists, normalized events, durable jobs, Telegram delivery and dashboard history.
- Acceptance: test wallet event appears once, retries safely, delivery recorded, opt-out respected, worker restart does not lose cursor/state.

### Phase 3 — subscriptions
- Unique payment orders and chain verifier; begin with one explicitly supported payment asset per network.
- Acceptance: correct payment activates once; wrong chain/recipient/amount, failed/unfinalized transfer and replay do not activate; late/underpaid cases are visible for resolution.

### Phase 4 — Ethereum and additional detections
- Add Ethereum only after independent chain-specific tests. Add token/contract/liquidity signals as separate, evidence-backed capabilities.
- Acceptance: documented coverage, source provenance, false-positive review and provider outage tests.

### Phase 5 — all-bot command centre
- Register and integrate each approved bot, expose heartbeat and capability metadata, unify billing/identity.
- Acceptance: every listed bot is tied to a real process and health signal; offline bots show offline.

### Phase 6 — launch and growth
- Public documentation, pricing, support, status page, demo videos, referral tracking and analytics with consent.
- Launch only after security review, backup restore test, end-to-end payment tests and operational runbook.

## 10. Initial release exclusions

No claim of detecting all threats or all tokens. No guaranteed profit, token safety, rug-pull prevention or investment advice. No automatic trading, wallet sweeping, treasury transfers, custody or private-key handling. No fabricated customers, activity, testimonials, uptime or performance figures.

## 11. Required evidence before public launch

Publish a feature matrix and test results; verify payment paths on the intended networks; test database restore; demonstrate tenant isolation; confirm provider rate limits and costs; verify alert delivery and retries; confirm privacy/terms; and document known limitations. A passing unit-test suite alone is not proof of production readiness.
