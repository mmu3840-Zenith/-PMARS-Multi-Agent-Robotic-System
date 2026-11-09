# PMARS Research Protocol

## Research objective
Evaluate a centralized hub coordinating mobile collection robots in a
static-obstacle grid simulation.

## System architecture
- Central hub: task creation, priority ordering, dispatch and item inventory.
- Mobile fleet: item collection, transport and return to parking.
- Navigation: four-connected grid and A* pathfinding.
- Monitoring: robot health, failure and restoration.
- Processing: category-based inventory sorting.

## Baseline methods
1. PMARS: priority-ordered tasks, nearest reachable idle robot.
2. Greedy: task-ID order, nearest reachable idle robot.
3. Random: task-ID order, random reachable idle robot.

All methods share the same environment, navigation and movement implementation.
The comparison therefore isolates allocation-order/selection differences,
not the entire system architecture.

## Benchmark design
30 seeded trials per strategy; four robots and twelve items per trial.
Metrics: completion rate, distance travelled, simulation steps and blocked
movements. Failed or incomplete trials remain in the raw CSV.

## Robustness design
Ten trials inject one simulated robot failure after eight simulation steps,
keep that robot unavailable for five steps, and then restore it.
This tests software task recovery, not real communication failures.

## Scalability design
Robot counts: 1, 2, 4, 8.
Item counts: 12, 24, 48.
Three seeds per configuration. These are exploratory measurements.

## Statistics
Report mean, sample standard deviation and descriptive 95% normal-approximation
confidence intervals. These intervals should not be interpreted as proof of
causation or generalization beyond the tested scenarios.

## Reproducibility
The experiment runner records per-trial CSV files and a JSON summary.
Run from the repository root:
`python experiments/pmars_research/run_research.py`

## Limitations
The system is a software simulation. It does not currently demonstrate
physical robot performance, camera-based visual recognition, real radio
communication, real-time hardware constraints or clinical capability.
