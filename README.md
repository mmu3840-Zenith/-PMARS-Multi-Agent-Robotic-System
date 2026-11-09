# PMARS - Hub-Centered Multi-Agent Robotic Collection Simulation

PMARS is a software simulation of a stationary central hub coordinating
multiple mobile robots that collect items, transport them to the hub, and
return to designated parking positions.

## Implemented simulation capabilities
- Centralized task assignment and priority handling.
- Multiple mobile collection robots.
- A* pathfinding on a four-connected grid.
- Static obstacle avoidance.
- Item pickup and delivery to the central hub.
- Category-based inventory sorting.
- Robot health reporting, failure and restoration.
- Task re-queuing after robot failure.
- Individual robot parking positions.
- Repeatable simulation experiments.

## Run the demonstration
`python run_pmars_full.py`

## Run tests
`python -m unittest discover -s tests -v`

## Run the research suite
`python experiments/pmars_research/run_research.py`

The research suite compares PMARS allocation with greedy and random
allocation, tests simulated robot failure recovery, and explores different
robot and item counts. Results are written to `results/pmars_research/`.

## Research outputs
- `benchmark_trials.csv`
- `robustness_trials.csv`
- `scalability_trials.csv`
- `summary.json`
- `docs/PMARS_RESEARCH_RELEASE.md`

## Architecture and research documents
- `docs/PMARS_ARCHITECTURE.mmd`
- `docs/PMARS_RESEARCH_PROTOCOL.md`
- `docs/PMARS_PAPER_DRAFT.md`
- `docs/PMARS_FULL_SYSTEM.md`

## Important limitations
PMARS is currently a computational simulation. Category sorting uses
predefined item metadata; it is not camera-based visual recognition.
The project has not been validated on physical robots or real wireless
communication hardware. Simulation results must not be represented as
physical performance.

## Reproducibility
The experiment runner fixes random seeds and preserves per-trial observations.
Do not discard incomplete trials when reporting results.
