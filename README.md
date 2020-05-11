
# PongPing


## Description
PongPing is a table tennis scoring system through image processing the live video of the match, where the system
will be able to score points to the competitors and flag a foul when applied.

## List of Contributors
| Names    |      Code     |    Github  |
|----------|:-------------:|:-------------|
| Abdelrahman Wael Helaly |  1500797 | [Helaly96](https://github.com/Helaly96)     |
| Ammar Yasser |   1500866  | [Ayasser96](https://github.com/AmmarYasser97)   |
| Mohamed Hesham | 1501320 | [MHesham98](https://github.com/MHesham98)       |
| Omar Ibrahim | 1500869 |   [mr-rofl](https://github.com/mr-rofl)   |
| Omar Ahmad | 1500873 |     [omarahmad293](https://github.com/omarahmad293)   |

## Features
1. Ball detection
2. Stadium Segmentation
3. Scoring
4. Ini Configuration File
5. Debugging Console

## Demo


## Development Environment & Dependencies 
In our development we used python language with some dependencies:
* OpenCV: To process the video
* PyQT: To make the GUI
* Numpy: To define arrays
* Shapely: To help in the scoring systems

PongPing built with some magic python libraries, so before start using PingPong run the following command

### Cloning

```bash
git clone https://github.com/Helaly96/ImageProcessing-PongPing.git
git cd /ImageProcessing-PongPing
```


### Installation of dependencies

After install the dependancies, next step is cloning PongPing.
```bash
pip install opencv-python pyqt5 puqt5-tools numpy shapely
```

### Usage
Then run our GUI
```bash
python gui.py
```

## Ball Tracking
To track the ball, a pipeline of stages had to be done:
1. Convert the image to grayscale
![Gray Image](images/gray.png "Gray Image")
2. Subtract current frame from previous one
![Difference Image](images/diff.png "Difference Image")
3. Blur the image with a gaussian blur
![Guassian Blur Image](images/blur1.png "Guassian Blur Image")
4. Threshold the image
![Thresholded Image](images/threshold.png "Thresholded Image")
5. Apply Opening on the image
![Opened Image](images/open.png "Opened Image")
6. Blur the image with a gaussian blur
![Second Guassian Blur](images/blur2.png "Second Guassian Blur")
7. Detect the contours
![Contours Detected](images/contours.png "Contours Detected")
8. Sort and filter the contours
![Real Contours](images/real_contours.png "Real Contours")
9. Select one of the contours to be the current trajectory
![Ball Contour](images/trajectories.png "Ball Contour")

## Stadium Segmentation
First we let the user select an approximate area of the stadium then we loop for a number of
frames to decrease the error just in case a player was hiding a part of the stadium or any other 
error in this loop we save the resulted frames from masking using a color filter in a list then 
we loop on this list to select the frame having the largest contour -having the largest
contours indicates segmenting the stadium better-.
At this point we've got the contours for the stadium, then we find the contours for the net and
eventually we draw those contours on the video.
[Stadium Segmentation Illustration](https://www.youtube.com/watch?v=hd54ugIYpQw&feature=youtu.be "Video")
## Scoring System
Integration of Four Classes is responsible to monitor the game using the inputs from both the Ball Tracking and Stadium Segmentation.

### Class Ball
Class responsible of tracking the ball position and direction throughout the game

### Class tableObject
Class responsible to create the polygon of either the stadium table or the net to be used in the calculations needed.

### Class Player
Class responsible to hold the players score, serve count, let allowance.

### Class Match
Class responsible to integrate between all the previous classes to monitor the matches and govern the main logic of the ping pong game.

## Ini Configuration
## Debuging Console

## Previous Development Approaches
1. [Trajectory & Kalmann filter]()
2. [Search for white contours in contours list]()
3. [Tweaking Video parameters]()
4. [Coloring the ball]()


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
