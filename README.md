Written by Thor Truelson

# Summary

The purpose of this tool is for a user to upload image files (.jpeg/.png) and extract the english
text from the images. 

# Details

The application interface is built with the streamlit module and is python based. The entirity of the 
code implmeneted in the main.py and imageModel.py files were entirely written by the author. 

The main model of the application is the Tesseract engine developed by HP. We are using the pytesseract 
engine API for the tesseract engine. This was all developed and tested with Ubuntu 22.04 and in a 
anaconda enviorment. I think tesseract has not been tested in MacOS. 

# Requirements for Install

From command line:

sudo apt-get install tesseract-ocr

From the conda enviorment:

pip install pytesseract 
pip install cv2
pip install numpy  
pip install pandas
pip install filetype
pip install PIL
pip install streamlit as st

