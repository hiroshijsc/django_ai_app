from PIL import Image
import os, glob
import numpy as np
from sklearn.model_selection import train_test_split

# パラメータの初期化
classes = ["car", "motorbike"]
num_classes = len(classes)
image_size = 224

# 画像の読み込みとNumpy配列への変換
X = []  #リスト
Y = []  #ラベル

for index, classlabel in enumerate(classes):
    photos_dir = "./" + classlabel
    files = glob.glob(photos_dir + "/*.jpg")
    for i, file in enumerate(files):
        image = Image.open(file)
        image = image.convert("RGB")
        image = image.resize((image_size, image_size))
        data = np.asarray(image)
        X.append(data)
        Y.append(index)

X = np.array(X)
Y = np.array(Y)

X_train, X_test, y_train, y_test = train_test_split(X, Y)
xy = (X_train, X_test, y_train, y_test)
np.save("./imagefiles_224.npy", xy)  # npyで画像を保存
