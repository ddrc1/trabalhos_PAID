import cv2
import glob
import re

images = []
numbers = re.compile(r'(\d+)')

def numericalSort(value):
    parts = numbers.split(value)
    parts[1::2] = map(int, parts[1::2])
    return parts

for filename in sorted(glob.glob("./key_frames/*"), key=numericalSort):
    image = cv2.imread(filename)
    images.append(image)

width, height = images[0].shape[0: 2]
out = cv2.VideoWriter("keyframes_video.mp4", cv2.VideoWriter_fourcc(*'DIVX'), 1, (height, width))

for image in images:
    out.write(image)
out.release()