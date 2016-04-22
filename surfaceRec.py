# -*- coding: utf-8 -*-
"""
Created on Mon Apr 11 21:30:56 2016

@author: 开圣
"""
import itertools
import numpy as np

def computeTriangleArea(listVertex):
    vec1 = listVertex[0] - listVertex[1]
    vec2 = listVertex[0] - listVertex[2]
    return np.linalg.norm(np.cross(vec1, vec2))/2
    

def computeH(template, L, norm):
    v = template.v
    ptsNum = len(v)
    cotVal = np.zeros((ptsNum, 1))
    areasVal = np.zeros((ptsNum, 1))
    for fa in template.face:
        p = map(lambda x:template.v[x], fa)
        area = computeTriangleArea(p)
        areasVal[fa] += area
        perm = itertools.permutations(fa, 2)
        for (i,j) in perm:
            dotP = np.inner(v[i]-v[j], norm[j]-norm[i])
            cotVal[i] += 0.5 * L[3*i,3*j] * dotP
    h = cotVal / areasVal
    H = np.reshape(h * norm, (norm.size, 1))
    return H
            
resultX = computeH(template, L, Norm)
for i in range(3):
    resultX[range(i, len(resultX), 3)] -= resultX[i]
template.v = resultX.reshape((len(resultX)/3, 3))
