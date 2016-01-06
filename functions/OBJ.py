# -*- coding: utf-8 -*-
"""
Created on Wed Jan 06 13:05:35 2016

@author: 开圣
"""

#deal with obj file

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
                            faceTemp = self.v[lineTemp[0] - 1]
                            self.face.append(faceTemp)
                        if j == 1:
                            vtfaceTemp = self.vt[lineTemp[1] - 1]
                            self.vtface.append(vtfaceTemp)
                        if j == 2:
                            vnfaceTemp = self.vn[lineTemp[2] - 1]
                            self.vnface.append(vnfaceTemp)
        
        #def vnCal(self):
            
                            