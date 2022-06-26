It works only on windows at the moment <br> 

---
Install Requirements
---

`pip install -r requirements.txt`

---
Run the program:
---
`python filter.py {path_to_video} {option}`   

for example, using the video in the project :

`python filter.py videos/sample.mp4 {option}` 

where option is one of these:
 - edges
 - sobelx
 - sobely
 - sobelxy
 - smooth

The output video will be in videos/

--- 
Sample Image
---

![sample](resources/sample.jpg)

---
Edges
---

![edges](https://github.com/WildMix/opencvfilters/blob/main/resources/sample_edges.jpg)

---
Sobelx
---

![sobelx](https://github.com/WildMix/opencvfilters/blob/main/resources/sample_sobelx.jpg)

---
Sobely
---

![sobely](https://github.com/WildMix/opencvfilters/blob/main/resources/sample_sobely.jpg)

---
Sobelxy
---

![sobelxy](https://github.com/WildMix/opencvfilters/blob/main/resources/sample_sobelxy.jpg)

---
Further Information
---

[Sobel Operator](https://www.youtube.com/watch?v=uihBwtPIBxM)  
[Canny Edge Detector](https://www.youtube.com/watch?v=sRFM5IEqR2w)