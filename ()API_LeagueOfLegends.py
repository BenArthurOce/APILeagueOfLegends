import requests
import json

#API + PLAYERNAME"
#===================
API_KEY = "----"
input_PlayerName = input("Type SummonerName Here: ")
games_Requested = 5


#RUN API 01: USERNAME TO PUUID
#==============================
def fReturn_Player_PUUID(input_PlayerName):
    URL = 'https://oc1.api.riotgames.com/lol/summoner/v4/summoners/by-name/'

    #Run API
    Full_URL = URL + input_PlayerName + "?api_key=" + API_KEY
    response_PlayerID = requests.get(Full_URL)

    a = response_PlayerID.json()['puuid']
    return a


#RUN API 02: GET LIST OF GAME ID FOR PLAYER
#==========================================
def fList_Of_Game_ID(PUUID):
    URL = "https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/"
    a = games_Requested

    #Run API
    sFull_URL = URL + PUUID + "/ids?start=0&count=" + str(a) + "&api_key=" + API_KEY
    response_GameList = requests.get(sFull_URL)

    #Update Global ID Game List
    a = []
    for data in response_GameList.json():
        a.append(data)
    return a


#RUN API 03: GET DETAILS OF EACH GAME
#==========================================
def fEach_Game_Details(input_PlayerName="BenArthur"):
    sBase_URL   = "https://americas.api.riotgames.com/lol/match/v5/matches/"
    PUUID       = fReturn_Player_PUUID(input_PlayerName)
    rGame_List  = fList_Of_Game_ID(PUUID)

    #Run Match API for each Game ID in Global List
    for i in range(len(rGame_List)):
        sGame_ID = rGame_List[i]
        Full_URL = sBase_URL + sGame_ID + "?api_key=" + API_KEY

        #Run Two API - One for metadata/participants, one for general game info
        response = requests.get(Full_URL)
        data_metadata   = response.json()['metadata']
        data_info       = response.json()['info']

        #Cycle Through metadata/Participants, find which player number our lookup is (k)
        #Then use that player number reference (k) to get player information in "info" dictionary
        k = -1
        for j in data_metadata['participants']:
            k += 1
            if j == PUUID:
                MatchID = data_metadata['matchId']
                TypeOfGame  = data_info['gameMode']
                Player_k = data_info['participants'][k]
                
                print("GameInfo| ID: {0:15} CMP: {1:13} Map:{2:7} |    KDA| {3:3}/{4:3}/{5:3} |   SpellCasts| Q:{6:3},   W:{7:3},   E:{8:3},   R:{9:3} |  SummonerCasts| D:{10:2},   F:{11:2} |".format(MatchID,Player_k['championName'],TypeOfGame,Player_k['kills'],Player_k['deaths'],Player_k['assists'],Player_k['spell1Casts'],Player_k['spell2Casts'],Player_k['spell3Casts'],Player_k['spell4Casts'],Player_k['summoner1Casts'],Player_k['summoner2Casts']))



fEach_Game_Details(input_PlayerName)