# FRC-Vision
Vision processing repository

[FRC Vision Processing Site](https://wpilib.screenstepslive.com/s/4485/m/24194)
[OpenCV Tutorials] (http://docs.opencv.org/2.4/doc/tutorials/tutorials.html)

##To Install

-First install `virtualenv`, `python3` and `pip`.

-Clone the repository

-In the terminal run `virtualenv -p python3 venv`

-Then run `source venv/bin/activate`

-By now you are in your virtual environment

-Install numpy, and opencv through `pip install numpy opencv-python imutils scipy scikit-image`



###What's Working?

Currently, our strategy has been to adjust camera contrast and hue ratings such that most objects maintain an
orangeish yellow hue. The GREEN LED light creates a green image on the reflective tape.

Then, we create contours from regions above a threshold grayscale brightness and eliminate those that aren't
the color green.

Mixed results thus far...
We need to make sure that the camera maintains a high contrast/hue setting to make the green easily distinguishable


#TODO

After finding the contours, we need to begin extracting data from them. These include:

-Distance
-Height
-Angle

for determining bot movement, and catapult launching mechanisms.
