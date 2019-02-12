from rlbot.utils.game_state_util import GameState, BallState, CarState, Physics, Vector3, Rotator
from States import *
import numpy as np
import time

def live_no_test(agent):
    return

def kickoff_test(agent):
    agent.state = kickoff()
    test_time = time.time() - agent.test_start
    if(test_time > 5):
        car_state = CarState(
            jumped=False, 
            double_jumped=False, 
            boost_amount=87, 
            physics=Physics(location=Vector3(x=100,y=3000,z=0),
                            velocity=Vector3(x=0, y=0, z=0), 
                            rotation=Rotator(np.pi, np.pi / 2, np.pi), 
                            angular_velocity=Vector3(x=0, y=0, z=0)))
        
        ball_state = BallState(
            physics=Physics(location=Vector3(x=0,y=0,z=0),
                            velocity=Vector3(x=0, y=0, z=0), 
                            rotation=Rotator(np.pi / 2, 0, 0), 
                            angular_velocity=Vector3(x=0, y=0, z=0)))

        game_state = GameState(ball=ball_state, cars={agent.index: car_state})

        agent.set_game_state(game_state)
        agent.test_start = time.time()
    else:
        return

def atba_test(agent):
    agent.state = atba()
    test_time = time.time() - agent.test_start
    if(test_time > 30):
        car_state = CarState(
            jumped=False, 
            double_jumped=False, 
            boost_amount=87, 
            physics=Physics(location=Vector3(x=1000,y=3000,z=0),
                            velocity=Vector3(x=0, y=0, z=0), 
                            rotation=Rotator(np.pi, np.pi / 2, np.pi), 
                            angular_velocity=Vector3(x=0, y=0, z=0)))
        
        ball_state = BallState(
            physics=Physics(location=Vector3(x=0,y=0,z=0),
                            velocity=Vector3(x=0, y=0, z=0), 
                            rotation=Rotator(np.pi / 2, 0, 0), 
                            angular_velocity=Vector3(x=0, y=0, z=0)))

        game_state = GameState(ball=ball_state, cars={agent.index: car_state})

        agent.set_game_state(game_state)
        agent.test_start = time.time()
    else:
        return

def aerialATBA_test(agent):
    agent.state = aerialATBA()
    test_time = time.time() - agent.test_start
    if(test_time > 20):
        car_state = CarState(
            jumped=False, 
            double_jumped=False, 
            boost_amount=87, 
            physics=Physics(location=Vector3(x=0,y=3000,z=0),
                            velocity=Vector3(x=0, y=0, z=0), 
                            rotation=Rotator(np.pi, np.pi / 2, np.pi), 
                            angular_velocity=Vector3(x=0, y=0, z=0)))
        ball_state = BallState(
            physics=Physics(location=Vector3(x=0,y=0,z=500),
                            velocity=Vector3(x=0, y=0, z=0), 
                            rotation=Rotator(np.pi / 2, 0, 0), 
                            angular_velocity=Vector3(x=0, y=0, z=0)))

        game_state = GameState(ball=ball_state, cars={agent.index: car_state})

        agent.set_game_state(game_state)
        agent.test_start = time.time()
    # else:
    #     ball_state = BallState(
    #         physics=Physics(location=Vector3(x=0,y=0,z=500),
    #                         velocity=Vector3(x=0, y=0, z=0), 
    #                         rotation=Rotator(np.pi / 2, 0, 0), 
    #                         angular_velocity=Vector3(x=0, y=0, z=0)))
    #     game_state = GameState(ball=ball_state)
    #     agent.set_game_state(game_state)
        

        
        return


def boost_and_turn_test(agent):
    agent.state = boost_and_turn()
    test_time = time.time() - agent.test_start
    if(test_time > 6):
        car_state = CarState(
            jumped=False, 
            double_jumped=False, 
            boost_amount=87, 
            physics=Physics(location=Vector3(x=-1000,y=2000,z=0),
                            velocity=Vector3(x=0, y=0, z=0), 
                            rotation=Rotator(np.pi, np.pi / 2, np.pi), 
                            angular_velocity=Vector3(x=0, y=0, z=0)))
        
        ball_state = BallState(
            physics=Physics(location=Vector3(x=0,y=4000,z=0),
                            velocity=Vector3(x=0, y=0, z=0), 
                            rotation=Rotator(np.pi / 2, 0, 0), 
                            angular_velocity=Vector3(x=0, y=0, z=0)))

        game_state = GameState(ball=ball_state, cars={agent.index: car_state})

        agent.set_game_state(game_state)
        agent.test_start = time.time()
    else:
        return