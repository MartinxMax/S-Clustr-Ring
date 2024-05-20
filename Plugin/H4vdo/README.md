
![](https://github.com/MartinxMax/MartinxMax/raw/main/Maptnh.jpg)


Video:

[![APT](https://i.ytimg.com/vi/39wn0NeZdK8/hqdefault.jpg?sqp=-oaymwE1CKgBEF5IVfKriqkDKAgBFQAAiEIYAXABwAEG8AEB-AH8CYAC0AWKAgwIABABGGUgZShlMA8=&rs=AOn4CLBBgNtaYXiHJFHzMnklzX7LGCRFYQ)](https://www.youtube.com/watch?v=39wn0NeZdK8)

# About H4vdo

RTMP lock screen playback video tool, you can send payload to the target, the target's screen plays content. The target cannot operate the computer

# Usuage

## Install

Choose to install dependent programs based on your operating system

![image.png](https://image.3001.net/images/20240519/1716115191_6649d6f7efa7d4d52b316.png!small)

## RTMP Server

`./rtsp-simple-server.exe`

![image.png](https://image.3001.net/images/20240519/1716113767_6649d1677cdec753f457f.png!small)

## Generate payload

`$ python3 H4vdo.py -rh 192.168.8.106 -path hacked`

If there is an issue with the secondary generation payload, please delete H4vdo_debug and generate it again

![image.png](https://image.3001.net/images/20240519/1716113826_6649d1a2705f8516f9fa7.png!small)

Copy all H4vdo debug files in the dist directory to the target machine

![image.png](https://image.3001.net/images/20240519/1716113849_6649d1b9c22636b59afde.png!small)

The victim will automatically lock the screen and play the RTMP server video by clicking on H4vdo.debugexe in the file

## Hacker push rtmp stream

`$ python3 H4vdo.py -rh 192.168.8.106 -path hacked -push`


### MP4

Enter 0, fill in the mp4 path for playback

![image.png](https://image.3001.net/images/20240519/1716114124_6649d2ccb5033e215e97c.png!small)


### Desktop

Enter 1 and fill in the name of the microphone that needs to be recorded

![image.png](https://image.3001.net/images/20240519/1716114260_6649d35446f1121ff6956.png!small)

### Camera

Enter 2, fill in the camera name and microphone name

![image.png](https://image.3001.net/images/20240519/1716114322_6649d3922171d8dd7e3d8.png!small)
