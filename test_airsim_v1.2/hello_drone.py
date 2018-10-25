"""
For connecting to the AirSim drone environment and testing API functionality
"""
from __future__ import absolute_import, division, print_function, unicode_literals

import setup_path 
import airsim

import numpy as np
import os
import tempfile
import pprint

import sys
import math
from airsim import Vector3r

g_drone_id = 0
g_image_id = 1
# g_image_folder = 'G:\\my_github\\AirSim\\Unreal\\Environments\\Blocks\\my_img\\'
# g_image_folder = 'G:\\my_github\\myAirsimProject\\CityEnviron\\image\\'
g_image_folder = 'D:\\airsim\\randomstuff-master\\mytest\\PythonClient_1.0\\img\\'

def mylog(msg):
    print('[drone_{}] {}'.format(g_drone_id, msg))

def mylog_screen():
    # TODO: fix this 
    global g_drone_id, g_image_id, g_image_folder
    # get camera images from the car
    responses = client.simGetImages([
        ImageRequest(0, AirSimImageType.DepthVis, pixels_as_float=True),  # center front, depth visualiztion image
        ImageRequest(0, AirSimImageType.Scene), # center front, scene vision image in png format
    ])
    mylog('Retrieved images: %d' % len(responses))

    tmp_dir = g_image_folder + 'drone_{}\\'.format(g_drone_id)
    mylog ("Saving images to %s" % tmp_dir)
    if not os.path.isdir(tmp_dir):
        try:
            os.makedirs(tmp_dir)
        except OSError:
            raise
    filename_prefix = tmp_dir + "{}-".format(g_image_id)
    g_image_id += 1
    for idx, response in enumerate(responses):
        filename = filename_prefix + str(idx)
        if response.pixels_as_float:
            mylog("Type %d, size %d" % (response.image_type, len(response.image_data_float)))
            AirSimClientBase.write_pfm(os.path.normpath(filename + '.pfm'), AirSimClientBase.getPfmArray(response))
        elif response.compress: #png format
            mylog("Type %d, size %d" % (response.image_type, len(response.image_data_uint8)))
            AirSimClientBase.write_file(os.path.normpath(filename + '.png'), response.image_data_uint8)
            #### send to forwarder
            # TODO: clean this
            with open(os.path.normpath(filename + '.png'), 'r') as fd:
                myrpcclient = msgpackrpc.Client(msgpackrpc.Address('192.168.56.102', 18800))
                result = myrpcclient.call('send', time.time(), response.image_data_uint8)
                print('image sent to forwarder: {}'.format(result))
        else: #uncompressed array
            mylog("Type %d, size %d" % (response.image_type, len(response.image_data_uint8)))
            img1d = np.fromstring(response.image_data_uint8, dtype=np.uint8) #get numpy array
            img_rgba = img1d.reshape(response.height, response.width, 4) #reshape array to 4 channel image array H X W X 4
            img_rgba = np.flipud(img_rgba) #original image is fliped vertically
            img_rgba[:,:,1:2] = 100 #just for fun add little bit of green in all pixels
            AirSimClientBase.write_png(os.path.normpath(filename + '.greener.png'), img_rgba) #write to png



def degreesToRadians(degrees):
    return math.pi * degrees / 180.0

def GeodeticToNedFast(geo, home):
    d_lat = geo.latitude - home.latitude;
    d_lon = geo.longitude - home.longitude;
    d_alt = home.altitude - geo.altitude;
    EARTH_RADIUS = 6378137.0
    x = degreesToRadians(d_lat) * EARTH_RADIUS
    y = degreesToRadians(d_lon) * EARTH_RADIUS * math.cos(degreesToRadians(geo.latitude))
    return Vector3r(x, y, d_alt)

def nedToGeodeticFast(local, home):
    d_lat = local.x_val / EARTH_RADIUS;
    d_lon = local.y_val / (EARTH_RADIUS * math.cos(degreesToRadians(home.latitude)));
    latitude = home.latitude + radiansToDegrees(d_lat);
    longitude = home.longitude + radiansToDegrees(d_lon);
    altitude = home.altitude - local.z_val;
    return GeoPoint(latitude,longitude,altitude)

def getCalibratedPos(pos, ref):
    return Vector3r(pos.x_val - ref.x_val, pos.y_val - ref.y_val, pos.z_val - ref.z_val)

def getCalibratedPosFromGps(gps, home, ref):
    pos = GeodeticToNedFast(gps, home)
    return Vector3r(pos.x_val - ref.x_val, pos.y_val - ref.y_val, pos.z_val - ref.z_val)


def degree2Radius(degree):
    return degree / 360 * 2 * math.pi

########################
# connect drone
########################
argc = len(sys.argv)
if argc < 1:
    mylog('usage: python _hello_drone.py {Drone1 | Drone2}')
    exit(0)
drone_name = (sys.argv[1])
# connect to the AirSim simulator
# ip = "127.0.0.1"
# port = 41451 + g_drone_id

# connect to the AirSim simulator
client = airsim.MultirotorClient()
client.confirmConnection()
client.enableApiControl(True, drone_name)
client.armDisarm(True, drone_name)

multirotor_state = client.getMultirotorState(vehicle_name=drone_name)
print('multirotor_state={}'.format(multirotor_state))

landed = multirotor_state.landed_state
if landed == airsim.LandedState.Landed:
    print("taking off...")
    client.takeoffAsync(vehicle_name=drone_name).join()
else:
    print("already flying...")
    client.hoverAsync(vehicle_name=drone_name).join()

# client.getGpsLocation()
home_gps_location = client.getMultirotorState(vehicle_name=drone_name).gps_location
pos = GeodeticToNedFast(home_gps_location, home_gps_location)
print('gps={}, pos={}'.format(home_gps_location, pos))

# client.getPosition()
kinematics_state = client.simGetGroundTruthKinematics(vehicle_name=drone_name)
print(kinematics_state)
cur_pos_vector3r = kinematics_state.position
cur_pos = (cur_pos_vector3r.x_val, cur_pos_vector3r.y_val, cur_pos_vector3r.z_val)
origin_pos = cur_pos
cur_yaw = 0

while True:
    scale = 1
    pressed_key = airsim.wait_key(
        'Press AWSD,R(up)F(down)QE(turn right/left) key to move vehicle {}m at {}m/s.\n'.format(scale, scale)
        + 'Press P to take images.\n'
        + 'Press B key to reset to original state.\n'
        + 'Press O key to release API control.\n'
    )
    pressed_key = pressed_key.decode('utf-8')
    pressed_key = pressed_key.lower()
    mylog("pressed_key={}".format(pressed_key))
    if pressed_key == 'p':
        mylog_screen()
    elif pressed_key == 'o':
        client.enableApiControl(False, drone_name)
        break
    elif pressed_key == 'b':
        client.reset()
    else:
        move_x, move_y, move_z, speed = 0, 0, 0, 1
        speed = speed*scale
        if pressed_key == 'a':
            move_y = -1*scale
        elif pressed_key == 'd':
            move_y = +1*scale
        elif pressed_key == 'w':
            move_x = +1*scale
        elif pressed_key == 's':
            move_x = -1*scale
        elif pressed_key == 'r':
            move_z = -1*scale
        elif pressed_key == 'f':
            move_z = +1*scale
        elif pressed_key == 'q':
            cur_yaw -= 30
            move_x = +1*scale
        elif pressed_key == 'e':
            cur_yaw += 30
            move_x = +1*scale

        # compute current angle
        if move_x:
            dx = move_x * math.cos(degree2Radius(cur_yaw))
            dy = move_x * math.sin(degree2Radius(cur_yaw))
            dz = move_z
        if move_y:
            dx = move_y * math.cos(degree2Radius(cur_yaw + 90))
            dy = move_y * math.sin(degree2Radius(cur_yaw + 90))
            dz = move_z
        cur_state = client.getMultirotorState(vehicle_name=drone_name)
        cur_pos = cur_state.kinematics_estimated.position
        print("{},{} => {},{}".format(move_x, move_y, dx, dy))

        next_pos = Vector3r(cur_pos.x_val + dx, cur_pos.y_val + dy, cur_pos.z_val + dz)
        mylog("try to move: {} -> {}".format(cur_pos, next_pos))
        # rc = client.moveByVelocityAsync(
        #     dx, dy, dz, 1,
        #     yaw_mode=airsim.YawMode(is_rate=False, yaw_or_rate=cur_yaw),
        #     vehicle_name=drone_name).join()
        rc = client.moveToPositionAsync(
            next_pos.x_val, next_pos.y_val, next_pos.z_val, speed,
            yaw_mode=airsim.YawMode(is_rate=False, yaw_or_rate=cur_yaw), 
            drivetrain=airsim.DrivetrainType.MaxDegreeOfFreedom,
            vehicle_name=drone_name)
        mylog("rc: {}".format(rc))
        
        ##########################
        # move in mininet
        ##########################
        if False:
            mylog("move nodes in mininet")
            rel_x, rel_y, rel_z = (
                origin_pos[0] - next_pos[0], 
                origin_pos[1] - next_pos[1], 
                origin_pos[2] - next_pos[2])
            myrpcclient = msgpackrpc.Client(msgpackrpc.Address('192.168.56.102', 19000))
            myrpcclient.call('move', time.time(), rel_x, rel_y, rel_z, speed)
        else:
            mylog("airsim only mode. skip mininet code section")
        
        # is collision?
        collision_info = client.simGetCollisionInfo(vehicle_name=drone_name)
        if collision_info.has_collided:
            mylog("Collision at pos %s, normal %s, impact pt %s, penetration %f, name %s, obj id %d" % (
                pprint.pformat(collision_info.position), 
                pprint.pformat(collision_info.normal), 
                pprint.pformat(collision_info.impact_point), 
                collision_info.penetration_depth, collision_info.object_name, collision_info.object_id))
            break

        cur_pos_vector3r = client.simGetGroundTruthKinematics(vehicle_name=drone_name).position 
        print('cur_pos_vector3r={}'.format(cur_pos_vector3r))
        cur_state = client.getMultirotorState(vehicle_name=drone_name)
        print('state={}'.format(cur_state))


