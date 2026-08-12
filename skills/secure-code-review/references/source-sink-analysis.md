# Source-Sink Analysis

How to reason about a specific source/sink pair before claiming a vulnerability exists.

## Definitions

- **Source**: where attacker-influenced data enters the code path under review (HTTP parameter, header, cookie, request body, uploaded file content/name, webhook payload, message queue message, third-party API response, or — for stored variants — previously-attacker-supplied data now read back from a database).
- **Sink**: an operation that is dangerous *if* it receives unsafe attacker-influenced data (query execution, shell command execution, file path construction, deserialization, template rendering, redirect target, outbound HTTP request URL, response body written back to a browser context, etc.). A sink is not dangerous in the abstract — it's dangerous relative to what reaches it.

## The Core Question

**Does attacker-influenced data reach this sink in a form the sink treats as unsafe?** Both halves matter:

- "Does it reach the sink" is a reachability question — see [data-flow-analysis.md](data-flow-analysis.md).
- "In a form the sink treats as unsafe" is a validation/encoding/parameterization question — a value can reach a dangerous sink and still be safe if it was parameterized, escaped, or type-constrained on the way.

## Common Reasoning Failures to Avoid

- **Proximity fallacy**: string concatenation *near* a query call is not evidence the concatenated value is attacker-controlled, or that it reaches the sink unparameterized. Read the actual call.
- **Name fallacy**: a function named `findById` doesn't tell you whether an ownership/authorization check exists — it tells you a lookup happens. Check what's around it.
- **Framework-blindness**: many sinks are only dangerous when a framework's default protection is bypassed (e.g. an ORM's raw-query escape hatch, a template engine's "trust this as HTML" API, `dangerouslySetInnerHTML`-style APIs). The existence of the *safe* default matters as much as the presence of a sink-shaped function call.
- **Single-hop assumption**: a source can pass through several functions, files, or even services before reaching a sink. Don't stop tracing at the first function boundary.

## Minimum Evidence for a Candidate Finding

- The exact source (with file/line).
- The exact sink (with file/line).
- At least one concrete step showing how the value gets from one to the other (even if not every intermediate step is confirmed — see [data-flow-analysis.md](data-flow-analysis.md) for how to represent partial confirmation).
- What, if anything, was checked for validation/sanitization/parameterization between them, and why it does or doesn't neutralize the sink.

Populate `source`, `sink`, and `data_flow` in [finding.schema.json](../../../schemas/finding.schema.json) directly from this analysis — don't paraphrase it into prose only.
