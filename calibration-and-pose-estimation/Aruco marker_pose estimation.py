from typing import Pattern
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
import cv2.aruco as aruco#노랑줄 떠도 무시하시면 됩니다 행님들

def plot_img(rows, cols, index, img, title):
    ax = plt.subplot(rows,cols,index)
    if(len(img.shape) == 3):
        ax_img = plt.imshow(img[...,::-1]) # same as img[:,:,::-1]), RGB image is displayed without cv.cvtColor
    else:
        ax_img = plt.imshow(img, cmap='gray')
    plt.axis('on')
    if(title != None): plt.title(title) 
    return ax_img, ax
    
def display_untilKey(Pimgs, Titles, file_out = False):
    for img, title in zip(Pimgs, Titles):
        cv.imshow(title, img)
        if file_out == True:
            cv.imwrite(title + ".jpg", img)
    cv.waitKey(0)
    
if __name__=='__main__':
    fr = cv.FileStorage("./camara_parameters.txt", cv.FileStorage_READ)
    intrisic_mtx = fr.getNode('camera intrinsic matrix').mat()
    dist_coefs = fr.getNode('distortion coefficient').mat()
    newcameramtx = fr.getNode('camera new intrinsic matrix').mat()
    print("camera intrinsic matrix:\n", intrisic_mtx)
    print('distortion coefficient', dist_coefs)
    print('camera new intrinsic matrix', newcameramtx)
    fr.release()
    
    pattern_size = (2,2)
    square_size=91#mm unit
    pattern_points=np.zeros((pattern_size[0]*pattern_size[1],3),np.float32)
    pattern_points[:,:2]=np.indices(pattern_size).T.reshape(-1,2)
    pattern_points *= square_size
    

    arucoDict = cv.aruco.Dictionary_get(cv.aruco.DICT_6X6_50)
    #마커 생성
    #marker_img=np.zeros((300,300,1), dtype="uint8")
    #cv.aruco.drawMarker(arucoDict,1,300,marker_img,1)
    #cv.imwrite('./m1.bmp',marker_img)
    arucoParams = cv.aruco.DetectorParameters_create()
    
    #undistort
    img =cv.imread('./marker/mk1.jpg')
    undist_img = cv.undistort(img, intrisic_mtx,dist_coefs,None,newcameramtx)
    #plt.figure(2)
    #plot_img(1,2,1,img,'distorted','off')
    #plot_img(1,2,2,undist_img,'undistorted','off')
    #plt.show()
    (corners,ids,rejected)=cv.aruco.detectMarkers(undist_img,arucoDict,parameters=arucoParams)
    if len(corners)>0:
        ids=ids.flatten()
        for (markerCorner, markerID) in zip(corners, ids):
            print("[INFO] Aruco marker ID: {}".format(markerID))
            if markerID == 1:
                corners = markerCorner.reshape((4,2))
                (topLeft,topRight,bottomRight,bottomLeft)=corners
                ret,rvecs,tvecs=cv.solvePnP(pattern_points,np.asarray([topLeft,topRight,bottomLeft,bottomRight]).reshape(-1,2),newcameramtx,None)
                
                axis = np.float32([[square_size,0,0],[0,square_size,0],[0,0,square_size]]).reshape(-1,3)
                # project 3D points to image plane
                imgpts, jac = cv.projectPoints(axis, rvecs, tvecs, newcameramtx, None)
                
                
                axis_center=tuple(topLeft.ravel().astype(int))
                
                cv.line(undist_img, axis_center, tuple(imgpts[0].ravel().astype(int)), (0,0,255), 2)
                cv.line(undist_img, axis_center, tuple(imgpts[1].ravel().astype(int)), (0,255,0), 2)
                cv.line(undist_img, axis_center, tuple(imgpts[2].ravel().astype(int)), (255,0,0), 2)
                display_untilKey([undist_img], ["pose"])
                 
                