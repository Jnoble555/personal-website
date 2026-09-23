# UltraTrain: public code excerpt

This is a small, runnable excerpt of the local Python pipeline behind the [UltraTrain case study](../../ultratrain.html). It demonstrates three decisions from the project: reading raw metric values when a Strava export repeats display column names, keeping zero-mile weeks visible while excluding race day from training volume, and flagging a possible after-midnight plan match for human review.

The files in `examples/` are **synthetic**. They are not Jack's activities, race track, or training plan. This excerpt does not reproduce the private dashboard or the GPS-based race split calculation, and it does not train an ML model.

From this directory, run:

```powershell
python sample.py examples/activities.csv --race-date 2025-11-22 --plan examples/plan.csv
```

The example should report four pre-race runs, 29.0 training miles, a 50.0-mile race, zero-mile weeks, and a possible overnight match for October 2. The match is deliberately **flagged, not assumed**.

The script uses Python's standard library and writes only aggregate JSON to standard output. Keep real account exports, route files, notes, and generated private dashboards outside a public repository.

Run the edge-case checks with `python -m unittest test_sample.py`.
