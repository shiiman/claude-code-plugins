# Copilot Instructions

GitHub Copilot review guidelines for this project.

## Project Overview

- **Repository**: {{REPO}}
- **Type**: {{PROJECT_TYPE}}

> **Note**: These values use template variables that are automatically replaced by the `setup` command when this file is generated:
> - `{{REPO}}`: The target repository name configured during setup.
> - `{{PROJECT_TYPE}}`: The project type (e.g., Web App, Backend, Library) selected during setup.

## Review Prefixes

Use these prefixes for review comments:

- **must.** - Required fix (security, correctness, breaking change)
- **imo.** - Improvement suggestion (code quality, performance)
- **nits.** - Minor issues (typos, formatting)
- **q.** - Questions (clarification needed)

## Priority Checks

### Required (must)

- Security vulnerabilities (OWASP Top 10)
- Breaking changes without documentation
- Hardcoded secrets or credentials
- Missing error handling

### Recommended (imo)

- Code duplication
- Missing tests for new functionality
- Performance improvements
- Documentation updates

## Do NOT

- Make assumptions about intent
- Suggest non-existent APIs or methods
- Provide duplicate comments
- Suggest over-optimization
