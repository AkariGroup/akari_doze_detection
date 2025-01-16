from scipy.spatial import distance

# 目のアスペクト比を計算する関数
def get_eye_aspect_ratio(eye):

    A = distance.euclidean(eye[1], eye[5])  # 縦の距離
    B = distance.euclidean(eye[2], eye[4])  # 縦の距離
    C = distance.euclidean(eye[0], eye[3])  # 横の距離
    return (A + B) / (2.0 * C)  # アスペクト比を返す

# goodかどうかを判定する関数
def is_good(landmarks):
    image_height = 960  # 使用する画像の高さ
    finger_tip_x = []
    
    # good の形を認識するために追加
    if int(landmarks.landmark[4].y * image_height) - int(landmarks.landmark[3].y * image_height) > -20: # 親指を上向きに伸ばしているかの判定
        return ""
        
    #  指先のx軸の値
    for i in range(2, 6):
        finger_tip_x.append(int(landmarks.landmark[4 * i].x * image_height)) # 指先
   
    # goodの手の形の認識
    for i in range(len(finger_tip_x) - 1):
        if abs(finger_tip_x[i] - finger_tip_x[i + 1]) >= 10:
            return ""
            
    return "good" # good だったら
    
# 手の形を判定する関数
def hand_shape(landmarks):
    """手の形を判定する関数"""
    fingers_list = []
    image_height = 480  # 使用する画像の高さ

    # 各指の曲がり具合を取得
    #手の根本の座標より下でまがってることになる
    for i in range(1, 6):  # インデックス1から5
        finger_tip = int(landmarks.landmark[4 * i].y * image_height) # 指先
        finger_base = int(landmarks.landmark[4 * i - 3].y * image_height) # 指の根本
        fingers_list.append(finger_tip < finger_base)  # 曲がっているかどうか

    # グー・チョキ・パーの判定
    if not fingers_list[1] and not fingers_list[2] and not fingers_list[3]:  # すべての指が曲がっている場合
        return "Rock"
    elif fingers_list[1] and fingers_list[2] and not fingers_list[3]:  # 人差し指と小指だけが立っている場合
        return "Scissors"
    elif all(fingers_list):  # それ以外はパー
        return "Paper"
    else:
        return "???????"