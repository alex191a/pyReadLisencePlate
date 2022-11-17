from email.mime import image
import cv2
import pytesseract
from easyocr import Reader
import numpy as np
def crop_img(img, scale=1.0):
    center_x, center_y = img.shape[1] / 2, img.shape[0] / 2
    width_scaled, height_scaled = img.shape[1] * scale, img.shape[0] * scale
    left_x, right_x = center_x - width_scaled / 2, center_x + width_scaled / 2
    top_y, bottom_y = center_y - height_scaled / 2, center_y + height_scaled
    img_cropped = img[int(top_y):int(bottom_y), int(left_x):int(right_x)]
    return img_cropped


def gammaCorrection(img):
    ## [changing-contrast-brightness-gamma-correction]
    lookUpTable = np.empty((1,256), np.uint8)
    for i in range(256):
        lookUpTable[0,i] = np.clip(pow(i / 255.0, gamma) * 255.0, 0, 255)

    res = cv2.LUT(img, lookUpTable)
    ## [changing-contrast-brightness-gamma-correction]

    img_gamma_corrected = res#cv2.hconcat([img, res])
    return img_gamma_corrected

print("fuck")
#filepath = "C:/Users/aol/Downloads/284726492_1067947430484623_4755717909050278760_n.png"
#filepath = "C:/Users/aol/Downloads/313888430_676020084051290_6385229983960281955_n.jpg"
#filepath ="C:/Users/aol/Downloads/315455089_827896401877279_2855901142268397829_n.jpg"
#filepath ="C:/Users/aol/OneDrive - Novicell APS/Pictures/315519545_3340712862818449_5419462414207795362_n.jpg"
filepath ="C:/Users/aol/Downloads/315519545_3340712862818449_5419462414207795362_n.jpg" 

loadedImage = cv2.imread(filepath)


alpha = 1.5 # Contrast control (1.0-3.0)
beta = 40 # Brightness control (0-100)



blueImage = cv2.cvtColor(loadedImage,cv2.COLOR_RGB2BGR)
backtoback = cv2.cvtColor(blueImage,cv2.COLOR_HSV2RGB)

greyImg = cv2.cvtColor(backtoback,cv2.COLOR_BGR2GRAY)
adjusted = cv2.convertScaleAbs(greyImg, alpha=alpha, beta=beta)
blur = cv2.GaussianBlur(adjusted, (5,5), 0) 
ret, Image = cv2.threshold(adjusted, 60 ,255,cv2.THRESH_BINARY) #29

Image = crop_img(Image,0.53)

edged = cv2.Canny(blur, 30, 200) 
cv2.imshow("testImage",Image)
cv2.imshow("TestImage2",edged)
cv2.imshow("TestImage3",blur)
cv2.imshow("tester", greyImg)
reader = Reader(['en'])
# detect the text from the license plate
detection = reader.readtext(edged)
if len(detection)>0:
    for text in detection: 
        if len(text[1].replace(" ", "")) ==7:
            print(text[1])
    
    
detection = reader.readtext(Image)
if len(detection)>0:
    for text in detection: 
        if len(text[1].replace(" ", "")) ==7:
            print(text[1])
    
cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.waitKey(1)
