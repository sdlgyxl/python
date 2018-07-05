#-*- coding:utf-8 -*-
#定义一个柱子类，下面会实例化A，B，C三个柱子
class pillar():
    def __init__(self,name,disks=0):
        self.name=name
        if disks:
            self.p=[i for i in range(disks,0,-1)]
        else:
            self.p=[]
 
    def name(self):
        return self.name
 
    def getDiskCounts(self):
        return len(self.p)
     
    def getTopDisk(self):
        diskCounts=self.getDiskCounts()
        if diskCounts:
            return self.p[diskCounts-1]
        return None
 
    def moveDisk(self):
        self.p.pop()
 
    def addDisk(self,newDisk):
        self.p.append(newDisk)
 
#给定两个柱子，确定应该移动哪个柱子上的盘子
def whichToMove(box):
    mins=box[0].getTopDisk(),box[0].name
    if mins[0]:
        if box[1].getTopDisk() and mins[0]>box[1].getTopDisk():
            mins=box[1].getTopDisk(),box[1].name
            box[1].moveDisk()
        else:
            box[0].moveDisk()
    else:
        mins=box[1].getTopDisk(),box[1].name
        box[1].moveDisk()
    return mins
 
#确定应该往哪个柱子上移动
def toNext(num,a):
    if disks%2==0:
        sequence={'a':'b','b':'c','c':'a'}
    else:
        sequence={'a':'c','c':'b','b':'a'}
    for i in [A,B,C]:
        if i.name==sequence[a]:
            if not i.getTopDisk():
                return i
            if num<i.getTopDisk():
                return i
            return name2obj(sequence[i.name])
 
def name2obj(a):
    for i in [A,B,C]:
        if i.name==a:
            return i
 
def show():
    f=open('e:\\temp\\hanoi.txt', 'w')
    for i in [A,B,C]:
        #print(i.name,'----',i.p)
        f.write('%s------%s\n'%(i.name, i.p))
    f.close()

def main():
    S=[A,B]
    f=open('e:\\temp\\hanoi.txt', 'w')
    while C.getDiskCounts()<disks:
        mins=whichToMove(S)
        tonext=toNext(mins[0],mins[1])
        tonext.addDisk(mins[0])
        S=[A,B,C]
        #刚移动的盘子，下一步肯定不会移动，所以将此柱子剔除，
        #从剩下的两个柱子中确定下一步应该从哪个柱子移动
        S.remove(tonext)
        #print('move %c --> %c,\tdisk %d'%(mins[1],tonext.name,mins[0]))
        f.print('move %c --> %c,\tdisk %d\n'%(mins[1],tonext.name,mins[0]))
    f.close()
 
if __name__=='__main__':
    disks=int(input('how many disks: '))
    A=pillar('a',disks)
    B=pillar('b')
    C=pillar('c')
    show()
    main()
    show()
