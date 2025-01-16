import time
import queue
from akari_client import AkariClient
from akari_client.color import Colors
from akari_client.position import Positions
from play_sound import play_sound

from motion import lose_motion, win_motion

# Akariクライアントの初期化
akari = AkariClient()
m5 = akari.m5stack
joints = akari.joints
joints.enable_all_servo()

# 待ち時間
def default_color():
    m5.set_display_text(
        text="",
        pos_x=Positions.CENTER,
        pos_y=Positions.CENTER,
        back_color=Colors.WHITE,
        refresh=True,
    )

# 待ち時間
def Break_Time(janken_in_progress_queue):
    time.sleep(13)
    janken_in_progress_queue.put("mati")

# じゃんけんの結果を表示する
def display_result(player_hand, akari_hand, result):

    m5.set_display_text(
        text=f"あなたの手: {player_hand}",
        pos_x=Positions.CENTER,
        pos_y=30,
        size=2,
        text_color=Colors.RED,
        back_color=Colors.WHITE,
        refresh=True,
    )
    
    m5.set_display_text(
        text=f"Akariの手: {akari_hand}",
        pos_x=Positions.CENTER,
        pos_y=90,
        size=2,
        text_color=Colors.RED,
        back_color=Colors.WHITE,
        refresh=False,
    )
    if akari_hand == "Rock":
        play_sound("./models/templetes/わしはグーじゃ_1倍速.wav")
    elif akari_hand == "Paper":
        play_sound("./models/templetes/わしはパーじゃ_1倍速.wav")
    elif akari_hand == "Scissors":
        play_sound("./models/templetes/わしはチョキじゃ_1倍速.wav")
    
    time.sleep(1)
    
    if result == "引き分け":
        play_sound("./models/templetes/引き分け_1倍速.wav")
    elif result == "負け":
        play_sound("./models/templetes/わしの勝ちじゃ_1倍速.wav")
        win_motion()
    elif result == "勝ち":
        play_sound("./models/templetes/うわあ、負けちゃった_1倍速.wav")
        lose_motion()

    if not result == "引き分け":
        m5.set_display_text(
            text=f"君の{result}",
            pos_x=Positions.CENTER,
            pos_y=150,
            size=3,
            text_color=Colors.BLACK,
            back_color=Colors.WHITE,
            refresh=False,
        )
        time.sleep(1)
    
# カウントダウンを表示
def display_count(akari_hand, result_queue):
    m5.set_display_text(
        text="",
        pos_x=Positions.CENTER,
        pos_y=Positions.CENTER,
        back_color=Colors.WHITE,
        refresh=True,
    )

    for i in range(3, 0, -1):
        m5.set_display_text(
            text=f"じゃんけんスタートまで",
            pos_x=Positions.CENTER,
            pos_y=70,
            size=2,
            text_color=Colors.RED,
            back_color=Colors.WHITE,
            refresh=False,
        )
        m5.set_display_text(
            text=f"{i}秒",
            pos_x=Positions.CENTER,
            pos_y=120,
            size=6,
            text_color=Colors.RED,
            back_color=Colors.WHITE,
            refresh=False,
        )
        time.sleep(1)

    m5.set_display_text(
        text="最初はグー",
        pos_x=Positions.CENTER,
        pos_y=Positions.CENTER,
        size=2,
        text_color=Colors.RED,
        back_color=Colors.WHITE,
        refresh=True,
    )
    time.sleep(1)
    
    play_sound("./models/templetes/最初はぐうー_1倍速.wav")
    
    m5.set_display_text(
        text="じゃんけん",
        pos_x=Positions.CENTER,
        pos_y=Positions.CENTER,
        size=2,
        text_color=Colors.RED,
        back_color=Colors.WHITE,
        refresh=True,
    )
    time.sleep(1)
    
    play_sound("./models/templetes/じゃんけんぽん_1倍速.wav")
     
    m5.set_display_text(
        text=f"ぽん",
        pos_x=Positions.CENTER,
        pos_y=Positions.CENTER,
        size=2,
        text_color=Colors.RED,
        back_color=Colors.WHITE,
        refresh=True,
    )

    time.sleep(1)

    result_queue.put(akari_hand)

# あいこまでのカウント
def draw_count(akari_hand,result_queue, result):

    time.sleep(1)

    m5.set_display_text(
        text=f"{result}",
        pos_x=Positions.CENTER,
        pos_y=150,
        size=3,
        text_color=Colors.BLACK,
        back_color=Colors.WHITE,
        refresh=False,
    )

    time.sleep(3)

    m5.set_display_text(
        text="あいこ しょっ ",
        pos_x=Positions.CENTER,
        pos_y=Positions.CENTER,
        size=2,
        text_color=Colors.RED,
        back_color=Colors.WHITE,
        refresh=True,
    )

    time.sleep(1)
    
    play_sound("./models/templetes/あいこでしょっ_1倍速.wav")
    
    m5.set_display_text(
        text="Akariが",
        pos_x=Positions.CENTER,
        pos_y=Positions.CENTER,
        size=2,
        text_color=Colors.RED,
        back_color=Colors.WHITE,
    )
    time.sleep(1)
    
    m5.set_display_text(
        text=f"{akari_hand}を出しました",
        pos_x=Positions.CENTER,
        pos_y=Positions.CENTER,
        size=2,
        text_color=Colors.RED,
        back_color=Colors.WHITE,
        refresh=True,
    )
    
    time.sleep(1.5)

    result_queue.put(akari_hand)

# 勝敗を判定する
def judge(player_hand, akari_hand):
    if player_hand == akari_hand:
        return "引き分け"
    elif (player_hand == "Rock" and akari_hand == "Scissors") or \
         (player_hand == "Scissors" and akari_hand == "Paper") or \
         (player_hand == "Paper" and akari_hand == "Rock"):
        return "勝ち"
    else:
        return "負け"