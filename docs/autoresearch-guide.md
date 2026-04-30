# AutoResearch — Team Guide
## Based on Karpathy's repo + David Ondrej's tutorial

### What is AutoResearch?

AutoResearch is an open-source project by Andrej Karpathy that lets an AI agent improve code autonomously. The agent runs experiments in a loop — it modifies code, tests if it improved, keeps what works, throws away what doesn't, and repeats. You can run ~100 experiments overnight while you sleep.

### The Core Loop

1. Agent comes up with a hypothesis
2. Modifies the code
3. Trains/runs for ~5 minutes
4. Evaluates the result
5. If better → git commit (keep it)
6. If worse → git reset (discard it)
7. Repeat forever

### The 3-File Architecture

- **program.md** — The "brain." YOU write this. It tells the agent what to optimize, the constraints, and the rules. This is the most important file.
- **train.py** (or whatever your "one file" is) — The ONLY file the agent can change. Could be code, config, a prompt, a math equation — anything you want to optimize.
- **prepare.py** — The metric/evaluation script. The agent CANNOT touch this. Ever. This is what measures success.

### Why It's Not Just for ML

The pattern works for ANYTHING with a clear metric:
- Trading strategies (metric: Sharpe ratio)
- Website speed optimization (metric: load time in ms)
- Marketing (metric: conversion rate)
- Prompt engineering (metric: accuracy score)
- Code performance (metric: execution time)
- Fine-tuning open source models

As Karpathy said: "Any metric you care about that is reasonably efficient to evaluate can be auto researched."

### The 3 Conditions for Success

1. **A clear metric** — one number, clear direction (lower/higher = better)
2. **Automated evaluation** — NO human in the loop
3. **One file the agent can change** — not two, not zero, ONE

### Where It Will Fail

- Brand design, UX, pricing — anything where "better" is subjective
- If you give it a bad metric, it will confidently optimize the wrong thing
- If the loop is too slow to iterate

### Quick Start: Karpathy's Original (needs NVIDIA GPU)

```bash
# 1. Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# 2. Clone the repo
git clone https://github.com/karpathy/autoresearch.git
cd autoresearch

# 3. Install dependencies
uv sync

# 4. Prepare data (one-time, ~2 min)
uv run prepare.py

# 5. Test a manual run (~5 min)
uv run train.py

# 6. Open Claude Code / Codex / Cursor and prompt:
# "Hi have a look at program.md and let's kick off a new experiment! Let's do the setup first."
```

### Quick Start: Any Project

1. Create your project (website, trading bot, whatever)
2. Create your eval script (prepare.py equivalent) — measures the metric
3. Write your program.md — borrow Karpathy's structure and adapt
4. Commit your baseline
5. Prompt your AI agent: "Read program.md, run baseline benchmark first. Record results.tsv then begin the experiment loop. Do not stop or ask me anything. Just keep running experiments autonomously."
6. Walk away.

### David Ondrej's Demo Results (website load time)

| Time | Load Time | Improvement |
|------|-----------|-------------|
| Baseline | 50ms | — |
| ~1 min | 33ms | -34% |
| ~3 min | 28ms | -44% |
| ~4 min | 25ms | -50% |

### For Smaller GPUs / Mac / Windows

Community forks:
- Mac: github.com/miolini/autoresearch-macos
- Mac MLX: github.com/trevin-creator/autoresearch-mlx
- Windows: github.com/jsegov/autoresearch-win-rtx

### Resources

- Repository: https://github.com/karpathy/autoresearch
- Video tutorial: https://youtu.be/uBWuKh1nZ2Y (David Ondrej)
- Karpathy's tweets: https://x.com/karpathy/status/2029701092347630069
