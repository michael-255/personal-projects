#######################################
#                                     #
#     Example PiCamera Program        #
#                                     #
#######################################

import os
import time
import datetime
import picamera
from Tkinter import *
from ttk import Style, Label, Combobox

# DEBUG OPTION - Adds a DEBUG button to the UI
_debug = True

# Container class for widgets
class PiCamInterface(Frame):
    # Initializations
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent # Tk root window
            
        # Program Variables
        self._resolution  = IntVar()
        self._hflip       = IntVar()
        self._vflip       = IntVar()
        self._brightness  = IntVar()
        self._contrast    = IntVar()
        self._previewTime = DoubleVar()
        self._recordTime  = DoubleVar()
        self._expoOpt     = StringVar()
        self._imageOpt    = StringVar()

        self.InitializeUI()
        

    #----------Setup Interface
    def InitializeUI(self):      
        self.parent.title("PiCamera Interface")
        self.style = Style()
        self.style.theme_use("clam") # default, clam, alt, classic
        self.pack(fill=BOTH, expand=1)

        # Layout
        frameResolution = Frame(self, relief=RAISED, borderwidth=1)
        frameOptions    = Frame(self, relief=RAISED, borderwidth=1)
        frameOptions1   = Frame(frameOptions, relief=RAISED, borderwidth=1)
        frameOptions2   = Frame(frameOptions, relief=RAISED, borderwidth=1)
        frameOptions3   = Frame(frameOptions, relief=RAISED, borderwidth=1)
        frameScales     = Frame(self, relief=RAISED, borderwidth=1)
        frameButtons    = Frame(self, relief=RAISED, borderwidth=1)

        #
        # CAMERA OPTIONS
        #
        # Left Frame []--
        labelOptions1 = Label(frameOptions1, text="Exposure Modes")
        comboExpoOpt = Combobox(frameOptions1, state='readonly', textvariable=self._expoOpt,
                                width=12)
        comboExpoOpt['values'] = ('off', 'auto', 'night', 'nightpreview', 'backlight',
                                  'spotlight', 'sports', 'snow', 'beach', 'verylong',
                                  'fixedfps', 'antishake', 'fireworks')
        # Center Frame -[]-
        labelOptions2 = Label(frameOptions2, text="Image Effects")
        comboImageOpt = Combobox(frameOptions2, state='readonly',textvariable=self._imageOpt,
                                 width=12)
        comboImageOpt['values'] = ('none', 'negative', 'solarize', 'sketch', 'denoise',
                                   'emboss', 'oilpaint', 'hatch', 'gpen', 'pastel',
                                   'watercolor', 'film', 'blur', 'saturation', 'colorswap',
                                   'washedout', 'posterise', 'colorpoint', 'colorbalance',
                                   'cartoon', 'deinterlace1', 'deinterlace2')
        # Right Frame --[]
        labelOptions3 = Label(frameOptions3, text="Misc. Options")
        check1 = Checkbutton(frameOptions3, text="Flip Horizontally", variable=self._hflip,
                             onvalue=True, offvalue=False, padx=4, pady=4)
        check2 = Checkbutton(frameOptions3, text="Flip Vertically", variable=self._vflip,
                             onvalue=True, offvalue=False, padx=4, pady=4)
        
        # Pack frameOptions
        frameOptions.pack(fill=BOTH, side=TOP)
        frameOptions1.pack(fill=BOTH, side=LEFT, expand=True)
        frameOptions2.pack(fill=BOTH, side=LEFT, expand=True)
        frameOptions3.pack(fill=BOTH, side=LEFT, expand=True)
        labelOptions1.pack(side=TOP)
        labelOptions2.pack(side=TOP)
        labelOptions3.pack(side=TOP)
        comboExpoOpt.pack(side=TOP)    
        comboImageOpt.pack(side=TOP)
        check1.pack(side=TOP)
        check2.pack(side=TOP)

        #
        # PICTURE RESOLUTION
        #
        labelResolution = Label(frameResolution, text="Picture Resolution")       
        R1 = Radiobutton(frameResolution, text="640 x 480", variable=self._resolution,
                         value=1, padx=8, pady=8)
        R2 = Radiobutton(frameResolution, text="1280 x 720", variable=self._resolution,
                         value=2, padx=8, pady=8)
        R3 = Radiobutton(frameResolution, text="1920 x 1080", variable=self._resolution,
                         value=3, padx=8, pady=8)
        R4 = Radiobutton(frameResolution, text="2592 x 1944", variable=self._resolution,
                         value=4, padx=8, pady=8)

        # Pack frameResolution
        frameResolution.pack(fill=BOTH, side=TOP)
        labelResolution.pack(fill=BOTH, side=TOP)
        R1.pack(side=LEFT)
        R2.pack(side=LEFT)
        R3.pack(side=LEFT)
        R4.pack(side=LEFT)

        #
        # SCALABLE SETTINGS (sliders)
        #
        labelScales = Label(frameScales, text="Scalable Settings")
        scaleRecord = Scale(frameScales, label="Recording Time (sec)", variable=self._recordTime,
                            resolution=0.5, from_=5, to=30, orient=HORIZONTAL, length=400)
        scalePreview = Scale(frameScales, label="Preview Time (sec)", variable=self._previewTime,
                          resolution=0.1, from_=1, to=10, orient=HORIZONTAL, length=400)
        scaleBright = Scale(frameScales, label="Brightness", variable=self._brightness,
                            resolution=1, from_=0, to=100, orient=HORIZONTAL,  length=400)
        scaleContrast = Scale(frameScales, label="Contrast", variable=self._contrast,
                            resolution=1, from_=-100, to=100, orient=HORIZONTAL,  length=400)

        # Pack frameScales
        frameScales.pack(fill=BOTH, side=TOP)
        labelScales.pack(fill=BOTH, side=TOP)
        scaleRecord.pack(side=TOP)
        scalePreview.pack(side=TOP)
        scaleBright.pack(side=TOP)
        scaleContrast.pack(side=TOP)

        #
        # BUTTONS
        #
        labelSpacer = Label(frameButtons)
        quitButton = Button(frameButtons, text="Quit", command=quit)
        button1 = Button(frameButtons, text="Take Picture", command=self.Picture)
        button2 = Button(frameButtons, text="Take Video", command=self.Video)
        button3 = Button(frameButtons, text="Defaults", command=self.Defaults)
        if _debug == True:
            buttonDebug = Button(frameButtons, text="DEBUG", command=self.Debug)

        # Pack frameButtons
        frameButtons.pack(fill=BOTH, side=TOP, expand=True)
        labelSpacer.pack()
        button1.pack(side=LEFT, anchor=NW)
        button2.pack(side=LEFT, anchor=NW)
        button3.pack(side=LEFT, anchor=NW)
        quitButton.pack(side=RIGHT, anchor=NE)
        if _debug == True:
            buttonDebug.pack(side=RIGHT, anchor=NE)

        # Start with default settings
        self.Defaults()

        
    #----------Single image capture function
    def Picture(self):
        print "-----Preparing Camera (Picture)-----"
        # Activating the PiCamera
        self.camera = picamera.PiCamera()

        # Update settings before taking picture
        self.Settings()

        # Use time to make a unique filename     
        now = datetime.datetime.now()
        _picname = "pipicture" + str(now.microsecond) + ".jpg"
        
        self.camera.start_preview()
        time.sleep( self._previewTime.get() )
        self.camera.stop_preview()
        self.camera.capture( _picname )
        print "Capturing picture: " + _picname        

        # Close camera to perserve CPU cycles and battery life
        self.camera.close()

        # Open image with gpicview
        print "Opening preview of image: " + _picname
        os.system("gpicview " + _picname)


    #----------Video capture function
    def Video(self):
        print "-----Preparing Camera (Video)-----"
        # Activating the PiCamera
        self.camera = picamera.PiCamera()

        # Update settings before taking video
        self.Settings()
        
        # Use time to make a unique filename     
        now = datetime.datetime.now()
        _vidname = "pivideo" + str(now.microsecond) + ".h264"

        self.camera.start_preview()     
        self.camera.start_recording( _vidname )
        self.camera.wait_recording( self._recordTime.get() )
        self.camera.stop_recording()
        self.camera.stop_preview()
        print "Capturing video: " + _vidname  
        
        # Close camera to perserve CPU cycles and battery life
        self.camera.close()

        # Open image with gpicview
        print "Playing preview of video: " + _vidname
        os.system("omxplayer --win '0 0 320 240' " + _vidname)
      

    #----------Restore default settings
    def Defaults(self):
        self._resolution.set(1)
        self._hflip.set(0)
        self._vflip.set(0)
        self._brightness.set(50)
        self._contrast.set(0)
        self._recordTime.set(5.0)
        self._previewTime.set(1.0)
        self._expoOpt.set('auto')
        self._imageOpt.set('none')
        print "Default settings restored"
                

    #----------Only usable if _debug = True
    def Debug(self):
        print "------VARIABLE INFORMATION------"
        print "  Exposure Mode: " + self._expoOpt.get()
        print "   Image Effect: " + self._imageOpt.get()
        print "Horizontal Flip: " + str(self._hflip.get())
        print "   Radio Button: " + str(self._resolution.get())
        print " Recording Time: " + str(self._recordTime.get())
        print "   Preview Time: " + str(self._previewTime.get())
        print "     Brightness: " + str(self._brightness.get())
        print "       Contrast: " + str(self._contrast.get())


    #----------Loads all appropriate settings for the camera
    def Settings(self):
        if self._resolution.get() == 1:
            self.camera.resolution = (640, 480)
            print "Camera resolution set to 640 x 480"
        if self._resolution.get() == 2:
            self.camera.resolution = (1280, 720)
            print "Camera resolution set to 1280 x 720"
        if self._resolution.get() == 3:
            self.camera.resolution = (1920, 1080)
            print "Camera resolution set to 1920 x 1080"
        if self._resolution.get() == 4:
            self.camera.resolution = (2592, 1944)
            print "Camera resolution set to 2592 x 1944"
            
        if self._hflip.get() == True:
            self.camera.hflip = True
        else:
            self.camera.hflip = False
            
        if self._vflip.get() == True:
            self.camera.vflip = True
        else:
            self.camera.vflip = False

        self.camera.brightness    = self._brightness.get()
        self.camera.contrast      = self._contrast.get()
        self.camera.exposure_mode = self._expoOpt.get()
        self.camera.image_effect  = self._imageOpt.get()
        print "Camera settings updated"
        

########## MAIN ##########
def main():
    root = Tk()
    root.geometry("+40+40") # Initial window position
    app = PiCamInterface(root)
    root.mainloop()
    

if __name__ == '__main__':
    main()
    
# END OF FILE
