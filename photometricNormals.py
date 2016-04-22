# -*- coding: utf-8 -*-
"""
Created on Wed Apr 06 16:26:08 2016

@author: 开圣
"""
import numpy as np
import os
from PIL import Image,ImageDraw

demoImagePath = r'D:\WinPython-64bit-2.7.10.1\mine\Unconstrained 3D Face Reconstruction\data\imgSet2\_Canon EOS 700D (294075042050)_11244.jpg'

def getM(template, pSet, imgSetDir):
    M = []
    X = np.array(template.v)
    Xh = np.c_[X, np.ones((len(X),1))]
    imgList = os.listdir(imgSetDir)
    for (p, imgName) in zip(pSet, imgList):
        imgPath = os.path.join(imgSetDir, imgName)
        im = np.array(Image.open(imgPath).convert('L'))
        proPts = np.round(map(lambda x:np.dot(p, x), Xh))[:,:2]
        tempM = map(lambda x:im[x[1], x[0]], proPts)
        M.append(tempM)
    return np.array(M)

def computeSt(template, M):
    vNum = len(template.v)
    imgNum = len(M)
    costVal = 0
    rho = np.ones((imgNum, vNum))
    n = np.c_[np.ones((vNum, 1)), np.array(template.vn)].T
    while 1:
        L = (M/rho).dot(np.linalg.pinv(n))
        Ln = np.dot(L, n)
        newCostVal = np.linalg.norm(Ln * rho - M)
        if abs(costVal - newCostVal) < 0.1:
            break
        costVal = newCostVal
        print costVal
        rhoVal = M/Ln
        meanRho = np.mean(rhoVal, axis = 0)
        meanRho = meanRho.reshape(vNum, 1)
        rho = (np.repeat(meanRho, imgNum, axis = 1)).T
    St = rho[:4,:] * n
    return St, rho
    
def normalRefine(M, St):
    [U,a,V] = np.linalg.svd(M)
    a = np.sqrt(a)    
    sDiag = np.diag(tuple(a[:4]))
    aLeft = np.r_[sDiag, np.zeros((len(U)-4, 4))]
    aRight = np.c_[sDiag, np.zeros((4, V.shape[1]-4))]
    S = aRight.dot(V)
    A = np.linalg.lstsq(S.T, St.T)[0].T
    L = U.dot(aLeft).dot(np.linalg.inv(A))
    refineS = np.linalg.lstsq(L, M)[0]
    return refineS

def getNorm(refineS, rho):
    tempN = refineS/rho[:4,:]
    return tempN[1:].T

def drawL(img, landmark):
    #img = Image.open(imgPath)
    imDraw = ImageDraw.Draw(img)
    radius = 10
    for p in landmark:
        x = p[0]
        y = p[1]
        imDraw.ellipse((x - radius,y -radius,x + radius, y + radius), fill = 'red', outline = 'red')
    return img

#3p vector turn to obj file

def projectL(P, landmark3D):
    lm = np.c_[landmark3D, np.ones((len(landmark3D), 1))]
    return P.dot(lm.T).T[:,0:2] 
    
def drawAlbedo(P, vertex3D, rho, imgShape):
    radius1 = 20
    #radius2 = 19
    rhoN = rho/rho.max()
    im = np.ones(imgShape)*255
    img = Image.fromarray(im)
    imDraw = ImageDraw.Draw(img)
    point2D = projectL(P, vertex3D)
    point2D = map(tuple, point2D.astype('int'))
    for ((p1,p2),r) in zip(point2D, rhoN):
        imDraw.ellipse((p1 - radius1,p2 -radius1,p1 + radius1, p2 + radius1), fill = r*255, outline = r*255)
        #imDraw.ellipse((p1 - radius2,p2 -radius2,p1 + radius2, p2 + radius2), outline = r*255)
    #im.astype('uint8')
    return img
    


if __name__ == '__main__':
    demoImg = Image.open(demoImagePath)
    imgShape = (demoImg.size[1],demoImg.size[0])
    pSet = pMatrix
    M = getM(template, pSet, imgSetDir)
    [St, rho] = computeSt(template, M)
    imgAlbedo = drawAlbedo(pSet[3], template.v, rho[0,:], imgShape)
    imgAlbedo.show()
    refineS = normalRefine(M, St)
    Norm = getNorm(refineS, rho)
    

        
    
    
    
            