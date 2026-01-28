# CLAUDE.md

Guidelines for Claude when working in this repository.

## Project Overview

Personal Claude Code plugins marketplace repository.

GitHub: https://github.com/shiiman/claude-code-plugins

## Plugin Structure

```text
plugins/{plugin-name}/
├── .claude-plugin/plugin.json  # Plugin metadata
├── commands/                   # Slash commands (.md)
├── skills/                     # Skill definitions
├── agents/                     # Agent/Subagent definitions
├── hooks/                      # Hook configurations
└── README.md                   # Plugin documentation
```

## Available Commands

- `/plugin-create` - Create a new plugin
- `/command-create` - Add a command to a plugin
- `/skill-create` - Add a skill to a plugin
- `/subagent-create` - Add a subagent to a plugin
- `/hook-create` - Add a hook to a plugin

## Available Skills

- `issue-create` - Create multiple issues from a plan (trigger: "Issue 作成", "Issue を作って")
- `pr-create` - Create a PR and close related issues (trigger: "PR 作成", "PR を作って")

## Documentation

- docs/plugin.md - Plugin creation guide
- docs/command.md - Command creation guide
- docs/skill.md - Skill creation guide
- docs/subagent.md - Subagent creation guide
- docs/hook.md - Hook creation guide
- docs/issues.md - Issue creation guide
- docs/pr.md - PR creation guide

## Commit Messages

Use Conventional Commits format:

- feat: New feature
- fix: Bug fix
- docs: Documentation update
- refactor: Code refactoring

## Plugin Naming Convention

**Important**: All plugin names MUST use the `shiiman-` prefix to avoid namespace collision with other marketplaces.

| Rule | Example |
|------|---------|
| Prefix required | `shiiman-` |
| Lowercase only | `shiiman-common` ✅ / `shiiman-Common` ❌ |
| Hyphen separator | `shiiman-code-review` ✅ / `shiiman_code_review` ❌ |
| No colons | `shiiman:common` ❌ (conflicts with command separator) |

**Invocation format**: `/shiiman-common:commit`

## Plugin Versioning

Follow [Semantic Versioning](https://semver.org/) (SemVer) for plugin versions:

| Change Type                        | Version Bump | Example         |
|------------------------------------|--------------|-----------------|
| Breaking change                    | MAJOR        | 1.0.0 → 2.0.0   |
| New feature (backward compatible)  | MINOR        | 1.0.0 → 1.1.0   |
| Bug fix (backward compatible)      | PATCH        | 1.0.0 → 1.0.1   |

**Rules**:

- Update `plugin.json` version when adding/modifying plugin features
- Update `marketplace.json` version to match `plugin.json` version
- New command, skill, subagent, or hook → MINOR bump
- Bug fix or documentation update → PATCH bump
- Breaking API/behavior change → MAJOR bump

**Update Process**:

When updating a plugin version:
1. Update `plugins/{plugin-name}/.claude-plugin/plugin.json` version
2. Update `plugins/{plugin-name}/README.md` (if needed)
3. Update `.claude-plugin/marketplace.json` entry version (must match `plugin.json`)

See [docs/plugin.md](docs/plugin.md) for detailed update procedures.

## Constraints

- No dependencies between plugins
- No secrets or credentials
- No binary files
