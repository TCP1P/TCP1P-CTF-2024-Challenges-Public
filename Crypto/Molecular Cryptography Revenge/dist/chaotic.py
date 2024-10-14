import numpy as np
from scipy.integrate import solve_ivp
import random

# System Parameters
a, b, c, d = 36, 3, 28, 16

# Initial Conditions
x0 = round(random.uniform(-20, 20), 1)
y0 = round(random.uniform(-30, 30), 1)
z0 = round(random.uniform(0.1, 40), 1)
q0 = round(random.uniform(-20, 20), 1)
k = round(random.uniform(-0.7, 0.7), 2)

# Time Settings
h = 0.001  # Time step
T = 1.0    # Total time
t_eval = np.arange(0, T, h)  # Evaluation times

# Define the system of ODEs
def chaos(t, vars):
    x, y, z, q = vars
    dx = a * (y - x)
    dy = -x * z + d * x + c * y - q
    dz = x * y - b * z
    dq = x + k
    return [dx, dy, dz, dq]

def generate_sequences(M, N):
    sol = solve_ivp(chaos, [0, T], [x0, y0, z0, q0], t_eval=t_eval, method='RK45')
    x_data = sol.y[0]
    y_data = sol.y[1]

    # Sampling Parameters
    total_samples = len(x_data)
    indices_x = np.linspace(0, total_samples - 1, M, dtype=int)
    indices_y = np.linspace(0, total_samples - 1, N, dtype=int)

    # Sample the Sequences
    x_sequence = x_data[indices_x]
    y_sequence = y_data[indices_y]
    
    lx = np.argsort(x_sequence)
    ly = np.argsort(y_sequence)

    return lx, ly
