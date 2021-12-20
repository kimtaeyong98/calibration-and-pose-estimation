from PIL.Image import NONE
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

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
    
    # pose test img 12번째 영상
    pattern_size = (9,6)
    square_size = 21 #mm unit
    
    pattern_points = np.zeros((pattern_size[0]*pattern_size[1],3), np.float32)
    pattern_points[:,:2]=np.indices(pattern_size).T.reshape(-1,2)
    
    pattern_points *= square_size
    
    import glob
    image_names = glob.glob('./*.jpg')
    #image_names[11]
    img = cv.imread(image_names[13])
    img_undist_test = cv.undistort(img, intrisic_mtx, dist_coefs, None, newcameramtx)
    img_undist_test_gray = cv.cvtColor(img_undist_test, cv.COLOR_BGR2GRAY)
    ret, corners = cv.findChessboardCorners(img_undist_test_gray, pattern_size)
    print(ret)
    
    if ret:
        criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_COUNT, 30, 0.1) #0.001
        corner2 = cv.cornerSubPix(img_undist_test_gray, corners, (5,5), (-1,-1), criteria)
        ret, rvecs, tvecs = cv.solvePnP(pattern_points, corner2, newcameramtx, None)
        print("rvecs:\n", rvecs)
        print("tvecs:\n", tvecs)
        
        axis = np.float32([[square_size,0,0],[0,square_size,0],[0,0,square_size]]).reshape(-1,3)
        # project 3D points to image plane
        imgpts, jac = cv.projectPoints(axis, rvecs, tvecs, newcameramtx, None)
        
        axis_center=tuple(corner2[0].ravel().astype(int))
        cv.line(img_undist_test, axis_center, tuple(imgpts[0].ravel().astype(int)), (0,0,255), 2)
        cv.line(img_undist_test, axis_center, tuple(imgpts[1].ravel().astype(int)), (0,255,0), 2)
        cv.line(img_undist_test, axis_center, tuple(imgpts[2].ravel().astype(int)), (255,0,0), 2)
        display_untilKey([img_undist_test], ["pose"])

    