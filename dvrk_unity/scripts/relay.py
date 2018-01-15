#!/usr/bin/env python
import rospy
from sensor_msgs.msg import JointState
from rospy_message_converter import json_message_converter
import pprint
import json
import socket
import sys


if len(sys.argv) < 2:
    print("usage: relay.py ARM IP PORT")
    sys.exit()

ARM = sys.argv[1]

UDP_IP = "10.162.34.70" if len(sys.argv) < 3 else sys.argv[2]
UDP_PORT = 8051 if len(sys.argv) < 4 else int(sys.argv[3])

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.connect((UDP_IP, UDP_PORT))

def callback(data):
    json_str = json_message_converter.convert_ros_message_to_json(data)
    sock.send(json_str)
    json_obj = json.loads(json_str)
    pprint.pprint(json_obj)

    # rospy.loginfo(rospy.get_caller_id() + "I heard\n %s", json_str)

def shutdown_callback():
    sock.close()
    print("shutdown")
    
def listener():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # node are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('listener', anonymous=True)
    rospy.on_shutdown(shutdown_callback)

    rospy.Subscriber("/dvrk/" + ARM + "/joint_states", JointState, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()


listener()
