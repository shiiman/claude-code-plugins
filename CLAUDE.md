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

- `/create-plugin` - Create a new plugin
- `/create-command` - Add a command to a plugin
- `/create-skill` - Add a skill to a plugin
- `/create-subagent` - Add a subagent to a plugin
- `/create-hook` - Add a hook to a plugin

## Documentation

- docs/plugin.md - Plugin creation guide
- docs/command.md - Command creation guide
- docs/skill.md - Skill creation guide
- docs/subagent.md - Subagent creation guide
- docs/hook.md - Hook creation guide

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

## Constraints

- No dependencies between plugins
- No secrets or credentials
- No binary files
