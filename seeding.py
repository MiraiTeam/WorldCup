import random
from teams import *

def GetPots(teams):
    #sorted by rank
    tr = sorted(teams,key = lambda Team : Team.rank)

    pots = [ [] for i in range(5)]
    selected = [False for i in range(len(tr))]
    #add host to pot 1
    for host in range(len(tr)):
        if tr[host].isHost():
            break

    pots[1].append(tr[host])
    selected[host] = True

    #add better team to pot 1
    haveSelected = 1
    for i in range(len(tr)):
        if not selected[i]:
            pots[1].append(tr[i])
            selected[i] = True
            haveSelected = haveSelected + 1
            if haveSelected == 8:
                break

    for i in range(len(tr)):
        if not selected[i]:
            t = tr[i]
            if t.confederation == 'AFC':
                pots[3].append(t)
            elif t.confederation == 'CAF':
                pots[2].append(t)
            elif t.confederation == 'CONCACAF':
                pots[3].append(t)
            elif t.confederation == 'CONMEBOL':
                pots[2].append(t)
            else:#UEFA
                pots[4].append(t)
            selected[i] = True
    return pots

def Seeding1(teams):
    pots = GetPots(teams)
    #step 1
    #a team from pot 4 to pot 2
    w = random.randint(0,len(pots[4])  - 1)
    pots[2].append(pots[4][w])
    country = pots[4][w].country
    del pots[4][w]
    return country,pots

def Seeding2(pots):
    #step 2
    groups = [[] for i in range(8)]
    groups[0].append(pots[1][0]);
    del pots[1][0]
    for i in range(1,8):
        w = random.randint(0,len(pots[1]) - 1)
        groups[i].append(pots[1][w])
        del pots[1][w]
    return groups

def Seeding3(pots,groups):
    g = 0
    for p in range(2,5):
        for i in range(8):
            w = random.randint(0,len(pots[p]) - 1)
            groups[g].append(pots[p][w])
            g = (g + 1) % 8
    return groups

def GetPotsInfo(pots):
    output = ''
    for p in range(1,5):
        output += 'pot' + str(p) + '\n'
        for t in pots[p]:
            output += ' ' + t.country + '\n'
    return output

def GetGroupsInfo(groups):
    output = ''
    for i in range(8):
        output += 'group ' + chr(ord('A') + i) + '\n'
        for t in groups[i]:
            output += ' ' + t.country + '\n'
    return output

def Seeding(teams):
    output = ''
    pots = GetPots(teams)
    output += 'First stage:\n'
    output += GetPotsInfo(pots)

    country,pots = Seeding1(teams)
    output += 'One European team was first randomly drawn from Pot 4 and placed into Pot 2: '
    output += country + '\n\n'
    output += 'After first draw\n'
    output += GetPotsInfo(pots)

    groups = Seeding2(pots)
    
    output += '\nThe Final Draw:\n'
    groups = Seeding3(pots,groups)
    output += GetGroupsInfo(groups)

    #Seeding Over
    print output
    file = open('finalDraw.txt','w')
    file.writelines(output)
    file.close()

teams = GetTeamsInfo()
Seeding(teams)