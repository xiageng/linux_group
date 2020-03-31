#!/usr/bin/env python
#-*- coding: utf-8 -*-

import cv2
import face_recognition


#video_capture = cv2.VideoCapture("video/video2.mp4")
video_capture = cv2.VideoCapture(0)
gxy_img = face_recognition.load_image_file("images/gxy.jpg")
gxy_face_encoding = face_recognition.face_encodings(gxy_img)[0]

know_face_encodings = [
    gxy_face_encoding
]
know_face_names = [
    "Geng Xiaoyan"
]

process_this_frame = True

while True:
    face_names = []
    face_locations = []
    face_encodings = []
    ret, frame = video_capture.read()
    if ret:
        #print("video capture read correct")
        pass
    else:
        print("there is an error when video capture")
        exit(1)
    size = 0.25
    small_frame = cv2.resize(frame, (0,0), fx = size, fy = size)
    #small_frame = frame
    rgb_small_frame = small_frame[:, :, ::-1]
    if process_this_frame:
        face_locations = face_recognition.face_locations(small_frame)
        face_encodings = face_recognition.face_encodings(small_frame, face_locations)

        for face_encoding in face_encodings:
            result = face_recognition.compare_faces(know_face_encodings,face_encoding,tolerance = 0.5)
            name = "Unknown"
            if True in result:
                first_match_index = result.index(True)
                name = know_face_names[first_match_index]
                #print("it's Geng Xiaoyan")
            print("result:%s,name:%d",result, name)
            face_names.append(name)

        #process_this_frame = not process_this_frame

    large_size = int(1/size)
    for (top, right, bottom, left), name in zip(face_locations,face_names):
        top *= large_size
        right *= large_size
        bottom *= large_size
        left *= large_size
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        #cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 255, 0), 1)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left, bottom), font, 1.0, (255, 255, 255), 1)

    cv2.imshow('Video', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()