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
                players += sorted(random.sample(team.players[p[i]].values(),z[i]), key = lambda Player : Player.id)
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
    menjiang = ['','']
    for i in range(2):
        for p in attack[i]:
            if p.position == 'GK':
                menjiang[i] = p.name
                break

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
                ev = Event(t,eventLib.GetEvent(teams[name[c]],teams[name[d]],attacker.name,defender.name,menjiang[d],1),score)
                events.append(ev)
                output += str(ev) + '\n'
                score[c] += 1
                k[c] *= (1.0 + morale)
                eventP *= (1.0 - weak)
                t += 120
                output += '当前比分: ' + str(score[0]) + ' : ' + str(score[1]) + '\n'
                #update player info
                teams[name[c]].players[attacker.position][attacker.name].info['g'] += 1
            else:
                #fail
                ev = Event(t,eventLib.GetEvent(teams[name[c]],teams[name[d]],attacker.name,defender.name,menjiang[d],0),score)
                events.append(ev)
                output += str(ev) + '\n'

        t += random.randint(3,180)
        if t >= time and (timeout and score[0] == score[1]):
			ev = Event(time,'进入加时赛',score)
			events.append(ev)
			output += str(ev) + '\n'
			output += '当前比分: ' + str(score[0]) + ' : ' + str(score[1]) + '\n'
			time += 30 * 60   #加时

	msg = '比赛结束，最终比分: ' + str(score[0]) + ' : ' + str(score[1]) + ', '
	
    if score[0] == score[1]:
		msg += '平局'
    else:
		msg += name[score[0] < score[1]] + '队胜利！'
    ev = Event(time,msg,score)
    events.append(ev)
    output += str(ev) + '\n'

    #统计结果
    if score[0] == score[1]:
        teams[A]['d'] += 1
        teams[A]['gf'] += score[0]
        teams[A]['ga'] += score[1]

        teams[B]['d'] += 1
        teams[B]['gf'] += score[1]
        teams[B]['ga'] += score[0]
    else:
        w = score[0] < score[1]
        l = 1 - w
        teams[name[w]].info['w'] += 1
        teams[name[l]].info['l'] += 1
        teams[A].info['gf'] += score[0]
        teams[A].info['ga'] += score[1]
        teams[B].info['gf'] += score[1]
        teams[B].info['ga'] += score[0]
	
    #update gd
    teams[A].info['gd'] = teams[A].info['gf'] - teams[A].info['ga']
    teams[B].info['gd'] = teams[B].info['gf'] - teams[B].info['ga']
    #update pts
    teams[A].info['pts'] = teams[A].info['w'] * 3 + teams[A].info['d']
    teams[B].info['pts'] = teams[B].info['w'] * 3 + teams[B].info['d']

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
