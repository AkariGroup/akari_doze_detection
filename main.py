import grpc
import time
import os
import threading
import random
import queue
import sys
import mediapipe as mp
import depthai as dai
import cv2
from akari_client import AkariClient
from play_sound import play_sound_siren
from play_sound import Config
from janken import display_result, display_count, draw_count, judge, Break_Time, default_color
from gesture import get_eye_aspect_ratio, is_good, hand_shape
from motion import default_positions

sys.path.append(os.path.join(os.path.dirname(__file__), "akari_motion_server/lib/grpc"))
import motion_server_pb2_grpc

# Akariロボットのモーションサーバーの設定
motion_server_port = "localhost:50055"
channel = grpc.insecure_channel(motion_server_port)
stub = motion_server_pb2_grpc.MotionServerServiceStub(channel)

# Akariクライアントの初期化
akari = AkariClient()
m5 = akari.m5stack

# MediaPipeの初期化
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_face_mesh = mp.solutions.face_mesh

# DepthAIのパイプライン設定
pipeline = dai.Pipeline()

# カメラ設定
cam_rgb = pipeline.createColorCamera()
cam_rgb.setPreviewSize(1280, 960)
cam_rgb.setInterleaved(False)

# ストリーミングの設定
xout_rgb = pipeline.createXLinkOut()
xout_rgb.setStreamName("rgb")
cam_rgb.preview.link(xout_rgb.input)

    
def main() -> None:
    """
    メイン関数
    """
    # 判定で使用
    janken_in_progress = False

    default_color()
    default_positions()

    # MediaPipe HandsとFace Meshを初期化
    with mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=2,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.7
    ) as hands, mp_face_mesh.FaceMesh(
        static_image_mode=False,
        max_num_faces=1,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    ) as face_mesh:
        
        # DepthAIデバイスを使ってフレームを取得・表示
        with dai.Device(pipeline) as device:
            video = device.getOutputQueue(name="rgb", maxSize=4, blocking=False)

            result_queue = queue.Queue()
            janken_in_progress_queue = queue.Queue()
            hand_result = ""
            hand_good = ""
            eyes_closed_start_time = None
            Config.sound_played = False
            
            while True:
                in_frame = video.get()  # フレームの取得
                frame = in_frame.getCvFrame()  # OpenCV形式に変換

                # フレームを反転（鏡像のようにする）
                frame = cv2.flip(frame, 1)

                # BGR画像をRGBに変換
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                # MediaPipeで手のランドマークを検出
                results_hands = hands.process(rgb_frame) 

                # 手が検出された場合、ランドマークを描画
                if results_hands.multi_hand_landmarks:
                    for hand_landmarks in results_hands.multi_hand_landmarks:
                        mp_drawing.draw_landmarks(
                            frame, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                            mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
                            mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2)
                        )

                        # 手の形を判定
                        hand_result = hand_shape(hand_landmarks)
                        hand_good = is_good(hand_landmarks)
                        
                        cv2.putText(frame, f"Hand Shape: {hand_result}", (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

                # MediaPipeで顔のパーツを検出
                results_face = face_mesh.process(rgb_frame)
                
                # 目のアスペクト値の初期化
                left_eye_ratio = 0
                right_eye_ratio = 0

                # 顔のパーツが検出された場合、ランドマークを描画
                if results_face.multi_face_landmarks:
                    for face_landmarks in results_face.multi_face_landmarks:
                        mp_drawing.draw_landmarks(
                            frame, face_landmarks,
                            mp_face_mesh.FACEMESH_TESSELATION,
                            mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=1, circle_radius=1),
                            mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=1)
                        )

                        # 左右の目のランドマーク座標を取得
                        left_eye = [
                            (face_landmarks.landmark[33].x, face_landmarks.landmark[33].y),
                            (face_landmarks.landmark[160].x, face_landmarks.landmark[160].y),
                            (face_landmarks.landmark[158].x, face_landmarks.landmark[158].y),
                            (face_landmarks.landmark[133].x, face_landmarks.landmark[133].y),
                            (face_landmarks.landmark[153].x, face_landmarks.landmark[153].y),
                            (face_landmarks.landmark[144].x, face_landmarks.landmark[144].y)
                        ]
                        right_eye = [
                            (face_landmarks.landmark[362].x, face_landmarks.landmark[362].y),
                            (face_landmarks.landmark[385].x, face_landmarks.landmark[385].y),
                            (face_landmarks.landmark[387].x, face_landmarks.landmark[387].y),
                            (face_landmarks.landmark[263].x, face_landmarks.landmark[263].y),
                            (face_landmarks.landmark[373].x, face_landmarks.landmark[373].y),
                            (face_landmarks.landmark[380].x, face_landmarks.landmark[380].y)
                        ]

                        # 目のランドマークを発光させる（各ランドマークを黄色で囲む）
                        for idx in [33, 158, 160, 133, 144, 362, 153, 385, 387, 263, 373, 380, ]:
                            x = int(face_landmarks.landmark[idx].x * frame.shape[1])
                            y = int(face_landmarks.landmark[idx].y * frame.shape[0])
                            cv2.circle(frame, (x, y), 2, (0, 255, 255), -1)  # 明るい黄色で目のランドマークを発光

                        # 目のアスペクト比を計算
                        left_eye_ratio = get_eye_aspect_ratio(left_eye)
                        right_eye_ratio = get_eye_aspect_ratio(right_eye)
                      
                # 閉じていると見なす閾値（適宜調整） 
                if (left_eye_ratio < 0.31 or right_eye_ratio < 0.31) and left_eye_ratio  > 0 and right_eye_ratio > 0:

                    cv2.putText(frame, "Eyes Closed", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

                    if eyes_closed_start_time is None:
                        eyes_closed_start_time = time.time()
                        
                    elif time.time() - eyes_closed_start_time >= 4 and not Config.sound_played:
                        # 5秒以上目を閉じている場合に音を鳴らす
                        playsound = threading.Thread(target=play_sound_siren, args=("./models/templetes/アラーム6秒.wav",))
                        playsound.start()
                        Config.sound_played = True 
                else:
                    cv2.putText(frame, "Eyes Open", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    eyes_closed_start_time = None

                if hand_good == "good" and janken_in_progress == False:
                    janken_in_progress = True
                    # akari_hand = random.choice(["Rock", "Scissors", "Paper"])
                    akari_hand = random.choice(["Rock"])
                    # カウントダウンを開始する
                    janken_thread = threading.Thread(target=display_count, args=(akari_hand, result_queue))
                    janken_thread.start()
                    
                if not result_queue.empty():
                    akari_hand = result_queue.get()  # キューの中身を取得
                    player_hand = hand_shape(hand_landmarks)
                    result = judge(player_hand, akari_hand)
                    janken_thread3 = threading.Thread(target=display_result, args=(player_hand, akari_hand, result))
                    janken_thread3.start()
                   
                    if result == "引き分け":
                        akari_hand = random.choice(["Rock", "Scissors", "Paper"])
                        # ここで重くなってしまう
                        janken_thread2 = threading.Thread(target=draw_count, args=(akari_hand, result_queue, result))
                        janken_thread2.start()
                    else:
                        # janken_thread3.join()]
                        janken_thread4 = threading.Thread(target=Break_Time, args=(janken_in_progress_queue,))
                        janken_thread4.start()

                if not janken_in_progress_queue.empty():
                    janken_in_progress_queue.get()
                    janken_in_progress = False
                    
                # フレームを表示
                cv2.imshow("Hand and Face Parts Detection", frame)

                # 'q'キーを押すと終了
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

    # 終了時にすべてのウィンドウを閉じる
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
