# -*- coding: utf-8 -*-
"""
Created on Wed Apr 06 16:26:08 2016

@author: 开圣
"""
import numpy as np
import os
from PIL import Image

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
        newCostVal = np.linalg.norm(Ln - M/rho)
        if abs(costVal - newCostVal) < 0.1:
            break
        costVal = newCostVal
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

if __name__ == '__main__':
    pSet = pMatrix
    M = getM(template, pSet, imgSetDir)
    [St, rho] = computeSt(template, M)
    refineS = normalRefine(M, St)
    Norm = getNorm(refineS, rho)
    

        
    
    
    
            