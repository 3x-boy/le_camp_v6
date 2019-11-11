# +*+*+*+*++*+*試験+*+*+*+*+*+*+*+

import keras
import time
import datetime
import numpy as np
import glob
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.layers import Input, Activation, Dropout, Flatten, Dense
from tensorflow.keras import optimizers
from tensorflow.keras import backend
from tensorflow.keras.layers import Dense, Dropout, BatchNormalization, Activation, Conv2D,MaxPooling2D, Flatten
from tensorflow.keras import layers
from tensorflow.keras.preprocessing.image import load_img,img_to_array



img_size = (178, 218)
dir_name = "googledrive"
file_type = "jpg"

img_list = glob.glob('./' + dir_name + '/*.' + file_type) 
print(len(img_list))



train_temp_img_array_list = []
print(1)
for img in img_list[:1000]:
    train_temp_img = load_img(img, grayscale=False, target_size=img_size)
    train_temp_img_array = img_to_array(train_temp_img) /255
    train_temp_img_array_list.append(train_temp_img_array)
    
train_x = np.array(train_temp_img_array_list) 
print(2)

test_temp_img_array_list = []
for img in img_list[1000:1500]:
    test_temp_img = load_img(img, grayscale=False, target_size=img_size)
    test_temp_img_array = img_to_array(test_temp_img) /255
    test_temp_img_array_list.append(test_temp_img_array)
    
test_x = np.array(test_temp_img_array_list) 
print(type(train_x))

train_x.shape

#分類するクラス
nb_classes = 2

#inputを設定
img_width, img_height = 178, 218

#バッチサイズ
batch_size = 64

#epoch数
epoch = 20

model = Sequential()
model.add(Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=(178, 218, 3)))
model.add(layers.Conv2D(64,(3,3),activation="relu"))
model.add(layers.MaxPooling2D((2,2)))
 
model.add(layers.Conv2D(128,(3,3),activation="relu"))
model.add(layers.MaxPooling2D((2,2)))
 
model.add(layers.Conv2D(128,(3,3),activation="relu"))
model.add(layers.MaxPooling2D((2,2)))
 
model.add(layers.Flatten())
model.add(Dense(512, activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(2, activation='softmax'))

model.summary()
model.compile(loss='categorical_crossentropy',optimizer=optimizers.RMSprop(lr=1e-4),metrics=['accuracy'])


for x in range(40):
    x += 1
    with open("./list_attr_celeba.txt","r") as f:
        smile_num = []
        for i in range(60000):
            line = f.readline()
            line = line.split()
            smile_num.append(int(line[x]))

    na = np.array(smile_num)
    na = np.where(na > 0, 1, 0)

    # ラベルデータをカテゴリの1-hotベクトルにエンコードする
    train_y = keras.utils.to_categorical(na[:1000], num_classes=nb_classes)
    test_y = keras.utils.to_categorical(na[1000:1500], num_classes=nb_classes)


    history = model.fit(train_x, train_y,
        batch_size=batch_size,
        verbose=1,
        epochs=epoch,
        validation_data=(test_x,test_y))
    
    #モデルの保存
    model.save('./models/model_No{}.h5'.format(x))
    print("OK:No{}".format(x))
    now = datetime.datetime.now()
    print(now)

