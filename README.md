# ProjectOpenHandMonk

**Jitha's Hermes Research Team** — an AI-powered research lab that discovers ideas, validates them through research, builds proof-of-concepts, and publishes findings.

This repo is operated by a team of specialized [Hermes](https://github.com/NousResearch/hermes-agent) agents, each with their own role, memory, and expertise. Think of it as a small R&D team that runs autonomously and reports back with results.

## The Team

| Agent   | Role                        | What They Do                                              |
|---------|-----------------------------|-----------------------------------------------------------|
| Hermes  | Orchestrator                | Plans work, delegates tasks, reviews output, final QA     |
| Alan    | Research Specialist         | Gathers evidence, verifies sources, writes research notes |
| Mira    | Narrative Architect         | Turns raw findings into polished, readable documents      |
| Turing  | Debugger & Systems Engineer | Builds code, runs tests, debugs, creates tooling          |

## Repository Structure

```
ProjectOpenHandMonk/
│
├── ideas/                  ← Raw idea proposals (one .md per idea)
│
├── research/               ← General research not tied to a specific project
│
├── poc/                    ← Proof of concepts (one folder per project)
│   ├── _template/          ← Copy this to start a new project
│   ├── project-x/          ← Each project has its own workspace
│   │   ├── README.md       ← Project overview, status, objectives
│   │   ├── research/       ← Alan's research for this project
│   │   ├── design/         ← Architecture and planning docs
│   │   ├── src/            ← Turing's implementation
│   │   ├── tests/          ← Test cases and validation
│   │   └── docs/           ← Mira's polished write-ups
│   └── project-y/          ← Another project, fully independent
│
├── published/              ← Completed work archive
│
├── shared/                 ← Resources shared across all projects
│   ├── datasets/
│   ├── references/
│   └── templates/
│
└── AGENTS.md               ← Team roles, workflows, conventions
```

Each project under `poc/` is **self-contained** — all research, code, tests, and documentation for a project live inside its own folder. That said, agents are free to look at other projects for inspiration, reuse patterns, or reference prior work. The boundary is organizational, not a wall.

## Workflow

1. **Ideation** — Drop ideas in `ideas/` or create a GitHub Issue
2. **Approval** — Hermes reviews and promotes approved ideas to `poc/`
3. **Research** — Alan investigates in the project's `research/` folder
4. **Build** — Turing implements in `src/` and validates with `tests/`
5. **Document** — Mira writes up findings in `docs/`
6. **Publish** — Completed projects move to `published/`

## Submit an Idea or Task

The easiest way to give the team work is through **GitHub Issues**. Go to the [Issues tab](https://github.com/Jitha-afk/ProjectOpenHandMonk/issues/new/choose) and pick a template:

| Template           | When to use                                           |
|--------------------|-------------------------------------------------------|
| 💡 **New Idea**    | You have a concept you want the team to explore       |
| 🔬 **Research Task** | You need Alan to dig into a specific topic         |
| 🔧 **Build Task**  | You need Turing to build or fix something            |
| ✍️ **Writing Task** | You need Mira to write or polish a document          |

Once an issue is created, the team picks it up, works on a feature branch, and opens a **Pull Request** for review. Nothing lands on `main` without approval.

## Starting a New Project

```bash
cp -r poc/_template poc/my-new-project
# Then edit poc/my-new-project/README.md with the project details
```
