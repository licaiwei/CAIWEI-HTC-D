#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
hand_drive.py - 该装置的驱动程序：
卡尔曼滤波，发布 sensor_msgs.msg.JointState 类型的 /Shadow_Hand/AD_value topic
后续将添加更多的功能，比如：把初始化程序设为service

@Created on MAY 1 2021
@author:菜伟
@email:li_wei_96@163.com
"""
import serial
import rospy
from sensor_msgs.msg import JointState
from Kalman_Filter import KalmanFilter
import numpy as np
import sys

if __name__ == "__main__":
    #
    # 打开串口
    try:
        ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
        rospy.loginfo(ser.name)
    except:
        rospy.loginfo("Failed to open serial")
        exit()
	
    #
    # 创建句柄
    rospy.init_node('hand_drive', anonymous=True)
    use_Kalman = rospy.get_param("/hand_drive/Kalman")
    rospy.loginfo("use_Kalman: %s", use_Kalman)

    pub_ADC = rospy.Publisher("/Shadow_Hand/AD_value", JointState, queue_size=1)  # 发布AD值
    rospy.sleep(1)

    #
    # 加载YAML文建定义的 关节名称 --- id
    Joint_Name_ID = {}         # 字典{"ADx":joint name,}  将yaml定义从参数服务器读取出来
    param_list = rospy.get_param_names()
    for param in param_list:
        if "/hand_joint_id_list/" in param:
            Joint_Name_ID[param.replace(
                "/hand_joint_id_list/", "")] = rospy.get_param(param)
    if len(Joint_Name_ID) == 0:
        rospy.INFO("Yaml configuration file not loaded")
        exit(1)

    #
    #
    AD_v = JointState()
    AD_v.name = Joint_Name_ID.keys()
    AD_v_index = [int(x.replace("AD", "")) for x in AD_v.name]
    rospy.loginfo(AD_v.name)
    raw_data = [0 for i in range(0, 16)]  # 0 数组

    if use_Kalman:
        K = KalmanFilter(16, 0.001, 0.01)  # 卡尔曼滤波器

    #
    # 清空一次
    while(1):
        ser.flush()
        line = ser.readline()
        try:
            ang = line.split()
            if ang[0] == "15":
                break
        except:
            pass

    #
    # 开始
    while not rospy.is_shutdown():
        ser.flush()
        try:   # 防止充电过程中断电等因素导致的乱码问题
            line = ser.readline()
            AD_s, deg_s = line.split()
            raw_data[int(AD_s)] = int(deg_s)

            if AD_s == "15":
                if use_Kalman:
                    xhat = K.kalmanFilter(np.reshape(raw_data, (16, 1)))  # 滤波
                    dealed_data = np.reshape(xhat, 16).tolist()
                    AD_v.position = [dealed_data[0][x] for x in AD_v_index]   # 设置角度
                else:
                    AD_v.position = [raw_data[x] for x in AD_v_index]   # 设置角度
                AD_v.header.stamp = rospy.Time.now()
                pub_ADC.publish(AD_v)
        except:
            pass
    ser.close()
