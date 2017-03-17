import matplotlib.pyplot as plt
from code_contributors import get_distribution

plt.plot(get_distribution({'A': 3, 'B': 10, 'C': 1}), label='1')
plt.plot(get_distribution({'A': 5, 'B': 2, 'C': 1}), label='2')
plt.ylabel('users')
plt.xlabel('commits')
plt.legend()
plt.show()
