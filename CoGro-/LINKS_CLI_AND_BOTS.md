# Grok CLI and bot links

Official product names as of 2026-09. Prefer these over third-party wrappers.

## Install CLI (Grok Build)

```bash
curl -fsSL https://x.ai/cli/install.sh | bash
```

Windows PowerShell

```powershell
irm https://x.ai/cli/install.ps1 | iex
```

npm alternative

```bash
npm i -g @xai-official/grok
```

Verify

```bash
grok --version
grok login
grok inspect
```

Headless

```bash
export XAI_API_KEY="xai-..."
grok -p "Explain CoGro- and sas-hash-fa"
```

ACP bot / IDE bridge

```bash
grok agent stdio
```

## Product URLs

| Surface | URL |
| --- | --- |
| CLI landing | https://x.ai/cli |
| CLI install script | https://x.ai/cli/install.sh |
| Build overview | https://x.ai/docs/build/overview |
| CLI reference | https://x.ai/docs/build/cli/reference |
| Modes and commands | https://x.ai/docs/build/modes-and-commands |
| Grok web | https://grok.com |
| X bot | https://x.com/grok |
| API console / keys | https://console.x.ai |
| npm package | https://www.npmjs.com/package/@xai-official/grok |
| Launch note | https://x.ai/news/grok-build-cli |

## How to run this repo in CLI

```bash
cd KittyBlackCode
grok
# or
grok -p "Load CoGro- only. Stay in FA role. Adapt hash merge for account_id x month."
```

Do not point the CLI at Physics Simulations when the task is VoP or PD.
