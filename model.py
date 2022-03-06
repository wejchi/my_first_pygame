import tensorflow as tf
from tensorflow import keras
import matplotlib.pyplot as plt
def get_model():
    input = tf.keras.layers.Input(shape=(512,512,3))
    x = tf.keras.layers.Rescaling(1./255, offset=0)(input)
    x = tf.keras.layers.Conv2D(56, kernel_size=(5, 5), activation='relu',
                               strides=2)(x)
    x = tf.keras.layers.Conv2D(56, kernel_size=(5, 5), activation='relu',
                               strides=2)(x)
    x = tf.keras.layers.Conv2D(128, kernel_size=(5, 5), activation='relu',
                               strides=2)(x)
    x = tf.keras.layers.Conv2D(128, kernel_size=(5, 5), activation='relu',
                               strides=2)(x)
    x = tf.keras.layers.Flatten()(x)
    x = tf.keras.layers.Dense(5, activation='sigmoid')(x)
    model = tf.keras.Model(inputs=input,outputs=x)
    model.compile(optimizer='Adam', loss='binary_crossentropy', metrics='accuracy')
    return model

def g_m():
    model = keras.Sequential()
    model.add(keras.layers.Dense(10,activation='elu',input_shape=(1,)))
    model.add(keras.layers.Dense(1))
    model.compile(optimizer='Adam', loss='MAE', metrics=['MSE','accuracy'])
    return model

if __name__ == '__main__':
    # model = g_m()
    # #model = get_dummy_model()
    # #model.summary()
    # x = list(range(-100,100))
    # y = [3*y for y in x]
    # model.fit(x,y,epochs=1000,verbose=1)
    # plt.plot(x,y)
    # y_pred = model.predict(x)
    # plt.plot(x,y_pred)
    # plt.show()
    pass

