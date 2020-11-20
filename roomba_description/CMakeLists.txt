cmake_minimum_required(VERSION 2.4.6)
project(roomba_description)
find_package(catkin REQUIRED COMPONENTS
    gazebo_ros
)
include_directories(
    ${catkin_INCLUDE_DIRS}
)
