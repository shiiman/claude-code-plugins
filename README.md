# shiiman-claude-code-plugins

Personal Claude Code plugins marketplace.

## Usage

```bash
claude plugin marketplace add shiiman/claude-code-plugins
```

## Structure

```
.
├── .claude-plugin/
│   └── marketplace.json    # Marketplace definition
├── plugins/                # Plugin directories
├── .gitignore
└── README.md
```

## Adding Plugins

To add a new plugin, create a directory under `plugins/` with the following structure:

```
plugins/my-plugin/
├── .claude-plugin/
│   └── plugin.json         # Plugin metadata (optional if strict: false)
├── commands/               # Slash commands (optional)
├── agents/                 # Agent definitions (optional)
├── skills/                 # Skill definitions (optional)
└── README.md
```

Then add an entry to `.claude-plugin/marketplace.json`:

```json
{
  "plugins": [
    {
      "name": "my-plugin",
      "source": "./plugins/my-plugin",
      "description": "My plugin description",
      "strict": false
    }
  ]
}
```
