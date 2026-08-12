# API Keys

**CWE-798**

## What to Look For

Third-party service API keys (payment processors, mapping/geocoding, email/SMS providers, analytics, AI/LLM providers) hardcoded in source, config files committed to the repository, or client-side/frontend code (where any key is inherently exposed to end users regardless of intent).

## Category-Specific Notes

- A key present in **frontend/client-side code** is exposed to anyone who loads the page — treat as effectively public regardless of the provider's intent, and check whether the provider offers a properly scoped, restrictable "publishable" key type vs. a full-access secret key being used incorrectly client-side.
- Check whether the specific provider's key format gives an immediate exploitability signal (e.g. a key prefix indicating full account access vs. a restricted/read-only key).

## Severity Notes

`critical` for a full-access key to a billing-capable or data-sensitive service found server-side; `high` to `critical` for any secret-type key exposed client-side.
