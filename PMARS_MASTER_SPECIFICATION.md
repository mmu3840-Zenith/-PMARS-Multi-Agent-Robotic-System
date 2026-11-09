# PMARS — Complete Eight-Phase Engineering Specification

## Core Architecture

PMARS is a multi-agent robotic system built around one stationary intelligent central hub and multiple autonomous mobile robots.

The stationary hub:
- Coordinates the mobile robot fleet.
- Receives and processes delivered items.
- Identifies and classifies items through a recognition subsystem.
- Assigns sorting destinations.
- Monitors robot status and health.
- Detects failures and unavailable robots.
- Redistributes tasks when necessary.
- Optimizes fleet-wide operations.

Mobile robots:
- Receive tasks from the hub.
- Navigate the environment.
- Collect and transport items.
- Report their status and telemetry.
- Handle local navigation decisions.
- Report errors and failures.

Use hybrid coordination: centralized fleet-level management and decentralized local robot autonomy.

## Phase 1 — System Foundation

Implement:
- Central hub.
- Mobile robot model.
- Fleet manager.
- Item and task models.
- Environment and simulation.
- Modular subsystem interfaces.
- Configuration and logging.

Acceptance:
- Hub can register and manage multiple robots.
- Robots can receive and complete tasks.
- Items can be represented and transported.
- Unit tests pass.

## Phase 2 — Intelligent Dispatch

Implement:
- Task assignment.
- Priority-aware scheduling.
- Distance-aware assignment.
- Fleet workload balancing.
- Task reassignment.
- Dispatch algorithm comparisons.

Acceptance:
- Tasks are assigned correctly.
- Unavailable robots are not assigned new work.
- Dispatch algorithms are evaluated using reproducible tests.

## Phase 3 — Robot Health Intelligence

Implement:
- Heartbeats.
- Robot telemetry.
- Health states.
- Failure detection.
- Timeout detection.
- Disconnection handling.
- Task recovery and reassignment.

Acceptance:
- Failed robots are detected.
- Their unfinished tasks can be recovered.
- False failure detection is tested.

## Phase 4 — Autonomous Navigation

Implement:
- Environment mapping.
- Path planning.
- Obstacle avoidance.
- Route updates.
- Congestion awareness.
- Collision prevention.

Acceptance:
- Robots can navigate simulated environments.
- Blocked routes are handled.
- Navigation performance is tested.

## Phase 5 — Communication Architecture

Implement:
- Hub-to-robot commands.
- Robot-to-hub telemetry.
- Message identifiers.
- Acknowledgements.
- Retry handling.
- Message validation.
- Communication failure recovery.

Acceptance:
- Messages are validated.
- Communication failures are handled.
- Robot and hub state remain consistent.

## Phase 6 — Item Recognition and Sorting

Implement:
- Item representation.
- Recognition subsystem interface.
- Item classification.
- Destination assignment.
- Confidence handling.
- Sorting workflow.
- Recognition error handling.

Important:
Simulated item labels are not real computer vision.
Keep actual camera-based computer vision as a separate extension.
Never claim predefined item labels are real computer vision.

Acceptance:
- Simulated items are classified and routed correctly.
- Recognition errors are handled.
- The recognition interface supports a future camera-based implementation.

## Phase 7 — Collective Optimization

Implement:
- Fleet-wide optimization.
- Adaptive task scheduling.
- Workload optimization.
- Congestion-aware assignment.
- Multi-robot cooperation.
- Adaptive coordination.
- Performance monitoring.
- Optional reinforcement learning where justified.
- Baseline algorithm comparisons.

Do not add machine learning merely for appearance.
Demonstrate measurable improvements against simpler baselines.

## Phase 8 — Complete System Validation

Implement and validate:
- Full subsystem integration.
- Unit tests.
- Integration tests.
- End-to-end tests.
- Robot failure tests.
- Communication failure tests.
- Navigation stress tests.
- Item recognition tests.
- Large-fleet simulations.
- Scalability tests.
- Reproducibility tests.
- Performance comparisons.

Produce:
- Raw experiment data.
- Experiment configurations.
- Reproducible random seeds.
- Benchmark summaries.
- Architecture documentation.
- Complete README.
- Known limitations.
- Final engineering validation report.

## Engineering Requirements

1. Preserve existing working functionality.
2. Inspect the entire repository before modifying it.
3. Identify incomplete and duplicate modules.
4. Use modular architecture.
5. Maintain backward compatibility where practical.
6. Test every major subsystem.
7. Run actual automated tests.
8. Never fabricate experimental results.
9. Separate simulated results from physical validation.
10. Save raw experiment data.
11. Document dependencies.
12. Keep secrets out of Git.
13. Do not delete existing research without justification.
14. Do not force-push or rewrite Git history.
15. Document all limitations honestly.

## Phase Acceptance Requirements

Each phase must have:
- Implementation.
- Unit tests.
- Integration tests where applicable.
- Actual test results.
- Documentation.
- Known limitations.
- Git commit.

A phase is not complete simply because files were created.

## Final Objective

Deliver one integrated PMARS system.

One stationary intelligent hub coordinates multiple autonomous mobile robots that collect, transport, identify and sort items.

The system continuously monitors robot health, handles failures, redistributes work and optimizes fleet operations.

The final system must be reproducible, modular, testable and extensible toward eventual physical robotic implementation.
