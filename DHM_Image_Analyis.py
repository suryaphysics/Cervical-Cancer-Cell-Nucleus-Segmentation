
#************* Code by Surya Kamal to Create a GUI based tool to automate Image Processing & Analysis process *************
                            #******** for the Detection of Cervical Cancer Cells *********


#          FUNCTIONS USED   |  FUNCTIONALITY
#       ------------------- | ------------------
#                           |
#       __ init__()         :->      To Initialize main thread to create and pack the Application Frame
#       create_widgets()    :->      To create all the components and widgets in the GUI
#       selectImage()       :->      To open a dialog box to select an Image file and display its path in the TextBox
#       imageReconstruct3D():->      To display the selected Image,crop the desired nuclei,
#                                    select the corresponding Phase Image and Display its Reconstruction in 3D
#       cropRect()          :->      To crop the desired rectangular region in an Image



#********** Import Different Libraries and Instansiate classes to call inbuilt functions ***********
import csv
from tkinter import filedialog          # Browse dialog box to select Image for Processing
import tkinter as tk                    # tk object created of class tkinter to call the inbuilt functions of the class
import numpy as np                      # np object created of class numpy to call the inbuilt functions of the class
import cv2                              # cv2 object of python-opencv library
import matplotlib.pyplot as plt         # plt object of class matplotlib library
import matplotlib.widgets as widgets    # widgets of matplotlib library
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from scipy import ndimage
from skimage import measure

#********** Main Application class containing all the functions ***********

class Application(tk.Frame):            # class defined for the Application and GUI Integration


    #********** init function to initialize all objects and functions ***********
    def __init__(self, master=None):
        super().__init__(master)
        self.pack(fill="both", expand=1)# pack function to Integrate the Buttons,Textbox,etc in the main Frame of GUI
        self.create_widgets()           # Initializing and calling function to create all widgets defined within the function



    #********** Definition of function to create all widgets( buttons, textbox,etc.) **********
    def create_widgets(self):

        self.label = tk.Label(self)     # Label object created
        self.label["text"] = "SELECT IMAGE FOR CELL ANALYSIS  " # Text to display above browse button
        self.label["bg"] = "white"      # Background Color of the text Label
        self.label["fg"] = "red"        # Font color of the text
        self.pack()                     # Integrating the label to main Frame of the GUI
        self.label.place(relx=0.5, rely=0.2, anchor="center")   # Position of the Label


        self.textBox = tk.Entry(self, width=39) # Textbox object created
        self.pack()                     # Integrating the Textbox to main Frame of the GUI
        self.textBox.place(relx=0.39, rely=0.35, anchor="center")   # Position of the Textbox


        self.button1 = tk.Button(self)  # Button object created
        self.button1["text"] = "Browse" # Name of the button
        self.button1["command"] = self.selectImage  # Function to be called on clicking the button
        self.button1.pack()             # Integrating the button to the main Frame of the GUI
        self.button1.place(relx=0.85, rely=0.35, anchor="center")   # Position of the Button


        self.button2 = tk.Button(self)  # Button object created
        self.button2["text"] = "Start Analysis" # Name of the button
        self.button2["fg"] = "green"    # Color of the text of the button
        self.button2["command"] = self.imageReconstruct3D # Function to be called on clicking the button
        self.button2.pack()             # Integrating the button to the main Frame of the GUI
        self.button2.place(relx=0.85, rely=0.5, anchor="center")    # Position of the Button


        self.quit = tk.Button(self, text="QUIT", fg="red",	# Button object created with functionality to exit the window
                              command=root.destroy)
        self.quit.pack()                # Integrating the button to the main Frame of the GUI
        self.quit.place(relx=0.5, rely=0.85, anchor="center")   # Position of the Button



    #*********** Definition of function which is called when Browse Button is clicked ***********
    def selectImage(self):

        self.textBox.delete(0, 'end')   # Clear the textBox whenever a new file has to be selected
        filename = filedialog.askopenfilename(filetypes=[("allfiles", "*"), ("pythonfiles", "*.txt")],  # dialog box which returns the full path of the selected Image
                                              title='Choose an Image file')
        self.textBox.insert(0, filename)# Inserting the path of the selected Image in the textbox



    #*********** Definition of function which is called when Start Analysis Button is clicked ***********
    def imageReconstruct3D(self):

        fileName = self.textBox.get()

        def cropRect(eclick, erelease):
            if eclick.ydata > erelease.ydata:
                eclick.ydata, erelease.ydata = erelease.ydata, eclick.ydata
            if eclick.xdata > erelease.xdata:
                eclick.xdata, erelease.xdata = erelease.xdata, eclick.xdata

            plt.close(fig)
            croppedImage = im[eclick.ydata.astype(int):erelease.ydata.astype(int),
                             eclick.xdata.astype(int):erelease.xdata.astype(int)]
            cv2.imwrite('croped.png', croppedImage)


            newImage = cv2.imread('croped.png', 0)
            blur = cv2.GaussianBlur(newImage, (5, 5), 0)
            ret, thOtsu = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)


            # Select Raw Image
            phaseFile = filedialog.askopenfilename(filetypes=[("allfiles", "*"), ("pythonfiles", "*.txt")],title='Choose a Phase Image file')

            fd = open(phaseFile,'rb')
            rows = arr.shape[0]
            cols = arr.shape[1]
            f = np.fromfile(fd, dtype=np.float32, count=rows * cols)
            phIm = f.reshape((rows, cols))  # notice row, column format
            fd.close()
            phIm = phIm[eclick.ydata.astype(int):erelease.ydata.astype(int),
                   eclick.xdata.astype(int): erelease.xdata.astype(int)]



            # Labelling
            label_im, nb_labels = ndimage.label(thOtsu)


            # Biggest Label selection
            sizes = ndimage.sum(thOtsu, label_im, range(1, nb_labels + 1))
            map = np.where(sizes == sizes.max())[0] + 1
            max_index = np.zeros(nb_labels + 1, np.uint8)
            max_index[map] = 1
            max_feature = max_index[label_im]

            finalBinary=ndimage.binary_fill_holes(max_feature)

            area_pixel_count = np.count_nonzero(finalBinary)

            maskedPhIm = np.multiply(phIm, finalBinary)

            sobelx = cv2.Sobel(maskedPhIm, cv2.CV_64F, 1,0, ksize=5)
            sobely = cv2.Sobel(maskedPhIm, cv2.CV_64F, 0, 1, ksize=5)


            #plt.subplot(161),plt.title('Selected Nucleus'),plt.imshow(croppedImage,'gray')
            #plt.subplot(162),plt.title('Thresholding'),plt.imshow(thOtsu,'gray')
            #plt.subplot(163),plt.title('Labelled'), plt.imshow(label_im, 'spectral'),plt.contour(label_im, [0.5], linewidths=2, colors='r')
            #plt.subplot(164),plt.title('Biggest Label'), plt.imshow(max_feature, 'gray')
            plt.subplot(221),plt.title('Final Binary'), plt.imshow(finalBinary, 'gray')
            plt.subplot(222),plt.title('Raw Image'), plt.imshow(maskedPhIm, 'gray')
            plt.subplot(223), plt.title('Sobel x'), plt.imshow(abs(sobelx), 'gray')
            plt.subplot(224), plt.title('Sobel y'), plt.imshow(abs(sobely), 'gray')

            TV = np.sum(np.sqrt(np.square(abs(sobelx)) + np.square(abs(sobely))))/area_pixel_count
            nonzero_index = np.nonzero(maskedPhIm)
            Volume = area_pixel_count


            print(TV,area_pixel_count)
            #newFile = fileName
            #with open("Output.csv", "a") as text_file:
            #    text_file.write("%s," % TV)

            xx, yy = np.mgrid[0:maskedPhIm.shape[0], 0:maskedPhIm.shape[1]]
            fig1 = plt.figure()
            ax1 = fig1.gca(projection='3d')
            ax1.plot_surface(xx, yy, maskedPhIm, rstride=1, cstride=1, cmap=plt.cm.spectral,
                            linewidth=0)

            plt.show()


        im = cv2.imread(fileName)
        fig = plt.figure()
        ax = fig.add_subplot(111)
        arr = np.asarray(im)
        plt_image = plt.imshow(arr)
        rs = widgets.RectangleSelector(ax, cropRect, drawtype='box',rectprops=dict(facecolor='white', edgecolor='white', alpha=0.1,
                                        fill=True))

        plt.show()

#********** Starting point of the Execution of Code ***********

root = tk.Tk()  # root object created of Tkinter class
root.title("Cancer Cell Detection Tool")   # Title of the User Interface
root.geometry("350x350")    # Dimension of the Main Window of the UI

app = Application(master=root)  # class object created and tkinter object is passed in the Application class
app.mainloop()  # mainloop function keeps the application running
