# Imports
import cv2
from easyocr import Reader
import easyocr
import re
from cam import Webcam
from PIL import ImageTk,Image as PILImage, ImageOps

# Tkinter for GUI
from tkinter import *

# Global variable for cam
cam = cv2.VideoCapture(0)

# Variable for license plate text
lisenceplate = ""
class Window(Frame):
	def __init__(self, master=None):
		Frame.__init__(self, master)
		self.master = master
		self.pack(fill=BOTH, expand=1)

		# Main label
		self.Heading = Label(self, text="OpenCV nummerplade læser", font=("Helvetica", 22, "bold"))
		self.Heading.place(x=400,y=20, anchor=CENTER)

		# Button to read license plate
		self.ReadLicensePlateButton = Button(self, text="Start", command=lambda:readLicensePlate(self))
		self.ReadLicensePlateButton.place(x=400,y=130, anchor="center")

		# License plate label
		self.licenseText = Label(self, text="...", font=("Helvetica", 16, "bold"))
		self.licenseText.place(x=400,y=160, anchor="center")


# Create GUI
root = Tk()
app = Window(root)
root.wm_title("Read license plate")
root.geometry("800x600")
# set window background color
root.configure(bg='lightgray')

def show_camera():

	# Create a Label to capture the Video frames
	label = Label(app)
	label.grid(row=0, column=0)
	label.place(x=400,y=300, anchor="center")
	
	# Check if cam is open
	if cam.isOpened() == 0:
		# Open cam
		cam.open()

	# Create label
	root.LiveCam = label

	# Show frames
	show_frames()

def restart_app():
	# Destroy previously captured image
	app.imgPanel.destroy()
	show_camera()

def kill_camera():
	cam.release
	root.LiveCam.destroy()

# Define function to show frame
def show_frames():
	if (root.LiveCam.winfo_exists() == 0):
		cam.release
		root.LiveCam.destroy()
		return
	# Get the latest frame and convert into Image
	cv2image = cv2.cvtColor(cam.read()[1],cv2.COLOR_BGR2RGB)
	img = PILImage.fromarray(cv2image).resize((300, 200))
	# Convert image to PhotoImage
	imgtk = ImageTk.PhotoImage(image = img)
	root.LiveCam.imgtk = imgtk
	root.LiveCam.configure(image=imgtk)

	# Repeat after an interval to capture continiously
	root.LiveCam.after(20, show_frames)

# Function for reading license plate
def readLicensePlate(self):

	# Update status
	self.licenseText.config(text="Læser nummerplade...")
	self.update()

	# Read image
	# Create variable that holds path for image
	filepath = "./pictures/284726492_1067947430484623_4755717909050278760_n.png"
	#filepath = "./pictures/313888430_676020084051290_6385229983960281955_n.jpg"
	#filepath ="./pictures/315455089_827896401877279_2855901142268397829_n.jpg"
	#filepath ="./pictures/315519545_3340712862818449_5419462414207795362_n.jpg"
	#filepath ="./pictures/315521287_544667254166335_5959194763568534518_n.jpg"
	#filepath ="./pictures/315518199_814526446486979_6015829447265578044_n.jpg"

	# Load image form filepath
	#loadedImage = cv2.imread(filepath)
	loadedImage = Webcam(cam)
	originalImage = loadedImage

	# Kill live camera
	cam.release
	root.LiveCam.destroy()

	# Show image
	#self.canvas = Canvas(root, width = 300, height = 300)
	#self.canvas.pack()
	#imgPIL = PILImage.open(filepath)
	imgPIL = PILImage.fromarray(loadedImage)
	imgPIL = ImageOps.fit(imgPIL, (600, 300), method = 0, bleed = 0.0, centering = (0.5, 0.5))
	img = ImageTk.PhotoImage(imgPIL)
	#img.resize((100, 50), Image.ANTIALIAS)
	#img.place(x=400,y=400, anchor="center")
	#self.canvas.create_image(20, 20, anchor="center", image=img)
	self.imgPanel = Label(root, image=img)
	self.imgPanel.image = img
	#self.imgPanel.pack(side = "bottom", fill = "both", expand = "yes")
	#self.imgPanel.place(x=400,y=400, anchor="center")
	self.imgPanel.place(x=400,y=200, anchor=N)
	self.imgPanel.update()

	# Crate variables for alpha and beta
	alpha = 1.5 # Contrast control (1.0-3.0)
	beta = 40 # Brightness control (0-100)

	# Load image and reize
	loadedImage = cv2.convertScaleAbs(ResizeWithAspectRatio(crop_img(loadedImage,0.53), 300, 300), alpha=alpha, beta=beta)

	# Crate blue image
	blueImage = cv2.cvtColor(loadedImage,cv2.COLOR_RGB2BGR)

	# Create backtoback image
	backtoback = cv2.cvtColor(blueImage,cv2.COLOR_HSV2RGB)

	# Create gray image
	greyImg = cv2.cvtColor(backtoback,cv2.COLOR_BGR2GRAY)

	# Create blur
	blur = cv2.GaussianBlur(greyImg, (5,5), 0) 

	# Create with threshold
	ret, Image = cv2.threshold(greyImg, 60 ,255,cv2.THRESH_BINARY)

	# Create edged image
	edged = cv2.Canny(blur, 30, 200) 

	# Open images in a new window
	""" cv2.imshow("testImage",loadedImage)
	cv2.imshow("TestImage2",edged)
	cv2.imshow("tester", greyImg) """

	# Initialize reader
	reader = Reader(['en'])

	# loop over edged image for detection
	# detect the text from the license plate
	detection = reader.readtext(edged)
	if len(detection)>0:
		for text in detection: 
			plate = Regex(text[1].replace(" ", ""))
			if len(plate) ==7 and checkifLisencePlate(plate):
				lisenceplate = plate  

	# Loop over the original image for detection
	detection = reader.readtext(Image)
	if len(detection)>0:
		for text in detection: 
			plate = Regex(text[1].replace(" ", ""))
			if len(plate) ==7 and checkifLisencePlate(plate):
				lisenceplate = plate

	# Loop over
	detection = reader.readtext(loadedImage)
	if len(detection)>0:
		for text in detection: 
			plate = Regex(text[1].replace(" ", ""))
			if len(plate) ==7 and checkifLisencePlate(plate):
				lisenceplate = plate

	# Loop over
	detection = reader.readtext(originalImage)
	if len(detection)>0:
		for text in detection: 
			plate = Regex(text[1].replace(" ", ""))
			if len(plate) ==7 and checkifLisencePlate(plate):
				lisenceplate = plate

	# Print license plate if found
	if lisenceplate != "":
		if len(lisenceplate):
			self.licenseText.config(text=lisenceplate)
			print(lisenceplate)
		else:
			self.licenseText.config(text="Ingen nummerplade fundet")
			print("Ingen nummerplade fundet")
	else:
		self.licenseText.config(text="Ingen nummerplade fundet")
		print("Ingen nummerplade fundet")

	# Update start button to restart application
	self.ReadLicensePlateButton.config(text="Restart", command=lambda:restart_app())
	self.ReadLicensePlateButton.update()

# Regex
def Regex(txt):
    x = re.sub( "\W", "", txt)
    return x

# Function for resizing image
def ResizeWithAspectRatio(image, width=None, height=None, inter=cv2.INTER_AREA):
    dim = None
    (h, w) = image.shape[:2]

    if width is None and height is None:
        return image
    if width is None:
        r = height / float(h)
        dim = (int(w * r), height)
    else:
        r = width / float(w)
        dim = (width, int(h * r))

    return cv2.resize(image, dim, interpolation=inter)

# Function for cropping image
def crop_img(img, scale=1.0):
    center_x, center_y = img.shape[1] / 2, img.shape[0] / 2
    width_scaled, height_scaled = img.shape[1] * scale, img.shape[0] * scale
    left_x, right_x = center_x - width_scaled / 2, center_x + width_scaled / 2
    top_y, bottom_y = center_y - height_scaled / 2, center_y + height_scaled
    img_cropped = img[int(top_y):int(bottom_y), int(left_x):int(right_x)]
    return img_cropped

# Function for checking if lisence plate is valid
def checkifLisencePlate(string):
	# Check if string is valid
	if len(string) == 7:
		# Check if first 2 characters are letters
		if string[0].isalpha() and string[1].isalpha():
			# Check if last 5 characters are numbers
			if string[2:].isdigit():
				return True
	
	# Is not valid
	return False

# Show live preview
show_camera()
# Main function
root.mainloop()
