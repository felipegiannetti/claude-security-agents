# Azure

**CWE-16**

## What to Look For

- **Storage accounts/blob containers**: public access level set to allow anonymous read, especially at the container (not just individual blob) level.
- **Network Security Groups**: inbound rules allowing `Any`/`0.0.0.0/0` source on sensitive ports.
- **Azure AD / RBAC**: role assignments at overly broad scope (subscription-wide `Owner`/`Contributor` for a service principal that only needs resource-group-scoped, narrower access).
- **Key Vault**: access policies granting broad permissions instead of least-privilege per-identity policies; soft-delete/purge-protection disabled on a vault holding production secrets.
- **SQL/Cosmos DB firewall rules**: `Allow Azure services` or `0.0.0.0-255.255.255.255` open ranges without justification.

## False-Positive Conditions

- Broad access is confirmed intentional and scoped to a narrow, justified resource group rather than subscription-wide.

## Severity Notes

Public blob container with sensitive content, open database firewall, or subscription-wide `Owner` on an application service principal: `critical`.
