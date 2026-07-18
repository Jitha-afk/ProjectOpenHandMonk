# ProjectOpenHandMonk — Team Operating Guide

## Purpose
Monorepo for the Hermes agent team to discover ideas, research them, build proof-of-concepts, and publish findings.

## Repository
- Local: ~/projects/ProjectOpenHandMonk
- Remote: https://github.com/Jitha-afk/ProjectOpenHandMonk

## Team Roster

| Agent   | Role                        | Profile Command     |
|---------|-----------------------------|---------------------|
| Hermes  | Orchestrator                | `hermes chat`       |
| Alan    | Research Specialist         | `alan chat`         |
| Mira    | Narrative Architect         | `mira chat`         |
| Turing  | Debugger & Systems Engineer | `turing chat`       |
| Klive   | AutoResearch & Optimization | `klive chat`        |

## Two Intake Channels

Work comes in through two channels:

### Channel 1: Telegram → Hermes
- User sends instructions to Hermes via Telegram
- Hermes decomposes the work and delegates to specialists
- Hermes relays tasks by switching profiles or leaving notes in the repo

### Channel 2: GitHub Issues
- User creates an issue using one of the templates:
  - **💡 New Idea** — labeled `idea`
  - **🔬 Research Task** — labeled `research`, `alan`
  - **🔧 Build Task** — labeled `build`, `turing`
  - **✍️ Writing Task** — labeled `writing`, `mira`
- Agents check for assigned issues before starting work
- When work is complete, the agent opens a PR referencing the issue

### How agents pick up work
1. Check `gh issue list --assignee @me` or issues with your label
2. Claim the issue by adding the `in-progress` label
3. Create a feature branch: `git checkout -b issue-<number>-short-description`
4. Do the work in the correct project folder
5. Commit with agent signature (automatic via hook)
6. Push the branch and open a PR with `gh pr create`
7. Reference the issue in the PR: `Closes #<number>`
8. Add the `needs-review` label — user reviews and merges

## Navigation Rules

1. **Never mix projects.** Each POC is self-contained under `poc/[project-name]/`.
2. **Know your folder.** Before working, confirm which project and subfolder you're in.
3. **Use the template.** New projects start by copying `poc/_template/`.
4. **General vs project research.** Broad research goes in `research/`. Project-specific research goes in `poc/[project-name]/research/`.

## Project Lifecycle

```
GitHub Issue (idea)  →  poc/[name]/  →  published/[name]/
   or Telegram            building         done
```

1. Ideas arrive via GitHub Issue or Telegram
2. Hermes approves and creates a project folder in `poc/` (copy from `_template/`)
3. Team works inside that project folder on feature branches:
   - Alan: `poc/[name]/research/`
   - Turing: `poc/[name]/src/` and `poc/[name]/tests/`
   - Mira: `poc/[name]/docs/`
4. Each piece of work gets a PR → user reviews and merges
5. Completed projects move to `published/`

## Git Workflow

### Branching
- `main` is the stable branch — no direct pushes for project work
- Feature branches: `issue-<number>-short-description`
- PRs are the only way work gets into main (so user can review)

### Commit Conventions
- Prefix commits with agent name: `[Alan] Added findings on X`
- Include the project name: `[Turing] poc/project-x: Add data pipeline`
- Commits are auto-signed via prepare-commit-msg hook

### PR Workflow
```bash
# 1. Create branch
git checkout -b issue-42-research-llm-trends

# 2. Do the work, commit
git add .
git commit -m "[Alan] poc/llm-trends: Initial research findings"

# 3. Push and create PR
git push origin issue-42-research-llm-trends
gh pr create --title "[Alan] Research findings for LLM trends" \
  --body "Closes #42" --label "needs-review,alan"
```

## Labels

| Label         | Purpose                        |
|---------------|--------------------------------|
| `idea`        | New idea proposal              |
| `research`    | Research task                  |
| `build`       | Build/engineering task         |
| `writing`     | Writing/documentation task     |
| `alan`        | Assigned to Alan               |
| `mira`        | Assigned to Mira               |
| `turing`      | Assigned to Turing             |
| `hermes`      | Assigned to Hermes             |
| `in-progress` | Work is underway               |
| `needs-review`| PR ready for user review       |

## Handoff Rules

1. Hermes decides who handles what
2. Research before writing — Alan gathers findings before Mira writes
3. Plan before building — Hermes plans before Turing implements
4. Specialists stay in lane
5. All work goes through PRs — user reviews and approves
