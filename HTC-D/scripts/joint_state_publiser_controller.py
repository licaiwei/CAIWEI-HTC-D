#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
joint_state_publiser_controller.py - 订阅 sensor_msgs.msg.JointState 类型的 /Shadow_Hand/AD_value topic，
转换成对应的关节角度（简单的线性映射）；读取参数服务器中的： AD-name 和 关节限位

@Created on MAY 1 2021
@author:菜伟
@email:li_wei_96@163.com
"""
import serial
import rospy
from sensor_msgs.msg import JointState
#from Kalman_Filter import KalmanFilter
import numpy as np
import sys

Joint_Name_ID = {}         # 字典{"ADx":joint name,}  将yaml定义从参数服务器读取出来
Joint_Name_Scale = {}         # 字典{"joint name":[ rate, offset],}  线性关系，直线点斜式

if __name__ == "__main__":
    #
    # 创建句柄
    rospy.init_node('hand_joint_states_publisher', anonymous=True)
    pub_hand_joint_states = rospy.Publisher("/Shadow_Hand/controller_joint_states", JointState, queue_size=5)  # 发布AD值
    rospy.sleep(1)

    #
    # 在参数服务器中，加载YAML文建定义的： 关节名称 --- id
    param_list = rospy.get_param_names()
    for param in param_list:
        if "/hand_joint_id_list/" in param:
            Joint_Name_ID[param.replace(
                "/hand_joint_id_list/", "")] = rospy.get_param(param)
    if len(Joint_Name_ID) == 0:
        rospy.INFO("Yaml configuration file not loaded")
        exit(1)
    #print(Joint_Name_ID)

    #
    # 在参数服务器中，加载YAML文建定义的： 关节名称 关节 AD限位；得到关节值的与AD值的线性系数
    for ADx in Joint_Name_ID:
        AD_p1 = rospy.get_param("/shadow_hand_joint_limit/" + Joint_Name_ID[ADx] + "/AD/p1")
        AD_p2 = rospy.get_param("/shadow_hand_joint_limit/" + Joint_Name_ID[ADx] + "/AD/p2")
        Angle_p1 = rospy.get_param("/shadow_hand_joint_limit/" + Joint_Name_ID[ADx] + "/Angle/p1")
        Angle_p2 = rospy.get_param("/shadow_hand_joint_limit/" + Joint_Name_ID[ADx] + "/Angle/p2")
        
        rate = (Angle_p2-Angle_p1)/(AD_p2-AD_p1)
        off_set = Angle_p1-rate*AD_p1
        Joint_Name_Scale[ Joint_Name_ID[ADx] ] = [rate, off_set, Angle_p1, Angle_p2] 

    if len(Joint_Name_Scale) == 0:
        rospy.INFO("Yaml joint limited configuration file not loaded")
        exit(1)

    AD_value = rospy.wait_for_message("/Shadow_Hand/AD_value", JointState)
    hand_joint_states = JointState()
    for i in range(0, len(AD_value.name)):
        joint_name = Joint_Name_ID[ AD_value.name[i] ] # 设置关节名称
        hand_joint_states.name.append( joint_name)
        hand_joint_states.velocity.append(0)
        hand_joint_states.effort.append(0)
    #print hand_joint_states

    # 从动手指骨关节
    hand_joint_states.name += ["lh_FFJ1", "lh_MFJ1", "lh_RFJ1"]
    hand_joint_states.velocity += [0, 0, 0]
    hand_joint_states.effort += [0, 0, 0]


    #
    # 发布 jointstates
    while not rospy.is_shutdown():
        AD_value = rospy.wait_for_message("/Shadow_Hand/AD_value", JointState)
        hand_joint_states.position = []
        for i in range(0, len(AD_value.name)):
            joint_name = Joint_Name_ID[ AD_value.name[i] ]
            rate = Joint_Name_Scale[joint_name][0]  # 设置关节角度
            offset = Joint_Name_Scale[joint_name][1]
            p1 = Joint_Name_Scale[joint_name][2]  # 设置关节角度
            p2 = Joint_Name_Scale[joint_name][3]
            AD = AD_value.position[i]
            ang = AD*rate + offset

            if (p1<=ang<=p2):
                hand_joint_states.position.append( ang )
            elif (ang<p1):
                hand_joint_states.position.append( p1 )
            elif (ang>p2):
                hand_joint_states.position.append( p2 )
           
        # 从动手指骨关节位置
        index = hand_joint_states.name.index("lh_FFJ2")
        hand_joint_states.position.append(hand_joint_states.position[index])
        index = hand_joint_states.name.index("lh_MFJ2")
        hand_joint_states.position.append(hand_joint_states.position[index])
        index = hand_joint_states.name.index("lh_RFJ2")
        hand_joint_states.position.append(hand_joint_states.position[index])

        hand_joint_states.header.stamp = rospy.Time.now()
        #print hand_joint_states
        pub_hand_joint_states.publish(hand_joint_states)
