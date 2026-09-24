# Championship DNA: five-team SQL sample

This small public sample reproduces the regular-season win-percentage chart on [the case study](https://jacknoble.org/celtics.html). The five records match the saved output of the original Celtics project and were checked against the linked NBA sources in the CSV. The larger source database is not needed to run this example and is not included here.

Run with Python 3; no packages or API keys are needed:

```bash
python projects/championship-dna/analyze.py
```

The query computes `100 × wins / (wins + losses)` in SQLite and sorts the five champions by that percentage. It is descriptive: every row is a champion, so this sample cannot test whether a statistic predicts championship outcomes.
