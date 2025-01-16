import time
from akari_client import AkariClient
from akari_client.position import Positions

# Akariクライアントの初期化
akari = AkariClient()
m5 = akari.m5stack
joints = akari.joints
joints.enable_all_servo()

# 初期位置
def default_positions():
    joints.set_joint_velocities(pan=5, tilt=5)
    joints.move_joint_positions(tilt=0.3, pan=0.0, sync=True)  # 左に振る

# 負けた場合の動作（首を左右に振る）
def lose_motion():
    joints.set_joint_velocities(pan=5, tilt=5)
    joints.move_joint_positions(tilt=0.0, pan=-0.3, sync=True)  # 左に振る
    joints.move_joint_positions(pan=0.3, sync=True)  # 右に振る
    joints.move_joint_positions(pan=-0.3, sync=True)  # 左に振る
    joints.move_joint_positions(pan=0.0, tilt = 0.0, sync=True)  # 左に振
    joints.set_joint_velocities(pan=2, tilt=2)
    time.sleep(1)
    joints.move_joint_positions(pan=-0.5, tilt = -0.3, sync=True)  
    time.sleep(2)
    joints.move_joint_positions(tilt=0.2,pan=0.0, sync=True)  # 正面に戻す

# 勝った場合の動作（首を小さく上下に振る）
def win_motion():
    joints.set_joint_velocities(pan=6, tilt=8)
    joints.move_joint_positions(tilt=0.3, pan=0.0, sync=True)  # 上を向く
    joints.move_joint_positions(tilt=-0.3, sync=True)  # 下を向く
    joints.move_joint_positions(tilt=0.3, sync=True)  # 上を向く
    joints.move_joint_positions(tilt=-0.3, sync=True)  # 下を向く
    joints.move_joint_positions(tilt=0.3, sync=True)  # 上を向く
    joints.move_joint_positions(tilt=-0.3, sync=True)  # 下を向く
    joints.move_joint_positions(tilt=0.2, pan = 0.0, sync=True)  # 正面に戻す