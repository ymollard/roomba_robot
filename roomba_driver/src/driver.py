#!/usr/bin/env python
import rospy
from pyroombaadapter import PyRoombaAdapter
from roomba_msgs.msg import Battery, BumperEvent, ButtonEvent, CliffEvent, InfraRedEvent, WheelDropEvent, Brush, SetLeds, PlaySong, SevenSegmentDisplay
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Range


class RoombaDriverNode(object):
    def __init__(self):
        self.rate = rospy.Rate(66)   # Robot updates data every 15ms

        # Robot customization
        self.port = rospy.get_param("port", "/dev/ttyUSB0")
        self.use_bumpers = rospy.get_param("use_bumpers", False)
        self.use_cliff_sensors = rospy.get_param("use_cliff_sensors", False)
        self.use_ir_receiver = rospy.get_param("use_ir_receiver", False)
        self.use_wheel_drops = rospy.get_param("use_wheel_drops", False)
        self.use_ir_sensors = rospy.get_param("use_ir_sensors", False)
        self.use_brushes = rospy.get_param("use_brushes", False)
        self.use_leds = rospy.get_param("use_leds", False)
        self.use_songs = rospy.get_param("use_songs", False)
        self.use_seven_segment_display = rospy.get_param("use_seven_segment_display", False)

        # Publishers
        self.pub_battery = rospy.Publisher("battery", Battery, queue_size=10)
        self.pub_odom = rospy.Publisher("odom", Odometry, queue_size=10)
        self.pub_bumpers = rospy.Publisher("bumpers", BumperEvent, queue_size=10)
        self.pub_buttons = rospy.Publisher("buttons", Battery, queue_size=10)
        if self.use_cliff_sensors: self.pub_cliff = rospy.Publisher("cliff", CliffEvent, queue_size=10)
        if self.use_ir_receiver: self.pub_ir = rospy.Publisher("ir_receivers", InfraRedEvent, queue_size=10)
        if self.use_wheel_drops: self.pub_wheel_drops = rospy.Publisher("wheel_drops", WheelDropEvent, queue_size=10)
        if self.use_ir_sensors: self.pub_range = rospy.Publisher("range", Range, queue_size=10)
        if self.use_brushes: self.pub_brushes = rospy.Publisher("brushes", Brush, queue_size=10)
        if self.use_leds: self.pub_leds = rospy.Publisher("leds", SetLeds, queue_size=10)
        if self.use_songs: self.pub_song = rospy.Publisher("play_song", PlaySong, queue_size=10)
        if self.use_seven_segment_display: self.pub_seven_seg_display = rospy.Publisher("seven_segment_display", SevenSegmentDisplay, queue_size=10)

        # Subscribers
        rospy.Subscriber("cmd_vel", Twist, self.cb_cmd_vel)


    def connect(self):
        self.adapter = PyRoombaAdapter(self.port)

    def publish(self):
        sensors = self.adapter.sensors()
        now = rospy.Time.now()

        battery = Battery(stamp=now)
        battery.state = Battery.CORD if sensors["Charging State"] == 1 else Battery.DOCK if sensors["Charging State"] == 2 else Battery.NOT_CHARGING
        battery.level = 100*sensors["Battery Charge"]/sensors["Battery Capacity"]
        #battery.time_remaining = rospy.Duration(battery.level/(last_charge-))
        self.pub_battery.publish(battery)

        if self.use_cliff_sensors: self.pub_cliff.publish(CliffEvent())
        if self.use_ir_receiver: self.pub_ir.publish()
        if self.use_wheel_drops: self.pub_wheel_drops.publish()
        if self.use_ir_sensors: self.pub_range.publish()
        if self.use_brushes: self.pub_brushes.publish()
        if self.use_leds: self.pub_leds.publish()
        if self.use_songs: self.pub_song.publish()
        if self.use_seven_segment_display: self.pub_seven_seg_display.publish()
            

    def run(self):
        while not rospy.is_shutdown():
            self.publish()
            self.rate.sleep()

if __name__ == "__main__":
    rospy.init_node("roomba_driver")
    node = RoombaDriverNode()
    node.run()