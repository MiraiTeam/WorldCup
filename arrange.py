import datetime
from seeding import *

class Arrangement:
    def __init__(self,A,B,group,place,time):
        self.A = A
        self.B = B
        self.group = group
        self.place = place
        self.time = time
    def GetTime(self):
        st = datetime.datetime(2014,6,11)
        nt = st + datetime.timedelta(days = self.time)
        months = ['','January','February','March','April','May','June',\
                    'July','August','September','October','November','December']
        return months[nt.month] + ' ' + str(nt.day)


def GetPlaces():
    places = []
    file = open('places.txt','r')
    for line in file:
        places.append(line.replace('\n',''))
    file.close()
    return places

def GetArrangement(groups,startDay):
    #return a List, the all arrangement
    arrange = []
    places = GetPlaces()
    day  = startDay
    for (i,j) in {(0,1),(1,2),(2,3),(3,0),(0,2),(1,3)}:
        for k in range(2):
            pl = random.sample(places,4)
            for u in range(4):
                g = k * 4 + u
                A = groups[g][i]
                B = groups[g][j]
                arrange.append(Arrangement(A,B,chr(ord('A') + g),pl[u],day))
            day += 1
    return arrange

def PrintArrangement(arrange):
    #arrange is a List
    #sort arrange by time
    arrange = sorted(arrange, key = lambda Arrangement : Arrangement.time)

    output = 'Matches by squads\n'
    #print arrangement by group
    arr = [[] for i in range(16)]
    for a in arrange:
        arr[ord(a.group) - ord('A')].append(a)

    for g in range(8):
        output += 'Group ' + chr(ord('A') + g) + '\n'
        for a in arr[g]:
            output += ' ' + a.A + ' vs ' + a.B + ', '
            output += a.place + ', '
            output += a.GetTime() + '\n'

    output += '\n'
    output += 'Matches by date\n'
    ti = -1
    for a in arrange:
        if ti != a.time:
            output += a.GetTime() + '\n'
            ti = a.time
        output += ' ' + a.A + ' vs ' + a.B + ', '
        output += a.place + '\n'

    print output
    file = open('schedule16.txt','w')
    file.writelines(output)
    file.close()

if __name__ == '__main__':
    teams = GetTeamsInfo()
    PrintTeamsInfo(teams)
    groups = Seeding(teams)
    arrange = GetArrangement(groups,0)
