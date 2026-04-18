# Sol OS — CLI Manifest

The Sol CLI provides a headless interface to SolManagerAgent using
GitHub Copilot CLI as the execution engine.

## Purpose
- Run SolManagerAgent outside VS Code from any terminal.
- Execute Cloud OS workflows in Codespaces, GitHub Actions, or local scripts.
- Maintain OS → project separation without requiring an open editor.
- Support local validation via AIStudio when available.

## Execution model
Every `sol` command routes to:

```
copilot chat -m "@SolManagerAgent <command>"
```

## Requirements
- GitHub Copilot CLI installed globally (`npm install -g @githubnext/github-copilot-cli`)
- Authenticated: `copilot auth login`
- Active directory must be a Sol-enabled project (contains `.vscode/sol-os/`)
- Cloud OS must be mirrored into `.vscode/sol-os/` before first use

## Script locations
| File | Purpose |
|---|---|
| `sol-os-cloud/scripts/sol` | The `sol` command — installed to `$PATH` |
| `sol-os-cloud/scripts/install-sol-cli.sh` | Installation helper |
| `sol-os-cloud/scripts/sync_os_to_project.sh` | Cloud OS → project mirror |

## Contract files (synced into projects)
| File | Description |
|---|---|
| `os/cli/cli_manifest.md` | This file |
| `os/cli/sol_cli_commands.md` | Full command reference |

## Supported commands
See `sol_cli_commands.md` for the full list.
