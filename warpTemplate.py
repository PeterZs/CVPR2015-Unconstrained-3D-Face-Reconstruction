# -*- coding: utf-8 -*-
"""
Created on Wed Jan 06 21:09:02 2016

@author: 开圣
"""
import numpy as np
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
        [p1, p2, p3] = map(np.array, map(lambda x:obj.v[x], face))
        for i in range(3):
            for j in range(3):
                if L[3*face[i], 3*face[j]] == 0:
                    L[3*face[i], 3*face[j]] = calCot(p3-p1, p3-p2)
                else:
                    L[3*face[i], 3*face[j]] = 0.5 * (calCot(p3-p1, p3-p2) + L[3*face[i], 3*face[j]])    
    return L
        
