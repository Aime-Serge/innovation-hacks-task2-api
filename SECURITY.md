# Security Policy

## Supported versions

This is an internship training project (Task 2 of the Innovation Hacks Full Stack Development
Internship). Only the `main` branch (latest commit) is supported. The tagged release
`task-2-submission` is a historical snapshot and does not receive fixes.

| Version | Supported |
| --- | --- |
| `main` (latest) | yes |
| `task-2-submission` (tag) | no, snapshot only |

## Reporting a vulnerability

If you find a security issue (for example: an authentication bypass, a way to read another
user's data without authorization, a secret committed to the repository, or a way to crash the
service with a crafted request), please report it privately rather than opening a public issue.

- Contact: <set-me>
- Please include: the endpoint or file involved, steps to reproduce, and the impact you expect.
- Do not include real credentials or personal data in your report.

There is no bug bounty for this project. As a training project, response times are best-effort
and not covered by an SLA.

## Known, accepted limitations

These are documented, intentional trade-offs (see the README's "Known limitations" section and
the ADRs under `docs/adr/`), not vulnerabilities to report:

- State is held in memory and resets on restart (single worker only).
- Tokens cannot be revoked before they expire; there is no refresh token or logout endpoint.
- The rate limiter is per process, not distributed.

## Secret scanning

This repository's CI workflow (`.github/workflows/ci.yml`) runs `gitleaks/gitleaks-action@v2`.
A local, manual proxy check for obvious hardcoded secrets can be run with:

```bash
git grep -nIE '(api[_-]?key|secret|password|token)\s*[:=]\s*["'"'"'][A-Za-z0-9_\-]{12,}'
```

Review any hits by hand; this proxy is not a substitute for gitleaks and does not catch every
secret pattern.
