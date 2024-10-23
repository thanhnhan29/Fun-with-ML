import numpy as np
import pandas as pd
from keras.models import load_model
import matplotlib.pyplot as plt
from keras import Sequential
from keras.layers import Dense, Dropout
from sklearn.model_selection import train_test_split
from keras.utils import to_categorical
import csv

data = pd.read_csv('train.csv')
data = np.array(data)
test = pd.read_csv('test.csv')
test = np.array(test)
test_x = test
data_x = data[:, 1:]
data_y = data[:, 0]
data_y = to_categorical(data_y, 10)
train_x, train_y = data_x, data_y
train_x, val_x, train_y, val_y = train_test_split(train_x, train_y, test_size=0.1)

model = Sequential()
model.add(Dense(512, input_dim=784, activation="relu"))
model.add(Dense(256, activation='relu'))
model.add(Dense(10, activation='softmax'))

model.summary()
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
his = model.fit(train_x, train_y, epochs=10, batch_size=1024, validation_data=(val_x, val_y))
# model.save("digit_recognizer.h5")
# model = load_model("digit_recognizer.h5")
res = model.predict(test_x)
print(his.history)
ans = []
for i in range(len(res)):
    ans.append([i + 1, np.argmax(res[i])])
# print(ans)
filename = "anns.csv"
fields = ["ImageId", "Label"]
with open(filename, 'w') as csvfile:
    # creating a csv dict writer object
    writer = csv.writer(csvfile)

    # writing headers (field names)
    # writer.writeheader()
    writer.writerow(fields)
    # writing data rows
    writer.writerows(ans)

plt.plot(his.history['val_loss'], linestyle='--', label='val_loss')
plt.plot(his.history['loss'], linestyle='--', label='loss')
plt.savefig('foo_relu_softmax.png')
