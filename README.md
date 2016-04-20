####### Hearthstone_bot #######

#Overview
Simple Hearthstone bot based on python2 and openCV
This bot is intended to be used on a linux system, nevertheless could be adpated for windows...


#Dependencies
*Python2
* OpenCV
*pip2.7 -> packet named python2_pip
* Python autopy // keyboard & mouse control
    $sudo pip2.7 install autopy
* Python numpy // mostly math
    $sudo pip2.7 install numpy
* hearthstone API www.hearthstoneapi.com

#Basic use
1/Set your game in english
2/Set your game resolution at 1024x768 and move the window in the top left corner.
....Why ? The bot processes your screen, in order to reduce the number of computation, only a small part of the screen is actually used.
3/Enter the deck you want to use in bot_deck.txt
....The bot will easily recognize your own cards
4/Launch the bot: $python2.7 game.py
....If it's your first run, the bot will generate an entire database. (pics + information)

#Working modules
-game management (start/stop/skip-pass turn)
-identify your hand
-play a card on the board

#Not working modules
-recognize a card already on the board, in particular from your opponent side.

Sorry for the code, looks like something terrible happened...
Sorry for the french name / french comment (such a bad habit ^^)



