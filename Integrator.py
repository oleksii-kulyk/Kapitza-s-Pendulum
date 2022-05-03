from scipy.integrate import solve_ivp
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import deque

#Initial Conditions: phi0, phidot0
#all given in SI units
initial = [np.pi/2, 0]
#Parameters: amplitude, freq, length, g
param = [ 0.24, 54, 1, 9.80665]
#found stability at: param = [ 0.24, 54, 1, 9.80665] and initial = [np.pi/2, 0]
a = param[0]
n = param[1]
l = param[2]
g = param[3]
history_len = 50  # how many trajectory points to display

def system(t, X):
    Xdot = [[],[]]
    Xdot[0] = X[1]
    Xdot[1] = - ( (a*n**2)/l * np.cos(n*t) + g/l ) * np.sin(X[0])
    return Xdot

###Integration
def IntegratePlot(system, method, initial, interval):
    solution = solve_ivp(system, interval, initial, method=method)
    
    fig = plt.figure()
    ax = fig.add_subplot()
    ax.grid()
    ax.set_xlabel(xlabel='Time, s')
    ax.set_ylabel(ylabel='Angle, rad')
    
    Epot = -g *( l * np.cos(solution.y[0]) + a * np.cos(n * solution.t))
    ax.plot(solution.t, Epot, label='Potential Energy', color='C1', alpha=0.7)
    ax.plot(solution.t, solution.y[0], label='Angle', color='C0')
    plt.plot([], [], ' ', label="Integrator: "+method)
    
    plt.legend()
    return solution

###Animation
def Animate(solution):
    fig = plt.figure(figsize=(5, 4))
    ax = fig.add_subplot(autoscale_on=False, xlim=(-2*l, 2*l), ylim=(-2*l, 2*l))
    ax.set_aspect('equal')
    ax.grid()
    
    line, = ax.plot([], [], 'o-', lw=2)
    trace, = ax.plot([], [], '.-', lw=1, ms=2)
    time_template = 'time = %.1fs'
    time_text = ax.text(0.05, 0.9, '', transform=ax.transAxes)
    history_x, history_y = deque(maxlen=history_len), deque(maxlen=history_len)
    
    x  =   l*np.sin(solution.y[0])
    y  = - l*np.cos(solution.y[0]) - a*np.cos(n*solution.t)
    Ox = np.zeros(len(solution.t))
    Oy = - a*np.cos(n*solution.t)
    
    dt = 0.02 #time differential for animation
    def animate(i):
        thisx = [Ox[i], x[i]]
        thisy = [Oy[i], y[i]]
    
        if i == 0:
            history_x.clear()
            history_y.clear()
    
        history_x.appendleft(thisx[1])
        history_y.appendleft(thisy[1])
    
        line.set_data(thisx, thisy)
        trace.set_data(history_x, history_y)
        time_text.set_text(time_template % (i*dt))
        return line, trace, time_text
    
    
    ani = animation.FuncAnimation(
        fig, animate, len(y), interval=dt*1000, blit=True)
    return ani
    #embed = ani.to_html5_video()
    #print(embed)
    
###Running the program
#Pick an integration method: #DOP853 #LSODA #Radau
method = ["RK45","DOP853","Radau","BDF","LSODA"]
#interval of integration in seconds
interval = (0,200)

for me in method:
    solution = IntegratePlot(system, me, initial, interval)
#ani = Animate(solution)

