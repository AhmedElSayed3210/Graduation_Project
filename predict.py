from keras.models import load_model
from keras.preprocessing import image
import numpy as np


# dimensions of our images
img_width, img_height = 224, 224

# load the model we saved
model = load_model('saved_models/small_last4.h5')
'''
model.compile(loss='categorical_crossentropy',
              optimizer='rmsprop',
              metrics=['accuracy'])
'''
# predicting images
img = image.load_img('5-4.jpeg', target_size=(img_width, img_height))
x = image.img_to_array(img)
x = np.expand_dims(x, axis=0)

images = np.vstack([x])
classes = model.predict(images, batch_size=1)
print(classes)
result = np.where(classes == np.amax(classes))

print(result[1])
print(result)
