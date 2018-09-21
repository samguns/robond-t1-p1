## Project: Search and Sample Return

---


[//]: # (Image References)

[image1]: ./misc/rover_image.jpg
[image2]: ./calibration_images/example_grid1.jpg
[image3]: ./calibration_images/example_rock1.jpg

## [Rubric](https://review.udacity.com/#!/rubrics/916/view) Points
### Here I will consider the rubric points individually and describe how I addressed each point in my implementation.  

---

### Notebook Analysis
#### 1. Run the functions provided in the notebook on test images (first with the test data provided, next on data you have recorded). Add/modify functions to allow for color selection of obstacles and rock samples.
Here is an example of how to include an image in your writeup.

![alt text][image1]

#### 1. Populate the `process_image()` function with the appropriate analysis steps to map pixels identifying navigable terrain, obstacles and rock samples into a worldmap.  Run `process_image()` on your test data using the `moviepy` functions provided to create video output of your result.
And another!

![alt text][image2]
### Autonomous Navigation and Mapping

#### 1. Fill in the `perception_step()` (at the bottom of the `perception.py` script) and `decision_step()` (in `decision.py`) functions in the autonomous mapping scripts and an explanation is provided in the writeup of how and why these functions were modified as they were.
I first started to implement the perception processes in `perception.py`. Most of the code are directly copied from `process_image()` in Jupyter notebook. It worked fine in identifying rock samples and navigable terrains. However, I found the fidelity wasn't satisfying, there's no guarantee to pass the 60% minimum requirement. I thought it's because if I took the whole image into consideration, those pixels too far away from the camera tend to be noisier, thus lower accuracy is inevitable. So I experimented the method suggests in the `livestream discussion` video, that is to narrow the view area to be just four meters ahead of Rover camera. After I applied this `roi_thresh()` to the color threshed image, the resulting fidelity improved quite a bit.

As for the decision making in `decision_step()`, I reconstructed the if/else decision tree into a more readable state machine calls that contains smaller code pieces to deal with its specific functions. Also, I adopted the idea that by applying an positive offset to the perceived mean angle, the Rover could steer itself as a left-side walk crawler. The first thing I noticed was since Rover starts with a random orientation, there's some chance it would loop around obstacles in the beginning if it went into walk crawler mode directly. To tackle this problem, I added an `init` state that forcing Rover to go straight forward in the first 3 seconds. Since by then the Rover got an acceptable result in map searching and sample identifying, I then decided to make the Rover to gather up samples. So I added a `sample` state to the state machine which makes Rover decelerating and approaching rock samples slowly when it finds a rock lies in front of its left side.

#### 2. Launching in autonomous mode your rover can navigate and map autonomously.  Explain your results and how you might improve them in your writeup.  

**Note: running the simulator with different choices of resolution and graphics quality may produce different results, particularly on different machines!  Make a note of your simulator settings (resolution and graphics quality set on launch) and frames per second (FPS output to terminal by `drive_rover.py`) in your writeup when you submit the project so your reviewer can reproduce your results.**

Here I'll talk about the approach I took, what techniques I used, what worked and why, where the pipeline might fail and how I might improve it if I were going to pursue this project further.  



![alt text][image3]
