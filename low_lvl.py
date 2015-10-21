#!/usr/bin/env python2.7
#-*-coding:Latin-1 -*

import autopy #sudo pip2.7 install autopy
import time
import numpy as np
import cv2 #sudo pacman -S opencv
import os
from pprint import pprint
import json
import threading #now the good stuff
#########FICHIER QUI CONTIENT LES FONCTIONS DE BAS NIVEAUX#########

#Fonction qui permet d'importer les préférences du bot
def config_import():
    fichier = open("config.txt","r")
    content = fichier.readlines()
    deck_cards=[]
    for ligne in content :
        deck_cards.append(ligne.rstrip('\n\r')
)
    fichier.close()
    print deck_cards
    return deck_cards # return the list of cards

def tuple_test (tuple_t):
    test_list=len(zip(*tuple_t[::-1]))
    return test_list

def tuple_zip(button):
    doublon = []
    for pt in zip(*button[::-1]):
        doublon.append(pt) # creation d'un liste de tuples
    pos = doublon_manager(doublon)
    autopy.mouse.move(pos[0][0],pos[0][1])
    autopy.mouse.click()
    return pos

#Prototype de fontion qui doit permettre le scaling automating des images sur le board
#On charge des images connues et on identifie la meilleur échelle
#On réutilisera cette échelle dans le reste du programme
#On utilise l'image de la tisseuse id#2023
def init_scale():# TODo OPTIMIZE !!!!
    print "Bot is scaling..."
    template = cv2.imread('src/2023.png',0)
    ref = (303,200)
    size = template.shape #normalisation 302x200
    k = float(ref[0])/float(size[0]) #1.1
    template = cv2.resize(template,(0,0), fx=k, fy=k)#changement d'echelle
    best_match_pick = [0,1] #[val,ratio]
    img_rgb = cv2.imread('src/scaling_pick.png')
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    for i in range(50,200) :

        k = i/100.0
        template_match = cv2.resize(template,(0,0), fx=k, fy=k)#changement d'echelle
        try :
            res = cv2.matchTemplate(img_gray,template_match,cv2.TM_CCOEFF_NORMED)
            min_val,max_val,min_loc,max_loc = cv2.minMaxLoc(res)
            if best_match_pick[0] < max_val :
                best_match_pick[0] = max_val
                best_match_pick[1] = k
            else :
                pass
        except :
            pass
    best_match_board = [0,1] #[val,ratio]
    img_rgb = cv2.imread('src/scaling_board.png')
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    for i in range(100,200) : #attention ! probleme pour les ratio inf a 100 ! pareil pour hand !
        k = i/100.0
        template_match = cv2.resize(template,(0,0), fx=k, fy=k)#changement d'echelle
        try :
            res = cv2.matchTemplate(img_gray,template_match,cv2.TM_CCOEFF_NORMED)
            min_val,max_val,min_loc,max_loc = cv2.minMaxLoc(res)
            if best_match_board[0] < max_val :
                best_match_board[0] = max_val
                best_match_board[1] = k
            else :
                pass
        except :
            pass

    best_match_hand = [0,1] #[val,ratio]
    img_rgb = cv2.imread('src/scaling_hand.png')
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    for i in range(100,200) :
        k = i/100.0
        template_match = cv2.resize(template,(0,0), fx=k, fy=k)#changement d'echelle
        try :
            res = cv2.matchTemplate(img_gray,template_match,cv2.TM_CCOEFF_NORMED)
            min_val,max_val,min_loc,max_loc = cv2.minMaxLoc(res)
            if best_match_hand[0] < max_val :
                best_match_hand[0] = max_val
                best_match_hand[1] = k
            else :
                pass
        except :
            pass

    best_match_mboard = [0,1] #[val,ratio]
    img_rgb = cv2.imread('src/scaling_mboard.png')
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = template[70:130,80:150] #on conserve le portrait
    for i in range(50,200) :
        k = i/100.0
        template_match = cv2.resize(template,(0,0), fx=k, fy=k)#changement d'echelle
        try :
            res = cv2.matchTemplate(img_gray,template_match,cv2.TM_CCOEFF_NORMED)
            min_val,max_val,min_loc,max_loc = cv2.minMaxLoc(res)
            if best_match_mboard[0] < max_val :
                best_match_mboard[0] = max_val
                best_match_mboard[1] = k
            else :
                pass
            print max_val,max_loc
        except :
            pass
    #res = cv2.resize(template,(0,0), fx=best_match_mboard[1], fy=best_match_mboard[1])
    #cv2.imshow('try',res)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()

    return best_match_pick[1],best_match_board[1],best_match_mboard[1],best_match_hand[1]



def clickone(button):
    doublon = []
    try :
        for pt in zip(*button[::-1]):
            doublon.append(pt) # creation d'un liste de tuples
        pos = doublon_manager(doublon)
        autopy.mouse.move(pos[0][0],pos[0][1])
        autopy.mouse.click()
        return 1
    except :
        #print("objectif not found")
        return 0

def click_one(pos):#pos = [x y]
    autopy.mouse.move(pos[0],pos[1])
    time.sleep(0.1)
    autopy.mouse.click()
    time.sleep(0.1)
    return 1

def clicktwo(button):
    try:
        doublon = []
        for pt in zip(*button[::-1]):
            #print pt #return les points d'interets
            #print type(pt) #return les points d'interets
            doublon.append(pt) # creation d'un liste de tuples
        pos = doublon_manager(doublon)
        #print("pos",pos)
        autopy.mouse.move(pos[0][0],pos[0][1])
        autopy.mouse.click()
        time.sleep(1)
        autopy.mouse.move(pos[1][0],pos[1][1])
        autopy.mouse.click()
        return 1
    except:
        #print("button not found")
        return 0

def moveone(button):
    try:
        doublon = []
        for pt in zip(*button[::-1]):
            doublon.append(pt) # creation d'un liste de tuples
        pos = doublon_manager(doublon)
        autopy.mouse.move(pos[0][0],pos[0][1])
        time.sleep(2)
        return 1
    except:
        #print("button not found")
        return 0

def moveeach(button):
    cpt = 0
    thresh = 50
    try:
        doublon = []
        for pt in zip(*button[::-1]):
            doublon.append(pt) # creation d'un liste de tuples
        pos = doublon_manager(doublon)
        for p in pos :
            autopy.mouse.move(p[0],p[1])
            cpt = cpt +1
        time.sleep(1)
        return cpt
    except:
        #print("button not found")
        return 0



def engageone(pos):
    autopy.mouse.move(pos[0],pos[1])
    time.sleep(0.5)
    autopy.mouse.click()
    time.sleep(0.5)
    autopy.mouse.move(600,500)
    time.sleep(0.5)
    autopy.mouse.click()
    time.sleep(0.5)


def findone(img_template,zone=0,accu=0.71,coord=((0,0),(1105,810))) :
    #zone : 0 allboard / 1 ennemy / 2 self /3 hand
    if zone == 0 : #allboard
        rect=((0,0),(1105,810))
    elif zone == 1 :#ennemy
        rect=((0,0),(1105,405))
    elif zone == 2 :#self
        rect=((0,500),(1105,810))
    elif zone == 4 : #board
        rect=((0,250),(1105,550))
    elif zone == 5 : # on the go
        rect=(coord)
    elif zone == 3 :#hand
        rect=((0,475),(1105,810))

    tps1 = time.clock()
    autopy.bitmap.capture_screen(rect ).save('src/screengrab.png')# capture de l'ecran
    tps2 = time.clock()

    tps1 = time.clock()
    img_rgb = cv2.imread('src/screengrab.png')
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    w, h = img_template.shape[::-1]
    res = cv2.matchTemplate(img_gray,img_template,cv2.TM_CCOEFF_NORMED)
    threshold = accu
    loc = np.where( res >= threshold)
    tps2 = time.clock()
    #print("temps de capture ecran",tps2-tps1)

    #########OFFSET###########
    offset= [0,0] #[vertical, horizontal]
    if zone == 1 :
        offset = [0,0]
    elif zone == 2 :
        offset = [500,0]
    elif zone == 3 :
        offset = [475,0]
    elif zone == 4 :
        offset =[250,0]
    elif zone == 5 :
        offset = [coord[0][1],coord[0][0]]

    loc1=[x +offset[0] for x in loc[0]]
    loc2=[x +offset[1] for x in loc[1]]
    loc3=(np.array(loc1),np.array(loc2))


    #cv2.imshow('try',res)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
    #print(loc,type(loc),len(loc))
    return loc3 #retourne l'emplacement de l'image

def findone_cannyfilter(img_template,zone=0,accu=0.17) :
    #zone : 0 allboard / 1 ennemy / 2 self /3 hand
    if zone == 0 : #allboard
        rect=((0,0),(1105,810))
    elif zone == 1 :#ennemy
        rect=((0,0),(1105,405))
    elif zone == 2 :#self
        rect=((0,500),(1105,810))
    elif zone == 4 : #board
        rect=((0,250),(1105,550))
    #elif zone == 3 :#hand
        #rect=((0,650),(1105,810))
    autopy.bitmap.capture_screen(rect ).save('src/screengrab.png')# capture de l'ecran
    img_rgb = cv2.imread('src/screengrab.png')
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(img_gray,50,200)
    res = cv2.matchTemplate(edges,img_template,cv2.TM_CCORR_NORMED)
    threshold = accu
    loc = np.where( res >= threshold)
    #########OFFSET###########
    offset= [0,0] #[vertical, horizontal]
    if zone == 1 :
        offset = [0,0]
    elif zone == 2 :
        offset = [500,0]
    elif zone == 4 :
        offset =[250,0]
    loc1=[x +offset[0] for x in loc[0]]
    loc2=[x +offset[1] for x in loc[1]]
    loc3=(np.array(loc1),np.array(loc2))
    #cv2.imshow('try',res)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
    #print(loc,type(loc),len(loc))
    return loc3 #retourne l'emplacement de l'image


def tri_opti(numb,liste) : #fonction de trie
    for t in liste:
        if t[0] == numb :
            ind = liste.index(t)
    liste.insert(0,liste[ind])
    liste.pop(ind+1)
    #print "numb",numb,"liste",liste
    return liste

def doublon_manager(l) :
    #print "doublon_manager"
    l=set(l) #supprime les doublons grossiers
    l=list(l)
    if l != []:
        l_buff=[l[0]]
        thresh = 20
        for sub in l :
            for sub_buff in l_buff :
                if (abs(sub[0]-sub_buff[0])>thresh ) and (abs(sub[1]-sub_buff [1])> thresh) and (sub not in l_buff) :
                    pass
                else :
                    b = 1 # passe à 1 quand un doublon est trouvé
            if b == 0 :
                l_buff.append(sub)
            b=0
    else : #gestion des exceptions
        #print("pas de valeur reçue")
        l_buff = []
    #print "liste sans doublon :",l_buff
    return l_buff

def attack(pos_card,pos_ennemy) :
    autopy.mouse.move(pos_card[0],pos_card[1])
    time.sleep(0.5)
    autopy.mouse.click()
    time.sleep(0.5)
    autopy.mouse.move(pos_ennemy[0],pos_ennemy[1])
    time.sleep(0.5)
    autopy.mouse.click()
    time.sleep(0.5)





#Basic function which allow to capture the screen
#and treat it easily
#Return a gray screen capture
def ce() :
    autopy.bitmap.capture_screen().save('src/screengrab.png')# capture de l'ecran
    img_rgb = cv2.imread('src/screengrab.png')
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    return img_gray


def image_process(img_gray,img_template,threshold=0.71) :
    res = cv2.matchTemplate(img_gray,img_template,cv2.TM_CCOEFF_NORMED)
    loc = np.where( res >= threshold)
    return loc

def loc_filter(loc):
    doublon = []
    for pt in zip(*loc[::-1]):
        doublon.append(pt) # creation d'un liste de tuples
    pos = doublon_manager(doublon)
    return pos

    return


#Low level functon which take as argument :
# - a list of cards to test
# - pic -> with image u want to use
# - number of thread wanted
# ---> return [card_name,[position]]
def card_identification(list_cards,zone=0,pic=u'pic_template',card_expected = 1,Nthread = 1) :
#zone : 0 allboard / 1 ennemy / 2 self /3 hand
    found = []
    screen = ce() #screen

    if zone == 0 : #allboard /!\/!\/!\/!\/!\/!\/!\ Completement optimisable -> ne garder que le cas 5
        offset = [0,0]#/!\/!\/!\AJOUTER le multi threading :)
        #screen = screen[0:1024, 0:768]
        screen = screen[0:800, 0:1024] # pas mal
        pass
    elif zone == 1 :#ennemy
        offset = [3,63]#/!\/!\/!\AJOUTER le multi threading :)
        screen = screen[63:830, 3:960]
    elif zone == 2 :#self
        offset = [3,63]#
        screen = screen[63:830, 3:960]
    elif zone == 3 :#hand
        offset = [183,522]#
        screen = screen[522:830,183:808]
    elif zone == 4 : #board
        offset = [122,279]#
        screen = screen[279:596,122:890] #on conserve le portrait
    elif zone == 5 : # on the go
        offset = [coord[0][0],coord[0][1]]
        screen = screen[coord[0][0]:coord[1][0],coord[0][1]:coord[1][1]] #on conserve le portrait

    if Nthread == 1 :
        for t in list_cards :
            loc = image_process(screen,t[pic],0.85)
            if tuple_test(loc) != 0 :
                loc=loc_filter(loc)#filtrage des doublons (un peu approximatif ...)
                #########OFFSET###########
                liste_tuple = []
                for u in loc :
                    t1 = u[0] +offset[0]
                    t2 = u[1] +offset[1]
                    liste_tuple.append([t1,t2])
                found.append([t[u'name'],liste_tuple])
                if card_expected  :# on s'arrete à la premiere carte trouvee
                    break
                else :
                    pass #on continue
    else :
        global found_thread
        global exitFlag
        exitFlag = 0
        found_thread = []
        list_thread = [myThread("T %d" % (i) ,1,screen,list_cards[len(list_cards)*i/Nthread:len(list_cards)*(i+1)/Nthread],pic,offset,card_expected) for i in range(Nthread)]
        for obj in list_thread :
            obj.start()
            obj.join()
        for entity in found_thread :
            found.append(entity)
    return found

class myThread (threading.Thread):
    def __init__(self,name, threadID,screen,list_cards,pic,offset,card_expected):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.screen =screen
        self.list_cards = list_cards
        self.pic = pic
        self.offset = offset
        self.card_expected = card_expected
    def run(self):
        u=high_image_process(self.name,self.screen,self.list_cards ,self.pic,self.offset,self.card_expected)
        for entity in u :
            found_thread.append(entity)
        if (u != []) and (self.card_expected ==1) :
            exitFlag = 1

def high_image_process(threadName,screen,list_cards,pic,offset,card_expected) :
    found = []
    for t in list_cards :
        if exitFlag:
           thread.exit()
        loc = image_process(screen,t[pic],0.85)
        if tuple_test(loc) != 0 :
            loc=loc_filter(loc)#filtrage des doublons (un peu approximatif ...)
            liste_tuple = []
            for u in loc :
                t1 = u[0] +offset[0]
                t2 = u[1] +offset[1]
                liste_tuple.append([t1,t2])
            found.append([t[u'name'],liste_tuple])
            if card_expected :# on s'arrete à la premiere carte trouvee
                break
            else :
                pass #on continue
    return found
"""
def print_time(threadName, delay, counter):
    while counter:
        if exitFlag:
            thread.exit()
        time.sleep(delay)
        print "%s: %s" % (threadName, time.ctime(time.time()))
        counter -= 1

"""

