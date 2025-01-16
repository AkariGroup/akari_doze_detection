import pyaudio
import wave

class Config:
    sound_played = False # 音が再生されたかどうか

def play_sound(file_path):

    # 再生するファイルを指定
    # file_path = "あなたの勝ち_1倍速.wav"

    # wavファイルを読み込む
    wf = wave.open(file_path, 'rb')

    # PyAudioインスタンスを作成
    p = pyaudio.PyAudio()

    # ストリームを開く
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    # データを読み込んで再生
    data = wf.readframes(1024)
    while data:
        stream.write(data)
        data = wf.readframes(1024)

    # ストリームを閉じる
    stream.close()
    p.terminate()

def play_sound_siren(file_path):

    # 再生するファイルを指定
    # file_path = "あなたの勝ち_1倍速.wav"

    # wavファイルを読み込む
    wf = wave.open(file_path, 'rb')

    # PyAudioインスタンスを作成
    p = pyaudio.PyAudio()

    # ストリームを開く
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    # データを読み込んで再生
    data = wf.readframes(1024)
    while data:
        stream.write(data)
        data = wf.readframes(1024)
    
    Config.sound_played = False

    # ストリームを閉じる
    stream.close()
    p.terminate()