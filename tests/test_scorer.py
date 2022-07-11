'''
Created on 2022-07-11

@author: wf
'''
from tests.basetest import Basetest
from excmanager.scorer import Scorer, MultipleChoiceScorer

class TestScorer(Basetest):
    '''
    test for general Scorer
    '''
    
    def testScorer(self):
        '''
        test Scorer
        '''
        scorer=Scorer()
        scorer.addScore(1,"some check", None)
        scorer.addScore(1,"some check","some problem")
        scorer.addScore(0.5,"some check",None)
        self.assertEqual(2.5,scorer.maxscore)
        self.assertEqual(1.5,scorer.score)
        
        
    def testMultipleChoiceScorer(self):
        '''
        test multiple Choice Scorer
        '''
        mcs=MultipleChoiceScorer()
        score1=mcs.evaluate_mctask({1,2,5}, {1,3,4}, 1, toManyEquals0=True)
        print(score1)