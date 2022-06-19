import cv2
import os

def sketch(src,name,dir,exist):
    if exist:
        result=True

        try:
            img=cv2.imread(src)

            gray_scale=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            inverted=255-gray_scale

            blurred_image=cv2.GaussianBlur(inverted,(21,21),sigmaX=0,sigmaY=0)
            inverted_blur=255-blurred_image
            pencil_sketch=cv2.divide(gray_scale,inverted_blur,scale=256)


            target_name="Outline_{}".format(name)
            target=os.path.join(dir,target_name)

            cv2.imwrite(target,pencil_sketch)

        except:
            result=False
            target=None
    else:
        result=False
        target=None
            
    return (target,result)