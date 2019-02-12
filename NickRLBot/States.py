import numpy as np
from Util import *
import time
from rlbot.agents.base_agent import BaseAgent, SimpleControllerState

class doNothing:
    def __init__(self):
        self.expired = False
    def execute(self, agent):
        controller_state = SimpleControllerState()
        return(controller_state)

class atba:
    def __init__(self):
        self.expired = False
    def execute(self, agent):
        
        target_speed = velocity2D(agent.ball) + (distance2D(agent.ball, agent.me)/1.5)
        #print("target_location", target.location)
        return self.exampleController(agent, target_speed)

    def exampleController(self, agent, target_speed):
        controller_state = SimpleControllerState()

        angle_to_ball = np.arctan2(agent.ball.local_location[1], agent.ball.local_location[0])
        current_speed = velocity2D(agent.me)
        #steering
        
        controller_state.steer = controller_state.yaw = clamp(angle_to_ball*2.5, -1, 1)
        #throttle
        if(target_speed > current_speed):
            controller_state.throttle = 1
            if(target_speed > 1400 and agent.start > 2.2 and current_speed < 2250 and np.abs(angle_to_ball) < .3): #there might be a problem here with self.start for boosting check later
                controller_state.boost = True
        elif target_speed < current_speed:
            controller_state.throttle = 0
            controller_state.boost = 0

        #dodging
        # time_difference = time.time() - agent.start
        # if time_difference > 2.2 and distance2D(agent.ball.location, agent.me.location) > 2000 and abs(angle_to_ball) < 1.3:
        #     agent.start = time.time()
        # elif time_difference <= .1:
        #     controller_state.jump = True
        #     controller_state.pitch = -1
        # elif time_difference > .1 and time_difference < .15:
        #     controller_state.jump = False
        #     controller_state.pitch = -1
        # elif time_difference > .15 and time_difference < 1:
        #     controller_state.jump = True
        #     controller_state.yaw = controller_state.steer
        #     controller_state.pitch = -1
        return controller_state

class shot:
    def __init__(self):
        self.expired = False
    def execute(self, agent):
        return(self.shotController(agent))
    def shotController(self, agent):
        controller_state = SimpleControllerState()
        goal_location = toLocal([0, -sign(agent.team)*FIELD_LENGTH/2, 0], agent.me) #100 is arbitrary since math is in 2D still
        goal_angle = np.arctan2(goal_location[1], goal_location[0])
        #print(goal_angle * 180 / np.pi)

        location = toLocal(agent.ball, agent.me)
        angle_to_target = np.arctan2(location[1], location[0])
        target_speed = velocity2D(agent.ball) + (distance2D(agent.ball, agent.me)/1.5)

        current_speed = velocity2D(agent.me)
        #steering
        if angle_to_target > .1:
            controller_state.steer = controller_state.yaw = 1
        elif angle_to_target < -.1:
            controller_state.steer = controller_state.yaw = -1
        else:
            controller_state.steer = controller_state.yaw = 0
        #throttle
        if angle_to_target >= 1.4:
            target_speed -= 1400
        else:
            if(target_speed > 1400 and target_speed > current_speed and agent.start > 2.2 and current_speed < 2250):
                controller_state.boost = True
        if target_speed > current_speed:
            controller_state.throttle = 1.0
        elif target_speed < current_speed:
            controller_state.throttle = 1

        #dodging
        time_difference = time.time() - agent.start
        if time_difference > 2.2 and distance2D(agent.ball, agent.me) <= 270:
            agent.start = time.time()
        elif time_difference <= .1:
            controller_state.jump = True
            controller_state.pitch = -1
        elif time_difference >= .1 and time_difference <= .15:
            controller_state.jump = False
            controller_state.pitch = -1
        elif time_difference > .15 and time_difference < 1:
            controller_state.jump = True
            controller_state.yaw = math.sin(goal_angle)
            controller_state.pitch = -abs(math.cos(goal_angle))

        return controller_state

class fly:
    def __init__(self):
        self.expired = False
    def execute(self, agent):
        return(self.flyController(agent))
    def flyController(self, agent):
        controller_state = SimpleControllerState()
        location = toLocal(agent.ball, agent.me)
        angle_to_target = np.arctan2(location[1], location[0])
        location_of_target = toLocal(agent.ball, agent.me)

        '''steering'''
        if angle_to_target > .1:
            controller_state.steer = 1
            #controller_state.yaw = 1
            controller_state.throttle = 1
            if distance2D(agent.ball, agent.me) < 1000:
                controller_state.boost = True
            
        elif angle_to_target < -.1:
            controller_state.steer = -1
            #controller_state.yaw = -1
            controller_state.throttle = 1
            if distance2D(agent.ball, agent.me) < 1000:
                controller_state.boost = True
            
        else:
            controller_state.steer = controller_state.yaw = 0
            controller_state.throttle = .5
            if angle_to_target < .1 and angle_to_target > -.1:
                controller_state.boost = True
            else: 
                controller_state.boost = False

        #jump
        time_difference = time.time() - agent.start
        if time_difference > 2.2:
            agent.start = time.time()
        elif time_difference < .1 and distance2D(agent.ball, agent.me) < 1000 and agent.ball.location[2] > 100:
            controller_state.jump = True
            print("jump")
        else:
            controller_state.jump = False


        if agent.ball.location[2] > agent.me.location[2] and agent.me.rotation[0] < verticalangle2D(agent.ball.local_location, agent.me) and agent.me.rotation[1] < angle_to_radians(0):#change angle, this is wrong
            controller_state.pitch = 1 # nose up
            
        elif agent.ball.location[2] < agent.me.location[2] and agent.me.rotation[0] > verticalangle2D(agent.ball.local_location, agent.me) and agent.me.rotation[1] > angle_to_radians(0):
            controller_state.pitch = -1 # nose down

        #updated code broke this
        # if(agent.ball.location[2] > agent.me.location[2]):
        #     print("ball above car", verticalangle2D(agent.ball.local_location, agent.me)*180/np.pi)
        # if(agent.ball.location[2] < agent.me.location[2]):
        #     print("ball below car", verticalangle2D(agent.ball.local_location, agent.me)*180/np.pi)
        
    


        return(controller_state)




        

        
        

        
class aerialATBA:
    def __init__(self):
        self.expired = False
    def execute(self, agent):
        controller_state = SimpleControllerState()
        target_speed = velocity2D(agent.ball) + (distance2D(agent.ball, agent.me)/1.5)
        local_pos = toLocal(agent.ball, agent.me)
        # print("location: ", location)
        # print("x-y angle : {}".format(np.arctan2(location[1], location[0])*180/np.pi))
        # print("y-z angle : {}".format(np.arctan2(location[2], location[1])*180/np.pi))
        # print("x-z angle : {} \n".format(np.arctan2(location[2], location[0])*180/np.pi))
        #print(local_pos)
        normed_vector = normalize_vector(agent.ball.local_location)
        #print(normed_vector)
        rotation_axis = np.cross(np.array([1, 0, 0]), normed_vector) 
        angle_to_ball = np.arctan2(agent.ball.local_location[1], agent.ball.local_location[0])
        current_speed = velocity2D(agent.me)
        '''rotation_axis
        [0] is the roll component, which is always 0 here
        [1] is the pitch component
        [2] is the yaw'''


        #steering
        if agent.me.wheel_contact == True: #ground
            if rotation_axis[2] > 0.1:
                controller_state.steer = 1 
            elif rotation_axis[2] < 0.1:
                controller_state.steer = -1
            else:
                controller_state.steer =  0
        else:                             #aerial
            if angle_to_ball > .1:
                #controller_state.steer = controller_state.yaw = clamp(rotation_axis[2]*2.5, -1, 1)
                controller_state.steer = controller_state.yaw = clamp(angle_to_ball, -1, 1)
            elif angle_to_ball < -.1:
                #controller_state.steer = controller_state.yaw = clamp(rotation_axis[2]*2.5, -1, 1)
                controller_state.steer = controller_state.yaw = clamp(angle_to_ball, -1, 1)
            else:
                controller_state.steer = controller_state.yaw = 0

        #throttle
        if(target_speed > current_speed):
            controller_state.throttle = 1
            if(target_speed > 1400 and agent.start > 2.2 and current_speed < 1400): #there might be a problem here with self.start for boosting check later
                controller_state.boost = True
        elif target_speed < current_speed:
            controller_state.throttle = 0
        
        if agent.me.wheel_contact == True and distance2D(agent.ball, agent.me) < 1000:
            controller_state.jump = False
        else:
            controller_state.boost = True
            if rotation_axis[1] < -.1:
                controller_state.pitch = clamp(-angle_to_ball, -1, 1)
            elif rotation_axis[1] > .1:
                controller_state.pitch = clamp(-angle_to_ball, -1, 1)
            else:
                controller_state.pitch = 0
        
        if agent.me.rotation[2] < 0:
            controller_state.roll = .5
        elif agent.me.rotation[2] > 0:
            controller_state.roll = -.5
        else:
            controller_state.roll = 0
        


        return controller_state



class kickoff:
    def __init__(self):
        self.expired = False
    def execute(self, agent):
        controller_state = SimpleControllerState()
        agent.start = time.time()
        controller_state.boost = True

        normed_vector = normalize_vector(agent.ball.local_location)
        rotation_axis = np.cross(np.array([1, 0, 0]), normed_vector)
        dist = distance3D(agent.ball, agent.me)
        #print(steer(dist))
        #steering
        if rotation_axis[2] > .1:
            controller_state.steer = controller_state.yaw = 1 * steer(agent)
            controller_state.boost = False
        elif rotation_axis[2] < -.1:
            controller_state.steer = controller_state.yaw = -1 * steer(agent)
            controller_state.boost = False
        else:
            controller_state.steer = controller_state.yaw = 0
            controller_state.boost = True
        

        return(controller_state)


''' future classes in order of need
class land_on_wheels:
class flick:
class dribble:
'''

class boost_and_turn():
    def __init__(self):
        self.expired = False
    def execute(self, agent):
        controller_state = SimpleControllerState()
        controller_state.throttle = True
        controller_state.boost = True
        controller_state.steer = -1
        return(controller_state)

class drive_and_turn():
    def __init__(self):
        self.expired = False
    def execute(self, agent):
        controller_state = SimpleControllerState()
        controller_state.throttle = True
        controller_state.steer = 1
        return(controller_state)