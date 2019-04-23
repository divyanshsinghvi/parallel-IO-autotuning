import cv2 as cv
from matplotlib import pyplot as plt
import os,fnmatch,re

listOfFiles = os.listdir("./bt_plots")
pattern = "*cb_buffer_size.png"
prefixes=[]
for entry in listOfFiles:  
    if fnmatch.fnmatch(entry, pattern):
        prefixes.append(re.sub('cb_buffer_size.png','',entry))
for prefix in prefixes:
    print(prefix)
    prefix= "./bt_plots/"+prefix
    image1 = cv.imread(prefix+'cb_buffer_size.png')
    cv.imshow('image',image1)
    cv.waitKey(0)
    image2 = cv.imread(prefix+'loss.png')
    image3 = cv.imread(prefix+'romio_cb_read.png')
    image4 = cv.imread(prefix+'romio_cb_write.png')
    image5 = cv.imread(prefix+'romio_ds_read.png')
    image6 = cv.imread(prefix+'romio_ds_write.png')
    image7 = cv.imread(prefix+'setstripe-size.png')
    image8 = cv.imread(prefix+'setstripe-count.png')
    image1 = cv.hconcat((image1, image2)) 
    image1 = cv.hconcat((image1, image3)) 
    image1 = cv.hconcat((image1, image4)) 
    image5 = cv.hconcat((image5, image6)) 
    image5 = cv.hconcat((image5, image7)) 
    image5 = cv.hconcat((image5, image8)) 
    final_frame = cv.vconcat((image1,image5))
    cv.imwrite(prefix+'final.png', final_frame)
