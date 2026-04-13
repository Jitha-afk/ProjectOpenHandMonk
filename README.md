# ProjectOpenHandMonk

Monorepo for the Hermes-powered research team. We discover ideas, research them, build proof-of-concepts, and publish findings.

## Team

| Agent   | Role                        | Profile Command     |
|---------|-----------------------------|---------------------|
| Hermes  | Orchestrator                | `hermes chat`       |
| Alan    | Research Specialist         | `alan chat`         |
| Mira    | Narrative Architect         | `mira chat`         |
| Turing  | Debugger & Systems Engineer | `turing chat`       |

## Repository Structure

```
ProjectOpenHandMonk/
│
├── ideas/                  ← Raw idea proposals (one .md per idea)
│
├── research/               ← General research not tied to a project
│
├── poc/                    ← Proof of concepts (one folder per project)
│   ├── _template/          ← Copy this to start a new project
│   ├── project-x/          ← Each project is fully self-contained
│   │   ├── README.md       ← Project overview, status, objectives
│   │   ├── research/       ← Alan's research for this project
│   │   ├── design/         ← Architecture and planning docs
│   │   ├── src/            ← Turing's implementation
│   │   ├── tests/          ← Test cases and validation
│   │   └── docs/           ← Mira's polished write-ups
│   └── project-y/          ← Another independent project
│
├── published/              ← Completed work archive
│
├── shared/                 ← Resources shared across projects
│   ├── datasets/
│   ├── references/
│   └── templates/
│
└── AGENTS.md               ← Team roles, workflows, conventions
```

## Workflow

1. **Ideation** — Drop ideas in `ideas/` as markdown files
2. **Approval** — Hermes reviews and promotes approved ideas to `poc/`
3. **Research** — Alan investigates in the project's `research/` folder
4. **Build** — Turing implements in `src/` and validates with `tests/`
5. **Document** — Mira writes up findings in `docs/`
6. **Publish** — Completed projects move to `published/`

## Starting a New Project

```bash
cp -r poc/_template poc/my-new-project
# Then edit poc/my-new-project/README.md with the project details
```

## Key Rule

**Each project under `poc/` is self-contained.** All research, code, tests, and documentation for a project live inside its own folder. Agents working on Project X should never need to look inside Project Y's folder.
