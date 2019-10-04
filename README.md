# PyMotion
A program that is run on raspberry Pi zero for motion detection taking sequential snapshots of the world.

This program compares two low resolution images (for speed) and  if a threshold of total motion is reach a fullsize photo is taken.

4th Oct 2019
my intial upload of something that is working. 
Running the software in shell will display an array of the image differences in text mode.
if threshold of pixel differences is reach a photo is taken.

Issues
* Very sensitive,  will pick up small movements over the entirety of the image.  Maybe threshold the pixel array and only pic up big differences.
World like to add time and date to the image.
