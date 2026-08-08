# Security Policy

## Supported Versions
Only the latest branch (`main`) is actively supported with security updates.

## Reporting a Vulnerability

If you discover any security vulnerabilities, API key leaks, or unintentional data exposure within this repository, **do not open a public issue.** 

Please email the maintainers directly. We will investigate the issue and push a patched release within 48 hours.

## Environment Variables
This project utilizes a `.env` file for secure credential injection (database passwords, etc.). 
- **NEVER** commit your `.env` file to version control.
- Use `.env.example` as a template for new environments.
- CI/CD pipelines (GitHub Actions) rely on GitHub Secrets (`${{ secrets.DB_PASSWORD }}`). Do not hardcode credentials into `.github/workflows/tests.yml`.
