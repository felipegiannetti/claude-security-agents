# Command Injection

**CWE-78** · OWASP: Injection (A03:2021)

## What to Look For

Attacker-influenced data reaching a shell/process execution call in a way that lets it be interpreted as shell syntax (command separators, pipes, subshells) rather than purely as an argument value. Highest-risk sinks: any API that invokes a command through a shell interpreter (e.g. `shell=True`-style execution, backtick/`$()`-style string execution) with a concatenated/formatted command string.

## Source-to-Sink Checklist

1. Confirm the value is attacker-influenced (filenames, user-supplied options, data embedded in a constructed command string).
2. Confirm the execution API actually invokes a shell (many "safe" process-spawning APIs take an argument array and never invoke a shell at all — check which one is used).
3. If a shell is invoked, confirm the value isn't properly quoted/escaped for that shell, or check whether it's passed as a discrete argument (safe) vs. interpolated into a single command string (unsafe).
4. Check whether even argument-array-style execution is still unsafe here — some tools accept option-like arguments (e.g. a leading `-`) that change behavior even without shell metacharacters.

## False-Positive Conditions

- **Argument-array execution with no shell involved**: the value is passed as one element of an argument list to a process-spawning API that doesn't invoke a shell — shell metacharacters in the value are inert.
- **Strict allowlist validation**: the value is validated against a fixed set of safe values (e.g. an enum) before use.
- **The command and its arguments are entirely code-defined**, with user input only influencing which fixed, pre-approved command is selected (not its content).

## Severity Notes

Default `critical` per `config/severity.config.yaml` — command injection typically maps directly to remote code execution in the application's runtime context.
