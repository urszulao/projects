import numpy as np
import matplotlib.pyplot as plt 
import math
import sys
from laser2D import Laser2D

fig, ax = plt.subplots(figsize = (17*2/3,11*2/3))
plt.xlim([-1,16]), plt.ylim([-1,10]),
plt.title('Robot in workspace with laser beams'), plt.xlabel('x(m)'),plt.ylabel('y(m)')

# Define the environment and show it
map = np.array([[0, 0, 4, 4, 6, 8, 10, 10, 8, 4, 4, 1, 0],
                [4, 0, 0, 2, 2, 0, 0, 4, 6, 6, 5, 5, 4]])*1.5
plt.plot(map[0,:],map[1,:])



# Draw coordinates of each point
for i_point in range(map.shape[1]):
    plt.text(map[0,i_point]+0.1,map[1,i_point]+0.1,
            '('+str(map[0,i_point])+','+str(map[1,i_point])+')',
            fontsize='x-large', bbox=dict(boxstyle='round', facecolor='green', alpha=0.5))


# Set robot pose and draw it
robot_pose = np.vstack([2., 2., -3.4*np.pi/2+0.1]) # [x,y,theta]^T
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

# Prepare figure
fig, ax = plt.subplots(figsize = (17*2/3,11*2/3))
plt.xlim([-1,16]), plt.ylim([-1,10]),
plt.title('Follow the wall'), plt.xlabel('x(m)'),plt.ylabel('y(m)')

# Define the environment and show it
map = np.array([[0, 0, 4, 4, 6, 8, 10, 10, 8, 4, 4, 1, 0],
                [4, 0, 0, 2, 2, 0, 0, 4, 6, 6, 5, 5, 4]])*1.5
plt.plot(map[0,:],map[1,:])

# Robot parameters
radius = 0.5;
l = 0.2 # m (Distance between the robot center and one wheel)
r = 0.1 # m (wheel radius)
v = 0.3 # m/s
robot_pose = np.vstack([3., 1., 3*np.pi/4]) # [x,y,theta]^T

# Draw initial pose
robot = plt.Circle(( robot_pose[0][0] , robot_pose[1][0] ), radius )
ax.add_patch( robot )
plt.plot([robot_pose[0], robot_pose[0]+0.5*np.cos(robot_pose[2])],
         [robot_pose[1], robot_pose[1]+0.5*np.sin(robot_pose[2])], linewidth=5)

# Laser parameters
FOV = 270 * np.pi/180         # radians
resolution = 10 * np.pi/180   # radians
max_distance = 10             # meters
noise_cov = np.array([[0.05, 0],[0, 0.0002]]) # covariance matrix
T = 1/10                      # s (Working period, inverse of working frequency)
Dl = 0                        # m Distance of the laser in the x-axis from the origin
laser_pose = robot_pose       # [x,y,theta]

# Create the laser object
# noise_cov = np.array([[0.1, 0],[0, 0.1]]) # covariance matrix
laser = Laser2D(FOV, resolution, max_distance, noise_cov, laser_pose)

# Configuration of the pure pursuit algorithm
dw = 1.5  # m Path distance to the wall
L = 1     # m (lookahead distance)

t_sim = 13  # seconds
l_sim = int(13/T) # Simulation length

# Follow that wall!
for i in range(l_sim):

  # Start by taking a measurement
  z = laser.take_observation(map) # z is a matrix with rows indexing distance
                                  # or angle, and columns indexing measurements
  # Get the index of the shortest distanceç
  i_min_d = np.argmin(z[0,:])
  rho_s = z[0,i_min_d]
  theta_s = z[1,i_min_d]

  # Get coordinate y of the path (in the local reference system X_hat Y_hat)
  y_p = np.sign(theta_s)*(Dl*np.cos(theta_s)+rho_s-dw)

  # Get goal coordinates
  if np.abs(y_p) < L:
    y_g = y_p
    x_g = np.sqrt(L**2-y_p**2)
  else:
    y_g = L*np.sign(y_p)
    x_g = 0

  # Retrieve Delta_y, curvature and motion
  Delta_y_aux = y_g*np.sin(theta_s) - x_g*np.cos(theta_s) # Follow wall on the left
  # Delta_y_aux = -y_g*np.sin(theta_s) + x_g*np.cos(theta_s) # Follow wall on the right

  gamma = 2*Delta_y_aux/(L**2) # Curvature is positive turning left and negative turning right
  v_l = v*(1-l*gamma)/r
  v_r = v*(1+l*gamma)/r

  # # Angular velocities (Not needed)
  # w_l = v_l/r
  # w_r = v_r/r

  # Compute robot motion
  theta = robot_pose[2]
  Delta_x = ((v_l+v_l)/2)*np.cos(theta)*T # Equivalent to ((r*w_l+r*w_r)/2)*np.cos(theta)*T
  Delta_y = ((v_l+v_r)/2)*np.sin(theta)*T # Equivalent to ((r*w_l+r*w_r)/2)*np.sin(theta)*T
  Delta_theta = ((v_r-v_l)/(2*l))*T       # Equivalent to ((r*w_r-r*w_l)/(2*l))*T

  # Get new robot pose
  robot_pose += np.vstack([Delta_x, Delta_y, Delta_theta])
  laser.set_pose(robot_pose)
  # robot = plt.Circle(( robot_pose[0][0] , robot_pose[1][0] ), radius )
  # ax.add_patch( robot )
  # plt.plot([robot_pose[0], robot_pose[0]+0.5*np.cos(robot_pose[2])],
  #         [robot_pose[1], robot_pose[1]+0.5*np.sin(robot_pose[2])], linewidth=5)
  plt.plot( robot_pose[0] , robot_pose[1], 'om' )

  # print('New robot pose:',robot_pose)

# Draw final robot pose
robot = plt.Circle(( robot_pose[0][0] , robot_pose[1][0] ), radius )
ax.add_patch( robot )
plt.plot([robot_pose[0], robot_pose[0]+0.5*np.cos(robot_pose[2])],
         [robot_pose[1], robot_pose[1]+0.5*np.sin(robot_pose[2])], linewidth=5)

plt.show()