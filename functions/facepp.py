# -*- coding: utf-8 -*-
"""
Created on Thu Jan 07 13:34:08 2016

@author: 开圣
"""
import urllib
from json import *
from PIL import Image
import numpy as np
#face++ api
from facepp import API,File
API_KEY = "b068f469bf92bbf202a2a351093f81c3"
API_SECRET = "zgoO7K66SOsk0rleEiJYX7LQuY5Bgii2"
api = API(API_KEY,API_SECRET)

def landmarkFromFacepp(imgPath):
    infor = api.detection.detect(img = File(imgPath))
    try:
        faceID = infor[u'face'][0][u'face_id']
    except:
        print ("no face detected")
    req_url = "http://api.faceplusplus.com/detection/landmark"
    params = urllib.urlencode({'api_secret':API_SECRET,'api_key':API_KEY,'face_id':faceID,'type':'83p'})
    req_rst = urllib.urlopen(req_url,params).read() # landmark data
    req_rst_dict = JSONDecoder().decode(req_rst)
    if len(req_rst_dict['result']) == 1:
        landmarkDict = req_rst_dict['result'][0]['landmark']
    imgInfo = Image.open(imgPath)
    xSize = imgInfo.size[0]
    ySize = imgInfo.size[1]
    landmarkList = sorted(list(landmarkDict))
    landmark_array = []
    for key in landmarkList:
        temp_xy = [landmarkDict[key]['x'],landmarkDict[key]['y']]
        landmark_array.append(np.array(temp_xy))
    landmarkArray = np.array(landmark_array)
    landmarkArray[:,0] = landmarkArray[:,0] * xSize / 100
    landmarkArray[:,1] = landmarkArray[:,1] * ySize / 100
    return landmarkArray
      
     