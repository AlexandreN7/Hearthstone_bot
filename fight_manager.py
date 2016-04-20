#!/usr/bin/env python2.7
#-*-coding:Latin-1 -*

import time
import numpy as np
import os
from pprint import pprint
import json
from threading import *
from low_lvl import *
from gauge import *
from PIL import Image
import urllib
import cv2

#Classe de gestion des combats
#Fonctionne avec la classe cards
#All the strategy should be here
class Fight_manager :
    def __init__(self,opponent,database):#construct
        self.cardsOnBoard = [] # list of cards class object
        self.oldcardsOnBoard = [] # list of cards class object
        self.nopponent=opponent[0]#class of opponent
        self.popponent=opponent[1][0]#position of opponent -> depacking tuple Oo
        print "Bot fight against",self.nopponent,self.popponent
        self.cardsInHand = []#update in
        self.redList = []#opponent minion to attack
        self.blackList = []#opponent minion to ignore
        self.data = database

    def turn(self): #gere les actions d'un tour
        return 0
##########SCAN###########################################
    def scan_board(self):
        print "Bot scan the board"
        tps1 = time.clock()
        found = []
        interest= self.data.search_database({u'type' : u'Minion',u'pic_mboard': 0})
        #interest= self.data.search_database({u'indeck' : 1})# liste de dictionnaire des cartes interessantes

        result =card_identification(interest,4,u'pic_mboard',6,4)
        if result != [] :
            for entity in result :
                found.append(entity) # ajout de la carte
        tps2 = time.clock()
        print found
        print ("time",tps2-tps1)

##########UPDATE############################################
    def update_board(self): #check cards object on the board
        return 0

    def update_hand(self,card_list): # card_list = [[name,[pos]],[...],...]
        for u in card_list :
            print u[0]
        return 0

    def update_mana(self): # number of mana
        return 0
##########STRATEGY###########################################
    def highStrategy(self):
        return 0

    def lowStragegy(self):
        return 0
##########LOW_LVL_FUNCTION##################################
    def attack(self,friendminion,opponentminion):
        return 0

    def target_opponent(self,opponentcard):
        return 0


