import numpy as np
import math
import cv2, os, argparse, shutil

# 画像取得フォルダ
INPUT_PATH = "./inputs/"

# 基本的なモデルパラメータ
FLAGS = None

# 学習済モデルの種類
CASCADE = ["default","alt","alt2","tree","profile","nose"]

# LOG出力最大人数
MAX_FACE = 2     # 2以外の時はソース修正

'''
パラメータ設定
'''
def getArg():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--cascade",
        type=str,
        default="alt",
        choices=CASCADE,
        help="cascade file."
  )
    parser.add_argument(
        "--scale",
        type=float,
        default=1.3,
        help="scaleFactor value of detectMultiScale."
  )
    parser.add_argument(
        "--neighbors",
        type=int,
        default=2,
        help="minNeighbors value of detectMultiScale."
  )
    parser.add_argument(
        "--min",
        type=int,
        default=40,
        help="minSize value of detectMultiScale."
  )
    parser.add_argument(
        "--input_dir",
        type=str,
        default=INPUT_PATH,
        help="The path of input directory."
  )
    parser.add_argument(
        "--move_dir",
        type=str,
        default="",
        help="The path of moving detected files."
  )
    return parser

'''
学習済みモデルのパスを返却
'''
def cascadePathChoice(FLAGS):
    if   FLAGS.cascade == CASCADE[0]:#"default":
        cascade_path = "./models/haarcascade_frontalface_default.xml"
    elif FLAGS.cascade == CASCADE[1]:#"alt":
        cascade_path = "./models/haarcascade_frontalface_alt.xml"
    elif FLAGS.cascade == CASCADE[2]:#"alt2":
        cascade_path = "./models/haarcascade_frontalface_alt2.xml"
    elif FLAGS.cascade == CASCADE[3]:#"tree":
        cascade_path = "./models/haarcascade_frontalface_alt_tree.xml"
    elif FLAGS.cascade == CASCADE[4]:#"profile":
        cascade_path = "./models/haarcascade_profileface.xml"
    elif FLAGS.cascade == CASCADE[5]:#"nose":
        cascade_path = "./models/haarcascade_mcs_nose.xml"
    return cascade_path

'''
画像処理
'''
def imgProcessing(FLAGS, faceCascade):

    # フォルダ内ファイルを変数に格納(ディレクトリも格納)
    files =  os.listdir(FLAGS.input_dir)

    count = 0                               # 画像枚数カウント
    log_dict = {0: 0, 1: 0, MAX_FACE: 0}    # 識別人数毎カウント

    # 集めた画像データ分繰り返し
    for file_name in files:
        count += 1

        # ファイルの場合(ディレクトリではない場合)
        if os.path.isfile(FLAGS.input_dir + file_name):
            # 顔画像処理　呼出
            log_dict = faceProcessing(FLAGS, log_dict, file_name)

    print('---{}枚中---'.format(count))
    for i in range(len(log_dict)):
        msg = ""
        if i == MAX_FACE:
            msg = str(i) + "人以上認識　"
        else:
            msg = str(i) + "人認識　　　"

        print('{}⇒{:>5}枚'.format(msg, log_dict[i]))


'''
顔画像処理
'''
def faceProcessing(FLAGS, log_dict, file_name):

    # 画像ファイル読込
    img = cv2.imread(FLAGS.input_dir + file_name)

    # 大量に画像があると稀に失敗するファイルがあるのでログ出力してスキップ(原因不明)
    if img is None:
        print(file_name + ':Cannot read image file')
        return False

    # カラーからグレースケールへ変換(カラーで顔検出しないため)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 顔検出
    face = faceCascade.detectMultiScale(gray, scaleFactor=FLAGS.scale, minNeighbors=FLAGS.neighbors, minSize=(FLAGS.min, FLAGS.min))

    if len(face) >= MAX_FACE:
        log_dict[MAX_FACE] += 1
    else:
        log_dict[len(face)] += 1

    return log_dict


'''
メイン
'''
# 直接実行されている場合、引数取得
if __name__ == "__main__":
    parser = getArg()

# パラメータ取得と実行
FLAGS, unparsed = parser.parse_known_args() 

#カスケード分類器の特徴量を取得する
faceCascade = cv2.CascadeClassifier(cascadePathChoice(FLAGS))

# 画像処理 呼出
imgProcessing(FLAGS, faceCascade)


