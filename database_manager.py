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
import subprocess

class Data_manager :
    """Classe de gestion de database"""
    def __init__(self):
        self.get_json() #creat a jason database from API
        self.k_pick,self.k_board,self.k_mboard,self.k_hand=init_scale()# get the right ratios
        print "Ratio mboard",self.k_mboard
        self.db_all = self.loading_cards() #load the database
        self.loading_img() # check for missing cards
        self.loading_deck() # deck loading
        self.mana = self.loading_database() #chargement des images

    def get_json(self):
        get_cmd = "sh ./src/get_database.sh"
        output = subprocess.check_output(['bash','-c', get_cmd])
        data_source=open('src/database_buf.json',"r")# -> contient un header indesirable
        data_target=open('src/database.json',"w")# -> contient les vrais data
        i=0 #increment
        for ligne_source in data_source :
            if i > 12 :
                data_target.write(ligne_source)
            i=i+1
        data_source.close()
        data_target.close()
        print "Database downloaded and adapted"
        return 0

    def download_img(self,img_url, filename):
            #first check is the image already exist
        dirList=os.listdir("src/cards_img/")
        listdir = []
        for dir in dirList :
            listdir.append(dir)
        if filename not in listdir : #si la carte n'est pas presente
            print("La carte :",filename,"is downloading")
            file_path = "./src/cards_img/%s" % ( filename)
            downloaded_image = file(file_path, "wb")
            image_on_web = urllib.urlopen(img_url)
            while True:
                buf = image_on_web.read(65536)
                if len(buf) == 0:
                    break
                downloaded_image.write(buf)
            downloaded_image.close()
            image_on_web.close()
        return file_path

    def loading_cards(self):
        json_data=open('src/database.json')
        data = json.load(json_data)
        json_data.close()
        cards = []
        main_cards=["Classic","Naxxramas","Blackrock Moutain","Basic","The Grand Tournament","Goblins vs Gnomes"]
        print("Sous deck charges :",main_cards)
        for classe in data :
            if classe in main_cards :
                for t in data[classe] :
                    cards.append(t)
        i=0
        return cards #return la liste de toutes les cartes du jeu

    def loading_img(self):
        for t in self.db_all :
            try :
                self.download_img(t[u'img'],t[u'name'])
            except :
                pass
    def loading_deck(self):
        print "Loading Deck"
        liste_deck = config_import() #import from config.txt
        for y in liste_deck :
            found = 0#Detecteur de fautes dans le fichier de config
            for t in self.db_all :
                if y == t[u'name']:
                    t[u'indeck'] = 1 #carte dans le deck
                    found = 1
                else :
                    pass
            if found == 1:
                print("Carte chargee ! :",y)
            else :
                print("Cette carte n'existe pas !",y)
        return 0

    def loading_database(self):
        mana_id=[]
        ref = (303,200)
        for i in self.db_all:#bot preload image
            path = 'src/cards_img/%s' %i[u'name']
            template = cv2.imread(path,0)
            if (template!=None) :
                size = template.shape #normalisation 302x200
                if size != ref :
                    #print name
                    k = float(ref[0])/float(size[0]) #1.1
                    template = cv2.resize(template,(0,0), fx=k, fy=k)#changement d'echelle
                    template = template[70:130,80:150] #on conserve le portrait
                else :
                    pass
                #template= template[90:120,90:120]
                i[u'pic_template']=template
                #Il vaut mieux faire les calculs maintenant ;)
                ##################HANDRESIZE#######################
                i[u'pic_hand']= cv2.resize(template,(0,0), fx=self.k_hand, fy=self.k_hand)#changement d'echelle
                ##################PICKRESIZE#######################
                i[u'pic_pick']= cv2.resize(template,(0,0), fx=self.k_pick, fy=self.k_pick)#changement d'echelle
                ##################BOARDRESIZE######################
                i[u'pic_board']= cv2.resize(template,(0,0), fx=self.k_board, fy=self.k_board)#changement d'echelle
                ##################MBOARDRESIZE######################
                i[u'pic_mboard']= cv2.resize(template,(0,0), fx=self.k_mboard, fy=self.k_mboard)#changement d'echelle

        for i in range(8): #depend of the max of your deck
            name = 'src/mana/mana%d.png' %i
            template = cv2.imread(name,0)
            if (template!=None) :
                #template= template[90:120,90:120]
                mana_id.append([i,template])
        print "Les images des cartes ont ete charge"
        return mana_id


    # Really importante function
    # Search in database according to argument
    # Return a list of concern cards
    # argument is a dictionnary : content = key of database

    def search_database(self,argument):
        found_list = []
        require_key = []
        for k in argument.keys():
            if argument[k] == 0 : #Si on veut recuperer seulement les cartes avec cette cle
                require_key.append(k)

        for d in self.db_all : # parcours de la database
            ok=0
            for d_key in argument.keys(): #on recupere les cles du dictionnaire
                #print("argument keys",argument.keys())
                #print ("argument original dico", d.keys())
                if d_key in d.keys() :
                    if d_key not in require_key :
                        pass
                    else :
                        break
                    if argument[d_key]==d[d_key] :
                        pass
                    else :
                        ok=1
                        break # si une condition n'est pas verifiee on sort de la boucle
                else :
                    ok =1
                    break
            if ok == 0 :
                found_list.append(d)# On ajoute une element qui verifie les conditions
        return found_list

