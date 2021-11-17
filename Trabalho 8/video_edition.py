import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

if not os.path.exists("./frames"):
    os.mkdir("./frames")
if not os.path.exists("./key_frames"):
    os.mkdir("./key_frames")

def convert_to_draw(frame):
    kernel_borders = np.array([[-1, -1, -1], [-1, 8, -1], [-1, -1, -1]])
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame = cv2.filter2D(frame, -1, kernel_borders)
    frame = cv2.bitwise_not(frame)
    return frame

file = "./short_movie.mp4"
cap = cv2.VideoCapture(file)
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
fps = cap.get(cv2.CAP_PROP_FRAME_COUNT)

count = 0
previous = np.zeros((height, width, 3))
last_keyframe_index = -1
frame_list = []
while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray_frame = convert_to_draw(frame)
    frame_list.append(gray_frame)

    diff = (frame.astype(float)-previous.astype(float))
    diff = np.mean(np.abs(diff))
    if diff > 10:
        if last_keyframe_index != -1:
            qtd = 5
            sub_keyframes_space = int((count - last_keyframe_index)/qtd)
            for i in reversed(range(qtd)):
                index = count - (i * sub_keyframes_space)
                sub_key_frame = frame_list[index]
                cv2.imwrite(f"./key_frames/{index}.png", sub_key_frame)
        else:
            cv2.imwrite(f"./key_frames/{count}.png", gray_frame)
        last_keyframe_index = count


    #### PARA SALVAR TODOS OS FRAMES#############
    #cv2.imwrite(f"./frames/{count}.png", gray_frame)
    #############################################

    ### PARA VISUALIZAR O VIDEO EM TEMPO REAL ###
    #cv2.imshow("short", gray_frame)
    #############################################

    
    
    cv2.waitKey(int(1000/fps))
    count += 1
    previous = frame