# How to work with the PAD suite

This short tutorial will guide you through the steps so you can build your own dataset focused on behavior analysis. I recommend you check out the [presentation](/docs/Presentation.pdf) and the [video demos](/docs/demos).

## 1. Data acquisition
This phase is about going out on the road and collecting samples, namely video and sensors data. Since the equipment would be different for each user I only provide some general guidelines:

- First things first, you need to know where to go, so you have to create a filming plan using tools like _uMap_ (find mine at http://u.osmfr.org/m/297205/). You should also think about when to film, as some days and hours may be more interesting than others. Remember to include a wide variety of scenarios!
- Set up the camera so it is centered in the vehicle and you have a clear view of the road and the surroundings. If it has configurable parameters (resolution, lens angle) you may want to play a little bit with them to find the best combination.
- For the sensors, most interesting ones are position, speed, acceleration, lights, steering, RADAR,... These should all include some kind of synchronization or timestamped data.

## 2. Media processing
Once you have all your data it is time to work on them a little bit. Here I will explain only video-related stuff.

- You probably want to have your videos in an easy-to-handle format, which for me was AVI. Use the **_any2avi_** tool to convert your videos to such format.
- Most likely you will have quite long videos, each containing several scenes. In order to separate each scene into an independent video use **_vid2clip_**. If you need to join two videos because there is an scene divided between them just launch **_clip2vid_** and problem solved!
- Finally, since you want to process frames rather than videos, run **_clip2frames_** to extract the frames and save them somewhere else.

## 3. Subject analysis
Now let's get to business!
From the frames, you want to obtain the position of the subjects (i.e. pedestrians and traffic lights). There are a few ways to accomplish this:

1. YOLO, which is nice and fast, is included in the suite (**_Run YOLO!_**), so the first thing you may want to try is to run it on all the frames of a scene and see if it works well enough. It will probably make some mistakes, which you can fix by using **_Bounding Box Remover_** and **_Bounding Box Creator_**. 
2. OpenCV automatic tracking is also implemented (**_Bounding Box Tracking v2_**). You have many different algorithms to choose from and see which one performs better. As in the previous case, you can fix detection errors with **_Bounding Box Remover_** and **_Bounding Box Creator_**.
3. You can manually draw each and every bounding box in each and every frame using the **_Bounding Box Creator_**. This can be quite tedious and time-consuming and should only be done when the other methods perform poorly.

If you have used automatic tracking you can skip this step, otherwise you need to perform tracking manually.
 
 1. First, use the **_Bounding Box Identification_** to assign unique identifiers to your subjects (Agents, Aliens, Traffic Lights). You only have to do this every time a subject enters or leaves the scene. You DO NOT have to do this for every frame in the sequence.
 2. Use the **_Bounding Box Tracking_** to propagate thos unique identifiers across the rest of the frames. Be aware that you cannot process all the frames at once. Instead, you have to launch it from every frame you used the **_Bounding Box Identification_** in until the next one you used it in.
 
 The last part of the analysis is behavior annotations. I use [BORIS](http://www.boris.unito.it/) for this purpose.
 
 1. Use **_frames2clip_** to obtain a video with the bounding boxes and identifiers you prepared earlier.
 2. After installing the software, create a new project and import all the different parameters from the [base project](/behavior) I provide.
 3. Follow the official tutorials  to perform the observations for each subject. Once you are done, export the observation data as TSV files.
 4. We are missing one part of the attention analysis: attributes. You can set attributes for the subjects in a sequence with the **_Attributes Manager_**.
 
 At this point you should have all your data properly processed and ready for the real analysis using AI techniques. This is up to you since it is not part of my project. If you want to see how your work looks when putting together all the data use the **_Data Fusion_** and enjoy the views!
 