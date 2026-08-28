import pybullet as p
import pybullet_data
import time

class SwarmEngine:
    def __init__(self):
        self.client = p.connect(p.DIRECT)
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        self.agents = []

    def spawn_agent(self, pos):
        agent = p.loadURDF('sphere2.urdf', pos)
        self.agents.append(agent)

    def step(self):
        p.stepSimulation()
        return len(self.agents)
