from keras.models import Sequential
from keras.layers import Dense,Activation,Dropout,Flatten,Conv2D,MaxPooling2D
from keras.utils.vis_utils import plot_model
from keras.utils.np_utils import to_categorical
from keras import optimizers
import matplotlib.pyplot as plt
import numpy as np
import math
import random
import os,glob
from PIL import Image


#getting and coordinating data
def make_sample(files):
    global X,Y
    X=[]
    Y=[]
    for cat,fname in files:
        add_sample(cat,fname)
    return np.array(X),np.array(Y)

def add_sample(cat,fname):
    img=Image.open(fname)
    img=img.convert("RGB")  #color!!!!
    img=img.resize((150,150))  #image size!!!!
    data=np.asarray(img)
    X.append(data)
    Y.append(cat)

categories=["messie2","commet2"]
X=[]  #image data
Y=[]  #label data
allfiles=[]    #all datas
testfiles=[]

root_dir="/Users/YusukeSakai/pythonfiles/c_and_n"
for idx,cat in enumerate(categories):
  image_dir=root_dir+"/"+cat
  files=glob.glob(image_dir+"/*.jpeg")    #jpegかjpgかに注意!!
  for f in files:
      allfiles.append((idx,f))

for idx,cat in enumerate(categories):
  image_dir=root_dir+"/"+cat+"_test"
  files=glob.glob(image_dir+"/*.jpg")
  for f in files:
    testfiles.append((idx,f))

random.shuffle(allfiles)
random.shuffle(testfiles)
#th=math.floor(len(allfiles)*0.8)  #deciding trainvs test
train=allfiles  #[0:th]
#test=allfiles[th:]
test=testfiles
X_train,y_train=make_sample(train[:2000])
#X_test,y_test=make_sample(test[:200])
X_test,y_test=make_sample(testfiles)
arr=(X_train,X_test,y_train,y_test)
np.save("/Users/YusukeSakai/pythonfiles/c_and_n/data/data.npy",arr)

#learning codes

model=Sequential()
model.add(Conv2D(filters=32,kernel_size=(3,3),padding="same",input_shape=X_train.shape[1:],activation="relu"))
model.add(MaxPooling2D((2,2)))
model.add(Conv2D(filters=64,kernel_size=(3,3),activation="relu"))
model.add(MaxPooling2D((2,2)))
#model.add(Dropout(0.25))
model.add(Conv2D(filters=128,kernel_size=(3,3),activation="relu"))
model.add(MaxPooling2D((2,2)))
model.add(Conv2D(filters=128,kernel_size=(3,3),activation="relu"))
model.add(MaxPooling2D((2,2)))
model.add(Flatten())
#model.add(Dropout())
model.add(Dense(512,activation="relu"))
model.add(Dense(2,activation="softmax"))
model.summary()
model.compile(optimizer=optimizers.RMSprop(lr=1e-5),loss="sparse_categorical_crossentropy",metrics=["accuracy"])
history=model.fit(X_train,y_train,verbose=1,epochs=4)
score=model.evaluate(X_test,y_test,verbose=1)
print("evaluate loss:{0[0]} \n evaluate acc:{0[1]}".format(score))
plt.plot(history.history["accuracy"],label="acc",ls="-",marker="o")
plt.ylabel("accuracy")
plt.xlabel("epochs")
plt.legend(loc="best")
plt.show()

#テスト
pred = np.argmax(model.predict(X_test[0:10]), axis=1)
print(pred)
print(y_test[0:10])
# テストデータの最初の10枚を表示します
for i in range(10):
    plt.subplot(1, 10, i+1)
    plt.imshow(X_test[i], "gray")
plt.show()
