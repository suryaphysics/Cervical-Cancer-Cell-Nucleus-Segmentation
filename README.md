# Cervical-Cancer-Cell-Nucleus-Segmentation
A small tool in python to read the bright-field image data and the phase image data recovered from a Digital holographic microscope (DHM) and segment the nuclei to calculate physical parameters like roughness and volume.

# Details
1. 1.png - sample image for stage 1 cervical cancer cells (data from AIIMS, New Delhi, India).
2. 1a.pngresult2 -phase image data recovered using a DHM 
3. DHM_Image_Analysis.py - ktinker based GUI in python, which provides interface to select and segment nuclei from cell images using OpenCV.

# Usage
1. Run the code.
2. Select and open '1.png' image file from the prompted GUI.
3. Select the rectangular area to segment.
4. Then finally select the corresponding raw phase data.
