import numpy as np
import imageio

frames = []

agents = np.random.rand(50,2)

for t in range(60):
    agents += np.random.randn(50,2)*0.02
    frame = (agents*255).astype('uint8')
    frames.append(frame)

imageio.mimsave('../../visuals/swarm_demo.gif', frames, fps=10)
print('GIF saved')
