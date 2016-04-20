#!/usr/bin/env python2.7
#-*-coding:Latin-1 -*

import time
import numpy as np
import os
import json
import urllib
import cv2
import subprocess
from threading import *
from low_lvl import *
from gauge import *
from PIL import Image
from database_manager import *

class Card :

    def __init__(self,name,position,status = "hand"):
        u=Data.search_database({u'name' : name})
        ##############ATTRIBUT###################
        self.name = u[u'name']
        self.health =u[u'health']
        self.attack =u[u'attack']
        self.status = "hand"
        self.type =u[u'type']
        self.pos = position
        self.rarity = u[u'rarity']
        self.img_hand=u[u'pic_hand']
        self.img_board=u[u'pic_board']
        #self.img_mboard=u[u'pic_mboard']

        return 0

