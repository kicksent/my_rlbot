import numpy as np
import math
from Utilities.LinearAlgebra import vec3

#useful values for field in unreal units
GOAL_WIDTH = 1900
FIELD_LENGTH = 10280
FIELD_WIDTH = 8240

''' takes in a car object, and returns an proper orthogonal orientation matrix 
    [[fx, lx, ux]
    [fy, ly, uy]
    [fz, lz, uz]]'''
def get_orientation_matrix(my_object):
    #print(my_object.rotation)
    CR = np.cos(my_object.rotation[2]) #roll
    SR = np.sin(my_object.rotation[2]) #roll
    CP = np.cos(my_object.rotation[0]) #pitch
    SP = np.sin(my_object.rotation[0]) #pitch
    CY = np.cos(my_object.rotation[1]) #yaw
    SY = np.sin(my_object.rotation[1]) #yaw

    v1 = np.array([CP*CY, CP * SY, SP])
    v2 =  np.array([CY * SP * SR - CR * SY, SY * SP * SR + CR * CY, -CP * SR])
    v3 =  np.array([-CR * CY * SP - SR * SY, -CR * SY * SP + SR * CY, CP * CR])
    matrix = np.matrix([v1, v2, v3]) 

    return matrix

'''returns angle between two objects in 2D(x,y) plane'''
def angle2D(target, object):
    difference = to_nparray(target) - to_nparray(object)
    return np.arctan2(difference[1], difference[0])

'''returns vertical angle between two objects in 2D(y,z) plane'''
def angleyz(target, object):
    difference = to_nparray(target) - to_nparray(object)
    return(np.arctan2(difference[2], difference[1]))

'''returns vertical angle between two objects in 2D(y,z) plane'''
def anglexz(target, object):
    difference = to_nparray(target) - to_nparray(object)
    return(np.arctan2(difference[2], difference[0]))


'''returns distance between two objects in 2D plane using pythagorean theorum'''
def distance2D(target, object):
    diff = to_nparray(target) - to_nparray(object)
    return np.sqrt(diff[0]**2 + diff[1]**2)

'''returns distance between two objects in 3D plane using pythagorean theorum'''
def distance3D(target, object):
    diff = to_nparray(target) - to_nparray(object)
    return np.sqrt(diff[0]**2 + diff[1]**2 + diff[2]**2)

def velocity2D(target):
    return np.sqrt(target.velocity.data[0]**2 + target.velocity.data[1]**2)

def normalize_vector(v):
    norm = np.linalg.norm(v)
    return(np.array([v[0]/norm, v[1]/norm, v[2]/norm]))

''' 
target - accepts obj (car or ball), list, or np.array 
    our_object - accepts car location
    returns local_location as an array
'''
def to_local(target_object,our_object):
    x = np.dot((to_nparray(target_object) - to_nparray(our_object)),  np.array(our_object.matrix[0].A1)) #A1 returns a flattened ndarray
    y = np.dot((to_nparray(target_object) - to_nparray(our_object)),  np.array(our_object.matrix[1].A1))
    z = np.dot((to_nparray(target_object) - to_nparray(our_object)),  np.array(our_object.matrix[2].A1))
    # print("x,y,z", np.array([x,y,z]))
    return np.array([x,y,z])

''' accepts class obj objects, lists of size 3, or np.array([x,y,z]) and returns np.array([x,y,z])'''
def to_nparray(target):
    if type(target) == type(np.array(1)):
        return target
    elif (type(target) == type([1])):
        return np.array(target)
    else:
        return target.location

def toLocal(target, object):
    if isinstance(target, np.ndarray):
        return target.local_location
    else:
        return(to_local(target, object))


def sign(x):
    if x <= 0:
        return -1
    else:
        return 1

def angle_to_radians(angle):
    return(np.pi/180)
    
# def steer(distance, angle):

# def yaw():

def rand_boost():
    return(np.random.randint(2, dtype='bool'))

def flutter_boost(percent_prob):
    return(True if np.random.binomial(1, percent_prob) else False)
    