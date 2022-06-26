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

![sobelx](resources/sample_edges.jpg)

---
Sobelx
---

![sobelx](resources/sample_sobelx.jpg)

---
Sobely
---

![sobelx](resources/sample_sobely.jpg)

---
Sobelxy
---

![sobelx](resources/sample_sobelxy.jpg)

---
Further Information
---

[Sobel Operator](https://www.youtube.com/watch?v=uihBwtPIBxM)  
[Canny Edge Detector](https://www.youtube.com/watch?v=sRFM5IEqR2w)