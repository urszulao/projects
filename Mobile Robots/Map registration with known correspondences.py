import numpy as np
import matplotlib.pyplot as plt
import math

X1 = np.array([[5, 6, 7, 6, 5],[2, 1, 0, -1, -2]]);
print(X1.shape[1])
P = np.vstack([1,1,0])
print(P.shape)

# This simulates the observation taken by a sensor mounted on the robot.
# suppose that the robot is placed at [0,0,0]'
X1 = np.array([[5, 6, 7, 6, 5],[2, 1, 0, -1, -2]]);

# Now the robot moves Delta_p (a pose increment)
Delta_p = np.vstack([2,1,-45*np.pi/180]);

# The scenario behaves differently, i.e when the robot move towards a wall,
# said wall appears closed in the observation. Also when the robot turns right 
# (negative Delta_theta) the  wall "turns" to the left in the observation
# These lines computes how the robot sees the environment after the motion.
T = np.vstack([-Delta_p[0],-Delta_p[1]]);
theta = -Delta_p[2][0]

c = np.cos(theta)
s = np.sin(theta)

R = np.array([[c, -s],
             [s, c]])

# This simulates a scenario where the robot first rotates and then moves. 
# X2 = R@X1 + T

# This simulates a scenario where the robot first moves and then rotates
X2 = R@(X1+T)

# Print both matrices:
print('Z1: \n', X1)
print('Z2: \n', X2)

# First, plotting "the map" and the two robot poses
fig, ax = plt.subplots(figsize = (11*0.6,8*0.6))
robot_pose = np.vstack([0.,0.,0]) # [x,y,theta]
radius = 0.3;
# Initial robot pose
robot = plt.Circle(( robot_pose[0] , robot_pose[1] ), radius, color='tab:orange' )
ax.add_artist( robot )
plt.plot([robot_pose[0], robot_pose[0]+0.5*np.cos(robot_pose[2])], 
         [robot_pose[1], robot_pose[1]+0.5*np.sin(robot_pose[2])], 
         linewidth=5, color='c')
plt.text(x=robot_pose[0]+0.1,y=robot_pose[1]+radius+0.1,s="p1")
# Robot pose after increment (this was a trick since the initial was [0,0,0])
robot_pose = Delta_p 
radius = 0.3;
robot = plt.Circle(( robot_pose[0] , robot_pose[1] ), radius, color='tab:orange' )
ax.add_artist( robot )
plt.plot([robot_pose[0], robot_pose[0]+0.5*np.cos(robot_pose[2])], 
         [robot_pose[1], robot_pose[1]+0.5*np.sin(robot_pose[2])], 
         linewidth=5, color='c')
plt.text(x=robot_pose[0]+0.1,y=robot_pose[1]+radius+0.1,s="p2")
plt.plot([3,7, 3],[4, 0, -4],'tab:gray')
plt.xlim([-1,10]), plt.ylim([-4,4]);
plt.show()

# Plotting the observations. Since we don't know where the robot is after 
# the motion, drawing its observation as is the robot remained at the initial position
plt.figure(figsize = (11*.6,8*.6))
plt.plot(X1[0,:],X1[1,:],'bo',label='Z1 (target)') # Target observation
plt.plot(X2[0,:],X2[1,:],'rx',label='Z2 (source)') # Source observation
plt.legend()
plt.xlim([-1,10]), plt.ylim([-4,4]);

# Compute ceter of mass
mu_X1 = (1/X1.shape[1])*np.sum(X1,axis=1) 
mu_X2 = (1/X2.shape[1])*np.sum(X2,axis=1)

print("X1 center of mass", mu_X1)
print("X2 center of mass", mu_X2)

# Substract the center of mass to the observations
X1_ = X1 - np.vstack(mu_X1)
X2_ = X2 - np.vstack(mu_X2)
print(X1_)
print(X2_)

# Compute the covariance matrix
W = X1_@X2_.T
print(W)
# Obtain the SVD decomposition
U, S, V = np.linalg.svd(W, full_matrices=True)
print(V)

# Obtain the SVD decomposition
U, S, V = np.linalg.svd(W, full_matrices=True)
print(V)

# Retrieve the transformation (rotation plus translation)
R = U@V.T
t = mu_X1-R@mu_X2
print('R:',R)
print('t:',t)

# Apply transformation and show results

# From 2 to 1
X2_to_X1 = R@X2 + np.vstack(t)
plt.figure(figsize = (11*.6,8*.6))
plt.plot(X1[0,:],X1[1,:],'bo',label='Z1 (target)') # Target observation
plt.plot(X2_to_X1[0,:],X2_to_X1[1,:],'r+',label='Z2 (source transformed)') # Source observation transformed
plt.legend()
plt.xlim([-1,10]), plt.ylim([-4,4]);

# From 1 to 2
X1_to_X2 = R.T@X1 - R.T@np.vstack(t)
plt.figure(figsize = (11*.6,8*.6))
plt.plot(X1_to_X2[0,:],X1_to_X2[1,:],'bo',label='X1 (target transformed)') # Target observation transformed
plt.plot(X2[0,:],X2[1,:],'r+',label='X2 (source)') # Source observation
# plt.legend
plt.xlim([-1,10]), plt.ylim([-4,4]);

X2_to_X1_to_X2 = R.T@X2_to_X1 - R.T@np.vstack(t)
plt.figure(figsize = (11*.6,8*.6))
plt.plot(X2[0,:],X2[1,:],'bo',label='Z1 (target)') # Target observation
plt.plot(X2_to_X1_to_X2[0,:],X2_to_X1_to_X2[1,:],'r+',label='Z2 (source transformed)') # Source observation transformed
plt.legend()
plt.xlim([-1,10]), plt.ylim([-4,4]);

# Robot pose
Delta_theta = math.atan2(R[1,0],R[0,0])*180/np.pi

Delta_p = np.vstack([np.vstack(t),Delta_theta])
print('Computed Delta_p:\n', Delta_p)