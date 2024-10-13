import requests
import tkinter as tk
from tkinter import *
import warnings
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import info
import time

inf = info.info()
api_key = inf.get_api_key()
summoner_name = str.title("")  # input("Enter in a summoner name: ")

ingame = True
previousGold = 0
totalGold = 0



def playerScreen():
    windowX = 800
    windowY = 600
    playerWindow = tk.Tk()
    playerWindow.geometry(f"{windowX}x{windowY}")
    frameX = int((windowX/5)-20)
    frameY = int((windowY/2)-20)

    mainFrame = Frame(playerWindow)
    mainFrame.grid(row=0, column=0)



    s1Frame = Frame(mainFrame, bg="RED", width=frameX, height=frameY)
    s1Frame.grid(row=0, column=0, padx=10)



    s1NameLabel = Label(s1Frame, text="Loading", bg="RED", wraplength=frameX)
    s1NameLabel.pack()
    s1wlLabel = Label(s1Frame, text='Loading', bg="RED", wraplength=frameX)
    s1wlLabel.pack()
    s1wrLabel = Label(s1Frame, text='Loading', bg="RED", wraplength=frameX)
    s1wrLabel.pack()


    # s1wrLabel.pack()

    #s1Frame.place(relwidth=0.8, relheight=.8, relx=0.1, rely=0.1)

    s2Frame = Frame(mainFrame, bg="GREEN", width=frameX, height=frameY)
    s2Frame.grid(row=0, column=2, padx=10)

    s2NameLabel = Label(s2Frame, text="Loading", bg="GREEN", wraplength=frameX)
    s2NameLabel.pack()
    s2wlLabel = Label(s2Frame, text='Loading', bg="GREEN", wraplength=frameX)
    s2wlLabel.pack()
    s2wrLabel = Label(s2Frame, text='Loading', bg="GREEN", wraplength=frameX)
    s2wrLabel.pack()



    s3Frame = Frame(mainFrame, bg="GREEN", width=frameX, height=frameY)
    s3Frame.grid(row=0, column=3, padx=10)

    s3NameLabel = Label(s3Frame, text="Loading", bg="GREEN", wraplength=frameX)
    s3NameLabel.pack()
    s3wlLabel = Label(s3Frame, text='Loading', bg="GREEN", wraplength=frameX)
    s3wlLabel.pack()
    s3wrLabel = Label(s3Frame, text='Loading', bg="GREEN", wraplength=frameX)
    s3wrLabel.pack()



    s4Frame = Frame(mainFrame, bg="GREEN", width=frameX, height=frameY)
    s4Frame.grid(row=0, column=4, padx=10)

    s4NameLabel = Label(s4Frame, text="Loading", bg="GREEN", wraplength=frameX)
    s4NameLabel.pack()
    s4wlLabel = Label(s4Frame, text='Loading', bg="GREEN", wraplength=frameX)
    s4wlLabel.pack()
    s4wrLabel = Label(s4Frame, text='Loading', bg="GREEN", wraplength=frameX)
    s4wrLabel.pack()


    s5Frame = Frame(mainFrame, bg="GREEN", width=frameX, height=frameY)
    s5Frame.grid(row=0, column=5, padx=10)

    s5NameLabel = Label(s5Frame, text="Loading", bg="GREEN", wraplength=frameX)
    s5NameLabel.pack()
    s5wlLabel = Label(s5Frame, text='Loading', bg="GREEN", wraplength=frameX)
    s5wlLabel.pack()
    s5wrLabel = Label(s5Frame, text='Loading', bg="GREEN", wraplength=frameX)
    s5wrLabel.pack()


    playerInfo(playerWindow)
    playerWindow.title("Summoner Info")

    playerWindow.mainloop()



def get_Player_Stats():
    id_url = "https://oc1.api.riotgames.com/lol/summoner/v4/summoners/by-name/" + summoner_name + "?api_key=" + api_key
    response = requests.get(id_url)
    results_json = response.json()
    encrypted_id = results_json['id']
    puuid = results_json['puuid']

    stats_url = "https://oc1.api.riotgames.com/lol/league/v4/entries/by-summoner/" + encrypted_id + "?api_key=" + api_key
    response = requests.get(stats_url).json()
    rd = response[0]  # response is returned as a single element list formatted as a dict. This makes it a dict
    wins = rd['wins']
    losses = rd['losses']
    tier = rd['tier']
    rank = rd['rank']
    lp = rd['leaguePoints']
    winrate = int(wins * 100 / (wins + losses))
    wrLabel.config(text=f'Win rate: {winrate}%')
    winsLabel.config(text=f'{wins} Wins')
    lossLabel.config(text=f'{losses} Losses')
    rankLabel.config(text=f'{tier} {rank} {lp}lp')

def gameState():
    global ingame
    global previousGold
    global totalGold
    gameStatusLabel.config(text="Player not in game")
    csminLabel.after(100000, get_Stats)
    if ingame == True:
        ingame = False
        previousGold = 0
        totalGold = 0
        time.sleep(5)
        get_Player_Stats()


def get_Stats():

    global previousGold
    global totalGold
    #pull data and turn to json
    warnings.simplefilter('ignore',InsecureRequestWarning)
    try:
        playerResponse = requests.get("https://127.0.0.1:2999/liveclientdata/playerscores?summonerName=", verify=False)
    except:
        gameState()
        return
    try:
        gameResponse = requests.get("https://127.0.0.1:2999/liveclientdata/gamestats", verify=False)
        activePlayerResponse = requests.get("https://127.0.0.1:2999/liveclientdata/activeplayer", verify=False)
        aResults_json = activePlayerResponse.json()
        gResults_json = gameResponse.json()
        presults_json = playerResponse.json()
        ingame = True
        gameStatusLabel.config(text="Player in game")
        # playerScreen()
        #game stats
        seconds = gResults_json['gameTime']
        minutes = seconds/60

        if seconds < 1:
            csminLabel.after(5000, get_Stats)
            return

        
        
        #player stats
        cs = presults_json['creepScore']
        #kd = presults_json['kills'] / presults_json['deaths']
        wardScore = '%.0f' % presults_json['wardScore']

        currentGold = aResults_json['currentGold']

        #gold
        if (currentGold - previousGold) > 0:
            totalGold = (currentGold - previousGold) + totalGold
        previousGold = currentGold
        goldmin = '%.0f' % (totalGold/minutes)


        
        wardLabel.config(text=f'Ward: {wardScore}')
        
        # if minutes < 1:
        #     goldLabel.config(test=f'Gold/min: 500')
        # else:
        goldLabel.config(text=f'Gold/min: {goldmin}')
        # if cs == 0:
        #csminLabel.after(1000, get_Stats)
            # return
        
        if (cs % 10) == 0: 
            csm = '%.2f' % (cs/minutes)

        if(seconds % 30) == 0:
            csm = '%.2f' % (cs/minutes)
        csminLabel.config(text=f"cs/min: {csm}")
        csminLabel.after(1000, get_Stats)
    
    except Exception as e: 
        print(e)
        gameState()
        return

    # print(cs)
    # print(kd)
    # print(wardScore)



root = tk.Tk()

root.geometry("200x200")
frame = Frame(root, relief=FLAT, height=100, width=100)
frame.pack()

gameStatusLabel = Label(frame, text="Pending")
gameStatusLabel.pack()

csminLabel = Label(frame, text='cs/min: 0.00')
csminLabel.pack()

wardLabel = Label(frame, text="Ward: 0")
wardLabel.pack()

goldLabel = Label(frame, text="Ward: 0")
goldLabel.pack()
csminLabel.after(1000, get_Stats)


wrLabel = Label(frame, text="Win rate: %")
wrLabel.pack()

winsLabel = Label(frame, text="")
winsLabel.pack()

lossLabel = Label(frame, text='')
lossLabel.pack()

rankLabel = Label(frame, text='')
rankLabel.pack()

get_Player_Stats()
frame.place(relwidth=0.8, relheight=.8, relx=0.1, rely=0.1)
root.title("Test")
root.wait_visibility(root)
root.attributes('-topmost', True)
root.attributes('-alpha', 0.5)



root.mainloop()


