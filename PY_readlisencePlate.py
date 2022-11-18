
import cv2
from easyocr import Reader
import re
from cam import Webcam

def Regex(txt):
    x = re.sub( "\W", "", txt)
    return x
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
def crop_img(img, scale=1.0):
    center_x, center_y = img.shape[1] / 2, img.shape[0] / 2
    width_scaled, height_scaled = img.shape[1] * scale, img.shape[0] * scale
    left_x, right_x = center_x - width_scaled / 2, center_x + width_scaled / 2
    top_y, bottom_y = center_y - height_scaled / 2, center_y + height_scaled
    img_cropped = img[int(top_y):int(bottom_y), int(left_x):int(right_x)]
    return img_cropped

print("fuck")
#filepath = "./pictures/284726492_1067947430484623_4755717909050278760_n.png"
#filepath = "./pictures/313888430_676020084051290_6385229983960281955_n.jpg"
#filepath ="./pictures/315455089_827896401877279_2855901142268397829_n.jpg"
#filepath ="./pictures/315519545_3340712862818449_5419462414207795362_n.jpg"
#filepath ="./pictures/315521287_544667254166335_5959194763568534518_n.jpg"
#filepath ="./pictures/315518199_814526446486979_6015829447265578044_n.jpg"
#loadedImage = cv2.imread(filepath)

loadedImage = Webcam()

originalImage = loadedImage

alpha = 1.5 # Contrast control (1.0-3.0)
beta = 40 # Brightness control (0-100)


loadedImage = crop_img(loadedImage,0.53)
loadedImage = ResizeWithAspectRatio(loadedImage, 300, 300)
loadedImage = cv2.convertScaleAbs(loadedImage, alpha=alpha, beta=beta)
blueImage = cv2.cvtColor(loadedImage,cv2.COLOR_RGB2BGR)
backtoback = cv2.cvtColor(blueImage,cv2.COLOR_HSV2RGB)

greyImg = cv2.cvtColor(backtoback,cv2.COLOR_BGR2GRAY)

blur = cv2.GaussianBlur(greyImg, (5,5), 0) 

ret, Image = cv2.threshold(greyImg, 60 ,255,cv2.THRESH_BINARY) #29



edged = cv2.Canny(blur, 30, 200) 
cv2.imshow("testImage",loadedImage)
cv2.imshow("TestImage2",edged)
cv2.imshow("tester", greyImg)
reader = Reader(['en'])
# detect the text from the license plate
detection = reader.readtext(edged)
lisenceplate =""
if len(detection)>0:
    for text in detection: 
        plate = Regex(text[1].replace(" ", ""))
        if len(plate) ==7:
            lisenceplate = plate  
detection = reader.readtext(Image)
if len(detection)>0:
    for text in detection: 
        plate = Regex(text[1].replace(" ", ""))
        if len(plate) ==7:
           lisenceplate = plate  
detection = reader.readtext(loadedImage)
if len(detection)>0:
    for text in detection: 
        plate = Regex(text[1].replace(" ", ""))
        if len(plate) ==7:
            lisenceplate = plate
detection = reader.readtext(originalImage)
if len(detection)>0:
    for text in detection: 
        plate = Regex(text[1].replace(" ", ""))
        if len(plate) ==7:
            lisenceplate = plate
if len(lisenceplate):
    print(lisenceplate)
cv2.waitKey(0)
cv2.destroyAllWindows()
