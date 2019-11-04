from google.colab import drive
drive.mount('/content/drive')




import os
import keras
from keras.applications.vgg16 import VGG16
from keras.models import Sequential, Model
from keras.layers import Input, Activation, Dropout, Flatten, Dense
from keras import optimizers
from keras.preprocessing.image import ImageDataGenerator
from keras import backend
from keras.layers import Dense, Dropout, BatchNormalization, Activation, Conv2D,MaxPooling2D, Flatten
from keras import layers
from keras.optimizers import Adadelta
import numpy as np
import time
import numpy as np
import glob
from keras.preprocessing.image import load_img,img_to_array




img_size = (178, 218)
dir_name = "drive/My Drive/googledrive"
file_type = "jpg"

img_list = glob.glob('./' + dir_name + '/*.' + file_type) 
print(len(img_list))




img_size = (178, 218)
dir_name = "drive/My Drive/googledrive"
file_type = "jpg"

img_list = glob.glob('./' + dir_name + '/*.' + file_type) 

train_temp_img_array_list = []
print(1)
for img in img_list[:5000]:
    train_temp_img = load_img(img, grayscale=False, target_size=img_size)
    train_temp_img_array = img_to_array(train_temp_img) /255
    train_temp_img_array_list.append(train_temp_img_array)
    
train_x = np.array(train_temp_img_array_list) 
print(1)
test_temp_img_array_list = []
for img in img_list[:1000]:
    test_temp_img = load_img(img, grayscale=False, target_size=img_size)
    test_temp_img_array = img_to_array(test_temp_img) /255
    test_temp_img_array_list.append(test_temp_img_array)
    
test_x = np.array(test_temp_img_array_list) 
print(type(train_x))

train_x.shape






#分類するクラス
classes = ["smile", "not_smile"]
nb_classes = len(classes)


#inputを設定
img_width, img_height = 178, 218

#データの格納先を設定
train_dir = "./train"
test_dir = "./test"

#trainデータの画像数
#nb_train_samples = 1000

#testデータの画像数
#nb_test_samples = 100

#バッチサイズ
batch_size = 64

#epoch数
epoch = 60




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

#model = Model(inputs=vgg16.input, outputs=top_model(vgg16.output))

#for layer in model.layers[:15]:
#    layer.trainable = False
model.summary()
model.compile(loss='categorical_crossentropy',optimizer=optimizers.RMSprop(lr=1e-4),metrics=['accuracy'])







import numpy as np

with open("list_attr_celeba.txt","r") as f:
    smile_num = []
    for i in range(5000):
        line = f.readline()
        line = line.split()
        smile_num.append(int(line[32]))

na = np.array(smile_num)
na = np.where(na > 0, 1, 0)
print(type(na))
print(na)

# ラベルデータをカテゴリの1-hotベクトルにエンコードする
train_y = keras.utils.to_categorical(na, num_classes=nb_classes)
test_y = keras.utils.to_categorical(na[:1000], num_classes=nb_classes)
print(train_y)



# ラベルデータをカテゴリの1-hotベクトルにエンコードする
train_y = keras.utils.to_categorical(na[:5000], num_classes=nb_classes)
test_y = keras.utils.to_categorical(na[:1000], num_classes=nb_classes)

history = model.fit(train_x, train_y,
    batch_size=batch_size,
    verbose=1,
    epochs=epoch,
    validation_data=(test_x,test_y))





import pandas as pd 

history_df = pd.DataFrame(history.history)
history_df[['loss', 'val_loss']].plot()
history_df[['acc', 'val_acc']].plot()


model.save('./smile_model.h5')



new_model = keras.models.load_model('smile_model.h5')
new_model.summary()


predict = new_model.predict(test_x)
print(predict)
predict.shape


count = 1
#笑顔：１, not笑顔：２
for idx, i in enumerate(predict):
    pre = np.argmax(i)
    if pre == np.argmax(test_y[idx]):
        count += 1
        print(pre)

print(idx)
print(pre)
print(np.argmax(test_y[idx]))
print(count)











test_temp_img_array_list = []
for img in img_list[:1000]:
    test_temp_img = load_img(img, grayscale=False, target_size=img_size)
    test_temp_img_array = img_to_array(test_temp_img) /255
    test_temp_img_array_list.append(test_temp_img_array)

print(1)
test_x = np.array(test_temp_img_array_list) 