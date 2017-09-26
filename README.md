# Cervical-Cancer-Cell-Nucleus-Segmentation
A tool in python using OpenCV to read the bright-field image data and the phase image data recovered from a Digital holographic microscope (DHM)[1] and segment the nuclei to calculate physical parameters like roughness and volume using Total variation.

# Details
1. 1.png - sample image for stage 1 cervical cancer cells (data from AIIMS, New Delhi, India).
2. 1a.pngresult2 -phase image data recovered using a DHM 
3. DHM_Image_Analysis.py - ktinker based GUI in python, which provides interface to select and segment nuclei from cell images using OpenCV.

# Usage
1. Run the code.
2. Select and open '1.png' image file from the prompted GUI.
3. Select the rectangular area to segment.
4. Then finally select the corresponding raw phase data.

# Citation
[1] Khare, Kedar & p t, Samsheerali & Joseph, Joby. (2013). Single shot high resolution digital holography. Optics express. 21. 2581-2591. 10.1364/OE.21.002581. We demonstrate a novel computational method for high resolution image recovery from a single digital hologram frame. The complex object field is obtained from the recorded hologram by solving a constrained optimization problem. This approach which is unlike the physical hologram replay process is shown to provide high quality image recovery even when the dc and the cross terms in the hologram overlap in the Fourier domain. Experimental results are shown for a Fresnel zone hologram of a resolution chart, intentionally recorded with a small off-axis reference beam angle. Excellent image recovery is observed without the presence of dc or twin image terms and with minimal speckle noise.
