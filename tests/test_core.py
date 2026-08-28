import random
import numpy as np
import pytest

from src.agents.nanobot import NanoBot
from src.environment.environment import Environment
from src.environment.tissue_environment import TissueEnvironment
from src.rl.dqn_agent import DQNAgent
from src.swarm.swarm_engine import SwarmEngine


def test_nanobot_initialization():
    bot = NanoBot(1)

    assert bot.id == 1
    assert bot.health == 100
    assert bot.act() == "repair"


def test_environment_initial_state():
    env = Environment()

    assert env.state == "stable"


def test_tissue_environment_creation():
    env = TissueEnvironment(n=10)

    assert len(env.graph.nodes) == 10
    assert isinstance(env.failed, set)


def test_failure_injection():
    env = TissueEnvironment(n=10)

    env.inject_failure(0)

    assert 0 in env.failed


def test_failure_propagation():
    random.seed(42)

    env = TissueEnvironment(n=10)
    env.inject_failure(0)

    before = set(env.failed)
    env.propagate()

    assert before.issubset(env.failed)


def test_dqn_agent_creation():
    agent = DQNAgent(state_dim=4, action_dim=2)

    assert agent.model is not None
    assert agent.target is not None
    assert agent.optimizer is not None
    assert agent.gamma == 0.99


def test_dqn_action_range():
    random.seed(42)
    np.random.seed(42)

    agent = DQNAgent(state_dim=4, action_dim=2)

    state = np.zeros(4, dtype=np.float32)
    action = agent.select_action(state)

    assert action in [0, 1]


def test_swarm_engine_initialization():
    engine = SwarmEngine()

    assert engine.client is not None
    assert isinstance(engine.agents, list)


def test_swarm_agent_spawn():
    engine = SwarmEngine()

    engine.spawn_agent([0, 0, 0])

    assert len(engine.agents) == 1


def test_swarm_step():
    engine = SwarmEngine()

    engine.spawn_agent([0, 0, 0])

    count = engine.step()

    assert count == 1
