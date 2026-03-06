# Contributing

Thanks for your interest in contributing! This document describes a minimal set of guidelines to make contributions smooth and consistent.

## How to contribute

1. Fork the repository and create a feature branch from `main`:

```bash
git checkout -b feat/your-feature
```

2. Make small, focused changes with clear commit messages.

3. Run the app and any checks locally before opening a PR:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
# run quick smoke check
python -c "import pandas; print('pandas', pandas.__version__)"
```

4. Push your branch and open a Pull Request against `main`. Describe the problem, your solution, and list any follow-ups.

## PR checklist

- [ ] Branch is up-to-date with `main`
- [ ] Changes are small and scoped
- [ ] `requirements.txt` updated if dependencies changed
- [ ] README / docs updated if behavior changed
- [ ] No sensitive data or credentials included

## Code style

- Prefer clear variable names and small functions.
- Keep formatting consistent; use `black`/`isort` if configured.

## Tests

This repository does not currently include an automated test suite. For code that changes behavior significantly, add a small smoke test and document how to run it in the PR.

## Communication

If you plan a large change, open an issue first to discuss the design.

---

If you'd like, I can also add a simple GitHub Actions workflow to run a smoke install/test on PRs.
