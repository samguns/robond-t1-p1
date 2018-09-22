## Project: Search and Sample Return

---

[//]: # (Image References)

[image1]: ./output/rock_sample.png
[image2]: ./output/nav_obs_angle.png

## [Rubric](https://review.udacity.com/#!/rubrics/916/view) Points
### Here I will consider the rubric points individually and describe how I addressed each point in my implementation.  

---

### Notebook Analysis
#### 1. Run the functions provided in the notebook on test images (first with the test data provided, next on data you have recorded). Add/modify functions to allow for color selection of obstacles and rock samples.
I applied the techniques taught in the class lecture to identify navigable terrain pixel, and mark the rest of pixels as obstacles. Similar to select navigable terrains, I used (actually, copied from `Walkthrough` video) color thresholding to identify rock samples.

Here's the result of rock sample identification.
![alt text][image1]

This is a result of generating navigable terrains, as well as steering reference angle.
![alt text][image2]

#### 1. Populate the `process_image()` function with the appropriate analysis steps to map pixels identifying navigable terrain, obstacles and rock samples into a worldmap.  Run `process_image()` on your test data using the `moviepy` functions provided to create video output of your result.
I followed the comments/hints within starter code in `process_image()` to fill up all the necessary procedures step by step. The result of whole Notebook Analysis is in *Rover_Project_Test_Notebook.html*.


### Autonomous Navigation and Mapping

#### 1. Fill in the `perception_step()` (at the bottom of the `perception.py` script) and `decision_step()` (in `decision.py`) functions in the autonomous mapping scripts and an explanation is provided in the writeup of how and why these functions were modified as they were.
I first started to implement the perception processes in `perception.py`. Most of the code are directly copied from `process_image()` in Jupyter notebook. It worked fine in identifying rock samples and navigable terrains. However, I found the fidelity wasn't satisfying, there's no guarantee to pass the 60% minimum requirement. I thought it's because if I took the whole image into consideration, those pixels too far away from the camera tend to be noisier, thus lower accuracy is inevitable. So I experimented the method suggests in the `livestream discussion` video, that is to narrow the view area to be just four meters ahead of Rover camera. After I applied this `roi_thresh()` to the color threshed image, the resulting fidelity improved quite a bit.

As for the decision making in `decision_step()`, I reconstructed the if/else decision tree into a more readable state machine calls that contains smaller code pieces to deal with its specific functions. Also, I adopted the idea that by applying an positive offset to the perceived mean angle, the Rover could steer itself as a left-side walk crawler. The first thing I noticed was since Rover starts with a random orientation, there's some chance it would loop around obstacles in the beginning if it went into walk crawler mode directly. To tackle this problem, I added an `init` state that forcing Rover to go straight forward in the first 3 seconds. Since by then the Rover got an acceptable result in map searching and sample identifying, I then decided to make the Rover to gather up samples. So I added a `sample` state to the state machine which makes Rover decelerating and approaching rock samples slowly when it finds a rock lies in front of its left side.

#### 2. Launching in autonomous mode your rover can navigate and map autonomously.  Explain your results and how you might improve them in your writeup.  

Applied `perception` and `decision` processes above, the Rover could navigate itself along left side wall. The fidelity is above 70% in most cases. And the Rover has the ability to collect rock samples. However, following issues remain to tackle with if I were to pursue this challenge later. First, it still has some change running into loops around obstacles in the map center. Most of the time, it can get itself out of stuck situations, but this is not guaranteed in every case. These two shortcomings list above requires a more robust and smarter *unstuck* logic. Second, the Rover should navigate along the wall closer, for I found there're some changes it couldn't perceive the sample when it's kind of hiding behind an obstacle. Last but not least, I haven't implemented the return to base procedure yet, which is a big challenge for me considering my short knowledge about optimal path planning.


#### System settings
OS: macOS 10.13

Resolution: 800 x 600

Graphics Quality: Good

FPS: 35 ~ 40
