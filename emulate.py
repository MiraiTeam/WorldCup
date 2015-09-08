#coding=utf-8
import random
from arrange import *
from event import *

def GetPlayers(team):
    #return a List, the all player in this team, ordered by id 
    players = []
    #FW,MF,DF,GK
    p = ['FW','MF','DF','GK']
    t = [(1,5,4,1),(2,4,4,1),(3,3,4,1)]
    random.shuffle(t)
    for z in t:
        try:
            for i in range(-1,-5,-1):
                players += sorted(random.sample(team.players[p[i]],z[i]), key = lambda Player : Player.id)
            break
        except ValueError:
            players = []

    return players


def GetPlayersInfo(players):
    output = ''
    for p in players:
        output += '#%d, %s, %s\n' % (p.id,p.name,p.position)
    return output

def CreatEvent():
    # not done yet
    f = open("events.txt")
    for x in f.readlines():
        print x
    f.close()

def Play(teams,A,B,pA,pB,eventLib,timeout = False):
    #teams,teamA,teamB,the players of A,the players of B
	#当timeout为True时，允许加时赛
    output = ''
    rankA = teams[A].rank
    rankB = teams[B].rank
    #射门能力值
    abilityA = 1000 / rankA
    abilityB = 1000 / rankB
    score = [0,0] #scoreA and scoreB
    attack = [pA,pB]
    name = [A,B]
    t = 0  #time seconds
    eventP = 350.0 / 5400   #发生事件的概率
    weak = 0.2             #衰弱值
    morale = 0.1           #士气
    events = []
    t += random.randint(180,300)
    time = 90 * 60
    while t < time:
        r = random.random()
        if r < eventP:
            #发生事件
            c = random.random() <= 0.5
            d = 1 -  c
            a = random.randint(0,abilityA)
            b = random.randint(0,abilityB)
            k = [a,b]
            #c is the attacker, and d is the defender
            attacker = random.choice(attack[c][1:])
            defender = random.choice(attack[d][1:])
            if k[c] > k[d]:
                #success
                ev = Event(t,eventLib.GetEvent(teams[name[c]],teams[name[d]],attacker.name,defender.name,1))
                events.append(ev)
                output += str(ev)
                output += '\n'
                score[c] += 1
                k[c] *= (1.0 + morale)
                eventP *= (1.0 - weak)
                t += 120
                output += '当前比分: ' + str(score[0]) + ' : ' + str(score[1]) + '\n'
            else:
                #fail
                ev = Event(t,eventLib.GetEvent(teams[name[c]],teams[name[d]],attacker.name,defender.name,0))
                events.append(ev)
                output += str(ev)
                output += '\n'

        t += random.randint(3,180)
        if t >= time and (timeout and score[0] == score[1]):
			time += 30 * 60   #加时

		
				
    ev = Event(time,'比赛结束')
    events.append(ev)
    output += str(ev) + '\n'
    output += '最终比分: ' + str(score[0]) + ' : ' + str(score[1]) + '\n'
    return output

def Emulate(teams,arrange,eventLib):
    A = arrange.A
    B = arrange.B
    pA = GetPlayers(teams[A])
    pB = GetPlayers(teams[B])
    output = ''
    output += 'Group state:\n'
    output += A + ' vs ' + B + '\n'
    output += A + '\n'
    #output += GetPlayersInfo(pA)
    output += B + '\n'
    #output += GetPlayersInfo(pB)

    output += 'Playing...\n'
    output += Play(teams,A,B,pA,pB,eventLib)

    print output
    file = open('www.txt','w')
    file.writelines(output)
    file.close()

if __name__ == '__main__':
    #CreatEvent()
    teams = GetTeamsInfo()
    groups = Seeding(teams)
    arrange = GetArrangement(groups,0)
    eventLib = EventLib()
    Emulate(teams,arrange[0],eventLib)
