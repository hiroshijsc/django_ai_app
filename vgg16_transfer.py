import numpy as np
from tensorflow import keras
from keras.models import Sequential, Model
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras.optimizers import SGD, Adam
from keras.utils import np_utils
from keras.applications import VGG16

classes = ["car", "motorbike"]
num_classes = len(classes)
image_size = 224

X_train, X_test, y_train, y_test = np.load("./imagefiles_224.npy")
X_train = X_train.astype("float") / 255.0
X_test  = X_test.astype("float") / 255.0
y_train = np_utils.to_categorical(y_train, num_classes)
y_test = np_utils.to_categorical(y_test, num_classes)

# モデルの定義
# VGGを転移学習で使用
model = VGG16(weights="imagenet", include_top=False, input_shape=(image_size, image_size, 3)) # 最後の層だけフリーズ

top_model = Sequential()
top_model.add(Flatten(input_shape=model.output_shape[1:]))
top_model.add(Dense(256, activation="relu"))
top_model.add(Dropout(0.5))
top_model.add(Dense(num_classes, activation="softmax"))

# 入力はVGG16のinput, top_modelのinputにVGG16のoutputを入れる
model = Model(inputs=model.input, outputs = top_model(model.output))
# VGGはフリーズ
for layer in model.layers[:15]:
    layer.trainable = False

# opt = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True) # rmsprop, adam
opt = Adam(lr = 0.0001)
model.compile(loss='categorical_crossentropy', optimizer=opt, metrics=["accuracy"])
model.fit(X_train, y_train, batch_size=32, epochs=16)

score = model.evaluate(X_test, y_test, batch_size=32)

model.save("./vgg16_transfer.h5")
