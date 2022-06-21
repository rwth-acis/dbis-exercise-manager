
class Exercise:
    def __init__(self, exc):
        '''
        This class manages the state of the exercise.

        Args:
            exc(int): exercise (ÜB), example: 1
            task(str): Task (Aufgabe), example: 2
            subtask(str): Subtask(Teilaufgabe), example: a
        '''

        self.exc = exc
        self.tasks = {}
        pass

    def addTask(self, task):
        if task.task in self.tasks:
            raise Exception("task already exists")
        if task.task not in self.tasks:
            self.tasks[task.task] = {}
        self.tasks[task.task] = task

    def getTasks(self):
        return self.tasks

    def getTaskByLabel(self, label):
        return self.tasks[label]

    def getTaskNo(self):
        return len(self.tasks)
    
    def getPoints(self):
        x = 0
        for t in self.tasks.values():
            x += t.getPoints()
        return x

    def __str__(self) -> str:
        return f"Übung {self.exc}, {self.getTaskNo()} Aufgaben, {self.getPoints()} Punkte"

class Task:
    def __init__(self, exc, task, points=0):
        '''
        This class manages the state of the task.

        Args:
            exc(int): exercise (ÜB), example: 1
            task(str): Task (Aufgabe), example: 2
            points(float): Points (Punkte), example: 2
        '''
        self.exc = exc
        self.task = task
        self.points = points
        self.subtasks = {}

        exc.addTask(self)

    def __str__(self):
        return self.getTaskInfo()

    def getTaskNo(self):
        return len(self.subtasks)

    def getTaskInfo(self): 
        return f"Aufgabe {self.task}, {self.getPoints()} Punkte, {self.getTaskNo()} Teilaufgaben"
        
    def getPoints(self):
        x = 0
        for t in self.subtasks.values():
            x += t.getPoints()
        return x

    def getScore(self):
        x = 0
        for t in self.subtasks.values():
            x += t.getScore()
        return x

    def setSolution(self, solution):
        self.solution = solution
    
    def getSolution(self):
        return self.solution

    def addSubtask(self, subtask):
        self.subtasks[subtask.subtask] = subtask

    def getSubtasks(self):
        return self.subtasks

    def getSubtaskByLabel(self, label):
        return self.subtasks[label]

class SubTask:
    def __init__(self, task, subtask, points):
        '''
        This class manages the state of the subtask.

        Args:
            exc(int): exercise (ÜB), example: 1
            subtask(str): Subtask (Teilaufgabe), example: 1.2
            points(float): Points (Punkte), example: 2
        '''        
        self.task = task
        self.subtask = subtask
        self.points = points
        self.score = 0

        task.addSubtask(self)

    def __str__(self):
        return self.getTaskInfo()

    def getTaskInfo(self): 
        return f"Teilaufgabe {self.subtask}, {self.points} Punkte"

    def getPoints(self):
        return self.points

    def setScore(self, score):
        self.score = score

    def getScore(self):
        return self.score

    def setSolution(self, solution):
        self.solution = solution
    
    def getSolution(self):
        return self.solution

    def getData(self):
        return self.data
    
    def setData(self, data):
        self.data = data

# Spätere Features:
#   def getScaledPoints(self):
#   def autograde(self):
