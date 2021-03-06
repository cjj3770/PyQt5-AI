import sys,os
if hasattr(sys, 'frozen'):
    os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']
from PyQt5 import QtCore,QtGui,QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from Btp import Ui_MainWindow
import random
import math
import numpy as np
import copy
from queue import Queue
from queue import LifoQueue

def BoardState(self, State):
    for i in range(4):
        for j in range(4):
            if State[i][j] == 1:
                self.label_A.setGeometry(50 * j+10, 50 * i+10, 50, 50)
            if State[i][j] == 2:
                self.label_B.setGeometry(50 * j+10, 50 * i+10, 50, 50)
            if State[i][j] == 3:
                self.label_C.setGeometry(50 * j+10, 50 * i+10, 50, 50)
            if State[i][j] == 55:
                self.label_T.setGeometry(50 * j+10, 50 * i+10, 50, 50)
            if State[i][j] == 9:
                self.label_O.setGeometry(50 * j+10, 50 * i+10, 50, 50)

def SequenceState(State):
    string = '+---+---+---+---+\n'
    for i in range(4):
        for j in range(4):
            string+='| {} '.format(' ' if State[i][j] == 0 else numbers_to_strings(State[i][j]))
        string += '|\n'
        string += '+---+---+---+---+\n'
    return string

def numbers_to_strings(item):
    switcher = {
        55: "T",
        9:"O",
        1: "A",
        2: "B",
        3: "C"
    }
    return switcher.get(item)

def ShowState(self):
    StartState[0][0] = DictState[self.lineEdit]
    StartState[0][1] = DictState[self.lineEdit_2]
    StartState[0][2] = DictState[self.lineEdit_3]
    StartState[0][3] = DictState[self.lineEdit_4]
    StartState[1][0] = DictState[self.lineEdit_5]
    StartState[1][1] = DictState[self.lineEdit_6]
    StartState[1][2] = DictState[self.lineEdit_7]
    StartState[1][3] = DictState[self.lineEdit_8]
    StartState[2][0] = DictState[self.lineEdit_9]
    StartState[2][1] = DictState[self.lineEdit_10]
    StartState[2][2] = DictState[self.lineEdit_11]
    StartState[2][3] = DictState[self.lineEdit_12]
    StartState[3][0] = DictState[self.lineEdit_13]
    StartState[3][1] = DictState[self.lineEdit_14]
    StartState[3][2] = DictState[self.lineEdit_15]
    StartState[3][3] = DictState[self.lineEdit_16]
    BoardState(self, StartState)

def GoalState(State):
    if (State[1][1] == 1 and State[2][1] == 2 and State[3][1] == 3):
        return True

def FindAgent(State):
    for i in range(4):
        for j in range(4):
            if State[i][j] == 55:
                return i, j

def FindObstacles(State):
    for i in range(4):
        for j in range(4):
            if State[i][j]==9:
                return i,j
    return None,None

def Move(State,Direction):
    NewState=copy.deepcopy(State)
    X,Y=FindAgent(NewState)
    Ox,Oy=FindObstacles(NewState)
    if Direction=="Up":
        NewX,NewY=X-1,Y
        if NewX<0:
            return None
        elif NewX==Ox and NewY==Oy:
            return None
        else:
            NewState[X][Y],NewState[NewX][NewY]=NewState[NewX][NewY],NewState[X][Y]
            return NewState
    if Direction=="Down":
        NewX,NewY=X+1,Y
        if NewX>3:
            return None
        elif NewX==Ox and NewY==Oy:
            return None
        else:
            NewState[X][Y],NewState[NewX][NewY]=NewState[NewX][NewY],NewState[X][Y]
            return NewState
    if Direction=="Right":
        NewX,NewY=X,Y+1
        if NewY>3:
            return None
        elif NewX==Ox and NewY==Oy:
            return None
        else:
            NewState[X][Y],NewState[NewX][NewY]=NewState[NewX][NewY],NewState[X][Y]
            return NewState
    if Direction=="Left":
        NewX,NewY=X,Y-1
        if NewY<0:
            return None
        elif NewX==Ox and NewY==Oy:
            return None
        else:
            NewState[X][Y],NewState[NewX][NewY]=NewState[NewX][NewY],NewState[X][Y]
            return NewState

def find(State,target):
    for i in range(4):
        for j in range(4):
            if target=="A":
                if State[i][j]==1:
                    return i,j
            if target=="B":
                if State[i][j]==2:
                    return i,j
            if target=="C":
                if State[i][j]==3:
                    return i,j

def h(State):
    Misplaced=0
    Distance=0
    if State[1][1] != 1:
        Misplaced+=1
        X,Y=find(State,"A")
        Distance += math.fabs(X-1)+math.fabs(Y-1)
    if State[2][1] != 2:
        Misplaced+=1
        X,Y=find(State,"B")
        Distance += math.fabs(X-2)+math.fabs(Y-1)
    if State[3][1] != 3:
        Misplaced+=1
        X,Y=find(State,"C")
        Distance += math.fabs(X-3)+math.fabs(Y-1)
    Heuristic=Distance+Misplaced
    return Heuristic

def f(Node, h):
    f = (Node.Depth + h)
    return f

class Node:
    def __init__(self, State, Parent, Action, Depth, Cost):
        self.State = State
        self.Parent = Parent
        self.Action = Action
        self.Depth = Depth
        self.Cost = Cost

def CreateNode(State, Parent, Action, Depth, Cost):
    return Node(State, Parent, Action, Depth, Cost)

def BfsExpandNode(Node, BfsQueue):
    childNodeState = Move(Node.State, "Up")
    if childNodeState is not None:
        BfsQueue.put(CreateNode(childNodeState, Node, "UP", Node.Depth + 1, 0))

    childNodeState = Move(Node.State, "Down")
    if childNodeState is not None:
        BfsQueue.put(CreateNode(childNodeState, Node, "DOWN", Node.Depth + 1, 0))

    childNodeState = Move(Node.State, "Right")
    if childNodeState is not None:
        BfsQueue.put(CreateNode(childNodeState, Node, "RIGHT", Node.Depth + 1, 0))

    childNodeState = Move(Node.State, "Left")
    if childNodeState is not None:
        BfsQueue.put(CreateNode(childNodeState, Node, "LEFT", Node.Depth + 1, 0))
    return BfsQueue

def DfsExpandNode(Node, DfsQueue):
    i = range(4)
    k = random.sample(i, len(i))
    for j in k:
        if j == 0:
            childNodeState = Move(Node.State, "Up")
            if childNodeState is not None:
                DfsQueue.put(CreateNode(childNodeState, Node, "UP", Node.Depth + 1, 0))
        if j == 1:
            childNodeState = Move(Node.State, "Down")
            if childNodeState is not None:
                DfsQueue.put(CreateNode(childNodeState, Node, "DOWN", Node.Depth + 1, 0))
        if j == 2:
            childNodeState = Move(Node.State, "Right")
            if childNodeState is not None:
                DfsQueue.put(CreateNode(childNodeState, Node, "RIGHT", Node.Depth + 1, 0))
        if j == 3:
            childNodeState = Move(Node.State, "Left")
            if childNodeState is not None:
                DfsQueue.put(CreateNode(childNodeState, Node, "LEFT", Node.Depth + 1, 0))
    return DfsQueue

def AstarExpandNode (Node):
    ExpandFringe=[]
    ExpandFringe.append(CreateNode(Move(Node.State,"Up"),Node, "UP", Node.Depth+1, f(Node,h(Node.State))))
    ExpandFringe.append(CreateNode(Move(Node.State,"Down"),Node, "DOWN", Node.Depth+1, f(Node,h(Node.State))))
    ExpandFringe.append(CreateNode(Move(Node.State,"Right"),Node, "RIGHT", Node.Depth+1, f(Node,h(Node.State))))
    ExpandFringe.append(CreateNode(Move(Node.State,"Left"),Node, "LEFT", Node.Depth+1, f(Node,h(Node.State))))
    ExpandFringe = [Node for Node in ExpandFringe if Node.State is not None]
    return ExpandFringe



StartState = np.zeros((4, 4), dtype=np.int)
TimeComplexity = 0
depth = 0
sequence=""
DepthLimit=0

def BFS(Start):
    global TimeComplexity, depth, sequence, StartState
    TimeComplexity = depth = 0
    sequence = ""
    BfsQueue = Queue()
    Moves = [None]
    Node = CreateNode(Start, None, None, 0, 0)
    BfsQueue.put(Node)
    if GoalState(Node.State) == True:
        sequence = "The time complexity is: 0"+"\n"+"Starting state was the goal"
        return Moves, TimeComplexity
    while True:
        if BfsQueue.empty():
            sequence ="No solution found"
            return None, TimeComplexity
        else:  # 否则
            Node = BfsQueue.get()
            TimeComplexity += 1
            StartState=Node.State
            depth=Node.Depth
        if GoalState(Node.State) == True:
            Moves = []
            Configuration = []
            sequence = ""
            while True:
                Moves.insert(0, Node.Action)
                Configuration.insert(0, Node.State)
                if Node.Depth == 1:
                    break
                Node = Node.Parent
            for count in range(0, len(Moves)):
                sequence+=Moves[count]+"\n"
                sequence+=SequenceState(Configuration[count])
            return Moves, TimeComplexity
        else:
            BfsQueue = BfsExpandNode(Node, BfsQueue)  # 如果不是目标状态

            if TimeComplexity % 10000 == 0:
                print(TimeComplexity)

def DFS(Start, DepthLimit):
    global TimeComplexity, depth, sequence, StartState
    if DepthLimit==999:
        TimeComplexity = depth = 0
        sequence = ""
    DfsQueue = LifoQueue()
    Moves = [None]
    Node = CreateNode(Start, None, None, 0, 0)
    DfsQueue.put(Node)

    if GoalState(Node.State) == True:
        sequence = "The time complexity is: 0"+"\n"+"Starting state was the goal"
        return Moves, TimeComplexity
    while True:
        if DfsQueue.empty():
            sequence ="No solution found"
            return None, TimeComplexity
        else:  # 否则
            Node = DfsQueue.get()
            TimeComplexity += 1
            StartState=Node.State
            depth=Node.Depth
        if GoalState(Node.State) == True:
            Moves = []
            Configuration = []
            sequence=""
            while True:
                Moves.insert(0, Node.Action)
                Configuration.insert(0, Node.State)
                if Node.Depth == 1:
                    break
                Node = Node.Parent
            for count in range(0, len(Moves)):
                sequence+=Moves[count]+"\n"
                sequence+=SequenceState(Configuration[count])
            return Moves, TimeComplexity
        else:
            if DepthLimit==999:
                DfsQueue = DfsExpandNode(Node, DfsQueue)  # 如果不是目标状态
            else:
                if Node.Depth <= DepthLimit:
                    DfsQueue = DfsExpandNode(Node, DfsQueue)  # 如果不是目标状态
            if TimeComplexity%10000==0:
                print(TimeComplexity)

def Astar(Start):
    global TimeComplexity, depth, sequence, StartState
    TimeComplexity=depth= 0
    sequence = ""
    Fringe = []
    Moves = [None]
    Node=CreateNode( Start, None, None, 0, h(Start))
    Fringe.append( Node )
    if GoalState(Node.State)==True:
        sequence = "The time complexity is: 0" + "\n" + "Starting state was the goal"
        return Moves, TimeComplexity
    while True:
        if len( Fringe ) == 0:
            sequence = "No solution found"
            return None, TimeComplexity
        else:
            if len(Fringe)>1:
                Fringe = sorted(Fringe, key=lambda Node: Node.Cost)
            Node = Fringe.pop(0)
            TimeComplexity+=1
            StartState=Node.State
            depth=Node.Depth
        if GoalState(Node.State) == True:
            Moves=[]
            Configuration = []
            sequence = ""
            while True:
                Moves.insert(0, Node.Action)
                Configuration.insert(0,Node.State)
                if Node.Depth == 1:
                    break
                Node = Node.Parent
            for count in range(0, len(Moves)):
                sequence += Moves[count] + "\n"
                sequence += SequenceState(Configuration[count])
            return Moves, TimeComplexity
        else:
            Fringe.extend(AstarExpandNode(Node))
            if TimeComplexity%10000==0:
                print(TimeComplexity)

class bfsWorkThread(QThread):
    trigger = pyqtSignal()
    def __int__(self):
        super(bfsWorkThread, self).__init__()
    def run(self):
        Result, Time = BFS(StartState)
        if Result == None:
            print("No solution found")
        elif Result == [None]:
            print("The time complexity is:", Time)
            print("Starting state was the goal")
        else:
            print("The time complexity is:", Time)
            print("The goal state was achieved in:", len(Result), "moves")
        self.trigger.emit()

class dfsWorkThread(QThread):
    trigger = pyqtSignal()
    def __int__(self):
        super(dfsWorkThread, self).__init__()
    def run(self):
        Result, Time = DFS(StartState,999)
        if Result == None:
            print("No solution found")
        elif Result == [None]:
            print("The time complexity is:", Time)
            print("Starting state was the goal")
        else:
            print("The time complexity is:", Time)
            print("The goal state was achieved in:", len(Result), "moves")
        self.trigger.emit()

def IDS(Start):
    global sequence, DepthLimit,TimeComplexity
    TimeComplexity=0
    for i in range(DepthLimit):
        Moves, Time = DFS(Start,i)
        TimeComplexity=TimeComplexity+Time
        print(TimeComplexity)
        if Moves is not None:
            return Moves,TimeComplexity
        if i==DepthLimit-1 and Moves==None:
            sequence = "No solution found"
            return Moves, TimeComplexity

class idsWorkThread(QThread):
    trigger = pyqtSignal()
    def __int__(self):
        super(idsWorkThread, self).__init__()
    def run(self):
        global TimeComplexity
        Result,TimeComplexity = IDS(StartState)
        if Result == None:
            print("No solution found")
        elif Result == [None]:
            print("The time complexity is:", TimeComplexity)
            print("Starting state was the goal")
        else:
            print("The time complexity is:", TimeComplexity)
            print("The goal state was achieved in:", len(Result), "moves")
        self.trigger.emit()

class astarWorkThread(QThread):
    trigger = pyqtSignal()
    def __int__(self):
        super(astarWorkThread, self).__init__()
    def run(self):
        Result, Time = Astar(StartState)
        if Result == None:
            print("No solution found")
        elif Result == [None]:
            print("The time complexity is:", Time)
            print("Starting state was the goal")
        else:
            print("The time complexity is:", Time)
            print("The goal state was achieved in:", len(Result), "moves")
        self.trigger.emit()

class mywindow(QMainWindow, Ui_MainWindow):
    def __init__(self,parent=None):
        global StartState, DictState
        super(mywindow, self).__init__(parent)
        self.setupUi(self)
        self.Dic={"A": 1, "B": 2, "C": 3, "T": 55, "O":9}
        self.Dict = {"A": self.lineEdit_13, "B": self.lineEdit_14, "C": self.lineEdit_15, "T": self.lineEdit_16, "O": self.lineEdit_4}
        DictState={self.lineEdit: 0,self.lineEdit_2: 0,self.lineEdit_3: 0,self.lineEdit_4: 9,
                        self.lineEdit_5: 0,self.lineEdit_6: 0,self.lineEdit_7: 0,self.lineEdit_8: 0,
                        self.lineEdit_9: 0,self.lineEdit_10: 0,self.lineEdit_11: 0,self.lineEdit_12: 0,
                        self.lineEdit_13: 1,self.lineEdit_14: 2,self.lineEdit_15: 3,self.lineEdit_16: 55}
        ShowState(self)
        regExp = QtCore.QRegExp("^[ABCTO]{1}$")
        self.lineEdit.setValidator(QtGui.QRegExpValidator(regExp,self))
        self.lineEdit_2.setValidator(QtGui.QRegExpValidator(regExp,self))
        self.lineEdit_3.setValidator(QtGui.QRegExpValidator(regExp,self))
        self.lineEdit_4.setValidator(QtGui.QRegExpValidator(regExp,self))
        self.lineEdit_5.setValidator(QtGui.QRegExpValidator(regExp,self))
        self.lineEdit_6.setValidator(QtGui.QRegExpValidator(regExp,self))
        self.lineEdit_7.setValidator(QtGui.QRegExpValidator(regExp,self))
        self.lineEdit_8.setValidator(QtGui.QRegExpValidator(regExp,self))
        self.lineEdit_9.setValidator(QtGui.QRegExpValidator(regExp,self))
        self.lineEdit_10.setValidator(QtGui.QRegExpValidator(regExp,self))
        self.lineEdit_11.setValidator(QtGui.QRegExpValidator(regExp,self))
        self.lineEdit_12.setValidator(QtGui.QRegExpValidator(regExp,self))
        self.lineEdit_13.setValidator(QtGui.QRegExpValidator(regExp,self))
        self.lineEdit_14.setValidator(QtGui.QRegExpValidator(regExp,self))
        self.lineEdit_15.setValidator(QtGui.QRegExpValidator(regExp,self))
        self.lineEdit_16.setValidator(QtGui.QRegExpValidator(regExp,self))

        regExpids = QtCore.QRegExp("[1-9][0-9]?")
        self.depthlimit_input.setValidator(QtGui.QRegExpValidator(regExpids,self))

    def runbfs(self):
        self.running()
        self.timer = QTimer(self)
        self.workThread = bfsWorkThread(self)
        self.timer.timeout.connect(self.showTime)
        self.timer.start(1)
        self.workThread.start()
        self.workThread.trigger.connect(self.timeStop)

    def rundfs(self):
        self.running()
        self.timer = QTimer(self)
        self.workThread = dfsWorkThread(self)
        self.timer.timeout.connect(self.showTime)
        self.timer.start(1)
        self.workThread.start()
        self.workThread.trigger.connect(self.timeStop)

    def runids(self):
        global DepthLimit
        self.running()
        self.timer = QTimer(self)
        DepthLimit = int(self.depthlimit_input.text())

        self.workThread = idsWorkThread(self)
        self.timer.timeout.connect(self.showTime)
        self.timer.start(1)
        self.workThread.start()
        self.workThread.trigger.connect(self.timeStop)

    def runastar(self):
        self.running()
        self.timer = QTimer(self)
        self.workThread = astarWorkThread(self)
        self.timer.timeout.connect(self.showTime)
        self.timer.start(1)
        self.workThread.start()
        self.workThread.trigger.connect(self.timeStop)

    def reset(self):
        global TimeComplexity
        global depth
        global sequence
        self.bfsbtn.setEnabled(True)
        self.dfsbtn.setEnabled(True)
        self.idsbtn.setEnabled(True)
        self.Astarbtn.setEnabled(True)
        ShowState(self)
        TimeComplexity=0
        depth=0
        sequence=""
        self.lcdTimeComplexity.display(TimeComplexity)
        self.lcdDepth.display(depth)
        self.textEdit.setText(sequence)

    def running(self):
        self.bfsbtn.setEnabled(False)
        self.dfsbtn.setEnabled(False)
        self.idsbtn.setEnabled(False)
        self.Astarbtn.setEnabled(False)
        self.lineEdit.setReadOnly(True)
        self.lineEdit_2.setReadOnly(True)
        self.lineEdit_3.setReadOnly(True)
        self.lineEdit_4.setReadOnly(True)
        self.lineEdit_5.setReadOnly(True)
        self.lineEdit_6.setReadOnly(True)
        self.lineEdit_7.setReadOnly(True)
        self.lineEdit_8.setReadOnly(True)
        self.lineEdit_9.setReadOnly(True)
        self.lineEdit_10.setReadOnly(True)
        self.lineEdit_11.setReadOnly(True)
        self.lineEdit_12.setReadOnly(True)
        self.lineEdit_13.setReadOnly(True)
        self.lineEdit_14.setReadOnly(True)
        self.lineEdit_15.setReadOnly(True)
        self.lineEdit_16.setReadOnly(True)
        self.resetbtn.setEnabled(False)
        self.depthlimit_input.setReadOnly(True)

    def finishRunning(self):
        self.bfsbtn.setEnabled(True)
        self.dfsbtn.setEnabled(True)
        self.idsbtn.setEnabled(True)
        self.Astarbtn.setEnabled(True)
        self.lineEdit.setReadOnly(False)
        self.lineEdit_2.setReadOnly(False)
        self.lineEdit_3.setReadOnly(False)
        self.lineEdit_4.setReadOnly(False)
        self.lineEdit_5.setReadOnly(False)
        self.lineEdit_6.setReadOnly(False)
        self.lineEdit_7.setReadOnly(False)
        self.lineEdit_8.setReadOnly(False)
        self.lineEdit_9.setReadOnly(False)
        self.lineEdit_10.setReadOnly(False)
        self.lineEdit_11.setReadOnly(False)
        self.lineEdit_12.setReadOnly(False)
        self.lineEdit_13.setReadOnly(False)
        self.lineEdit_14.setReadOnly(False)
        self.lineEdit_15.setReadOnly(False)
        self.lineEdit_16.setReadOnly(False)
        self.resetbtn.setEnabled(True)
        self.depthlimit_input.setReadOnly(False)

    def timeStop(self):
        global sequence
        self.timer.stop()
        print("运行结束用时", str(TimeComplexity))
        self.textEdit.setPlainText(sequence)
        self.finishRunning()

    def showTime(self):
        global TimeComplexity
        global StartState
        global depth
        BoardState(self, StartState)
        self.lcdTimeComplexity.display(TimeComplexity)
        self.lcdDepth.display(depth)

    def depthLimitChange(self):
        global DepthLimit
        if self.depthlimit_input.text()=="":
            self.idsbtn.setEnabled(False)
        else:
            DepthLimit = int(self.depthlimit_input.text())
            self.idsbtn.setEnabled(True)

    def textchange(self):
        global StartState
        global DictState
        rlt=self.sender()
        #print(rlt)
        if(rlt.text()==""):
            for key, val in self.Dict.items():
                if (rlt == val and key=="O"):
                    self.Dict.pop("O")
                    DictState[val]=0
                    print("删除O键成功")
                    self.label_O.setGeometry(240, 160, 50, 50)
                    break
                elif (rlt == val and key!="O"):
                    val.setText(key)
        elif(rlt.text()=="O" and "O" not in self.Dict and rlt not in self.Dict.values()):
            self.Dict.update({"O":rlt})
            DictState[rlt]=9
            print("添加O键成功")
        elif(rlt.text()=="O" and "O" not in self.Dict and rlt in self.Dict.values()):
            for key, val in self.Dict.items():
                if (rlt == val):
                    val.setText(key)
                    break
        else:
            print("满足")
            flag=False
            for key, val in self.Dict.items():
                if (rlt == val):
                    print(111)
                    flag=True
                    temp = self.Dict[key]
                    tempp = self.Dict[rlt.text()]
                    tempval = DictState[temp]
                    temppval = DictState[tempp]
                    self.Dict[rlt.text()] = temp
                    self.Dict[key] = tempp
                    self.Dict[key].setText(key)
                    DictState[temp] = temppval
                    DictState[tempp] = tempval
                    break
            if(flag==False):
                for key, val in self.Dict.items():
                    if (rlt.text() == key):
                        temp=self.Dict[rlt.text()]
                        tempval=DictState[temp]
                        rltval=DictState[rlt]
                        self.Dict[rlt.text()].setText("")
                        self.Dict[rlt.text()]=rlt
                        DictState[temp]=rltval
                        DictState[rlt]=tempval
                        break
        ShowState(self)

if __name__=="__main__":
    app=QApplication(sys.argv)
    myshow=mywindow()
    myshow.show()
    sys.exit(app.exec_())
