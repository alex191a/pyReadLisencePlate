
from tkinter import *

# Window 
class MainWindow(Frame):
	def __init__(self, master=None):
		Frame.__init__(self, master)
		self.master = master
		self.pack(fill=BOTH, expand=1)
		self.configure(background='white', width=500, height=500)

		self.frame = lambda:start



# Tkinter init
root = Tk()

# Create windows
app = MainWindow(root)

# Other stuff
root.title("OpenCV - Frames test")
root.geometry("800x600")

# Command for switching frames
def show_frame(frame):
	
	app.frame.destroy()

	# Assign new frame
	app.frame = frame

	# Show frame
	app.frame.pack()

# Create some frames
start = Frame(app, width=800, height=600, bg="lightblue")
# Create buttons
start.button1 = Button(app, text="Button 1", command=lambda:show_frame(frame1))
start.button2 = Button(app, text="Button 2", command=lambda:show_frame(frame2))
start.button1.place(x=100,y=100)
start.button2.place(x=100,y=200)

frame1 = Frame(app, width=800, height=600, bg="lightgray")
frame1.button = Button(start, text="Start", command=lambda:show_frame(start))
frame1.button.place(x=100,y=100)


frame2 = Frame(app, width=800, height=600, bg="red")
frame2.button = Button(start, text="Start", command=lambda:show_frame(start))
frame2.button.place(x=100,y=100)


# Main loop
root.mainloop()
