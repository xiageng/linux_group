#import the libraries

import os
import face_recognition

path = os.getcwd()
images = os.listdir("images")
#load my image
image_to_be_matched = face_recognition.load_image_file("myimage/mayun.jpg")
face_locations = face_recognition.face_locations(image_to_be_matched)
face_landmarks_list = face_recognition.face_landmarks(image_to_be_matched)
exit(0)
#encoding the loaded image into feature vector
image_to_be_matched_encoded = face_recognition.face_encodings(image_to_be_matched)[0]

for image in images:
    current_image = face_recognition.load_image_file("images/"+ image)
    current_image_encoded = face_recognition.face_encodings(current_image)[0]
    result = face_recognition.compare_faces([image_to_be_matched_encoded], current_image_encoded)
    if result[0] == True:
        print("Matched:" + image)
    else:
        print("Not matched" + image)