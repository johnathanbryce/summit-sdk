# Security Policy

## Supported Versions

We release security updates for the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 1.x     | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

**Please do not report security vulnerabilities through public GitHub issues.**

Instead, please report them via email to: **[johnathanbryce@gmail.com]**

You should receive a response within **48 hours**. If the vulnerability is confirmed, we will:

1. Work on a patch immediately
2. Release a security update as soon as possible
3. Credit you in the release notes (unless you prefer to remain anonymous)

## Security Best Practices

The Summit SDK follows these security practices:

- All dependencies are monitored via Dependabot
- All commits to `main` require pull request review
- Secrets are never committed to the repository
- All API communications use HTTPS
- User data is never logged or stored (except as documented)

## Disclosure Policy

When we receive a security bug report, we will:

1. Confirm the vulnerability and determine affected versions
2. Audit code to find similar issues
3. Prepare fixes for all supported versions
4. Release patched versions immediately
5. Publish a security advisory on GitHub

Thank you for helping keep Summit SDK secure!