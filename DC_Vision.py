#from IPython import get_ipython
#get_ipython().run_line_magic('matplotlib', 'qt5')



import cv2
import numpy as np

def drawcontours(n,xt,yt,cnts,gray,color):
    ## filter by area number defects
    s1=0
    s2=500000
    xcnts=[]
    spot=1
    
    img=gray
    font=cv2.FONT_HERSHEY_SIMPLEX
    fontScale=1
    fontColor=color
    lineType=1
    
    for cnt in cnts:
        if s1<=cv2.contourArea(cnt) <s2:
            
            x, y, xs, ys = cv2.boundingRect(cnt)
            cv2.putText(img,str(spot), 
                    (x+2,y+2), 
                    font, 
                    fontScale,
                    fontColor,
                    lineType)
            
            radius=0.5*(xs+ys)/2
            xcnts.append([n,xt,yt,spot,x,y,np.pi*radius**2])
            #np.size(cnt)
            spot+=1
            
    #cv2.imshow('Image2',gray)  
    #ax2.imshow(gray, cmap='gray')      
    return [img,xcnts]

def xy(n):
    x=(n)%rows
    y=int(np.floor(n/rows))
    
    if y%2==0:     
        x=(n)%rows
    else:
        x=(rows-1)-(n)%rows        
    xprev=x
       
    return [x,y]


def openimage(path):
    gray = cv2.imread(path, 0)  
    return gray

def histogram(image,lb,ub):   
    
    
    a=image.ravel()
    a_bool=np.logical_and(a >lb, a < ub)
    ab = a[a_bool]
    
    mean=np.mean(ab)
    stdev=np.std(ab)
    return {"ravel": a, "mean": mean, "stdev": stdev} 
     
def gray_RGB(img):
    gray_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)    
    return gray_rgb

def morphing_open(img, active,size):
    if active==1:
        kernel = np.ones((size,size),np.uint8)
        img=cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)  
    return img

def morphing_close(img, active,size):
    if active==1:
        kernel = np.ones((size,size),np.uint8)
        img=cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)   
    return img

def equal_hist(img, active, clip, size):
    if active==1:
        clahe=cv2.createCLAHE(clipLimit=clip, tileGridSize=(size,size))   
        img = clahe.apply(img)
    return img   
    
  
    
    
def blackdefects(im_num,x,y, img, gray_rgb, size, tres, morph_close, morph_open):
    #Black Spots
    
    size=2*np.round(size/0.5,0)+1  
    threshed = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,int(size),tres)
    #threshed = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,11,50)    

    threshed=morphing_open(threshed,morph_open['active'],morph_open['size'])
    threshed=morphing_close(threshed,morph_close['active'],morph_close['size'])
    
    
    cnts = cv2.findContours(threshed, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[-2]
    #cnts = cv2.findContours(threshed, cv2.RETR_LIST, cv2.CHAIN_APPROX_TC89_KCOS)[-2]
    
    cv2.drawContours(gray_rgb, cnts,-1, (0, 110, 0), thickness=cv2.FILLED)
    
    contours=drawcontours(im_num,x,y,cnts,gray_rgb,(0, 110, 0))    

    #Mean area defect
    if len(contours[1])==0:
        areamean=0
    else:
        areas=np.array(contours[1])
        areamean=np.mean(areas[:,6])
        
    return  {"image": contours[0], "defect_count": len(contours[1]),"area_mean": areamean, "defects_all": contours[1]} 

def whitedefects(im_num,x,y, img, gray_rgb, size, tres, morph_close, morph_open):
    #White Spots
     
    size=2*np.round(size/0.5,0)+1
    threshed = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,int(size),-tres)    
    #threshed = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,50)
    
    threshed=morphing_open(threshed,morph_open['active'],morph_open['size'])
    threshed=morphing_close(threshed,morph_close['active'],morph_close['size'])
        
    cnts = cv2.findContours(threshed, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[-2]
    #cnts = cv2.findContours(threshed, cv2.RETR_LIST, cv2.CHAIN_APPROX_TC89_KCOS)[-2]
    
    cv2.drawContours(gray_rgb, cnts,-1, (256, 0, 0), thickness=cv2.FILLED)
    
    contours=drawcontours(im_num,x,y,cnts,gray_rgb,(256, 0, 0))    

    #defectareablack=defectareablack+xcnts
    #pblack[n]=len(xcnts)
    
    #Mean area defect
    if len(contours[1])==0:
        areamean=0
    else:
        areas=np.array(contours[1])
        areamean=np.mean(areas[:,6])
            
    return  {"image": contours[0], "defect_count": len(contours[1]),"area_mean": areamean , "defects_all": contours[1]} 


