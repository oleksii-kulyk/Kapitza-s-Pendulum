import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from scipy.integrate import solve_ivp
from math import fmod
from collections import deque

###Parameters and Initial Conditions, all given in SI units

#Initial Conditions:
#phi0 = 0 when pendulum is straight down
phi0, phidot0 = "np.pi", "np.pi/3" #in radians and radians per second
initial = [eval(phi0), eval(phidot0)]

#Parameters: amplitude, freq, length, g
a, n, l, g = 0.10, 80, 2, 9.80665 # SI units: meters, Hz, meters, m/s^2
#friction coefficient
gamma = 0.005 # unitless
#found stability at: param = [ 0.24, 54, 1, 9.80665] and initial = [np.pi/2, 0]

history_len = 50  # how many trajectory points to display

#interval of integration in seconds, how long to simulate for
interval = (0,200) # seconds

#default numerical integration method
integration_method = "LSODA"

#name template for saving the plot and animation files
savename = f"pi-pi!3-{a}-{n}-{l}-{gamma}-g_{integration_method}."

def system(t, X): #X[0] = phi, X[1] = d phi/dt
    Xdot = [[],[]]
    Xdot[0] = X[1]
    Xdot[1] = - ( (a*n**2)/l * np.cos(n*t) + g/l ) * np.sin(X[0]) - gamma*X[1] # gamma*X[1] is a friction term
    return Xdot

###Integration
def IntegratePlot(system, method, initial, interval):
    solution = solve_ivp(system, interval, initial, method=method, dense_output=True)
    
    #setting up the plot
    fig_angle_Epot = plt.figure()
    ax = fig_angle_Epot.add_subplot()
    ax.grid()
    ax.set_xlabel(xlabel='Time, s')
    ax.set_ylabel(ylabel='Angle, rad')

    #plotting system properties
    #potential energy and angle of pendulum
    Epot = -g *( l * np.cos(solution.y[0]) + a * np.cos(n * solution.t))
    ax.plot(solution.t, Epot, label='Potential Energy', color='C1', alpha=0.7)
    ax.plot(solution.t, solution.y[0], label='Angle', color='C0')
    plt.plot([], [], ' ', label="Integrator: "+method)
    plt.legend()
    savepath = "./Results/"+savename+"png"
    fig_angle_Epot.savefig(savepath, dpi=300)

    # plotting phase space
    fig_x_y = plt.figure()
    ax2 = fig_x_y.add_subplot(autoscale_on=False, xlim=(-1.15*l, 1.15*l), ylim=(-1.15*l, 1.15*l))
    ax2.set_aspect('equal')
    ax2.grid()
    ax2.set_xlabel(xlabel='x, meters')
    ax2.set_ylabel(ylabel='y, meters')

    #get x, y coords from angle phi
    x  =   l*np.sin(solution.y[0])
    y  = - l*np.cos(solution.y[0]) - a*np.cos(n*solution.t)
    ax2.scatter(x, y, marker='.', s=0.1)
    savepath = "./Results/"+"Phase-"+savename+"png"
    fig_x_y.savefig(savepath, dpi=300)

    return solution

###Animation
def Animate(solution):
    fig = plt.figure(figsize=(5, 4))
    ax = fig.add_subplot(autoscale_on=False, xlim=(-1.5*l, 1.5*l), ylim=(-1.5*l, 1.5*l))
    ax.set_aspect('equal')
    ax.grid()
    ax.plot(0, 0, marker='o', markersize=11, color='tab:blue') #pivot point
    
    line, = ax.plot([], [], 'o-', lw=2, color='tab:blue')
    trace, = ax.plot([], [], '.-', lw=1, ms=2, color='tab:orange')
    time_template = 'time = %.1fs'
    time_text = ax.text(0.05, 0.9, '', transform=ax.transAxes)
    angle_template = 'angle = %.1fπ rad'
    angle_text = ax.text(0.95, 0.9, '', transform=ax.transAxes, horizontalalignment='right')
    history_x, history_y = deque(maxlen=history_len), deque(maxlen=history_len)
    
    #get x, y coords from angle phi
    x  =   l*np.sin(solution.y[0])
    y  = - l*np.cos(solution.y[0]) - a*np.cos(n*solution.t)
    Ox = np.zeros(len(solution.t))
    Oy = - a*np.cos(n*solution.t)

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
        time_text.set_text(time_template % solution.t[i])
        angle = fmod(solution.y[0][i], 2*np.pi) / np.pi
        angle_text.set_text(angle_template % angle)
        return line, trace, time_text, angle_text
    
    frame_time = (solution.t[-1] - solution.t[0]) / len(solution.t) * 1000  # in milliseconds
    ani = animation.FuncAnimation(
        fig, animate, len(y), interval=frame_time, blit=True)
    return ani


###Running the program
if __name__ == "__main__":
    print("Running Integrator.py")
    print("Pick an integration method:e.g. #DOP853 #LSODA #Radau\n")

    methods = ["RK45","DOP853","Radau","BDF","LSODA"]
    print("Available methods are: ", methods)
    integration_method = input("Enter the method you want to use (default is LSODA):")

    if integration_method not in methods:
        integration_method = "LSODA"
        print("Using default method: LSODA")
    else:
        print("Using method: ", integration_method)

    solution = IntegratePlot(system, integration_method, initial, interval)
    ani = Animate(solution)
    plt.show()

    #saving the animation, may take a while (30 minutes for 200 seconds of animation on my 2019 PC)
    #change the path to your ffmpeg.exe
    matplotlib.rcParams['animation.ffmpeg_path'] = r"C:/Users/Oleksiy/miniconda3/pkgs/ffmpeg-6.1.1-hc79a5da_3/Library/bin/ffmpeg.exe"
    writer = animation.FFMpegWriter(fps=30, bitrate=-1)
    savepath = "./Results/"+savename+"mp4"
    print(f"Saving animation to {savepath}")
    ani.save(savepath, writer=writer)


