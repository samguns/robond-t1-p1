import numpy as np
import time


def process_forward_mode(Rover):
    nav_extent = len(Rover.nav_angles)
    if nav_extent < Rover.stop_forward:
        Rover.mode = 'stop'
        return

    if Rover.rock_angle > 0 and Rover.rock_dist <= 1:
        Rover.mode = 'sample'
        return

    if Rover.vel <= Rover.stuck_velocity:
        Rover.stuck_check_count += 1
        if Rover.stuck_check_count >= Rover.stuck_threshold:
            # There's an obstacle prevent Rover moving forward
            Rover.mode = 'stuck'
            return
    else:
        Rover.stuck_check_count = 0

    return


def process_sample_mode(Rover):
    nav_extent = len(Rover.nav_angles)
    if Rover.near_sample == 1:
        Rover.mode = 'stop'
        return

    if nav_extent < Rover.stop_forward:
        Rover.mode = 'stop'
        return

    if Rover.vel <= Rover.stuck_velocity:
        Rover.stuck_check_count += 1
        if Rover.stuck_check_count >= Rover.stuck_threshold:
            # There's an obstacle prevent Rover moving forward
            Rover.mode = 'stuck'
            return
    else:
        Rover.stuck_check_count = 0

    return


def process_stop_mode(Rover):
    nav_extent = len(Rover.nav_angles)
    # If we're in stop mode but still moving keep braking
    if Rover.vel > 0.2:
        Rover.mode = 'stop'
        return

    if Rover.near_sample == 1:
        Rover.mode = 'stop'
        return

    # Now we're stopped and we have vision data to see if there's a path forward
    if nav_extent < Rover.go_forward:
        Rover.mode = 'stuck'
    else:
        Rover.mode = 'forward'

    return


def process_stuck_mode(Rover):
    nav_extent = len(Rover.nav_angles)
    if nav_extent >= Rover.go_forward:
        Rover.mode = 'forward'

    Rover.stuck_check_count = 0
    return


def rover_forward(Rover):
    if Rover.vel < Rover.max_vel:
        Rover.throttle = Rover.throttle_set
    else:
        Rover.throttle = 0

    Rover.brake = 0

    if len(Rover.nav_angles) > 0:
        running_time = time.time() - Rover.start_time
        if running_time > 3:
            anchor_angle = np.mean(Rover.nav_angles * 180 / np.pi)
            Rover.steer = anchor_angle + Rover.angle_offset
        else:
            Rover.steer = 0
    else:
        Rover.steer = 0
    return


def rover_sample(Rover):
    # If we detected a rock ahead of rover's left side,
    # steers it towards the rock sample.
    if Rover.rock_angle > 15:
        Rover.throttle = 0
        Rover.brake = 0
        Rover.steer = 15
        return

    if Rover.vel < Rover.max_approaching_sample_vel:
        Rover.throttle = Rover.sample_throttle_set
        Rover.brake = 0
    else:
        Rover.throttle = 0
        Rover.brake = Rover.sample_brake_set

    Rover.steer = Rover.rock_angle
    return


def rover_stop(Rover):
    Rover.throttle = 0
    Rover.brake = Rover.brake_set
    Rover.steer = 0
    return


def rover_stuck(Rover):
    # There's an obstacle prevent Rover moving forward
    Rover.throttle = 0
    Rover.brake = 0
    # Because the Rover is a kind of left wall-crawler, the simplest
    # strategy here is just stop and turn 15 degree to the right
    Rover.steer = -15
    return


# This is where you can build a decision tree for determining throttle, brake and steer 
# commands based on the output of the perception_step() function
def decision_step(Rover):

    # Implement conditionals to decide what to do given perception data
    # Here you're all set up with some basic functionality but you'll need to
    # improve on this decision tree to do a good job of navigating autonomously!

    # Example:
    # Check if we have vision data to make decisions with
    if Rover.nav_angles is not None:
        # State transition
        if Rover.mode == 'forward':
            process_forward_mode(Rover)
            rover_forward(Rover)
        elif Rover.mode == 'stop':
            process_stop_mode(Rover)
            rover_stop(Rover)
        elif Rover.mode == 'stuck':
            process_stuck_mode(Rover)
            rover_stuck(Rover)
        elif Rover.mode == 'sample':
            process_sample_mode(Rover)
            rover_sample(Rover)

    # Just to make the rover do something 
    # even if no modifications have been made to the code
    else:
        Rover.throttle = Rover.throttle_set
        Rover.steer = 0
        Rover.brake = 0
        
    # If in a state where want to pickup a rock send pickup command
    if Rover.near_sample and Rover.vel == 0 and not Rover.picking_up:
        Rover.send_pickup = True
    
    return Rover

