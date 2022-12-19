# Imports
import copy
import cv2
from easyocr import Reader
import easyocr
import re
from lib import cam as WebCam
from lib import api
from PIL import ImageTk,Image as PILImage, ImageOps

# Tkinter for GUI
# from tkinter import *

import customtkinter as tk

# Global variable for cam
cam = cv2.VideoCapture(0)

# Boolean debug mode
debug = False

# Variable for license plate text
class Window(tk.CTkFrame):
	def __init__(self, master=None):
		tk.CTkFrame.__init__(self, master)
		self.master = master
		self.pack(fill=tk.BOTH, expand=1)
		self.configure(background='white', width=800, height=600)

		# Main label
		self.Heading = tk.CTkLabel(self, text="OpenCV nummerplade læser", text_font=("Helvetica", 22, "bold"))
		self.Heading.place(relx=0.5,y=25, anchor=tk.CENTER)

		# Button to read license plate
		self.ReadLicensePlateButton = tk.CTkButton(self, text="Start", command=lambda:readLicensePlate(self))
		self.ReadLicensePlateButton.place(relx=0.5,y=110, anchor="center")

		# License plate label
		self.licenseText = tk.CTkLabel(self, text="...", text_font=("Helvetica", 12, "bold"))
		self.licenseText.place(relx=0.5,y=160, anchor="center")

        # Is police label
		self.isPolice = tk.CTkLabel(self, text="...", text_font=("Helvetica", 12, "normal"))
		self.isPolice.place(relx=0.5,y=180, anchor="center")

		# Label to show API status
		self.apiStatus = tk.CTkLabel(self, text="...", text_font=("Helvetica", 12, "normal"))
		self.apiStatus.place(x=0, rely=0.95, anchor="w")

		# Mail entry label
		self.mailEntryLabel = tk.CTkLabel(self, text="Mail:", text_font=("Helvetica", 12, "normal"))
		self.mailEntryLabel.place(relx=0.5,y=420, anchor="center")

		# Mail entry
		self.mailEntry = tk.CTkEntry(self, width=200)
		self.mailEntry.place(relx=0.5,y=440, anchor="center")

# Create GUI
root = tk.CTk()
root.resizable(False, False)

app = Window(root)
root.wm_title("Læs nummerplade med OpenCV" if debug == False else "DEBUG - Læs nummerplade med OpenCV")
# root.geometry("800x600")
# set window background color
root.configure(bg='lightgray')

def is_api_online():

	apiCheck = api.check_api_status()

	# Check if API is online
	if apiCheck["success"] == True:
		app.apiStatus.configure(text="Online", fg="#778899")
	else:
		app.apiStatus.configure(text="Offline" if debug == False else f"Offline - {apiCheck['status']}", fg="#f08080")

def show_camera():

	# Define button
	app.ReadLicensePlateButton.configure(text="Start", command=lambda:readLicensePlate(app))

	# Create a Label to capture the Video frames
	label = tk.CTkLabel(app)
	label.grid(row=0, column=0)
	label.place(relx=0.5,y=300, anchor="center")
	label.size = (300, 200)
	
	# Check if cam is open
	if cam.isOpened() == 0:
		# Open cam
		cam.open(0)

	# Create label
	app.LiveCam = label

	# Show frames
	show_frames()

def restart_app():
	# Destroy previously captured image
	app.imgPanel.destroy()
	show_camera()
	app.isPolice.configure(text="...")
	app.licenseText.configure(text="...")

def kill_camera():
	cam.release()
	app.LiveCam.destroy()

# Define function to show frame
def show_frames():
	if (app.LiveCam.winfo_exists() == 0):
		cam.release()
		app.LiveCam.destroy()
		return
	# Get the latest frame and convert into Image
	cv2image = cv2.cvtColor(crop_img(cam.read()[1],0.53),cv2.COLOR_BGR2RGB)
	img = PILImage.fromarray(cv2image).resize((300, 200))
	# Convert image to PhotoImage
	imgtk = ImageTk.PhotoImage(image = img)
	app.LiveCam.imgtk = imgtk
	app.LiveCam.configure(image=imgtk)

	# Repeat after an interval to capture continiously
	app.LiveCam.after(20, show_frames)

# Function for reading license plate
def readLicensePlate(self):

	# Check if mail is entered
	if self.mailEntry.get() == "":
		self.licenseText.configure(text="Indtast mail")
		return

	# Update status
	self.licenseText.configure(text="Læser nummerplade...")
	self.isPolice.configure(text="Tjekker politi...")
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
	originalImage = crop_img(WebCam.Webcam(cam),0.53)
	loadedImage = copy.copy(originalImage)

	# Kill live camera
	cam.release()
	app.LiveCam.destroy()

	# Show image
	#self.canvas = Canvas(root, width = 300, height = 300)
	#self.canvas.pack()
	#imgPIL = PILImage.open(filepath)
	imgPIL = PILImage.fromarray(cv2.cvtColor(originalImage.copy(),cv2.COLOR_BGR2RGB))
	imgPIL = ImageOps.fit(imgPIL, (300, 200), method = 0, bleed = 0.0, centering = (0.5, 0.5))
	img = ImageTk.PhotoImage(imgPIL)
	#img.resize((100, 50), Image.ANTIALIAS)
	#img.place(x=400,y=400, anchor="center")
	#self.canvas.create_image(20, 20, anchor="center", image=img)
	self.imgPanel = tk.CTkLabel(app, image=img)
	self.imgPanel.image = img
	#self.imgPanel.pack(side = "bottom", fill = "both", expand = "yes")
	#self.imgPanel.place(x=400,y=400, anchor="center")
	self.imgPanel.place(relx=0.5,y=200, anchor=tk.N)
	self.imgPanel.update()

	# Crate variables for alpha and beta
	alpha = 1.5 # Contrast control (1.0-3.0)
	beta = 40 # Brightness control (0-100)

	# Load image and reize
	# loadedImage = cv2.convertScaleAbs(ResizeWithAspectRatio(crop_img(loadedImage,0.53), 300, 300), alpha=alpha, beta=beta)

	# ResizedImage
	resizedImage = cv2.convertScaleAbs(ResizeWithAspectRatio(loadedImage, 300, 300), alpha=alpha, beta=beta)

	# Crate blue image
	blueImage = cv2.cvtColor(resizedImage, cv2.COLOR_RGB2BGR)

	# Create backtoback image
	backtoback = cv2.cvtColor(blueImage, cv2.COLOR_HSV2RGB)

	# Create gray image
	greyImg = cv2.cvtColor(backtoback, cv2.COLOR_BGR2GRAY)

	# Create blur
	blur = cv2.GaussianBlur(greyImg, (5,5), 0) 

	# Create with threshold
	ret, Image = cv2.threshold(greyImg, 60 ,255,cv2.THRESH_BINARY)

	# Create edged image
	edged = cv2.Canny(blur, 30, 200) 

	# Open images in a new window if debug mode is enabled
	if debug == True:
		cv2.imshow("Step 1: Resize",resizedImage)
		cv2.imshow("Step 2: Blue image",blueImage)
		cv2.imshow("Step 3: BackToBack",backtoback)
		cv2.imshow("Step 4: Greyscale", greyImg)
		cv2.imshow("Step 5: Threshold", Image)
		cv2.imshow("Step 6: Edged",edged)


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
	detection = reader.readtext(resizedImage)
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


	# Check if lisence plate is a police car
	if checkifLisencePlate(lisenceplate):

		# Update license plate UI
		if len(lisenceplate):
			self.licenseText.configure(text=lisenceplate)
			print(lisenceplate)
		else:
			self.isPolice.configure(text="...")
			self.licenseText.configure(text="Ingen nummerplade fundet")
			print("Ingen nummerplade fundet")

		# Check if license plate is police
		isPoliceCheck = api.IsPolice(lisenceplate, self.mailEntry.get())

		# Update police check	
		if isPoliceCheck["success"] == True:
			# Check if car is police owned
			if isPoliceCheck["IsPolice"] == True:
				print("is police")
				self.isPolice.configure(text="Politibil")
			else:
				print("is not police")
				self.isPolice.configure(text="Ikke politibil")
		# If error
		else:
			print("Error police check")
			self.isPolice.configure(text="Fejl: " + isPoliceCheck["status"])


	# Update start button to restart application
	self.ReadLicensePlateButton.configure(text="Genstart", command=lambda:restart_app(), state="normal")
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

# Run API Check
root.after(1000, lambda: is_api_online())

# Main function
root.mainloop()
