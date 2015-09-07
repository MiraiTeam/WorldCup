class Player:
    def __init__(self,name,country,id,position):
        self.name = name
        self.country = country
        self.id = id
        self.position = position

def GetPlayers():
    players = []
    file = open('players.txt','r')
    country = ''
    for u in file:
        u = u.replace('\n','')
        sp = u.split(' ')
        if sp[-1] == '\n':
            del sp[-1]
        try:
            id = int(sp[0])
            pos = sp[1]
            name = ' '.join(sp[2:])
            players.append(Player(name,country,id,pos))
        except:
            country = u
            print u
    file.close()
    return players

#GetPlayers()
