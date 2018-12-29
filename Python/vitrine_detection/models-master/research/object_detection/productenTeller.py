import numpy as np
import os
import six.moves.urllib as urllib
import sys
import tarfile
import tensorflow as tf
import zipfile
from collections import defaultdict
from io import StringIO
from matplotlib import pyplot as plt
from PIL import Image
import cv2
import time
sys.path.append("..")
from utils import label_map_util
from utils import visualization_utils as vis_util
import picamera
import Bakkerbase

def maakFoto():
  with picamera.PiCamera() as camera:
      print('..Wachten, foto wordt gemaakt')
      camera.resolution = (640, 420)
      camera.start_preview()
      # Camera warm-up time
      time.sleep(2)
      camera.capture('images/cam29.jpg')
      print('..foto is gemaakt')
      time.sleep(2)

def splitProducten():
  arrayCoordinators = [[50, 180, 150, 280],[50, 180, 270,400],[280,400, 150,280],[280,400, 270,400]]
  img = cv2.imread('images/cam29.jpg')
  for list in arrayCoordinators:
      crop_img = img[list[0]:list[1], list[2]:list[3]]
      cv2.imwrite('images/plek{}.jpg'.format(arrayCoordinators.index(list)), crop_img)
  print('..Wachten, producten zijn gesplitst')
  time.sleep(2)

while True:

  maakFoto()
  splitProducten()
  # What model to download.
  MODEL_NAME = 'asus2'

  # Path to frozen detection graph. This is the actual model  that is used for the object detection.
  PATH_TO_CKPT = MODEL_NAME + '/frozen_inference_graph.pb'

  # List of the strings that is used to add correct label for each box.
  PATH_TO_LABELS = os.path.join('data', 'vitrine_detection.pbtxt')

  NUM_CLASSES = 2


  producten = [False, False, False, False]


  detection_graph = tf.Graph()
  with detection_graph.as_default():
    od_graph_def = tf.GraphDef()
    with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
      serialized_graph = fid.read()
      od_graph_def.ParseFromString(serialized_graph)
      tf.import_graph_def(od_graph_def, name='')




  label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
  categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES,   use_display_name=True)
  category_index = label_map_util.create_category_index(categories)


  def load_image_into_numpy_array(image):
    (im_width, im_height) = image.size
    return np.array(image.getdata()).reshape(
        (im_height, im_width, 3)).astype(np.uint8)



  # For the sake of simplicity we will use only 2 images:
  # image1.jpg
  # image2.jpg
  # If you want to test the code with your images, just add path to the images to the TEST_IMAGE_PATHS.
  PATH_TO_TEST_IMAGES_DIR = 'images/'
  #TEST_IMAGE_PATHS = [ os.path.join(PATH_TO_TEST_IMAGES_DIR, 'IMG_{}.PNG'.format(i)) for i in range(7464, 7483) ]
  #TEST_IMAGE_PATHS = [ os.path.join(PATH_TO_TEST_IMAGES_DIR, 'plek1.jpg') ]
  TEST_IMAGE_PATHS = [ os.path.join(PATH_TO_TEST_IMAGES_DIR, 'plek{}.jpg'.format(i)) for i in range(0, 4) ]

  # Size, in inches, of the output images.
  IMAGE_SIZE = (20, 16)



  with detection_graph.as_default():
    with tf.Session(graph=detection_graph) as sess:
      # Definite input and output Tensors for detection_graph
      image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
      # Each box represents a part of the image where a particular object was detected.
      detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
      # Each score represent how level of confidence for each of the objects.
      # Score is shown on the result image, together with the class label.
      detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
      detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')
      num_detections = detection_graph.get_tensor_by_name('num_detections:0')
      for image_path in TEST_IMAGE_PATHS:
        image = Image.open(image_path)
        # the array based representation of the image will be used later in order to prepare the
        # result image with boxes and labels on it.
        image_np = load_image_into_numpy_array(image)
        # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
        image_np_expanded = np.expand_dims(image_np, axis=0)
        # Actual detection.
        (boxes, scores, classes, num) = sess.run(
            [detection_boxes, detection_scores, detection_classes, num_detections],
            feed_dict={image_tensor: image_np_expanded})

      # Visualization of the results of a detection.
        vis_util.visualize_boxes_and_labels_on_image_array(
            image_np,
            np.squeeze(boxes),
            np.squeeze(classes).astype(np.int32),
            np.squeeze(scores),
        category_index,
          use_normalized_coordinates=True,
            line_thickness=1)
        plt.figure(figsize=IMAGE_SIZE)
        plt.imshow(image_np)
        cv2.imwrite('checkImages/test{}.jpg'.format(TEST_IMAGE_PATHS.index(image_path)), image_np)
        
        taco = 0
        for index,value in enumerate(classes[0]):
          if scores[0,index] > 0.5 and category_index.get(value)['name'] == 'koekje':
            taco += 1
                
        if taco > 0:
          producten[TEST_IMAGE_PATHS.index(image_path)] = True


  producten_data = [
    {'available': producten[0], 'product_name': 'Plek1'},
    {'available': producten[1], 'product_name': 'Plek2'},
    {'available': producten[2], 'product_name': 'Plek3'},
    {'available': producten[3], 'product_name': 'Plek4'}
  ]
  Bakkerbase.save_vitrine(producten_data)
  print('..Data verzonden naar api')
  time.sleep(100)

