import json
from tests.basetest import Basetest
from excmanager.Task import *

class Testexercises(Basetest):
    '''
    Test Excercise Manager
    '''
    def setUp(self, debug=False, profile=True):
        return super().setUp(debug, profile)

    def testExc(self):
        '''
            test exercise and task structure setup
        '''
        exc = Exercise( 1 )
        task1 = Task( exc, "1.1" )
        subtask1 = SubTask( task1, "a", points = 2 )

        solution = json.dumps({'test': 2})

        subtask1.setSolution(solution)

        debug=self.debug
        #debug=True
        if debug:
            print( exc )
            print( task1 )
        if debug:
            print(exc)
            print(exc.getTasks())
            print(exc.getTaskByLabel("1.1").getSubtasks())
            print(exc.getTaskByLabel("1.1").getSubtaskbyLabel("a").getSolution())


        self.assertEqual(1, exc.getTaskNo())
        self.assertEqual(1, task1.getTaskNo())
        self.assertEqual(2, exc.getPoints())

        self.assertEqual(1, len(exc.getTaskByLabel("1.1").getSubtasks().keys()))
        self.assertEqual(2, exc.getTaskByLabel("1.1").getSubtaskByLabel("a").getPoints())
        