import numpy as np
from tensorflow import keras


def make_model(test_x, model_name):

    model_list = []
    model = keras.models.load_model('./{}_model.h5'.format(model_name))
    model.summary()
    predict = model.predict(test_x)
    img_idx = []
    for idx, i in enumerate(predict):
        pre = np.argmax(i)
        if pre == 0:
            img_idx.append(idx)


    return img_idx

#img_idx = make_model(test_x, "smile")