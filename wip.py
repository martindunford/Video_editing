#! .venv/bin/python3
# importing necessary packages
import cv2 as cv2
import time
def main():
    # Load two images
    img1 = cv2.imread('blending/messi.jpg')
    img2 = cv2.imread('blending/cv.png')
    # assert img1 is not None, "file could not be read, check with os.path.exists()"
    assert img2 is not None, "file could not be read, check with os.path.exists()"
    # I want to put logo on top-left corner, So I create a ROI
    rows,cols,channels = img2.shape
    # Top left portion of image1 that is size of image2
    roi = img1[0:rows, 0:cols]
    # Now create a mask of logo and create its inverse mask also
    img2gray = cv2.cvtColor(img2,cv2.COLOR_BGR2GRAY)
    cv2.imshow('Step 1',img2gray)
    cv2.waitKey(0)
    # Threshold is 10. So almost everything converted to 255 (white)
    #  then inverted so white on black to black on white
    ret, mask = cv2.threshold(img2gray, 10, 255, cv2.THRESH_BINARY)
    mask_inv = cv2.bitwise_not(mask)
    cv2.imshow('Step 2',mask_inv)
    cv2.waitKey(0)

    # Now black-out the area of logo in ROI
    img1_bg = cv2.bitwise_and(roi,roi,mask = mask_inv)
    cv2.imshow('Step 3',img1_bg)
    cv2.waitKey(0)
    # Take only region of logo from logo image.
    img2_fg = cv2.bitwise_and(img2,img2,mask = mask)
    cv2.imshow('Step 4',img2_fg)
    cv2.waitKey(0)

    # Put logo in ROI and modify the main image
    dst = cv2.add(img1_bg,img2_fg)
    img1[0:rows, 0:cols ] = dst
    cv2.imshow('Step 5',img1)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
if __name__ == '__main__':
    main()