import matplotlib.pyplot as plt
import numpy as np

agents = [8,16,32]

normal = [2.3,4.8,9.6]
stress = [2.4,5.0,9.8]
cascade = [0.8,1.2,1.5]

plt.figure()
plt.plot(agents, normal, label='Normal')
plt.plot(agents, stress, label='Stress')
plt.plot(agents, cascade, label='Failure')
plt.title('PMARS Throughput Scaling')
plt.legend()
plt.savefig('../../visuals/results_plot.png')

plt.figure()
plt.bar(['Normal','Stress','Cascade'], [100,100,11])
plt.title('System Stability')
plt.savefig('../../visuals/architecture.png')

print('Plots generated')
