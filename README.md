# akari_nemuken  
AKARIとじゃんけんをしたり、AKARIがユーザーの眠気検知をするアプリです  

## アプリの概要  
Akariが居眠りを検知してくれるアプリ．  
・居眠りが検知されると，アラームが鳴る仕組みとなっている．  
・眠気を覚ますためにじゃんけん機能がある．  
・グットサインをするとじゃんけんが開始される．

## セットアップ方法
1. ローカルにクローンする  
cd ~  
git clone　https://github.com/AkariGroup/akari_doze_detection   
cd akari_doze_detection  
2. submoduleの更新  
git submodule update --init  
3. 仮想環境の作成  
python3 -m venv venv  
. venv/bin/activate 
sudo apt install portaudio19-dev 
pip install -r requirements.txt  
 
## 起動方法
1. 仮想環境の有効化    
. venv/bin/activate  
2. 顔認識やて認識を行うためにAKARIのカメラを起動させる  
python3 main.py  
3. 終了する時  
AKARI_VIEWウィンドウを選択した状態でキーボードのqキーを押す  

## その他  
このアプリケーションは愛知工業大学 情報科学部 知的制御研究室により作成されたものです.  
**スピーカーは別途外付けする必要があります・** 