import numpy as np
import math
import cv2, os, argparse, shutil

# 切り抜いた画像の保存先ディレクトリ
SAVE_PATH = "./outputs/"

# 画像取得フォルダ
INPUT_PATH = "./inputs/"

# 画像のサイズ
WIDTH = 178
HEIGHT = 218
JGP = ".jpg"
size = WIDTH, HEIGHT, 3

# 基本的なモデルパラメータ
FLAGS = None

# 学習済モデルの種類
CASCADE = ["default","alt","alt2","tree","profile","nose"]

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
    # 顔検知に成功した数(デフォルトで0を指定)
    face_detect_count = 0
    
    # 顔検知に失敗した数(デフォルトで0を指定)
    face_undetected_count = 0
    
    # フォルダ内ファイルを変数に格納(ディレクトリも格納)
    files =  os.listdir(FLAGS.input_dir)

    # 出力フォルダ存在チェック 呼出
#    saveDirectoryCreate(FLAGS)

    count = 0
    # 集めた画像データ分繰り返し
    for file_name in files:
        count += 1
        print('No.{} : {}-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+'.format(count, file_name))

        # ファイルの場合(ディレクトリではない場合)
        if os.path.isfile(FLAGS.input_dir + file_name):
            # 顔画像処理　呼出
            cnts = faceProcessing(FLAGS, face_detect_count, face_undetected_count, file_name)
            face_detect_count = cnts[0]
            face_undetected_count = cnts[1]

        print('　認識できた人数 : {}'.format(face_detect_count))
    print('Undetected Image Files:%d' % face_undetected_count)

'''
出力フォルダ存在チェック
'''
def saveDirectoryCreate(FLAGS):
    # 成功ファイルを移動いない場合は、出力用のディレクトリが存在する場合、削除して再作成
    if FLAGS.move_dir == "":
        if os.path.exists(SAVE_PATH):
            shutil.rmtree(SAVE_PATH)
        os.mkdir(SAVE_PATH)

'''
顔画像処理
'''
def faceProcessing(FLAGS, face_detect_count, face_undetected_count, file_name):

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

    if len(face) > 0:
        for rect in face:
            # 画像出力　呼出
            face_detect_count = faceOutput(img, rect, face_detect_count)

        # 検出できたファイルは移動
        if FLAGS.move_dir != "":
            shutil.move(FLAGS.input_dir + file_name, FLAGS.input_dir + FLAGS.move_dir)
    

    else:
        #print('　×××No Face×××')
        face_undetected_count += 1

    return face_detect_count, face_undetected_count


'''
画像出力
'''
def faceOutput(img, rect, face_detect_count):
    face_detect_count += 1
    face_file_name = ""

    # 顔画像（余白あり）取得
    white_img = imgCreate(img, rect, face_detect_count)

    # ファイル名作成    
    face_file_name = '{:0>3}{}'.format(face_detect_count, JGP)

    # 画像出力
    cv2.imwrite(SAVE_PATH + face_file_name, white_img)

    return face_detect_count

'''
顔画像作成（余白あり）
'''
def imgCreate(img, rect, face_detect_count):
    # 切り取った顔画像
    img_face = img[rect[1]:rect[1] + rect[3], rect[0]:rect[0] + rect[2]]

    # np.fillでホワイトベース作成
    white_img = np.zeros(size, dtype=np.uint8)
    white_img.fill(255)

    # 余白設定
    img_width = img_face.shape[1]
    img_height = img_face.shape[0]
    #print("img_width：", img_width," img_height：", img_height)

    # 顔画像が規定サイズより大きい場合
    if WIDTH < img_width or HEIGHT < img_height:
        # リサイズ
        img_face = cv2.resize(img_face, dsize=(WIDTH, WIDTH))
        img_width = img_height = WIDTH

    x_offsetH = math.floor((WIDTH - img_width) / 2)
    y_offsetH = math.floor((HEIGHT - img_height) / 2)
    #print("x：", x_offsetH, " y：", y_offsetH)

    # ホワイトベースの上に顔画像を重ねる
    white_img[x_offsetH:x_offsetH+img_width, y_offsetH:y_offsetH+img_height] = img_face

    return white_img

'''
メイン
'''

# 直接実行されている場合、引数取得
if __name__ == "__main__":
    parser = getArg()

# パラメータ取得と実行
FLAGS, unparsed = parser.parse_known_args() 

# 学習済モデルファイルパス取得
cascade_path = cascadePathChoice(FLAGS)

#カスケード分類器の特徴量を取得する
faceCascade = cv2.CascadeClassifier(cascade_path)

# 画像処理 呼出
imgProcessing(FLAGS, faceCascade)


