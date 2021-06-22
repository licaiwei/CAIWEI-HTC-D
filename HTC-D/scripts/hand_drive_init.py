#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
hand_drive_init.py - 该装置的驱动初始化程序：
因为每个人的手型不一样，所以在佩戴好设备之后使用该程序。
在文件夹 HTC-D/scripts 下：
    rosrun HTC-D hand_drive_init.py
根据图片提示设置手指的限位，并保存 yaml
保存后的 yaml 剪切到 sr_description/config 文件里

@Created on MAY 1 2021
@author:菜伟
@email:li_wei_96@163.com
"""

import serial
import rospy
from sensor_msgs.msg import JointState
import sys
import os
import cv2

pic_path = "../data/"

if __name__ == "__main__":
    #
    # 创建句柄
    rospy.init_node('hand_drive_init', anonymous=True)
    rospy.loginfo("Hand drive initinal produce .")
    rospy.sleep(1)

    #
    # 加载YAML文建定义的 关节名称 --- id
    Joint_Name_ID = {}     # 字典{"ADx":joint name,}  将yaml定义从参数服务器读取出来
    param_list = rospy.get_param_names()
    for param in param_list:
        if "/hand_joint_id_list/" in param:
            Joint_Name_ID[param.replace(
                "/hand_joint_id_list/", "")] = rospy.get_param(param)
    if len(Joint_Name_ID) == 0:
        rospy.INFO("Yaml configuration file not loaded")
        exit(1)

    #
    # 手型1标定 lh_FFJ2 lh_FFJ3 lh_MFJ2 lh_MFJ3 lh_RFJ2 lh_RFJ3 "lh_FFJ4", "lh_MFJ4", "lh_RFJ4"
    img1 = cv2.imread(pic_path+"1.png", 1)
    cv2.imshow(" Keeping hand-type1", img1)
    key = cv2.waitKey()
    if( key==121 ): # "y"
        pass
    elif( key==110): # "n"
        print("Exiting...")
        sys.exit(1)
    else:
        print("Input Error")
        sys.exit(1)
    
    lists = ["lh_FFJ2", "lh_FFJ3", "lh_MFJ2", "lh_MFJ3", "lh_RFJ2", "lh_RFJ3", "lh_FFJ4", "lh_MFJ4", "lh_RFJ4"]
    joint_state = rospy.wait_for_message("/Shadow_Hand/AD_value", JointState) # 读 AD

    for i in lists:
        for k in Joint_Name_ID:
            if Joint_Name_ID[k]==i:
                index = 0
                for l in joint_state.name:
                    if l==k:
                        break
                    index += 1
                rospy.set_param("/shadow_hand_joint_limit/"+i+"/AD/p1", joint_state.position[index] )
                break
    cv2.destroyAllWindows()

    #
    # 手型2标定 lh_FFJ2 lh_FFJ3 lh_MFJ2 lh_MFJ3 lh_RFJ2 lh_RFJ3
    img2 = cv2.imread(pic_path+"2.png", 1)
    cv2.imshow(" Keeping hand-type2", img2)
    key = cv2.waitKey()
    if( key==121 ):
        pass
    elif( key==110):
        print("Exiting...")
        sys.exit(1)
    else:
        print("Input Error")
        sys.exit(1)
    lists = ["lh_FFJ2", "lh_FFJ3", "lh_MFJ2", "lh_MFJ3", "lh_RFJ2", "lh_RFJ3",]
    joint_state = rospy.wait_for_message("/Shadow_Hand/AD_value", JointState) # 读 AD

    for i in lists:
        for k in Joint_Name_ID:
            if Joint_Name_ID[k]==i:
                index = 0
                for l in joint_state.name:
                    if l==k:
                        break
                    index += 1
                rospy.set_param("/shadow_hand_joint_limit/"+i+"/AD/p2", joint_state.position[index] )
                break
    cv2.destroyAllWindows()

    #
    # 手型3标定  "lh_FFJ4", "lh_MFJ4", "lh_RFJ4"
    img3 = cv2.imread(pic_path+"3.png", 1)
    cv2.imshow(" Keeping hand-type3", img3)
    key = cv2.waitKey()
    if( key==121 ):
        pass
    elif( key==110):
        print("Exiting...")
        sys.exit(1)
    else:
        print("Input Error")
        sys.exit(1)
    lists = ["lh_FFJ4", "lh_MFJ4", "lh_RFJ4"]
    joint_state = rospy.wait_for_message("/Shadow_Hand/AD_value", JointState) # 读 AD

    for i in lists:
        for k in Joint_Name_ID:
            if Joint_Name_ID[k]==i:
                index = 0
                for l in joint_state.name:
                    if l==k:
                        break
                    index += 1
                rospy.set_param("/shadow_hand_joint_limit/"+i+"/AD/p2", joint_state.position[index] )
                break
    cv2.destroyAllWindows()
 

    #
    # 手型4标定  "lh_THJ4", lh_THJ2, lh_THJ1
    img4 = cv2.imread(pic_path+"4.png", 1)
    cv2.imshow(" Keeping hand-type4", img4)
    key = cv2.waitKey()
    if( key==121 ):
        pass
    elif( key==110):
        print("Exiting...")
        sys.exit(1)
    else:
        print("Input Error")
        sys.exit(1)
    lists = ["lh_THJ4", "lh_THJ2", "lh_THJ1"]
    joint_state = rospy.wait_for_message("/Shadow_Hand/AD_value", JointState) # 读 AD

    for i in lists:
        for k in Joint_Name_ID:
            if Joint_Name_ID[k]==i:
                index = 0
                for l in joint_state.name:
                    if l==k:
                        break
                    index += 1
                rospy.set_param("/shadow_hand_joint_limit/"+i+"/AD/p1", joint_state.position[index] )
                break
    cv2.destroyAllWindows()

    #
    # 手型5标定  "lh_THJ4"
    img5 = cv2.imread(pic_path+"5.png", 1)
    cv2.imshow(" Keeping hand-type5", img5)
    key = cv2.waitKey()
    if( key==121 ):
        pass
    elif( key==110):
        print("Exiting...")
        sys.exit(1)
    else:
        print("Input Error")
        sys.exit(1)
    lists = ["lh_THJ4"]
    joint_state = rospy.wait_for_message("/Shadow_Hand/AD_value", JointState) # 读 AD

    for i in lists:
        for k in Joint_Name_ID:
            if Joint_Name_ID[k]==i:
                index = 0
                for l in joint_state.name:
                    if l==k:
                        break
                    index += 1
                rospy.set_param("/shadow_hand_joint_limit/"+i+"/AD/p2", joint_state.position[index] )
                break
    cv2.destroyAllWindows()


    #
    # 手型6标定 lh_THJ2, lh_THJ1
    img6 = cv2.imread(pic_path+"6.png", 1)
    cv2.imshow(" Keeping hand-type6", img6)
    key = cv2.waitKey()
    if( key==121 ):
        pass
    elif( key==110):
        print("Exiting...")
        sys.exit(1)
    else:
        print("Input Error")
        sys.exit(1)
    lists = ["lh_THJ2", "lh_THJ1"]
    joint_state = rospy.wait_for_message("/Shadow_Hand/AD_value", JointState) # 读 AD

    for i in lists:
        for k in Joint_Name_ID:
            if Joint_Name_ID[k]==i:
                index = 0
                for l in joint_state.name:
                    if l==k:
                        break
                    index += 1
                rospy.set_param("/shadow_hand_joint_limit/"+i+"/AD/p2", joint_state.position[index] )
                break
    cv2.destroyAllWindows()

    rospy.sleep(0.5)
    os.system( "rosparam dump shadow_hand_joint_limit_config.yaml /shadow_hand_joint_limit" )
