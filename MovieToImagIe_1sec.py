# coding:utf-8
import cv2
import os
import sys
import datetime


def save_frame_sec(video_path):
    """
    指定された動画から１秒毎に静止画で保存する。
    【引数】
        1.video_path:動画ファイルパス
    【処理概要】
        1.システム日付を取得（保存用フォルダ名として使用）
        2.動画を取得
        3.動画の全フレーム数を計算
        4.１秒当たりのフレーム数を取得
        5．動画を１秒毎にｊｐｇ形式で保存する。
    """

    now = datetime.datetime.now()                # システム日付を取得
    now = now.strftime("%Y_%m_%d_%H_%M_%S")
    cap = cv2.VideoCapture(video_path)           # 動画を取得
    Fs = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))  # 動画の全フレーム数を計算

    if not cap.isOpened():
        return

    result_path = "test/temp/" + now + "/"       # 保存先のディレクトリを指定
    os.makedirs(os.path.dirname(result_path), exist_ok=True)   # 保存先のディレクトリがなければ作成する

    fps = cap.get(cv2.CAP_PROP_FPS)             # １秒当たりのフレーム数を取得

    # print(cap.get(cv2.CAP_PROP_FPS))

    cnt = 0
    for i in range(0, Fs):
        if i % fps == 0:
            cap.set(cv2.CAP_PROP_POS_FRAMES, round(i))
            ret, frame = cap.read()
            if ret:
                cnt += 1
                cv2.imwrite(result_path + str(cnt) + ".jpg", frame)


if __name__ == '__main__':
    args = sys.argv
    save_frame_sec(args[1])
