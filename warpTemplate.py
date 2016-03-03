# -*- coding: utf-8 -*-
"""
Created on Wed Jan 06 21:09:02 2016

@author: 开圣
"""
import numpy as np
from PIL import Image,ImageDraw
#calculate cot for L
def calCot(vec1, vec2):
    cos = vec1.dot(vec2)/(np.sqrt(vec1.dot(vec1))*np.sqrt(vec2.dot(vec2)))
    sin = np.sqrt(1 - cos**2)
    cot = cos/sin
    return cot

# calculate L
def calL(obj):
    ptsNum = len(obj.v)
    L = np.zeros((3*ptsNum, 3*ptsNum))
    for face in obj.face:
        p = map(np.array, map(lambda x:obj.v[x], face))
        for i in range(3):
            for j in range(3):
                if i != j:
                    k = 3 - i -j
                    if L[3*face[i], 3*face[j]] == 0:
                        val = calCot(p[k]-p[i], p[k]-p[j])
                        L[3*face[i], 3*face[j]] = val
                        L[3*face[i]+1, 3*face[j]+1] = val
                        L[3*face[i]+2, 3*face[j]+2] = val
                    else:
                        val = 0.5 * (calCot(p[k]-p[i], p[k]-p[i]) + L[3*face[i], 3*face[j]])
                        L[3*face[i], 3*face[j]] = val
                        L[3*face[i]+1, 3*face[j]+1] = val
                        L[3*face[i]+2, 3*face[j]+2] = val
    return L

# calculate P (weakly perspective)    
def calP(landmark2D, landmark3D):
    b1 = landmark2D[:,0]
    b2 = landmark2D[:,1]
    A = np.c_[landmark3D, np.ones((len(landmark3D), 1))]
    #import pdb
    #pdb.set_trace()
    m1 = np.linalg.lstsq(A, b1)[0]
    m2 = np.linalg.lstsq(A, b2)[0]
    M = np.c_[m1, m2, np.array([0,0,0,1])]
    return M.T

    
def drawL(imgPath, landmark):
    img = Image.open(imgPath)
    imDraw = ImageDraw.Draw(img)
    radius = 10
    for p in landmark:
        x = p[0]
        y = p[1]
        imDraw.ellipse((x - radius,y -radius,x + radius, y + radius), fill = 'red', outline = 'red')
    return img

#load landmark index    
def loadLandmark(fp):
    text = open(fp, 'r')    
    landmarkIndex = []
    for line in text:
        line = line.split()[0]
        landmarkIndex.append(int(float(line)))
    return landmarkIndex