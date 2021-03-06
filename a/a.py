from tkinter import *
import numpy
import random
import time

#доделать ботгейм(сделать интерфейс и функционал и тд)

global amount, deck, playingDeck, decision
deck = [1,2,3,4,5,6,7,8,9,10,"jack","queen","king","ace"]
playingDeck = deck*4
score = 0
botScore = 0

def w(id,state):
    can.itemconfigure(id,state=state)

def dec(q):
    decision = q
    print(decision)

def lobby(): 
    amount = 0.0
    feed.config(text="Добро пожаловать в 21 для тех кто не играет в 21\nВведите количество игроков:")
    w(5,"normal")
    w(6,"hidden")
    w(7,"normal")

def giveCard(deck):
    score = deck[-1]
    info = translate(score)
    playingDeck.pop()
    score = info[1]
    cardname = info[0]
    return cardname,score

def translate(card): #переводит карты, которые не цифры, на русский для удобной игры
    cardNum = 0
    if isinstance(card,int) is not True:
        if card == "jack":
            card = "Валет"
            cardNum = 2
        elif card == "queen":
            card = "Королева"
            cardNum = 3
        elif card == "king":
            card = "Король"
            cardNum = 4
        elif card == "ace":
            card = "Туз"
            cardNum = 11
    else:
        cardNum = card
    return card, cardNum

def botPlay(deck,score,level,plScore):
    if level == 0:
        finScore = score
        name, score = giveCard(deck)
        print(type(score))
        finScore += score
        #return finScore
    elif level == 1:
        finScore = score
        if score > 14:
            if score < 21 and score > 16:
                score = giveCard(deck)
            else:
                score = 0
        else:
            score = giveCard(deck)
        finScore += score
    elif level == 666:
        finScore = score
        if (plScore <= 20 or plScore > 17) and plScore < finScore:
            score = 0
        else:
            score = giveCard(deck)
        finScore += score
    return finScore

def get_key(val,myDict): # взято с geeksforgeeks, выдает ключ по значению
    for key, value in myDict.items():
        if val == value:
            return key

def levelChoice():
    botlevel = 0
    if entry.get().lower() not in ["начальный","средний","шпион"]:
        if entry.get().lower() == "начальный":
            botlevel = 0
        elif entry.get().lower() == "средний":
            botlevel = 1
        elif entry.get().lower() == "шпион":
            botlevel = 666
    else:
        w(3,"normal")
        w(4,"normal")
        w(5,"hidden")
        w(8,"hidden")
        botGame(playingDeck,botlevel)

def botGame(deck,level):
    global botScore, score
    endgame = False
    if endgame is not True:
        if score < 21 and botScore < 21 and score != 21 and botScore != 21:
            feed.config(text="Хотите ли вы взять карту? y/n\n")
            main.wait_variable(decision)
            if decision.get() == 'y':
                cardname, plusScore = giveCard(deck)
                cardFeed.config(text=f"Вы вытянули: {cardname} с достоинством {plusScore}")
                botScore = botPlay(deck,botScore,level,score)
                score += plusScore
                scoreInfo.config(text=f"У вас {score} очков\nОчки бота:{botScore}")
            elif decision.get() == 'n':
                botScore = botPlay(deck,botScore,level,score)
                scoreInfo.config(text=f"У вас {score} очков\nОчки бота:{botScore}")
            else:
                feed.config(text="Неверная команда.")
            main.after(1000,botGame(deck,level))
        else:
            if botScore < 22 and (botScore == 21 or botScore > score or score > 21):
                print('Победил бот.')
                main.after(50000,main.destroy())
            elif score < 22 and (score == 21 or score > botScore or botScore > 21):
                print('Вы победили')
                main.after(50000,main.destroy())
            else:
                print("Ничья")
                main.after(50000,main.destroy())
def game(players):
    deck = playingDeck
    random.shuffle(deck)
    endgame = False
    randomlist = []
    if endgame is not True:
        if players > 1:
            temp = 0
            x = 0
            plDict = {}
            if 2<players<8:
                for i in range(players):
                    x += 1
                    temporary = input(f"Введите имя {x}-го игрока: ")
                    #plList.append(temporary)
                    plDict[temporary] = 0
                for j in plDict:
                    for i in range(2):
                        info = giveCard(deck)
                        temp += info[1]
                    plDict[j] = temp
                    temp = 0
                for i in list(plDict.keys()):
                # for i in list(plDict.keys()):print(i,end=' ')
                # было так, но я раб pylint'a
                    print(i,end=' ')
                print()
                for i in list(plDict.values()):
                    print(i,end=' ')
                if 21 in list(plDict.values()):
                    print(f"Выйграл {get_key(21,plDict)} игрок.")
                    endgame = True
                while any(i >= 21 for i in list(plDict.values())) is not True:
                    for i in plDict:
                        dec = input(f"\nУ игрока {i}:{plDict[i]} очков, он хочет взять карту(y/n)?\n")
                        if dec == "y":
                            cardname, plusScore = giveCard(deck)
                            plDict[i] += plusScore
                            print(f"Игрок {i} вытянул: {cardname} с достоинством {plusScore}. Его очки: {plDict[i]}")
                        elif dec == "n":
                            pass
                        else:
                            print("Неизвестная команда, пропускаем.")
                if 21 not in list(plDict.values()) and any(i < 21 for i in list(plDict.values())):
                    for i in list(plDict.values()):
                        if i < 21:
                            randomlist.append(i)
                    randomlist.sort()
                    print(f"Выйграл {get_key(randomlist[-1],plDict)}.")
                elif 21 in list(plDict.values()):
                    if list(plDict.values()).count(21) > 2:
                        print("Ничья.")
                    else:
                        ret = get_key(21, plDict)
                        print(f"Победил игрок {ret}.")
                main.after(2000,game(players))
            else:
                print('Неверное кол-во игроков.')
        elif players == 1:
            w(8,"normal")
            w(7,"hidden")
            entry.delete(0,END)
            feed.config(text="Какого уровня бота вы желаете?\nНачальный\nСредний\nШпион\n")
            levelChoice()
        else:
            print('Не пиши бред.')
    else:
        pass

main = Tk()
main.geometry("600x600")
main.title("21")
can = Canvas(main,width=600,height=600)
can.pack()
decision = StringVar()
feed = Label(main)
askCard=Label(main)
take = Button(main,text="Взять",command=lambda:decision.set("y"))
passCard = Button(main,text="Пропустить",command=lambda:decision.set("n"))
entry = Entry(main)
mainButton = Button(main,text="Играть",command=lobby)
playButton = Button(main,text="Продолжить",command=lambda: game(int(entry.get())))
botButton = Button(main,text="Выбрать",command=levelChoice)
scoreInfo = Label(main)
cardFeed = Label(main)
feedId = can.create_window(300,200,window=feed)
askCardId = can.create_window(300,300,window=askCard,state='hidden')
takeId = can.create_window(250,500,window=take,state='hidden')
passCardId= can.create_window(350,500,window=passCard,state='hidden')
entryId = can.create_window(300,300,window=entry,state='hidden')
mainButtonId = can.create_window(300,300,window=mainButton)
playButtonId = can.create_window(300,350,window=playButton,state='hidden')
botButtonId = can.create_window(300,350,window=botButton,state="hidden")
scoreInfoId = can.create_window(100,100,window=scoreInfo)
cardFeedId = can.create_window(300,100,window=cardFeed)

#can.itemconfigure(4, state='hidden')
print(entryId,botButtonId)
main.mainloop()