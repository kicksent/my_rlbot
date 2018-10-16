


from rlbot.agents.base_agent import BaseAgent, SimpleControllerState
from rlbot.utils.structures.game_data_struct import GameTickPacket
#from Utilities.Simulation import *
from Utilities.LinearAlgebra import vec3, dot, euler_rotation
from Utilities.Simulation import Ball, Car
from Utilities.LinearAlgebra import vec3
from Util import *
from States import *
import numpy as np
import time
import math
from rlbot.utils.game_state_util import GameState, BallState, CarState
from GameStateTesting import *

class obj:
    def __init__(self):
        self.location = np.array([0,0,0])
        self.velocity = np.array([0,0,0])
        self.rotation = np.array([0,0,0]) # pitch, yaw, roll
        self.rvelocity = np.array([0,0,0]) 
        self.local_location = np.array([0,0,0])
        self.boost = 0
        self.matrix = None
        self.wheel_contact = False
        self.jumped = False
        self.double_jumped = False

class kicksent(BaseAgent):

    def initialize_agent(self):
        # This runs once before the bot starts up
        self.controller_state = SimpleControllerState()
        self.me = obj()
        self.ball = obj()
        self.players = []
        self.start = time.time()
        self.state = shot()
        self.ball_prediction = None
        self.game_state = GameState()
        self.ball_state = BallState()
        self.car_state = CarState()
        self.test_num = 1 #set to 0 for no testing
        self.test_start = time.time()
        self.time_to_target = 1 #use this to update renderer
    
    def test_state(self, test_num):
        options = { 
            0 : live_no_test,
            1 : kickoff_test,
            2 : ATBA_test,
            3 : aerialATBA_test
        }
        options[test_num](self)
        

    def get_output(self, packet: GameTickPacket) -> SimpleControllerState:
        #preprocess the data from the packet
        self.preprocess(packet)
        #run test scenario, set self.test_num to 0 for no test scenarios
        self.test_state(self.test_num)
        #render, must be called between begin and end, only call once each!
        self.renderer.begin_rendering()
        self.render_ball_line_prediction()
        self.render_target_location()
        self.renderer.end_rendering()

        return self.state.execute(self)


    def preprocess(self,game):
        #car data processing
        self.players = []
        car = game.game_cars[self.index]
        self.me.location = np.array([car.physics.location.x, car.physics.location.y, car.physics.location.z])
        self.me.velocity = np.array([car.physics.velocity.x, car.physics.velocity.y, car.physics.velocity.z])
        self.me.rotation = np.array([car.physics.rotation.pitch, car.physics.rotation.yaw, car.physics.rotation.roll])
        self.me.rvelocity = np.array([car.physics.angular_velocity.x, car.physics.angular_velocity.y, car.physics.angular_velocity.z])
        self.me.matrix = get_orientation_matrix(self.me)
        self.me.boost = car.boost
        self.me.wheel_contact = car.has_wheel_contact
        self.me.jumped = car.jumped
        self.me.double_jumped = car.double_jumped

        #ball data processing
        ball = game.game_ball.physics
        self.ball.location = np.array([ball.location.x, ball.location.y, ball.location.z])
        self.ball.velocity = np.array([ball.velocity.x, ball.velocity.y, ball.velocity.z])
        self.ball.rotation = np.array([ball.rotation.pitch, ball.rotation.yaw, ball.rotation.roll])
        self.ball.rvelocity = np.array([ball.angular_velocity.x, ball.angular_velocity.y, ball.angular_velocity.z])

        self.ball.local_location = to_local(self.ball, self.me)

        #collects info for all other cars in match, updates objects in self.players accordingly
        for i in range(game.num_cars):
            if i != self.index:
                car = game.game_cars[i]
                temp = obj()
                temp.index = i
                temp.team = car.team
                temp.location.data = np.array([car.physics.location.x, car.physics.location.y, car.physics.location.z])
                temp.velocity.data = np.array([car.physics.velocity.x, car.physics.velocity.y, car.physics.velocity.z])
                temp.rotation.data = np.array([car.physics.rotation.pitch, car.physics.rotation.yaw, car.physics.rotation.roll])
                temp.rvelocity.data = np.array([car.physics.angular_velocity.x, car.physics.angular_velocity.y, car.physics.angular_velocity.z])
                temp.boost = car.boost
                flag = False
                for item in self.players:
                    if item.index == i:
                        item = temp
                        flag = True
                        break
                if not flag:
                    self.players.append(temp)

    def render_ball_line_prediction(self):
        ''' Get ball predictions '''
        self.ball_prediction = self.get_ball_prediction_struct()

        # if ball_prediction is not None:
        #     for i in range(0, ball_prediction.num_slices):
        #         prediction_slice = ball_prediction.slices[i]
        #         self.logger.info("At time {}, the ball will be at ({}, {}, {})".
        #             format(prediction_slice.game_seconds, prediction_slice.physics.location.x, prediction_slice.physics.location.y, prediction_slice.physics.location.z))
        '''Render Line Prediction'''
        
        for i in range(200):
            self.renderer.draw_line_3d(
                [self.ball_prediction.slices[i].physics.location.x, 
                self.ball_prediction.slices[i].physics.location.y, 
                self.ball_prediction.slices[i].physics.location.z], 
                [self.ball_prediction.slices[i+1].physics.location.x, 
                self.ball_prediction.slices[i+1].physics.location.y, 
                self.ball_prediction.slices[i+1].physics.location.z], 
                self.renderer.create_color(255,255,0,255))
                
        

    def render_target_location(self):
        # if(time > 3):
        #     return
        # else:
        i = int(np.floor(self.time_to_target * 60))
        #print("i = ", i)
        if(i >= 360):
            print("You cannot create a target more than 3 seconds in the future.")
            return
        line_length = 50
        alpha = 255
        r=255
        g=0
        b=0
        self.renderer.draw_line_3d(
            [self.ball_prediction.slices[i].physics.location.x+line_length, 
            self.ball_prediction.slices[i].physics.location.y, 
            self.ball_prediction.slices[i].physics.location.z], 
            [self.ball_prediction.slices[i].physics.location.x-line_length, 
            self.ball_prediction.slices[i].physics.location.y, 
            self.ball_prediction.slices[i].physics.location.z], 
                self.renderer.create_color(alpha,r,g,b))
        self.renderer.draw_line_3d(
            [self.ball_prediction.slices[i].physics.location.x, 
            self.ball_prediction.slices[i].physics.location.y+line_length, 
            self.ball_prediction.slices[i].physics.location.z], 
            [self.ball_prediction.slices[i].physics.location.x, 
            self.ball_prediction.slices[i].physics.location.y-line_length, 
            self.ball_prediction.slices[i].physics.location.z], 
            self.renderer.create_color(alpha,r,g,b))
        self.renderer.draw_line_3d(
            [self.ball_prediction.slices[i].physics.location.x, 
            self.ball_prediction.slices[i].physics.location.y, 
            self.ball_prediction.slices[i].physics.location.z+line_length], 
            [self.ball_prediction.slices[i].physics.location.x, 
            self.ball_prediction.slices[i].physics.location.y, 
            self.ball_prediction.slices[i].physics.location.z-line_length], 
            self.renderer.create_color(alpha,r,g,b))
        self.renderer.draw_line_3d(
            [self.ball_prediction.slices[i].physics.location.x+line_length, 
            self.ball_prediction.slices[i].physics.location.y+line_length, 
            self.ball_prediction.slices[i].physics.location.z], 
            [self.ball_prediction.slices[i].physics.location.x-line_length, 
            self.ball_prediction.slices[i].physics.location.y-line_length, 
            self.ball_prediction.slices[i].physics.location.z], 
            self.renderer.create_color(alpha,r,g,b))
        self.renderer.draw_line_3d(
            [self.ball_prediction.slices[i].physics.location.x, 
            self.ball_prediction.slices[i].physics.location.y+line_length, 
            self.ball_prediction.slices[i].physics.location.z+line_length], 
            [self.ball_prediction.slices[i].physics.location.x, 
            self.ball_prediction.slices[i].physics.location.y-line_length, 
            self.ball_prediction.slices[i].physics.location.z-line_length], 
            self.renderer.create_color(alpha,r,g,b))
        self.renderer.draw_line_3d(
            [self.ball_prediction.slices[i].physics.location.x+line_length, 
            self.ball_prediction.slices[i].physics.location.y, 
            self.ball_prediction.slices[i].physics.location.z+line_length], 
            [self.ball_prediction.slices[i].physics.location.x-line_length, 
            self.ball_prediction.slices[i].physics.location.y, 
            self.ball_prediction.slices[i].physics.location.z-line_length], 
            self.renderer.create_color(alpha,r,g,b))
        







        # d = 10 #dimension of rect 
        # self.renderer.draw_rect_3d(
        #     translate_points3D([self.ball_prediction.slices[i].physics.location.x, 
        #         self.ball_prediction.slices[i].physics.location.y, 
        #         self.ball_prediction.slices[i].physics.location.z], self, -d/2, 0, d/2), 
        #     d, d, True, self.renderer.black())
        
            
        



    
 

    


