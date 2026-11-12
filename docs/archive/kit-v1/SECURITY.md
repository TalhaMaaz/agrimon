# Security Policy

This is a university final-year project. No production deployment exists.

## Reporting a vulnerability

Use GitHub private vulnerability reporting (Security tab, "Report a vulnerability") if it is enabled for this repository. Do not open a public issue for a security problem. If it is not enabled, contact the maintainer through the email on the GitHub profile.

## Scope

Code in this repository, its CI configuration and its dependencies. Third-party datasets and services are out of scope.

## Handling of secrets and data

Credentials are never committed. Data, rasters and model weights are not stored in git. If a secret is committed by mistake, rotate it immediately and then remove it from history.
