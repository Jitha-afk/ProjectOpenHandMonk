# ProjectOpenHandMonk — Team Operating Guide

## Purpose
Monorepo for the Hermes agent team to discover ideas, research them, build proof-of-concepts, and publish findings.

## Repository
- Local: ~/projects/ProjectOpenHandMonk
- Remote: https://github.com/Jitha-afk/ProjectOpenHandMonk

## Team Roster

| Agent   | Role                        | Works In                          |
|---------|-----------------------------|-----------------------------------|
| Hermes  | Orchestrator                | ideas/, plans, project READMEs    |
| Alan    | Research Specialist         | research/, poc/*/research/        |
| Mira    | Narrative Architect         | poc/*/docs/, published/           |
| Turing  | Debugger & Systems Engineer | poc/*/src/, poc/*/tests/, shared/ |

## Navigation Rules

1. **Never mix projects.** Each POC is self-contained under `poc/[project-name]/`.
2. **Know your folder.** Before working, confirm which project and subfolder you're in.
3. **Use the template.** New projects start by copying `poc/_template/`.
4. **General vs project research.** Broad research goes in `research/`. Project-specific research goes in `poc/[project-name]/research/`.

## Project Lifecycle

```
ideas/  →  poc/[name]/  →  published/[name]/
 new        building         done
```

1. Ideas start as .md files in `ideas/`
2. Approved ideas get a project folder in `poc/` (copy from `_template/`)
3. Team works inside that project folder:
   - Alan: `poc/[name]/research/`
   - Turing: `poc/[name]/src/` and `poc/[name]/tests/`
   - Mira: `poc/[name]/docs/`
4. Completed projects move to `published/`

## Commit Conventions

- Prefix commits with the agent name: `[Alan] Added findings on X`
- Include the project name when working in a POC: `[Turing] poc/project-x: Add data pipeline`
- Keep commits focused — one logical change per commit

## Handoff Rules

1. Hermes defines scope and creates the project folder
2. Alan researches first — findings go in before building starts
3. Turing builds based on Alan's research
4. Mira documents based on both research and implementation
5. Hermes reviews and approves for publishing

## Important

- Always `git pull` before starting work to avoid conflicts
- Always commit and push when done with a work session
- If two agents need to work on the same project simultaneously, coordinate through Hermes
