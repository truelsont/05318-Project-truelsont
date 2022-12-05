

import pytesseract 
import cv2
import numpy as np 
import pandas
import filetype
import PIL


# Image Pre-Processing Functions to improve output accurracy
# Convert to grayscale
def grayscale(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Remove noise
def remove_noise(img):
    return cv2.medianBlur(img, 5)

# Thresholding
def threshold(img):
    # return cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    return cv2.threshold(img, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

# dilation
def dilate(img):
    kernel = np.ones((5, 5), np.uint8)
    return cv2.dilate(img, kernel, iterations=1)

# erosion
def erode(img):
    kernel = np.ones((5, 5), np.uint8)
    return cv2.erode(img, kernel, iterations=1)

# opening -- erosion followed by a dilation
def opening(img):
    kernel = np.ones((5, 5), np.uint8)
    return cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)

# canny edge detection
def canny(img):
    return cv2.Canny(img, 100, 200)

# skew correction
def deskew(img):
    coords = np.column_stack(np.where(img > 0))
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
    (h, w) = img.shape[:2]
    center = (w//2, h//2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(
        img, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return rotated

optionalTransformation = ["deskew", "erosion", "dilation", "remove_noise"]

def convert_img(img, flags):
    retImg = img.copy()

    #if "canny" in flags: 
     #   retImg = canny(retImg)

    retImg = grayscale(retImg)
    
    if "deskew" in flags: 
        retImg = deskew(retImg)

    if "remove_noise" in flags: 
        retImg = remove_noise(retImg)
    
    if "dilation" in flags:
        retImg = dilate(retImg)

    

    if "erosion" in flags:
        retImg = erode(retImg)

    
    
    retImg= cv2.bitwise_not(retImg)
    retImg = threshold(retImg)

    return retImg

def convert_img_file(file,flags): 

    pil_image = PIL.Image.open(file).convert('RGB')

    opencvImage = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
    retArray = convert_img(opencvImage,flags)

    return PIL.Image.fromarray(retArray)

def ocrConfidence(details, confidence):
    #given the confidence extract stuff
    df = pandas.DataFrame.from_dict(details)
    df['conf'] = pandas.to_numeric(df['conf'], errors='coerce')
    df.dropna(subset = ['conf'])

    df = df[(df['conf'] >= confidence)]
    return df

def highlightText(dfDetails, file):
    pil_image = file

    img = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)


    hlImage = img.copy()
    df_dict = dfDetails.to_dict('records')
    for r in df_dict:
        x,y,w,h = r['left'],r['top'],r['width'],r['height']
        topLeft = (x,y)
        botRight = (x+w,y+h)
        yellow = (0,255,255)
        thickness = -1
        hlImage = cv2.rectangle(hlImage, topLeft,botRight,yellow,1)


    hlImage = cv2.cvtColor(np.array(hlImage), cv2.COLOR_BGR2RGB)
    return PIL.Image.fromarray(hlImage)

def extractString(details):
    wordString = ' '.join(details['text'])
    return wordString


def ocrImageExtraction(image):

    opencvImage = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)


    config_param = r'--oem 3 --psm 6'
    details = pytesseract.image_to_data(opencvImage, output_type = pytesseract.Output.DICT)
    return details

        

    



