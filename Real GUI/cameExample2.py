from ximea import xiapi
import cv2

# create handle and open camera
cam = xiapi.Camera()
cam.open_device()

# create image handle
img = xiapi.Image()
cam.set_exposure(100000)
# start data acquisition
cam.start_acquisition()

while True:
    # get data and pass to img
    cam.get_image(img)
    
    data = img.get_image_data_numpy()
    
    #cv2.imshow("cam stream",data[600:800,550:850])# 
    cv2.circle(data,(730,700), 10, (255,0,0), 2) 
    cv2.imshow("cam stream",data)
   
    
    k = cv2.waitKey(1)

    if k == ord('q'):
        break

# clear handle and close window
cam.stop_acquisition()
cam.close_device()
cv2.destroyAllWindows()