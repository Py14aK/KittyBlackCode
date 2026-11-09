# Skills library

Agent skills as plain markdown, readable on GitHub and on a phone.

- [featured/](featured/README.md): 15 skills for maths, statistics, proofs, review and idea generation. These are the skills behind the Copilot agent pack.
- [all/](all/README.md): 527 skills from public repositories (Anthropic, Google, Hugging Face, OpenAI, K-Dense scientific skills, Superpowers, dangeles roles), indexed by source.

Each skill is a folder with a `SKILL.md`. The format is the open Agent Skills standard, so a folder can be copied into:

| Tool | Folder |
|---|---|
| Claude Code, Grok Build | `~/.claude/skills/` |
| Codex, Copilot in VS Code, Kilo Code | `~/.agents/skills/` |
| claude.ai | Settings > Capabilities > Skills (upload the folder as a zip) |

Only `.md` files are copied here. Skills that run scripts need the original repository, which is linked from each index.
