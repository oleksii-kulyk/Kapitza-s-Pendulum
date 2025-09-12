# Kapitza's Pendulum Simulation
This repository contains a Python script that simulates, plots, and animates the motion of a [Kapitza's Pendulum][https://en.wikipedia.org/wiki/Kapitza%27s_pendulum].

Kapitza's pendulum is a classic physics problem demonstrating how a dynamically stable equilibrium can be created. It shows that an inverted rigid pendulum, which is normally unstable at its upper equilibrium point, can be stabilized by vertically oscillating its pivot point at a high frequency.
## Features
*   **Numerical Simulation**: Solves the differential equation of motion for a pendulum with a vertically oscillating pivot.
*   **Multiple Solvers**: Allows the user to choose from various numerical integration methods provided by SciPy, including `RK45`, `DOP853`, `Radau`, `BDF`, and `LSODA`.
*   **Data Visualization**: Generates a plot of the pendulum's angle and potential energy over the simulation time.
*   **Animation**: Creates a real-time animation of the pendulum's motion, showing the oscillating pivot, the pendulum arm, and a trace of the bob's trajectory.
#### Requirements
*   Python 3.x
*   NumPy
*   SciPy
*   Matplotlib

You can install the required libraries using pip:
```bash
pip install numpy scipy matplotlib
```
## Usage
1.  Clone the repository:
    ```bash
    git clone https://github.com/oleksii-kulyk/kapitza-s-pendulum.git
    cd kapitza-s-pendulum
    ```

2.  Run the script from your terminal:
    ```bash
    python Integrator.py
    ```

3.  The program will prompt you to select an integration method. You can choose one from the provided list (e.g., `Radau`) or press Enter to use the default `LSODA` method.

    ```
    Running Integrator.py
    Pick an integration method:e.g. #DOP853 #LSODA #Radau

    Available methods are:  ['RK45', 'DOP853', 'Radau', 'BDF', 'LSODA']
    Enter the method you want to use (default is LSODA):
    ```

4.  Upon execution, two Matplotlib windows will open:
    *   A plot showing the pendulum's angle and potential energy versus time.
    *   An animation window displaying the pendulum's movement.
## Customization
You can modify the simulation's parameters by editing the top section of the `Integrator.py` file.

*   **Initial Conditions**:
    ```python
    # Initial Conditions: phi0, phidot0 (angle, angular velocity)
    # phi0 = np.pi corresponds to the inverted (upright) position
    initial = [np.pi, np.pi/100]
    ```

*   **Physical Parameters**:
    ```python
    # Parameters: amplitude (m), frequency (rad/s), length (m), g (m/s^2)
    param = [ 0.10, 60, 2, 9.80665]
    ```

*   **Simulation Duration**:
    ```python
    # Interval of integration in seconds
    interval = (0, 200)
