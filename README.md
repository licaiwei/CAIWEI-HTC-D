# CAIWEI：HTC-D (Hand Transport Capture Device）手部运动捕获装置

## 硬件相关

[stm32CubeMX 与 MDK5工程文件](https://github.com/licaiwei/HTC-D/hardware/STM32)
[Altium Designer 工程文件](https://github.com/licaiwei/HTC-D/hardware/PCB)
[Solideworks 文件](https://github.com/licaiwei/HTC-D/hardware/Mechanism)
[HTC-VIVE（可选)]()

## 软件相关
#### 编程环境
ROS Melodic
pyserial
openVR（可选）

#### 使用方法
##### 获取代码
打开一个`termial`，定位到你的 `workspace/src` 下

```bash
git clone 
```
##### 启动驱动程序
使用前获得USB权限，查看USB设备
```bash
ls -l /dev/ttyUSB*
[out] crw-rw---- 1 root dialout 188, 0 6月  13 13:33 /dev/ttyUSB0
sudo chmod 777 /dev/ttyUSB0
```
启动驱动程序，默认使用卡尔曼滤波
```bash
roslaunch hand_demo hand_bringup.launch 
```
或者你可以不使用卡尔曼滤波，输入以下命令
```bash
roslaunch hand_demo hand_bringup.launch use_Kalman:=false
```
##### 启动手指位置的校准程序
因为每个人的手型不一样，所以在佩戴好设备之后应当启动该程序做手指位置的校准。
打开一个新的`termial`，定位到文件夹 `hand_demo/scripts` 下：

```bash
rosrun hand_demo hand_drive_init.py
```
根据图片提示设置手指的限位，在设置过程中，点击键盘`y`继续下一个设置，点击`n`为退出。完整的运行完整个程序后，该程序会生成并保存手指位姿的关节限位信息文件：`shadow_hand_joint_limit_config.yaml`
保存后的`shadow_hand_joint_limit_config.yaml`剪切到`sr_description/config`文件夹里即完成校准。
##### 启动demo
```bash
rosrun hand_demo joint_state_publiser_controller.py
```
如果要使用`Rviz`可视化：
```bash
roslaunch sr_description display.launch
```
