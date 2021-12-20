import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

def plot_img(rows, cols, index, img, title, axis='on'):
    ax = plt.subplot(rows,cols,index)
    if(len(img.shape) == 3):
        ax_img = plt.imshow(img[...,::-1]) # same as img[:,:,::-1]), RGB image is displayed without cv.cvtColor
    else:
        ax_img = plt.imshow(img, cmap='gray')
    plt.axis(axis)
    if(title != None): plt.title(title) 
    return ax_img, ax
    
def display_untilKey(Pimgs, Titles, file_out = False):
    for img, title in zip(Pimgs, Titles):
        cv.imshow(title, img)
        if file_out == True:
            cv.imwrite(title + ".jpg", img)
    cv.waitKey(0)

def detect_2d_point_from_cbimg(file_name, pattern_size):#2d포인트 찾는 함수
    img = cv.imread(file_name)
    img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)   
    
    found, corners = cv.findChessboardCorners(img_gray, pattern_size, None)
    if found:
        criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_COUNT, 30, 0.1) #0.001
        cv.cornerSubPix(img_gray, corners, (5,5), (-1,-1), criteria)#더 정밀하게 코너를 찾아줌.
        cv.drawChessboardCorners(img, pattern_size, corners, found)
    
    if not found:
        print('chessboard not found') 
        return None
    
    return (corners, img)   
    
if __name__=='__main__':
    pattern_size = (9,6)#격자포인트 수
    square_size = 21 #(실제 격자 크기 자로 재야함.)
    
    
    pattern_points = np.zeros((pattern_size[0]*pattern_size[1],3), np.float32)
    pattern_points[:,:2]=np.indices(pattern_size).T.reshape(-1,2)
    
    pattern_points *= square_size
    print(pattern_points)
    
    import glob
    image_names = glob.glob('./*.jpg')#이미지 한번에 다 불러오기
    print(image_names)
    
    chessboard_imgs = []#2d포지션 저장
    
    chessboard_imgs = [detect_2d_point_from_cbimg(file_name, pattern_size) for file_name in image_names]
    # Arrays to store object points and image points from all the images.
    obj_points = [] #3d point in real world space
    img_points = [] #2d point in image plane.
    idx=1
    plt.figure(1)
    for x in chessboard_imgs:
        if x is not None:
            img_points.append(x[0])
            obj_points.append(pattern_points)
            plot_img(5,4,idx,x[1],None,'off')
            idx +=1
    plt.show()
    
    h, w = cv.imread(image_names[0]).shape[:2]
    print(image_names[0])
    print('image size : %d' %w + ', %d' %h +' x%d images' %len(image_names))
    
    rms_err, intrisic_mtx, dist_coefs, rvecs, tevecs = cv.calibrateCamera(obj_points, img_points, (w, h), None, None)
    
    print("\nRMS:", rms_err)
    print("camera intrinsic matrix:\n", intrisic_mtx)
    print("distortion coefficients", dist_coefs.ravel())
    
    newcameramtx, roi = cv.getOptimalNewCameraMatrix(intrisic_mtx, dist_coefs, (w, h), 1, (w, h))
    print("camera new intrinsic matrix:\n", newcameramtx)
    

    # store the camera parameters (문서참고)
    fs=cv.FileStorage("./camara_parameters.txt", cv.FileStorage_WRITE)
    fs.write('camera intrinsic matrix', intrisic_mtx)
    fs.write('distortion coefficient', dist_coefs)
    fs.write('camera new intrinsic matrix', newcameramtx)
    fs.release()


    img_test = cv.imread(image_names[12])
    # undistort
    img_undist_test = cv.undistort(img_test, intrisic_mtx, dist_coefs, None, newcameramtx)
    
    plt.figure(2)
    plot_img(1,2,1,img_test, 'distorted', 'off')
    plot_img(1,2,2,img_undist_test, 'undistorted', 'off')
    plt.show()