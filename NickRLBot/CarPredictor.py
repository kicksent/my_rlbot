    
#Car Predictor
from Util import *
from rlbot.agents.base_agent import BaseAgent, SimpleControllerState
class CarPredictor:
    def __init__(self):
        self.time_step = 1/60

    def get_car_prediction(self, agent, time_length):


        return self.curved_line_prediction(agent, time_length)

    
    ''' creates an array of predicted positions for a straight line 
    TO DO: 
        -check to see if velocity > MAX_CAR_SPEED if boost is on
    '''
    def straight_line_prediction(self, agent, time_length):
        car_path = []
        velocity = np.array([
            agent.me.velocity[0], 
            agent.me.velocity[1],
            0 if agent.me.wheel_contact == True and np.abs(agent.me.velocity[2]) < .2 else agent.me.velocity[2] 
        ])

        acceleration = agent.me.acceleration / 60
        initial_slice = Slice(agent.me.location, agent.time, velocity, agent.me.matrix, acceleration)
        car_path.append(initial_slice)
        cur_slice = initial_slice
        time_so_far = 0
        while(time_so_far < time_length):
            next_vel = cur_slice.velocity
            if(agent.me.acceleration.all() != 0):
                next_vel += acceleration / 60
            pos = cur_slice.position + next_vel / 60 
           
            if(cur_slice.position[2] > OCTANE_ELEVATION):
                next_vel = np.array([next_vel[0], next_vel[1], next_vel[2] - GRAVITY * self.time_step])
            else:
                next_vel = np.array([next_vel[0], next_vel[1], 0])
            
            #check if velocity estimate is greater than MAX_SPEED and correct it
            if(np.linalg.norm(next_vel) > MAX_CAR_SPEED):
                next_vel = normalize_vector(velocity) * MAX_CAR_SPEED

            next_slice = Slice(pos, agent.time + time_so_far, next_vel, cur_slice.orientation, acceleration)
            car_path.append(next_slice)

            time_so_far += self.time_step
            cur_slice = next_slice
        
        return car_path

    def curved_line_prediction(self, agent, time_length):
        car_path = []
        velocity = np.array([
            agent.me.velocity[0], 
            agent.me.velocity[1],
            0 if agent.me.wheel_contact == True and np.abs(agent.me.velocity[2]) < .2 else agent.me.velocity[2] 
        ])
        rvelocity_ground = agent.me.rvelocity
        acceleration = agent.me.acceleration / 60
        initial_slice = Slice(agent.me.location, agent.time, velocity, agent.me.matrix, acceleration)
        car_path.append(initial_slice)
        cur_slice = initial_slice
        time_so_far = 0
        while(time_so_far < time_length):
            next_vel = cur_slice.velocity
            if(agent.me.acceleration.all() != 0):
                next_vel += acceleration / 60
            pos = cur_slice.position

            # TO DO : rotate vector by theta if turning
            if(agent.me.wheel_contact == True):
                #print(agent.me.acceleration[2])
                turned_vector = RotateVector2d(next_vel, rvelocity_ground[2]/60)
                #print(pos[0], pos[1], turned_vector[0], turned_vector[1])
                next_vel[0] = turned_vector[0]
                next_vel[1] = turned_vector[1]
                #print(pos[0], pos[1])
                
                #next_vel[2] = 0
            pos += next_vel / 60
            #print(pos)
            
            if(cur_slice.position[2] > OCTANE_ELEVATION):
                next_vel = np.array([next_vel[0], next_vel[1], next_vel[2] - GRAVITY * self.time_step])
            else:
                next_vel = np.array([next_vel[0], next_vel[1], 0])
            
            #check if velocity estimate is greater than MAX_SPEED and correct it
            # if(np.linalg.norm(next_vel) > MAX_CAR_SPEED):
            #     next_vel = normalize_vector(velocity) * MAX_CAR_SPEED

            next_slice = Slice(np.array(pos, copy=True), agent.time + time_so_far, next_vel, cur_slice.orientation, acceleration)
            car_path.append(next_slice)

            time_so_far += self.time_step
            cur_slice = next_slice
        
        return car_path


class Slice:
    def __init__(self, position, time, velocity, orientation, acceleration):
        self.position = position
        self.time = time
        self.velocity = velocity
        self.orientation = orientation
        self.acceleration = acceleration
    def get_slice(self):
        return([self.position, self.time, self.velocity, self.orientation])
