#Listing the import files.
import tensorflow as tf
from tensorflow.keras.datasets import mnist
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Conv2D, Dense, MaxPooling2D, Flatten
from tensorflow.keras.optimizers import Adam
import numpy as np
import pickle 
from PIL import Image

def build_model_acc(input_shape, num_classes):
    x = Input(input_shape)
    y = Conv2D(8,  (3, 3),padding="same", activation='relu')(x)
    y = MaxPooling2D((2,2))(y)
    y = Conv2D(16, (3, 3),padding="same", activation='relu')(y)
    y = MaxPooling2D((2,2))(y)
    y = Flatten()(y)
    y = Dense(128, activation="relu")(y)
    y = Dense(64, activation="relu")(y)
    y = Dense(num_classes, activation="softmax")(y)
    return Model(x,y)

#defining the model
def build_model_rob(input_shape, num_classes):
    x = Input(input_shape)
    y = Conv2D(8,  (3, 3),padding="same", activation='sigmoid')(x)
    y = MaxPooling2D((2,2))(y)
    y = Conv2D(16, (3, 3),padding="same", activation='sigmoid')(y)
    y = MaxPooling2D((2,2))(y)
    y = Conv2D(64, (3, 3),padding="same", activation='sigmoid')(y)
    y = MaxPooling2D((2,2))(y)
    y = Flatten()(y)
    y = Dense(128, activation="sigmoid")(y)
    y = Dense(64, activation="relu")(y)
    y = Dense(num_classes, activation="softmax")(y)
    return Model(x,y)
    
#Defniing the batch size for the training
batch_size = 8
num_classes = 10
epochs = 50
image_shape = (28, 28, 1)

(x_train, y_train), (x_test, y_test) = mnist.load_data()

x_train = x_train.astype('float32') / 255.0
x_test  = x_test.astype('float32')  / 255.0

#Reshaping the images for uniform image sizes
x_train = x_train.reshape((-1,) + image_shape)
x_test  = x_test.reshape((-1,) + image_shape)

# X_train = tf.keras.utils.normalize(X_train, axis=1)
# X_test = tf.keras.utils.normalize(X_test, axis=1)

print(x_train.shape)

y_train = tf.keras.utils.to_categorical(y_train, num_classes)
y_test  = tf.keras.utils.to_categorical(y_test, num_classes)

#Passing all the parameters to build the model
model = build_model_acc(image_shape, num_classes)
model.summary()
model.compile(
    optimizer=Adam(lr=1e-4),
    loss=tf.keras.losses.categorical_crossentropy,
    metrics=['accuracy']
)

model.fit(
    x_train,y_train,
    epochs=epochs,
    # validation_data=(x_test,y_test)
)
#model is being saved. This helps us use the model in the future, instead of training it again.
model.save('model_v1')


# The bottom part of the code is for evaluation of the model. 
# # ========== Evaluate ==========
# test_loss, test_acc = model.evaluate(x_test, y_test,verbose=0)
# print("Testing loss:{:.4f}, acc:{:.4f}".format(test_loss, test_acc))

# x_test_adv = get_adv_images(x_test, y_test, model, tf.keras.losses.categorical_crossentropy, 0.3)
# adv_loss, adv_acc = model.evaluate(x_test_adv, y_test,verbose=0)
# print("Adversarial loss:{:.4f}, acc:{:.4f}".format(adv_loss, adv_acc))

# # ========== Save images ==========
# output_col_row = 10
# image = np.reshape(x_test[:output_col_row**2], (output_col_row, output_col_row, image_shape[0], image_shape[1], image_shape[2]))
# image = np.transpose(image, (0, 2, 1, 3, 4))
# image = np.reshape(image, (output_col_row * image_shape[0], output_col_row * image_shape[1], image_shape[2]))
# image = np.clip(255 * image, 0, 255)
# image = image.astype("uint8")
# Image.fromarray(image[:,:,0], "L").save("test.png")

# image = np.reshape(x_test_adv[:output_col_row**2], (output_col_row, output_col_row, image_shape[0], image_shape[1], image_shape[2]))
# image = np.transpose(image, (0, 2, 1, 3, 4))
# image = np.reshape(image, (output_col_row * image_shape[0], output_col_row * image_shape[1], image_shape[2]))
# image = np.clip(255 * image, 0, 255)
# image = image.astype("uint8")
# Image.fromarray(image[:,:,0], "L").save("adv.png")
