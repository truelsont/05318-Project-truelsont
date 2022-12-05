import streamlit as st
import streamlit.components.v1 as components

import pandas as pd
import plotly.express as px

import imageModel



if '1imageIdx' not in st.session_state:
    st.session_state['1imageIdx'] = 0


'# Image to .txt file Tool'

st.write(''' Hi there! The purpose of this tool is to take uploaded 
.jpeg/.png files and extract the text of the photo. There are 
various steps in this tool that require user inputs. Please upload the
files you wish to extract text from below''')

uploadedFiles = st.file_uploader(label = "Upload image(s)",type = (["jpg","jpeg","png"]), accept_multiple_files = True)
if st.session_state['1imageIdx'] > len(uploadedFiles): 
    imageIndex = 0


imageLeftButton, imageCols, imageRightButton = st.columns(3)


def funArrow(i):
    if len(uploadedFiles) == 0: 
        return 
    imageIndex = st.session_state['1imageIdx']
    imageIndex += i
    imageIndex %= len(uploadedFiles)
    st.session_state['1imageIdx'] = imageIndex
    return 

if not uploadedFiles:
    st.write("Upload Files to Proceed")
    st.stop()
    

imageLeftButton, imageCols, imageRightButton = st.columns([1,6,1])

with imageLeftButton: 
    if st.button("Prev"):
        funArrow(-1)
with imageRightButton:
        if st.button("Next"):
            funArrow(1)
with imageCols:
    imageIndex = st.session_state['1imageIdx']
    st.image(uploadedFiles[imageIndex], caption="Uploaded Image Preview")


st.write('''To improve the tools performance it usually preferable 
to add some transformations to the image, such as making the image
black and white. There are some default transformations applied,
choose some additional transformations and observe what the image is transformed to.''')

transformations = imageModel.optionalTransformation
flags = st.multiselect("Transformations", options = transformations)

submitTransformation = st.checkbox("Submit selected transformation")


if not submitTransformation:
    st.write('''Press submit transformations to see how the image is changed for input into the 
            model''')
    st.stop()

imageLeftButton2, ogImageCol, transformedImageCol, imageRightButton2 = st.columns([1,4,4,1])
image = None
transformedImage = None 
with imageLeftButton2: 
    if st.button("Prev", key = "left2"):
        funArrow(-1)
with imageRightButton2:
        if st.button("Next", key = "right2"):
            funArrow(1)
with ogImageCol:
    imageIndex = st.session_state['1imageIdx']
    st.image(uploadedFiles[imageIndex], caption="Original Image")
with transformedImageCol:
    imageIndex = st.session_state['1imageIdx']
    image = (uploadedFiles[imageIndex])

    transformedImage = imageModel.convert_img_file(image, flags)

    st.image(transformedImage, caption = "Transformed Image")

st.write('''If the transformation looks good, press the run text extraction button and the model
will attempt to extract the text. The below confidence slider affects the how the model behaves. As it
increases the engine will be more selective in what it believes is a word. Slide it around and observe
the performance on the input.''')

confidenceInterval = st.slider(label = "Confidence Bound", min_value=0, max_value=100, value=30, step=1)
runExtraction= st.checkbox("Run Text Extraction")

if not runExtraction:
    st.stop()


OCRdetails = None


with st.spinner(''):
    OCRdeatils = imageModel.ocrImageExtraction(transformedImage)
st.success('Done!')


deatilsDF = imageModel.ocrConfidence(OCRdeatils, confidenceInterval)

#st.dataframe(data=deatilsDF)
hlImage = imageModel.highlightText(deatilsDF, transformedImage)
st.image(hlImage, caption = "TO DO")

resultString = imageModel.extractString(deatilsDF)
st.write('''Extracted Text:

''' + resultString)



runAll = st.checkbox('''If the output looks good enough click the below
button to extract the text from the uploaded images and convert it to a .txt file.''')

if not runAll:
    st.stop()

allStrs = []
with st.spinner(''):
    for imageFile in uploadedFiles:
        transImg = imageModel.convert_img_file(image, flags)
        OCRdetails = imageModel.ocrImageExtraction(transImg)
        resString = imageModel.extractString(OCRdetails)
        allStrs.append(resString)
st.success('Done!')

finalStr = '\n\n NEW FILE FROM UPLOAD \n\n'.join(allStrs)

if st.download_button('Download text from image',finalStr):
   st.write('Thanks for downloading!')










