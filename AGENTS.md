# AGENTS.md

Guidelines for AI agents (Codex, Devin, etc.) working on agent/subagent definitions in this repository.

For general project rules (naming, versioning, constraints), see [CLAUDE.md](CLAUDE.md).

## Agent File Format

Agent definitions live in `plugins/{plugin-name}/agents/{agent-name}.md` and use YAML frontmatter:

```yaml
---
name: agent-name
description: One-line description of what this agent does.
allowed-tools: Read, Bash, Glob, Grep
model: sonnet
---
```

### Frontmatter Fields

| Field           | Required | Description                                                                                       |
| --------------- | -------- | ------------------------------------------------------------------------------------------------- |
| `name`          | Yes      | Must match filename (without `.md`). Lowercase, hyphen-separated.                                 |
| `description`   | Yes      | Concise summary (1-2 sentences). Used by Claude Code to decide when to invoke the agent.          |
| `allowed-tools` | Yes      | Comma-separated list of tools the agent can use. See [Allowed Tools Guide](#allowed-tools-guide). |
| `model`         | No       | Model to use. Default: `sonnet`. Use `opus` only for complex reasoning tasks.                     |

## Allowed Tools Guide

Choosing the right `allowed-tools` set is critical. Grant the **minimum permissions** required for the agent's task.

### Tool Categories

| Tool    | Capability             | Risk Level                         |
| ------- | ---------------------- | ---------------------------------- |
| `Read`  | Read files             | Low - read-only                    |
| `Glob`  | Find files by pattern  | Low - read-only                    |
| `Grep`  | Search file contents   | Low - read-only                    |
| `Bash`  | Execute shell commands | **High** - can modify system state |
| `Edit`  | Modify existing files  | **Medium** - changes code          |
| `Write` | Create/overwrite files | **Medium** - changes code          |

### Recommended Tool Sets by Agent Type

| Agent Type              | Recommended Tools                     | Rationale                                          |
| ----------------------- | ------------------------------------- | -------------------------------------------------- |
| **Reviewer / Analyzer** | `Read, Bash, Glob, Grep`              | Needs Bash for `gh` CLI, but should NOT edit files |
| **Specialist / Fixer**  | `Read, Write, Edit, Bash, Grep, Glob` | Needs write access to apply fixes                  |
| **Read-only Inspector** | `Read, Glob, Grep`                    | Pure analysis, no side effects                     |

### Decision Checklist

1. Does the agent need to **run commands** (gh, go, terraform, docker)? → Add `Bash`
2. Does the agent need to **modify code**? → Add `Edit` (and `Write` only if creating new files)
3. Does the agent only **read and analyze**? → Stick to `Read, Glob, Grep`
4. Never grant `Edit`/`Write` to a reviewer-type agent — reviewers report findings, they don't fix them.

## Agent Body Structure

After the frontmatter, the Markdown body defines the agent's behavior:

```markdown
# {Role Title}

{1-2 sentence description of expertise and value.}

## 実行内容

- Specific task 1
- Specific task 2

## 使用タイミング

- When to invoke this agent

## 専門知識

- Domain expertise this agent relies on

## 出力形式

{Expected output format — tables, reports, etc.}

## 使用例

{Example invocations}

## 注意事項

- Do's and Don'ts
```

### Required Sections

| Section             | Purpose                                                    |
| ------------------- | ---------------------------------------------------------- |
| Title + description | Claude Code uses this to match user intent to the agent    |
| 実行内容            | Explicit list of what the agent does (no ambiguity)        |
| 使用タイミング      | When to trigger — helps Claude Code select the right agent |

### Optional but Recommended

| Section  | Purpose                                                        |
| -------- | -------------------------------------------------------------- |
| 専門知識 | Reference standards (OWASP, SOLID, etc.) for grounded analysis |
| 出力形式 | Structured output templates improve consistency                |
| 注意事項 | Guard rails — what the agent should NOT do                     |

## Design Best Practices

### 1. Single Responsibility

Each agent should do ONE thing well.

```text
# Good
reviewer        → reviews code
debugger        → debugs CI failures
command-runner  → executes build/test commands

# Bad
all-in-one      → reviews, fixes, deploys (too broad)
```

### 2. Description Quality

The `description` field is the primary signal for agent selection. Make it specific and action-oriented.

```yaml
# Good
description: Pull Request の変更内容を包括的にレビューし、GitHub に直接コメントを投稿。

# Bad
description: コードを見る。
```

### 3. Include Concrete Commands

If the agent uses `Bash`, document the specific commands it should run. This prevents hallucinated commands.

```markdown
## 使用する gh コマンド

### PR 情報の取得

gh pr view {pr番号} --json title,body,additions,deletions

### レビューコメントの投稿

gh pr review {pr番号} --comment --body "レビュー内容"
```

### 4. Structured Output

Define output tables/templates so results are consistent across invocations.

```markdown
## 出力形式

| 重要度 | ファイル | 行  | 問題                         |
| ------ | -------- | --- | ---------------------------- |
| 高     | foo.ts   | 42  | SQL インジェクションの可能性 |
```

### 5. Guard Rails (注意事項)

Explicitly state what the agent should and should NOT do.

```markdown
## 注意事項

- ✅ エラーログを詳細に分析する
- ✅ 具体的な修正提案を含める
- ❌ 漠然とした提案を避ける
- ❌ ログを読まずに推測で回答しない
```

## Common Pitfalls

| Pitfall                             | Fix                                                                     |
| ----------------------------------- | ----------------------------------------------------------------------- |
| Agent description too vague         | Be specific about what it does and when                                 |
| Giving `Edit`/`Write` to a reviewer | Reviewers should only read and report                                   |
| No output format defined            | Add a template table or report structure                                |
| Overly broad scope                  | Split into multiple focused agents                                      |
| Missing command documentation       | List exact CLI commands the agent should use                            |
| Using `opus` model unnecessarily    | Default to `sonnet`; only use `opus` for tasks requiring deep reasoning |

## Naming Conventions

### Plugin

All plugin names MUST use the `shiiman-` prefix to avoid namespace collision with other marketplaces.

| Rule             | Example                                                |
| ---------------- | ------------------------------------------------------ |
| Prefix required  | `shiiman-`                                             |
| Lowercase only   | `shiiman-common` ✅ / `shiiman-Common` ❌              |
| Hyphen separator | `shiiman-code-review` ✅ / `shiiman_code_review` ❌    |
| No colons        | `shiiman:common` ❌ (conflicts with command separator) |
| Keep it short    | `shiiman-claude` ✅ / `shiiman-claude-manager` ❌      |

### Skill

| Rule                         | Example                                          |
| ---------------------------- | ------------------------------------------------ |
| name field format            | `{plugin-name}:{skill-name}`                     |
| Directory matches skill-name | `skills/pr-create/` → `shiiman-github:pr-create` |
| No redundant plugin prefix   | `review` ✅ / `common-review` ❌                 |
| Lowercase + hyphen only      | `add-commit` ✅ / `add_commit` ❌                |

Invocation format: `/{plugin-name}:{skill-name}` (e.g., `/shiiman-github:pr-create`)

### Agent / Subagent

```text
# Pattern: {role} or {domain}-{role}
reviewer              # generic reviewer
code-reviewer         # code-specific reviewer
security-checker      # security-specific checker
plan-reviewer         # Terraform plan reviewer
command-runner        # command execution specialist

# Rules
- Lowercase only
- Hyphen-separated
- Must match the `name` field in frontmatter
- Must match the filename (e.g., code-reviewer.md → name: code-reviewer)
- No plugin prefix in agent name (reviewer ✅ / github-reviewer ❌)
```

### Common rules

- All resource names use kebab-case (`a-z`, `0-9`, `-`)

## Registration in plugin.json

After creating an agent file, register it in the plugin's `plugin.json`:

```json
{
  "agents": [
    {
      "name": "agent-name",
      "path": "agents/agent-name.md"
    }
  ]
}
```

Ensure `name` in `plugin.json` matches the frontmatter `name` and the filename.

## Markdown Formatting

All `.md` files (including agent definitions) are formatted with Prettier.

- Run `npm run format` after creating or editing agent `.md` files
- Run `npm run format:check` to verify formatting
- Config: `.prettierrc` (`proseWrap: "preserve"` to keep Japanese line breaks intact)
