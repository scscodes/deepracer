import math


def reward_function(params):
    # AWS DEFAULT PARAMS #
    all_wheels_on_track = params['all_wheels_on_track']
    x = params['x']
    y = params['y']
    distance_from_center = params['distance_from_center']
    is_left_of_center = params['is_left_of_center']
    heading = params['heading']
    progress = params['progress']
    steps = params['steps']
    speed = params['speed']
    steering_angle = params['steering_angle']
    track_width = params['track_width']
    waypoints = params['waypoints']
    closest_waypoints = params['closest_waypoints']
    is_offtrack = params['is_offtrack']
    is_crashed = params['is_crashed']
    is_reversed = params['is_reversed']

    # BASE REWARD #
    reward = 1.00

    # VARIABLES #
    direction_threshold = 10.0  # max acceptable diff, agent heading and track direction
    abs_steering_threshold = 20.0  # max acceptable yaw/steering value

    # HELPER FUNCTIONS #
    def _calc_heading_diff():
        # aws sample; return diff between track and agent heading
        next_point = waypoints[closest_waypoints[1]]
        prev_point = waypoints[closest_waypoints[0]]
        track_direction = math.atan2(next_point[1] - prev_point[1], next_point[0] - prev_point[0])
        track_direction = math.degrees(track_direction)
        direction_diff = abs(track_direction - heading)
        # normalize the output
        if direction_diff > 180:
            direction_diff = 360 - direction_diff
        return direction_diff

    # APPLIED REWARDS & PENALTIES #

    # orientation; penalize excessive yaw values
    if abs(steering_angle) > abs_steering_threshold:
        reward *= 0.80

    # orientation; penalize excessive heading differential
    if _calc_heading_diff() > direction_threshold:
        reward *= 0.80

    # velocity; maintain acceptable speed range
    if 1.00 < speed <= 2.00:
        reward *= 1.5
    else:
        reward *= 0.80

    # penalize clearly undesirable behavior
    if is_crashed or is_offtrack or is_reversed:
        reward = 1e-3

    return float(reward)