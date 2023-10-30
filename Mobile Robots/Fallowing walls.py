import numpy as np
import matplotlib.pyplot as plt 
import math
import sys
from laser2D import Laser2D

fig, ax = plt.subplots(figsize = (17*2/3,11*2/3))
plt.xlim([-1,16]), plt.ylim([-1,10]),
plt.title('Robot following a wall'), plt.xlabel('x(m)'),plt.ylabel('y(m)')

# Define the environment and show it
map = np.array([[0, 0, 4, 4, 6, 8, 10, 10, 8, 4, 4, 1, 0],
                [4, 0, 0, 2, 2, 0, 0, 4, 6, 6, 5, 5, 4]])*1.5
plt.plot(map[0,:],map[1,:])

# Set robot pose and draw it
robot_pose = np.vstack([8., 4., -3.4*np.pi/2+0.1]) # [x,y,theta]^T
radius = 0.3;
robot = plt.Circle(( robot_pose[0] , robot_pose[1] ), radius )
ax.add_artist( robot )
plt.plot([robot_pose[0], robot_pose[0]+0.5*np.cos(robot_pose[2])],
        [robot_pose[1], robot_pose[1]+0.5*np.sin(robot_pose[2])], linewidth=5)

# Prepare the laser
FOV = 270 * np.pi/180        # radians
resolution = 10 * np.pi/180  #radians
max_distance = 10         # meters
noise_cov = np.array([[0, 0],[0, 0]]) # covariance matrix
laser_pose = robot_pose   # [x,y,theta]

laser = Laser2D(FOV, resolution, max_distance, noise_cov, laser_pose)
z = laser.take_observation(map)
laser.draw_observation(z,laser_pose,fig,ax)
plt.show()