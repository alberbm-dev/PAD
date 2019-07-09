# Official Pedestrian Awarenes Dataset repository

Welcome, amigo!

This repository contains the code I developed as part of my Bachelor's Project, which is called **Development of an intelligent system to detect and predict pedestrians' intentions in urban environments**. It is an integrated suite of tools to process videos, work with bounding boxes and make behavior-related stuff. Here you will also find the files resulting from the behavioral analysis I performed in that project.

I hope I can make my paper publicly available at some point. In the meantime, contact me if you have questions or comments (albertobm@protonmail.com).

## The Suite

The suite is pretty straightforward and easy to use.

I strongly recommend using virtual environments to run it. I used Pipenv to manage the project and the requirements.

In order to use the _Run YOLO!_ tool you must first download the weights and configuration files from Darknet's official website, as well as the list of categories on the COCO dataset.

### Requirements
The suite is developed under Pop!\_OS (Ubuntu 18.04) in Python 3.6, but should work just fine in any other operative system.
- Codecs and formats support (for example ubuntu-restricted-extras, ffmpeg,...).
- Numpy: https://www.numpy.org
- OpenCV-Python: https://opencv-python-tutroals.readthedocs.io/en/latest/
- Munkres: https://pypi.org/project/munkres/
- screeninfo: https://pypi.org/project/screeninfo/
- wxPython: https://github.com/wxWidgets/Phoenix
- VLC (optional, but strongly recommended): https://www.videolan.org/vlc/

## The Dataset

The Pedestrian Awareness Dataset is focused on analyzing pedestrians' behavior in urban environments. It includes a series of small clips corresponding to crossing/not-crossing scenarios, bounding boxes data for subjects appearing in those scenes, and behavioral and attributes annotations for those same subjects.

Here you have an example of my work:

![](scene_behav_02.png) 

_For both privacy and storage reasons I will not publish the recorded videos here. If you are interested in getting them, please send an e-mail to albertobm@protonmail.com stating who you are, your purposes,..._

_Anyone who recognizes him or herself in any of the videos and wants to avoid its distribution can send an e-mail to albertobm@protonmail.com and I will remove it from the list of videos I can share._
