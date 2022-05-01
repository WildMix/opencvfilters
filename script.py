import cv2
import os
import sys
import moviepy.editor as mp

global name_video, frames, vidcap, width, height, fps, option, directory_frames, directory_option, frameSize, clip

name_video = sys.argv[1]
vidcap = cv2.VideoCapture(name_video)
clip = mp.VideoFileClip(name_video)
#player = MediaPlayer(name_video)
width = int(vidcap.get(cv2.CAP_PROP_FRAME_WIDTH ))
height = int(vidcap.get(cv2.CAP_PROP_FRAME_HEIGHT ))
fps =  vidcap.get(cv2.CAP_PROP_FPS)
option = sys.argv[2]
name_video = name_video[7:-4]
directory_frames = "frames/%s" % name_video
directory_option = directory_frames + "/" + option + "/"
directory_audio = "sounds/" + name_video + "/"
directory_video = "videos/avi/"
if not os.path.isdir(directory_video):os.mkdir(directory_video) 
path_to_video = directory_video + name_video + "_" + option + ".avi"
path_to_audio = directory_audio + name_video + ".mp3"
path_to_output_video = "videos/" + name_video + "_" + option + ".mp4"
frames = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
frameSize = (width,height)



if not os.path.isdir(directory_audio): 
 os.mkdir(directory_audio)
 clip.audio.write_audiofile(path_to_audio)


def get_id(filename) -> str:
 count = 0
 for ch in filename:
  count += 1
  if ch == '.':
   break   
 return filename[6:count-1] 

if option != "edges" and option != "sobelx" and option != "sobely" and option != "sobelxy": exit()

# Getting frame rate, height and width of the video


# Extract the frames from the video only if is the first time

if not os.path.isdir(directory_frames): 

	os.mkdir(directory_frames)
		
	count=0 
	while(vidcap.isOpened()):
		ret, frame = vidcap.read()
		
		if ret == False:
		 break
		cv2.imwrite(directory_frames + "/frame_" + str(count)+ ".jpg" ,frame)
		count+=1

	vidcap.release()
	cv2.destroyAllWindows()



# Process the frames with only edges, sombelx, sombely or sombelxy  


if not os.path.isdir(directory_option):
 os.mkdir(directory_option)
 
 directory_encoded = os.fsencode(directory_frames)

 for file in os.listdir(directory_encoded):
		filename = os.fsdecode(file)

		if filename.endswith(".jpg"):

		 img = cv2.imread(directory_frames + "/" + filename)

		 img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		 img_blur = cv2.GaussianBlur(img_gray, (3,3), 0) 


		if option == "edges": img = cv2.Canny(image=img_blur, threshold1=100, threshold2=200)
		elif option == "sobelx": img = cv2.Sobel(src=img_blur, ddepth=cv2.CV_64F, dx=1, dy=0, ksize=5)
		elif option == "sobely": img = cv2.Sobel(src=img_blur, ddepth=cv2.CV_64F, dx=0, dy=1, ksize=5)
		elif option == "sobelxy": img = cv2.Sobel(src=img_blur, ddepth=cv2.CV_64F, dx=1, dy=1, ksize=5)
		else:
		 print("error")
		 exit()
		#cv2.imshow(img)
		cv2.imwrite(directory_option + "frame_" + get_id(filename) + ".jpg", img) 

  
# Make the final video



out = cv2.VideoWriter(path_to_video,cv2.VideoWriter_fourcc(*'DIVX'), fps, (frameSize))


# collecting all the frames
i=0
while i <= frames:
 filename = directory_option + "/frame_" + str(i) + ".jpg"
 img = cv2.imread(filename)
 out.write(img)
 i+=1


out.release() 


# join audio track
audio = mp.AudioFileClip(path_to_audio)
video1 = mp.VideoFileClip(path_to_video)
final = video1.set_audio(audio)

final.write_videofile(path_to_output_video, fps, threads=1, codec='libx264')



