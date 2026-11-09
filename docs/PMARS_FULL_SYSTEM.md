# PMARS Full-System Simulation

PMARS models a stationary central hub coordinating mobile collection robots.

## Implemented simulation features

- Centralized task dispatch and priority scheduling.
- Nearest reachable robot assignment.
- A* grid navigation and static obstacle avoidance.
- Occupancy-aware path recalculation.
- Robot health reporting, failure and restoration.
- Task recovery and reassignment after failure.
- Item collection, hub delivery and category sorting.
- Robot return-to-parking behavior.
- Repeatable seeded simulation experiments.

## Limitations

This is a computational grid simulation, not a physical robot deployment.
Collision handling is grid-cell based, not a complete continuous multi-agent
motion-planning solution. Dynamic obstacles, sensor uncertainty, localization
error, battery consumption, wireless communication faults and real hardware
dynamics remain future validation work.

Item categories are supplied as simulation data. This is not camera-based
computer vision or learned visual classification.

## Run

```powershell
python .\run_pmars_full.py
python -m unittest discover -s tests -v
python .\experiments\pmars_full\run.py 
Experiment results are written to results/pmars_full/trial_results.csv.
They represent simulation executions, not physical robot measurements.
