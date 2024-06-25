import numpy as np
from scipy.optimize import minimize

# Measured data
frequencies = np.array([13, 190, 449, 680, 744, 1080, 1361, 1662, 2155, 2648]) * 1e3  # kHz to Hz
measured_impedances = np.array([15.02, 18.30, 38.40, 104.44, 104.82, 36.62, 23.42, 17.43, 12.80, 10.47])
#


# Define the impedance function
def impedance(f, R1, R2, L, C):
    j = 1j
    return R1 + ((R2 + j * 2 * np.pi * f * L) / (1 - (2 * np.pi * f)**2 * L * C + j * 2 * np.pi * f * R2 * C))

# Define the objective function (SSE)
def objective_function(params):
    R1, R2, L, C = params
    predicted_impedances = np.abs(impedance(frequencies, R1, R2, L, C))
    return np.sum((predicted_impedances - measured_impedances)**2)

# Initial guess for parameters
initial_guess = [10, 10, 10e-6, 10e-9]  # R1, R2, L, C

# Bounds for the parameters
bounds = [(0, 20), (0, 20), (0, 20e-6), (0, 20e-9)]

# Nelder-Mead optimization
result = minimize(objective_function, initial_guess, method='Nelder-Mead', bounds=bounds)

# Print the results
# Print the results
print("Optimized Parameters:")
print(f"R1: {result.x[0]:.2f} Ohms")
print(f"R2: {result.x[1]:.2f} Ohms")
print(f"L: {result.x[2]:.2e} H")
print(f"C: {result.x[3]:.2e} F")
print(f"Optimization Function Value: {result.fun:.9f}")  # Increased precision


# tacka pod G)
import matplotlib.pyplot as plt

# Frequency range for plotting
frequencies_plot = np.arange(0, 3000 * 1e3 + 10 * 1e3, 10 * 1e3)  # 0 to 3000 kHz with 10 kHz steps

# Calculate impedance for the optimized parameters
predicted_impedances_plot = np.abs(impedance(frequencies_plot, result.x[0], result.x[1], result.x[2], result.x[3]))

# Plot the results
plt.figure(figsize=(8, 6))
plt.plot(frequencies / 1e3, measured_impedances, 'o', label='Measured Impedance')  # Measured data
plt.plot(frequencies_plot / 1e3, predicted_impedances_plot, '-', label='Calculated Impedance')  # Calculated data

plt.xlabel('Frequency (kHz)')
plt.ylabel('Impedance (Ω)')
plt.title('Measured vs. Calculated Impedance')
plt.legend()
plt.grid(True)
plt.show()