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
        
