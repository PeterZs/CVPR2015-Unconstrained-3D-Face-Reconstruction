# -*- coding: utf-8 -*-
"""
Created on Wed Jan 06 13:05:35 2016

@author: 开圣
"""

#deal with obj file
import numpy as np

class obj:
    def __init__(self, filePath):
        self.path = filePath
        self.v = []
        self.vn = []
        self.vt = []
        self.face = []
        self.vnface = []
        self.vtface = []
        
    def load(self):
        f = open(self.path, 'r')
        for line in f:
            line = line.split(' ')
            if line[0] == 'v':
                vTemp = map(float, line[1:4])
                self.v.append(vTemp)
            if line[0] == 'vn':
                vnTemp = map(float, line[1:4])
                self.vn.append(vnTemp)
            if line[0] == 'vt':
                vtTemp = map(float, line[1:3])
                self.vt.append(vtTemp)
            if line[0] == 'f':
                k = len(line[1].split('/'))
                faceTemp = []
                vnfaceTemp = []
                vtfaceTemp = []
                for i in range(1,4):
                    lineTemp = line[i]
                    lineTemp = map(int, lineTemp.split('/'))
                    for j in range(k):
                        if j == 0:
                            faceTemp.append(lineTemp[0] - 1)                           
                        if j == 1:
                            vtfaceTemp.append(lineTemp[1] - 1)                            
                        if j == 2:
                            vnfaceTemp.append(lineTemp[2] - 1)                            
                self.face.append(faceTemp)
                if k == 2:
                    self.vtface.append(vtfaceTemp)
                else:
                    self.vtface.append(vtfaceTemp)
                    self.vnface.append(vnfaceTemp)
        if self.vn == []:
            self.vnCal()
                
    #cal the vn
    def vnCal(self):
        vArray = np.array(self.v)
        normsTemp = []#save the norms value
        for i in range(len(self.v)):
            normsTemp.append([])
        for face in self.face:
            v1 = vArray[face[0]]
            v2 = vArray[face[1]]
            v3 = vArray[face[2]]
            tempNorm = np.cross((v1 - v2), (v1 - v3))
            normsTemp[face[0]].append(tempNorm)
            normsTemp[face[1]].append(tempNorm)
            normsTemp[face[2]].append(tempNorm)
        #import pdb
        #pdb.set_trace()
        for norm in normsTemp:
            norm = map(np.mean, np.rot90(norm))
            self.vn.append(norm)
                
            
                
                            