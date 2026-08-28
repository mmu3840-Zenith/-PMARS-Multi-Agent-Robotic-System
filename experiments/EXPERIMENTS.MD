# PMARS Experimental Protocol

## Reproducibility & Evaluation Framework

This document describes the experimental protocol used to evaluate the Personalized Multi-Agent Robotic System (PMARS).

The objective is to make the computational experiments reproducible and to clearly separate the simulation implementation from the analysis of experimental results.

---

## 1. Experimental Objective

PMARS evaluates whether coordinated multi-agent task allocation and routing can improve system-level performance compared with simpler baseline strategies.

The evaluation focuses on:

* task completion latency
* collision/conflict behavior
* task efficiency
* system stabilization
* scalability
* failure behavior

---

## 2. Experimental Pipeline

The intended evaluation pipeline is:

```text
Configuration
     ↓
Initialize Simulation
     ↓
Set Random Seed
     ↓
Run Simulation
     ↓
Collect Raw Metrics
     ↓
Repeat Trials
     ↓
Aggregate Results
     ↓
Statistical Analysis
     ↓
Generate Tables / Figures
```

The experiment runner should be treated as the source of truth for generated measurements.

---

## 3. Reproducibility

Experiments use deterministic random seeds where supported.

Documented seed set:

```text
42
7
21
99
123
```

Repeated trials are performed for each experimental configuration.

The research protocol uses:

**50 trials per configuration**

where the implementation and available experiment runner support the stated protocol.

---

## 4. Experimental Variables

The primary independent variables include:

### Agent Population

The number of concurrently simulated agents.

Example scaling levels:

```text
10
25
50
100
```

### Workload

The number and arrival rate of tasks presented to the system.

### Coordination Configuration

The system can be evaluated with different coordination components enabled or disabled.

### Routing Strategy

Different routing and allocation approaches can be compared against PMARS.

### Environmental Stress

Experiments can increase workload and spatial contention to identify system performance boundaries.

---

# 5. Evaluation Metrics

## 5.1 Task Latency

Task latency measures the time required for an assigned task to reach completion.

Lower latency indicates faster task completion.

---

## 5.2 Collision / Conflict Count

The simulation records collision or spatial conflict events according to the implementation's event definitions.

Lower values indicate fewer coordination conflicts.

---

## 5.3 Task Efficiency

Task efficiency measures completed work relative to the simulation's execution process.

The exact calculation should follow the implementation used by the experiment runner.

---

## 5.4 Stabilization

Stabilization measures how quickly the simulated system returns toward its defined stable operating condition after a disturbance or workload change.

---

## 5.5 Failure Rate

Failure rate measures the proportion of agents or tasks classified as failed under the experiment's defined conditions.

---

# 6. Baseline Methods

PMARS should be evaluated against clearly defined comparison strategies.

## Random Allocation / Routing

Tasks or routing decisions are assigned without the complete PMARS coordination mechanism.

This provides a low-coordination baseline.

---

## Greedy Routing

Each agent selects a locally efficient route, such as a shortest-distance choice, without considering the complete collective system state.

This provides a local-optimization baseline.

---

## Fixed Queue Scheduling

Tasks are processed according to a fixed queue order without dynamic reordering based on current system conditions.

---

# 7. Ablation Study

Ablation experiments remove individual PMARS components.

The purpose is to determine whether observed performance improvements are attributable to specific architectural mechanisms.

## Full System

```text
Telemetry
+
Dynamic Allocation
+
Routing
+
Conflict Resolution
+
Execution
```

## Without Telemetry Bounds

```text
Allocation
+
Routing
+
Conflict Resolution
+
Execution
```

## Without Conflict Resolution

```text
Telemetry
+
Allocation
+
Routing
+
Execution
```

Additional ablations should be added when a component can be isolated experimentally.

---

# 8. Trial Structure

Each experimental configuration follows the same general process.

```text
FOR each configuration:

    FOR each random seed:

        initialize environment

        initialize agents

        initialize task workload

        run simulation

        collect metrics

        save raw results

    aggregate trial results

    calculate summary statistics

    generate comparison outputs
```

This structure minimizes differences between experimental conditions.

---

# 9. Statistical Reporting

Results should be reported using summary statistics calculated from the individual trials.

Where applicable:

* mean
* standard deviation
* confidence intervals
* effect size
* statistical significance

should be reported.

The experimental protocol uses significance testing where appropriate.

A reported statistical result should always identify:

1. the compared methods,
2. the metric being tested,
3. the number of observations,
4. the statistical test,
5. the resulting significance value.

---

# 10. Results Reporting

Results should be generated from raw experiment outputs rather than manually entered into tables.

Recommended pipeline:

```text
Raw CSV / JSON
      ↓
Analysis Script
      ↓
Aggregated Statistics
      ↓
Research Tables
      ↓
Figures
```

This reduces transcription errors and makes published results easier to audit.

---

# 11. Scaling Experiments

Scaling experiments investigate how coordination performance changes as the number of agents increases.

Example:

```text
10 Agents
    ↓
25 Agents
    ↓
50 Agents
    ↓
100 Agents
```

For each population size, the same evaluation metrics should be collected.

The objective is to identify:

* performance scaling
* coordination overhead
* congestion thresholds
* conflict growth
* task latency changes

---

# 12. Stress Testing

Stress experiments intentionally increase system difficulty.

Potential stress variables include:

### Increased Workload

More tasks are introduced into the environment.

### Increased Agent Density

More agents operate within the same spatial region.

### Increased Task Arrival Rate

Tasks arrive faster than under the nominal workload.

### Reduced Available Space

Agents have fewer spatial resources in which to operate.

Stress testing is intended to reveal failure boundaries rather than only best-case performance.

---

# 13. Failure Analysis

When a configuration performs poorly, the experiment should record the associated failure mode where possible.

Examples include:

```text
Task Queue Bottleneck
Spatial Deadlock
Conflict Increase
Coordination Overhead
Agent Failure
System Instability
```

Failure analysis is treated as part of the research result.

A system that performs well under normal conditions but fails catastrophically under moderate stress should not be characterized as universally robust.

---

# 14. Reproducing an Experiment

The recommended reproduction procedure is:

```text
1. Clone the repository

2. Install dependencies

3. Select the experiment configuration

4. Set the documented random seed

5. Run the experiment runner

6. Save raw output

7. Repeat for all required seeds

8. Run the analysis pipeline

9. Compare generated results with the documented results
```

Example command structure:

```powershell
python run_experiments.py
```

If the repository uses a different runner or command, the command above should be replaced with the actual implementation command.

---

# 15. Expected Outputs

A complete experiment should produce machine-readable results where supported.

Recommended outputs include:

```text
results/
├── raw/
│   ├── trial_*.csv
│   └── trial_*.json
│
├── processed/
│   └── aggregated_results.csv
│
└── figures/
    ├── latency.png
    ├── collisions.png
    └── efficiency.png
```

The exact structure should follow the implementation in the repository.

---

# 16. Data Integrity

Experimental results should not be manually modified after generation.

The preferred workflow is:

```text
Simulation
   ↓
Raw Data
   ↓
Analysis
   ↓
Published Result
```

If a result is corrected, the underlying experiment or analysis script should be corrected and the result regenerated.

---

# 17. Current Experimental Boundaries

PMARS is a computational simulation.

The current evaluation does not establish physical robotic performance.

The experiments do not fully model:

* sensor noise
* actuator dynamics
* motor friction
* physical collision forces
* 3D robotic kinematics
* real communication packet loss
* hardware execution

Therefore, the experimental results should be interpreted as evidence about the behavior of the implemented simulation model.

They should not be presented as direct evidence of physical robotic deployment.

---

# 18. Interpretation of Results

A performance improvement in simulation does not automatically imply equivalent improvement in physical robots.

The intended interpretation is:

> Under the defined computational environment and experimental conditions, the evaluated coordination mechanism produced the observed performance differences.

This distinction is maintained to avoid overclaiming beyond the experimental evidence.

---

# 19. Experimental Checklist

Before considering an experiment complete:

* [ ] Configuration documented
* [ ] Baseline documented
* [ ] Random seeds documented
* [ ] Number of trials documented
* [ ] Raw results preserved
* [ ] Metrics defined
* [ ] Analysis reproducible
* [ ] Figures generated from data
* [ ] Statistical test documented
* [ ] Failure cases recorded
* [ ] Limitations reported

---

# 20. Research Reproducibility Standard

A result should be considered reproducible only when another researcher can determine:

**What was run?**

**With which configuration?**

**Using which seed?**

**For how many trials?**

**Using which metric definition?**

**Compared against which baseline?**

**Using which analysis procedure?**

PMARS documentation therefore treats reproducibility as part of the engineering system rather than as an afterthought.

---

## Summary

The PMARS experimental framework follows:

```text
DEFINE
  ↓
CONFIGURE
  ↓
RUN
  ↓
REPEAT
  ↓
RECORD
  ↓
ANALYZE
  ↓
COMPARE
  ↓
REPORT
```

The objective is not simply to produce high-performing simulation results, but to make the computational evidence **traceable, repeatable, and appropriately bounded by the limitations of the simulation.**
