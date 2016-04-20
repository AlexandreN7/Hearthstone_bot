#!/usr/bin/env python2.7
#-*-coding:Latin-1 -*
"""
Open Source Hearthstone bot
Python2 / OpenCV

"""
import autopy #sudo pip2.7 install autopy
import time
import numpy as np
import cv2 #sudo pacman -S opencv
import os
from pprint import pprint
import json
from threading import *
from low_lvl import *
from gauge import *
from PIL import Image
from database_manager import *
from fight_manager import *


###########GLOBAL############
Data = Data_manager() #La database doit pouvoir etre utiliser par toutes les fonctions
#############################

class Game_manager :
    """Classe principale"""
    def __init__(self):
        #self.k_pick,self.k_board,self.k_hand=init_scale()# get the right ratios
        self.name = "hunter"
        self.mode = "agressive"
        self.throwThresh = 2
        self.turnNb = 0 #compteur de tour
        self.mana = 1 # compteur de mana
        self.cardsNb = 0
        self.bot_turn = 0 # 1-actuellement au bot de jouer
        self.hand = []
        self.coin = 0
        self.board = []
        self.board_ennemy = []
        self.board_priority = []

    def start(self) : #cherche le bouton play et lance la game
        print("Bot look for play button...")
        img_template = cv2.imread('src/ingame/play.png',0)
        play_button=findone(img_template)
        return clickone(play_button)

    def earlygame(self): #s'occupe de toute les actions avant le tour 1 A OPTIMISER !
        print("Bot look for confirm button...")
        found_ok = 0
        start_button = ([],[])
        sec = 0
        pb=progressbarClass(60,"/")
        while (tuple_test(start_button)==0 and sec < 60):
            pb.progress(sec)
            img_template=cv2.imread('src/ingame/ok.png',0)
            start_button=findone(img_template)
            time.sleep(1) #on attend 1 sec
            sec = sec +1
        if self.pick_cards() == 1 : # identify card on hand
            clickone(start_button)
            time.sleep(8) #time to change cards
            heroes_list = ["Rogue","Warlock","Warrior","Shaman","Priest","Druid","Hunter","Mage","Paladin"]
            #Recherche de la classe de l'adversaire
            for i in range(len(heroes_list)) :
                template = cv2.imread('src/heroes/'+heroes_list[i]+'.png',0)
                result=findone(template,1)
                if tuple_test(result)!=0 :
                    w = tuple_zip(result)
                    self.ennemy =heroes_list[i],w
            self.fight = Fight_manager(self.ennemy,Data)
        else :
            print "Fail de la fonction early game"

        #Fonction qui permet de savoir  qui commence à jouer

        print "Bot determine qui doit jouer ..."
        template = cv2.imread('src/ingame/fin_du_tour_en.png',0)
        result=findone(template)
        if tuple_test(result)!=0 :
            print "tour du bot"
            self.bot_turn = 1 #passe notre tour
            return clickone(result)
        else :
            template = cv2.imread('src/ingame/fin_du_tour_green_en.png',0)
            result=findone(template)
            if tuple_test(result)!=0 :
                print "tour du bot"
                self.bot_turn = 1 #tour du bot
                return clickone(result)
            else :
                template = cv2.imread('src/ingame/ennemy_turn.png',0)
                result=findone(template)
                if tuple_test(result)!=0 :
                    self.bot_turn = 0 #passe notre tour
                    print "Le bot passe son tour"
                    self.bot_turn = 0
                    return clickone(result)
                else :
                    print "FACK"

    #Fonction elementaire qui permet le choix des cartes au debut de la partie
    def pick_cards(self):
        pick = []
        print("\nBot try to identify your hand ...")
        tps1 = time.clock()
        interest= Data.search_database({u'indeck' : 1})# liste de dictionnaire des cartes interessantes
        result =card_identification(interest,0,u'pic_pick',0,1)
        if result != [] :
            for entity in result :
                pick.append(entity) # ajout de la carte
        for t in pick : #click
            pass
        found = []
        for entity in pick :
            found.append(Data.search_database({u'name' : entity[0]}))
        to_throw = []
        for entity in found :
            if u'cost' in entity[0].keys() :
                if entity[0][u'cost'] <= self.throwThresh :
                    pass
                else : # on throw la carte
                    for u in pick :
                        if entity[0][u'name'] == u[0] :
                            print "THROW",u[0]
                            for pos in u[1] : #liste de positions
                                click_one(pos)
        tps2 = time.clock()
        print "Temps de choix de cartes" , tps2 - tps1
        return 1


    def end_turn(self) :
        print "Bot termine le tour"
        time.sleep(5)
        template = cv2.imread('src/ingame/fin_du_tour_en.png',0)
        result=findone(template)
        #print result
        if tuple_test(result)!=0 :
            self.bot_turn = 0 #passe notre tour
            return clickone(result)

        template = cv2.imread('src/ingame/fin_du_tour_green_en.png',0)
        result=findone(template)
        #print result
        if tuple_test(result)!=0 :
            self.bot_turn = 0 #passe notre tour
            return clickone(result)

    def wait_turn(self) : # durée d'un tour 70 s
        print "Bot attend la fin du tour"
        time.sleep(5)
        sec = 0
        template = cv2.imread('src/ingame/fin_du_tour_green_en.png',0)
        result=([],[])
        while (tuple_test(result)!=0):
            if(sec > 70) :
                print "FAIL",sec
                break
                return 0
            img_template = cv2.imread('src/ingame/ennemy_turn_en.png',0)
            start_button=findone(img_template)
            time.sleep(0.5) #on attend 1 sec
            sec = sec + 0.5
        self.bot_turn = 1 #passe a notre tour
        self.turnNb = self.turnNb+1 #on incrémente le nombre de tour
        return 1

    def scan_hand(self) : #identifie le status de la game
        print "Bot scan la main ..."
        tps1 = time.clock()
        x=250
        y=790
        self.hand = [] #on recommence tout
        tps1 = time.clock()
        while x < 800 :
            autopy.mouse.move(x,y)
            interest= Data.search_database({u'indeck' : 1})# liste de dictionnaire des cartes interessantes
            result =card_identification(interest,3,u'pic_hand',1,1)
            if result != [] :
                if self.hand == [] : #premier passage
                    for entity in result :
                        self.hand.append(entity) # ajout de la carte

                elif (self.hand[-1][0] == result[0][0]) and (abs(self.hand[-1][1][0][0]-x)> 50) : #Detection de doublons
                    pass
                else :
                    for entity in result :
                        self.hand.append(entity) # ajout de la carte
            x=x+50
        tps2 = time.clock()
        print ("Time", tps2-tps1)

        self.fight.update_hand(self.hand)# card_list = [[name,[pos]],[...],...]
        print self.hand
        return 0


    def scan_board(self):
        print "Scan board ..."
        tps1 = time.clock()
        monster=([],[])
        self.board = []
        self.board_ennemy=[]
        self.board_priority = []

        #######################SCAN DES MONSTRES DU BOARD######################
        print "Bot scan ses cartes sur le board ..."
        img_template = cv2.imread('src/circle_colored.png')
        img_template  = cv2.Canny(img_template , 50, 200)
        w, h = img_template.shape[:2]#offset du template
        monster=findone_cannyfilter(img_template,0,5800000)#initially 60000000 but detection failed
        if tuple_test(monster)!=0 :
            cpt = 0
            thresh = 50
            doublon = []
            for pt in zip(*monster[::-1]):
                doublon.append((pt[0]+w/2,pt[1]+h/2)) # creation d'un liste de tuples
            pos = doublon_manager(doublon)
            print pos

            for m in pos :
                if m[1] < 405 :
                    self.board_ennemy.append(m)
                else :
                    self.board.append(m)
        print "board ennemy",self.board_ennemy
        print "board",self.board
        time.sleep(2)
        ############### SCAN DE SON COTE DE TERRAIN #####################
        """
        print "Bot identifie les cartes sur son board ..."
        for i in self.board :
            autopy.mouse.move(i[0],i[1])
            for t in self.db_deck:#deck
                if t[u'type'] == "minion" :
                    changed = cv2.resize(t[u'img'],(0,0), fx=self.k_board, fy=self.k_board)#changement d'echelle
                    result=findone(changed,4,0.75)
                    if tuple_test(result)!=0 :
                        print t[u'name']
                        break

        ####################### SCAN ENNEMI ############################
        print "Bot identifie ses cartes sur le board ennemi ..."
        for i in self.board_ennemy :
            autopy.mouse.move(i[0],i[1])
            for t in self.db_all:#parcourt du deck
                if t[u'type'] == "minion" :
                    if t[u'hero'] == self.ennemy or t[u'hero'] == "neutral":
                        changed = cv2.resize(t[u'img'],(0,0), fx=k, fy=k)#changement d'echelle
                        result=findone(changed,4,0.7)
                        if tuple_test(result)!=0 :
                            #self.hand.append((t[u'name'],t[u'id'],x,790,t[u'mana']))
                            print t[u'name']
                            #self.board_ennemy.append(self.ennemy[1])
                            #attack(i,self.board_ennemy[0])
                            break
                            """
        tps2 = time.clock()
        print("temps ",tps2 - tps1)




    def engage_cards(self):
        min_mana = self.turnNb
        sorted_list = sorted(self.hand,  key=lambda attribut: attribut[4]) #trier en fonction du mana

        if sorted_list[0][4] <= min_mana :
            engageone((sorted_list[0][2],sorted_list[0][3]))
            min_mana =self.turnNb - sorted_list[0][4]
            print "On engage :",sorted_list[0][0]
            print "Il reste :",min_mana,"de mana"
            sorted_list.remove(sorted_list[0])

            if sorted_list[0][4] <= min_mana :
                engageone((sorted_list[0][2],sorted_list[0][3]))
                min_mana =self.turnNb - sorted_list[0][4]
                print "On engage :",sorted_list[0][0]
                print "Il reste :",min_mana,"de mana"
                sorted_list.remove(sorted_list[0])

                if sorted_list[0][4] <= min_mana :
                    engageone((sorted_list[0][2],sorted_list[0][3]))
                    min_mana =self.turnNb - sorted_list[0][4]
                    print "On engage :",sorted_list[0][0]
                    print "Il reste :",min_mana,"de mana"
                    sorted_list.remove(sorted_list[0])

        else :
            print "rien a jouer"

    def play_turn(self) : #fonction essentielle qui per,et la gestion d'événenemts un tour
        time.sleep(3) #temps de piocher
        self.scan_hand()
        self.fight.scan_board()
        #self.engage_cards()

if __name__ == '__main__':
    bot = Game_manager()
    #test_dico = {u'cost':2,u'rarity' : u'Common', u'playerClass':u'Hunter'}
    #test_dico = {u'name' : u'Houndmaster'}
    #test_dico = {u'rarity':u'Legendary',u'playerClass':u'Mage'}
    #tps1 = time.clock()
    #info= bot.Data.search_database({u'indeck' : 1})
    #print info
    #tps2 = time.clock()
    #print ("Temps de recherche",tps2-tps1)
    #print bot.Data.db_all
    print Data.db_all[200].keys()
    if bot.start() == 1 :
    	bot.earlygame()#appeler une fois pour initialiser la game
        while 1:
            if bot.bot_turn == 1 :
                bot.play_turn()
                bot.end_turn()
            else :
                bot.wait_turn()

