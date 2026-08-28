\# PMARS Architecture



\*\*Personalized Multi-Agent Robotic System\*\*



> A simulation framework for studying adaptive task allocation, routing, conflict resolution, and coordinated behavior in multi-agent robotic environments.



\---



\## 1. System Overview



PMARS is organized as a closed-loop multi-agent coordination system.



The core execution cycle is:



```text

┌─────────────────────┐

│    Environment      │

│ Tasks + Agent State │

└──────────┬──────────┘

&#x20;          │

&#x20;          ▼

┌─────────────────────┐

│      Telemetry      │

│   State Collection  │

└──────────┬──────────┘

&#x20;          │

&#x20;          ▼

┌─────────────────────┐

│   Task Allocation   │

│ Dynamic Assignment  │

└──────────┬──────────┘

&#x20;          │

&#x20;          ▼

┌─────────────────────┐

│    Routing Engine   │

│ Path Selection      │

└──────────┬──────────┘

&#x20;          │

&#x20;          ▼

┌─────────────────────┐

│ Conflict Resolution │

│ Spatial Safety      │

└──────────┬──────────┘

&#x20;          │

&#x20;          ▼

┌─────────────────────┐

│   Agent Execution   │

│ Movement + Tasks    │

└──────────┬──────────┘

&#x20;          │

&#x20;          ▼

┌─────────────────────┐

│ Metrics + Feedback  │

└──────────┬──────────┘

&#x20;          │

&#x20;          └──────────────► Next Coordination Cycle

```



The architecture follows:



\*\*Observe → Allocate → Route → Resolve → Execute → Measure → Repeat\*\*



\---



\# 2. Design Objectives



PMARS was designed around five system objectives:



1\. \*\*Coordinate multiple agents\*\*

2\. \*\*Allocate tasks dynamically\*\*

3\. \*\*Reduce spatial conflicts\*\*

4\. \*\*Adapt decisions using current system state\*\*

5\. \*\*Produce reproducible experimental measurements\*\*



The system is evaluated as a collective rather than treating each simulated agent as an isolated optimizer.



\---



\# 3. Environment Layer



The environment represents the simulated workspace.



It maintains the state required by the coordination system, including:



\* agent positions

\* task locations

\* task availability

\* coordinate boundaries

\* spatial occupancy

\* simulation time

\* workload conditions



PMARS currently uses an abstract \*\*2D computational environment\*\*.



It does not attempt to reproduce complete physical robot dynamics.



\---



\# 4. Agent Layer



Each simulated agent maintains an operational state.



Conceptually:



```text

Agent

├── Position

├── Current Task

├── Target

├── Route

├── Execution State

└── Conflict State

```



During each simulation cycle, agents:



1\. observe their current state,

2\. receive or select work,

3\. calculate movement,

4\. execute movement,

5\. update their state,

6\. contribute new state information to the next cycle.



This creates a feedback relationship between individual agent behavior and collective system behavior.



\---



\# 5. Telemetry Layer



The telemetry layer provides the coordination system with the current simulation state.



```text

Environment

&#x20;    │

&#x20;    ├── Agent state

&#x20;    ├── Task state

&#x20;    ├── Spatial state

&#x20;    └── Workload

&#x20;         │

&#x20;         ▼

&#x20;      Telemetry

&#x20;         │

&#x20;         ▼

&#x20;    Coordination

```



The telemetry system allows downstream modules to make decisions using the latest available state.



Telemetry-related constraints are also examined through controlled ablation experiments.



\---



\# 6. Task Allocation



The allocation layer determines which agent should perform which task.



A simplified representation is:



```text

Task Pool

&#x20;  │

&#x20;  ├── Task A ──► Agent 3

&#x20;  ├── Task B ──► Agent 7

&#x20;  ├── Task C ──► Agent 1

&#x20;  └── Task D ──► Agent 5

```



The allocation process considers the current simulation state rather than relying exclusively on a fixed assignment.



This separates:



\*\*Task decision\*\*



from



\*\*Movement decision\*\*



so that the routing layer can independently determine how an agent reaches its assigned target.



\---



\# 7. Routing Engine



After an assignment is made, the routing layer determines an appropriate movement sequence.



```text

Assigned Task

&#x20;     │

&#x20;     ▼

Target Location

&#x20;     │

&#x20;     ▼

Candidate Route

&#x20;     │

&#x20;     ▼

Spatial Evaluation

&#x20;     │

&#x20;     ▼

Selected Route

```



PMARS evaluates its coordination approach against simpler routing strategies, including greedy distance-based routing.



The purpose is to determine whether coordinated routing provides benefits beyond individually selecting locally efficient paths.



\---



\# 8. Conflict Resolution



Multiple agents operating simultaneously can create spatial conflicts.



The conflict-resolution layer evaluates candidate movement before execution.



```text

Candidate Action

&#x20;      │

&#x20;      ▼

Conflict Check

&#x20;      │

&#x20;   ┌──┴───┐

&#x20;   │      │

&#x20;  Safe  Conflict

&#x20;   │      │

&#x20;   ▼      ▼

&#x20;Execute  Resolve

&#x20;           │

&#x20;           ▼

&#x20;       Recalculate

```



This component becomes increasingly important as agent density and workload increase.



The contribution of conflict resolution is evaluated through ablation testing.



\---



\# 9. Execution Layer



Once a movement decision passes the relevant checks, the agent executes the action inside the simulation.



Execution updates:



\* position

\* task progress

\* occupancy

\* conflict state

\* experiment metrics



The resulting state is returned to the environment and telemetry layers.



\---



\# 10. Closed-Loop Control



The complete architecture operates as a feedback loop:



```text

&#x20;         ┌───────────────────────────┐

&#x20;         │                           │

&#x20;         ▼                           │

&#x20;      OBSERVE                        │

&#x20;         │                           │

&#x20;         ▼                           │

&#x20;      ALLOCATE                       │

&#x20;         │                           │

&#x20;         ▼                           │

&#x20;       ROUTE                         │

&#x20;         │                           │

&#x20;         ▼                           │

&#x20;      RESOLVE                        │

&#x20;         │                           │

&#x20;         ▼                           │

&#x20;      EXECUTE                        │

&#x20;         │                           │

&#x20;         ▼                           │

&#x20;      MEASURE                        │

&#x20;         │                           │

&#x20;         └──────── FEEDBACK ─────────┘

```



This is important because PMARS is not evaluated only as a static planning algorithm.



The system is repeatedly evaluated against the changing state of the environment.



\---



\# 11. Coordination Cycle



A simplified execution cycle is:



```text

for each simulation timestep:



&#x20;   collect environment state



&#x20;   update agent telemetry



&#x20;   identify available tasks



&#x20;   allocate tasks



&#x20;   generate or update routes



&#x20;   evaluate spatial conflicts



&#x20;   resolve conflicts



&#x20;   execute agent actions



&#x20;   update environment



&#x20;   record metrics

```



The process repeats until the experiment reaches its termination condition.



\---



\# 12. Data Flow



The main information flow is:



```text

&#x20;                 ┌──────────────┐

&#x20;                 │     Tasks    │

&#x20;                 └──────┬───────┘

&#x20;                        │

&#x20;                        ▼

┌────────────┐    ┌──────────────┐

│ Environment├───►│   Telemetry  │

└────────────┘    └──────┬───────┘

&#x20;                        │

&#x20;                        ▼

&#x20;                 ┌──────────────┐

&#x20;                 │  Allocation  │

&#x20;                 └──────┬───────┘

&#x20;                        │

&#x20;                        ▼

&#x20;                 ┌──────────────┐

&#x20;                 │   Routing    │

&#x20;                 └──────┬───────┘

&#x20;                        │

&#x20;                        ▼

&#x20;                 ┌──────────────┐

&#x20;                 │   Conflict   │

&#x20;                 │  Resolution  │

&#x20;                 └──────┬───────┘

&#x20;                        │

&#x20;                        ▼

&#x20;                 ┌──────────────┐

&#x20;                 │    Agents    │

&#x20;                 └──────┬───────┘

&#x20;                        │

&#x20;                        ▼

&#x20;                 ┌──────────────┐

&#x20;                 │    Metrics   │

&#x20;                 └──────────────┘

```



\---



\# 13. Mathematical Objective



The broader research formulation treats coordination as a multi-objective optimization problem.



A conceptual utility function is:



$$

U(s,a)=\\alpha E(s,a)-\\beta C(s,a)-\\gamma\\tau(s,a)

$$



where:



\* \\(E(s,a)\\) represents projected efficiency,

\* \\(C(s,a)\\) represents collision or conflict cost,

\* \\(\\tau(s,a)\\) represents latency,

\* \\(\\alpha,\\beta,\\gamma\\) are weighting coefficients.



The formulation reflects the central engineering trade-off:



\*\*efficiency vs. safety vs. latency\*\*



The exact implementation should be distinguished from the broader mathematical research formulation where appropriate.



\---



\# 14. Experimental Interface



PMARS separates simulation execution from experimental evaluation.



```text

&#x20;            Simulation

&#x20;                │

&#x20;                ▼

&#x20;         Raw Experiment Data

&#x20;                │

&#x20;                ▼

&#x20;       Evaluation Pipeline

&#x20;                │

&#x20;         ┌──────┴──────┐

&#x20;         ▼             ▼

&#x20;      Analysis       Figures

&#x20;         │             │

&#x20;         └──────┬──────┘

&#x20;                ▼

&#x20;            Results

```



This separation makes it possible to run multiple experimental configurations without manually extracting results from individual simulations.



\---



\# 15. Reproducibility



The experimental framework is designed around reproducible computational experiments.



The research protocol uses fixed seed sequences and repeated trials.



Current documented seeds include:



```text

42

7

21

99

123

```



The intended workflow is:



```text

Paper

&#x20; ↓

Configuration

&#x20; ↓

Simulation

&#x20; ↓

Raw Results

&#x20; ↓

Analysis

&#x20; ↓

Figures / Tables

```



Results should be generated from the experiment pipeline rather than manually entered.



\---



\# 16. Ablation Architecture



Ablation experiments remove individual components to measure their contribution.



\### Full System



```text

Telemetry

&#x20;  +

Allocation

&#x20;  +

Routing

&#x20;  +

Conflict Resolution

&#x20;  +

Execution

```



\### Without Telemetry Bounds



```text

Allocation

&#x20;  +

Routing

&#x20;  +

Conflict Resolution

&#x20;  +

Execution

```



\### Without Conflict Resolution



```text

Telemetry

&#x20;  +

Allocation

&#x20;  +

Routing

&#x20;  +

Execution

```



Comparing these configurations helps distinguish improvements caused by the complete system from improvements attributable to individual components.



\---



\# 17. Baselines



PMARS uses simpler strategies as comparison points.



\### Random Allocation / Routing



Tasks or movement decisions are assigned without the complete coordination mechanism.



\### Greedy Routing



Agents select locally efficient routes, such as shortest-distance choices, without the full multi-agent coordination architecture.



\### Other Baselines



Additional baselines may be introduced when required by a particular experiment.



Baseline definitions should remain explicit so that comparisons are reproducible.



\---



\# 18. Scalability



PMARS can evaluate system behavior at different agent populations.



Example scaling regimes include:



```text

10

25

50

100

```



Increasing the number of agents can introduce:



\* spatial contention

\* increased coordination overhead

\* task queue pressure

\* collision opportunities

\* local routing deadlocks



Therefore, scalability experiments are used to identify performance boundaries rather than simply demonstrating a maximum agent count.



\---



\# 19. Failure Modes



PMARS explicitly documents system failure conditions.



\### Task Queue Bottlenecks



High task arrival rates can overwhelm available coordination capacity.



\### Spatial Deadlocks



High agent density can produce local configurations in which agents compete for limited spatial resources.



\### Coordination Degradation



At sufficiently high workload or density, coordination mechanisms may no longer compensate for increasing system contention.



Failure modes are treated as experimental observations rather than hidden implementation defects.



\---



\# 20. Current Limitations



The current system is simulation-based.



It does not currently model:



\* real motor friction

\* actuator backlash

\* realistic sensor noise

\* complete 3D kinematics

\* physical robot dynamics

\* real ROS communication

\* physical network packet behavior

\* hardware-level swarm deployment



Therefore:



> \*\*PMARS demonstrates computational coordination behavior, not physical robotic deployment.\*\*



This distinction is maintained throughout the research documentation.



\---



\# 21. Relationship to the Research Program



PMARS forms part of a broader research direction investigating:



\* adaptive multi-agent coordination

\* swarm intelligence

\* task allocation

\* supervisory control

\* failure-aware systems

\* resilient autonomous behavior



The repository represents the computational implementation and experimental artifact.



The associated research paper provides the broader theoretical and experimental framing.



\---



\# 22. Future Extension Path



A possible progression toward higher-fidelity robotic validation is:



```text

Current

2D Computational Simulation

&#x20;       │

&#x20;       ▼

Higher-Fidelity Simulation

&#x20;       │

&#x20;       ▼

Sensor / Communication Noise

&#x20;       │

&#x20;       ▼

ROS 2 Integration

&#x20;       │

&#x20;       ▼

3D Robotic Simulation

&#x20;       │

&#x20;       ▼

Physical Robot Validation

```



These are future research directions and should not be interpreted as capabilities demonstrated by the current implementation.



\---



\# 23. Engineering Principle



The central design principle of PMARS is:



> \*\*Evaluate multi-agent coordination as a closed-loop system under both normal operation and failure conditions.\*\*



The objective is therefore not merely to maximize a single performance metric.



The system should also reveal:



\* where coordination succeeds,

\* where it degrades,

\* which components contribute to performance,

\* how failures emerge,

\* and whether the experimental results can be reproduced.



\---



\## Architecture Summary



```text

┌─────────────────────────────────────────────┐

│                  PMARS                      │

├─────────────────────────────────────────────┤

│                                             │

│  Environment                                │

│       ↓                                     │

│  Telemetry                                  │

│       ↓                                     │

│  Task Allocation                             │

│       ↓                                     │

│  Routing                                    │

│       ↓                                     │

│  Conflict Resolution                         │

│       ↓                                     │

│  Agent Execution                             │

│       ↓                                     │

│  Metrics                                    │

│       │                                     │

│       └──────────► Feedback                  │

│                                             │

└─────────────────────────────────────────────┘

```



\*\*Observe → Allocate → Route → Resolve → Execute → Measure → Repeat\*\*



