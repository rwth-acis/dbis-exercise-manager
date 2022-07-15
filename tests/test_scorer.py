'''
Created on 2022-07-11

@author: wf
'''
from tests.basetest import Basetest
from excmanager.scorer import Scorer, MultipleChoiceScorer, SetScorer

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
        
    def testSetScorer(self):
        '''
        test Set Scorer
        '''
        examples=[ {
            "sub":{1,3,5,7,8},
            "expected":{1,2,5,6},
            "score": 0
        },
        {
            "sub":{1,2,3},
            "expected":{1,2,3},
            "score": 1
        },
        {
            "sub":{1,2},
            "expected":{1,2,3},
            "score": 2/3
        },
        {
            "sub":{1,2,3},
            "expected":{1,2},
            "score": 1/2
        },
        {
            "sub":{1,2,3},
            "expected":{1,2,4},
            "score": 1/3
        }
        ]
        debug=True
        doTest=True
        for i,example in enumerate(examples):
            setScorer=SetScorer()
            sub=example["sub"]
            expected=example["expected"]
            expectedScore=example["score"]
            score=setScorer.evaluate_set(sub,expected, max_points=1)
            if debug:
                print(f"{i+1}:{sub} expected: {expected} score -> {score} vs expected Score {expectedScore}")
            if doTest:   
                self.assertEqual(score,expectedScore)