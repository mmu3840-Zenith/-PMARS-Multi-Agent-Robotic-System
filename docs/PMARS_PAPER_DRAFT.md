# PMARS Research Paper - Working Draft

## Title
A Centralized Hub and Autonomous Mobile Fleet for Multi-Item Collection:
A Reproducible Grid-Based Simulation Study

## Abstract
This work presents PMARS, a simulation of a stationary central hub coordinating
mobile collection robots. The hub dispatches collection tasks, receives items,
sorts delivered items by category, and monitors robot availability. Mobile
robots use A* pathfinding in a four-connected environment with static obstacles.
The research evaluation compares priority-based nearest-robot allocation with
greedy nearest-robot and random allocation baselines. Additional experiments
examine simulated robot failure recovery and workload scaling. All quantitative
claims are to be populated from the generated raw datasets and report. The
system is a computational prototype and has not been validated on physical
robots.

## 1. Introduction
Multi-robot collection systems require coordination between task allocation,
navigation, delivery and fleet availability. PMARS explores a hub-centered
architecture in which a stationary coordinator manages a fleet of mobile
collection agents.

## 2. System design
The central hub maintains task and inventory state. Tasks contain an item,
category, location and priority. The dispatcher assigns pending tasks to
reachable idle robots. Robots navigate to items, collect them, return to the
hub and then move to individual parking positions.

## 3. Methods
The environment is a discrete four-connected grid. Static obstacles are
handled by A* search. The benchmark uses identical environments and seeds
across PMARS, greedy and random allocation variants. Raw trial data is
exported for independent analysis.

## 4. Evaluation
Insert the generated tables from `docs/PMARS_RESEARCH_RELEASE.md`.
Do not report an improvement unless the corresponding baseline comparison
and uncertainty are supported by the exported data.

## 5. Robustness and scalability
Report the failure-recovery and scalability experiments separately.
Distinguish successful task recovery from communication resilience.
The current simulator does not model physical wireless networks.

## 6. Limitations
The study is simulation-only. It does not establish physical robot reliability,
camera recognition accuracy, real-world throughput, safety, or deployment
readiness. The current baseline comparison evaluates allocation policies
within a shared simulation rather than comparing against external systems.

## 7. Conclusion
PMARS provides a testable software architecture for hub-coordinated mobile
collection. Further work should include hardware experiments, dynamic
obstacles, realistic communication models, and independent replication.
