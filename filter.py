import cv2
import os
import sys
import moviepy.editor as mp
import numpy as np
import shutil
import platform

global name_video, frames, vidcap, width, height, \
    fps, option, directory_frames, directory_option, \
    frameSize, clip, separator, start

if platform.system() == "Linux":
    separator = "/"
    start = "/"
if platform.system() == "Windows":
    separator = chr(92) + chr(92)
    start = "C:" + separator


# Set up


# get the name of the video
def get_name_video(s: str) -> str:
    basename = os.path.basename(s)
    return basename.split('.')[0]


# Directory in which there will be the project, eg. /home/myself/Documents/python/
directory_abs = os.getcwd() + separator

name_video = sys.argv[1]
vidcap = cv2.VideoCapture(name_video)
clip = mp.VideoFileClip(name_video)
# width, height and frame rate  of the input video
width = int(vidcap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(vidcap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = vidcap.get(cv2.CAP_PROP_FPS)

option = sys.argv[2]
if option != "edges" and option != "sobelx" and option != "sobely" and option != "sobelxy" and option != "smooth": exit()

name_video = get_name_video(name_video)
# directory of the input videos's frames, the frames of the output videos, the audio of the videos and the processed
# videos without audio
directory_frames = directory_abs + "frames" + separator + name_video + separator
directory_option = directory_frames + separator + option
directory_audio = directory_abs + "sounds" + separator + name_video + separator
directory_video = directory_abs + "videos" + separator + "avi" + separator

# create directory_video if it doesn't estist
if not os.path.isdir(directory_video): os.mkdir(directory_video)

path_to_video = directory_video + name_video + "_" + option + ".avi"
path_to_audio = directory_audio + name_video + ".mp3"
path_to_output_video = directory_abs + "videos" + separator + name_video + "_" + option + ".mp4"

frames = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
frameSize = (width, height)
kernel = ((np.ones((5, 5), np.float32)) / 25)


def get_id(filename) -> str:
    count = 0
    for ch in filename:
        count += 1
        if ch == '.':
            break
    return filename[6:count - 1]


def extract_audio():
    if not os.path.isdir(directory_audio):
        os.mkdir(directory_audio)
        clip.audio.write_audiofile(path_to_audio)


def extract_frames():
    if not os.path.isdir(directory_frames):
        os.mkdir(directory_frames)
        count = 0

        while vidcap.isOpened():
            ret, frame = vidcap.read()
            if not ret:
                break
            cv2.imwrite(directory_frames + "frame_" + str(count) + ".jpg", frame)
            count += 1
        vidcap.release()
    # cv2.destroyAllWindows()


def process_video():
    if not os.path.isdir(directory_option):
        os.mkdir(directory_option)

        directory_encoded = os.fsencode(directory_frames)

        for file in os.listdir(directory_encoded):
            filename = os.fsdecode(file)

            if filename.endswith(".jpg"):

                img = cv2.imread(directory_frames + separator + filename)

                img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                img_blur = cv2.GaussianBlur(img_gray, (3, 3), 0)
                img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

                if option == "edges":
                    img = cv2.Canny(image=img_blur, threshold1=100, threshold2=200)
                elif option == "sobelx":
                    img = cv2.Sobel(src=img_blur, ddepth=cv2.CV_64F, dx=1, dy=0, ksize=5)
                elif option == "sobely":
                    img = cv2.Sobel(src=img_blur, ddepth=cv2.CV_64F, dx=0, dy=1, ksize=5)
                elif option == "sobelxy":
                    img = cv2.Sobel(src=img_blur, ddepth=cv2.CV_64F, dx=1, dy=1, ksize=5)
                elif option == "smooth":
                    img = cv2.filter2D(img, -1, kernel)
                else:
                    print("error")
                    exit()
                cv2.imwrite(directory_option + "frame_" + get_id(filename) + ".jpg", img)


def make_video():
    out = cv2.VideoWriter(path_to_video, cv2.VideoWriter_fourcc(*'DIVX'), fps, (frameSize))
    # collecting all the frames
    i = 0
    while i <= frames:
        filename = directory_option + "frame_" + str(i) + ".jpg"
        img = cv2.imread(filename)
        out.write(img)
        i += 1
    out.release()
    # join audio track
    audio = mp.AudioFileClip(path_to_audio)
    video1 = mp.VideoFileClip(path_to_video)
    final = video1.set_audio(audio)
    final.write_videofile(path_to_output_video, fps, threads=1, codec='libx264')


def remove_cache():
    shutil.rmtree(directory_option, ignore_errors=True)
    shutil.rmtree(directory_video, ignore_errors=True)
    shutil.rmtree(directory_audio, ignore_errors=True)


extract_audio()

extract_frames()

process_video()

make_video()

remove_cache()
