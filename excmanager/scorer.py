'''
Created on 2022-07-11

@author: wf
'''
import fractions
class Scorer():
    '''
    general scorer
    '''
    def __init__(self,verbose:bool=True,debug:bool=False):
        '''
        constructor
        
        Args:
            verbose(bool): if True show scoring checks and problems, default: True
            debug(bool): if True show debugging information, default: False
        '''
        self.maxscore=0.0 # maximum score
        self.score=0 # total score reached
        self.verbose=verbose
        self.debug=debug
    
    def addScore(self,amount:float,check:str,problem:str=None,negativeOnProblem:bool=False):
        '''
        add the given amount to self.score if there is no problem 
        increment self.maxscore by 1
        
        Args:
            amount(float): the amount to add
            check(str): message text about what was checked
            problem(str): message text about a problem - if this is not none the score will not be increased
            negativeOnProblem(bool): if True subtract the amount if a problem occured
        '''
        self.maxscore+=amount
        frac=fractions.Fraction.from_float(amount).limit_denominator()
        amountstr=f"{frac.numerator}/{frac.denominator}" if frac.denominator>1 else f"{frac.numerator}"
        if problem is not None:
            if negativeOnProblem:
                msg=f"subtracting {amountstr}"
                self.score-=amount
            else:
                msg=f"no score"
            if self.verbose:
                print(f"{msg} for {check} due to {problem}❌")
            return
        else:
            self.score+=amount
            if self.verbose:
                print(f"adding {amountstr} to score for {check}✅")
                
class MultipleChoiceScorer(Scorer):
    '''
    scorer for multiple choice questions
    
    Für jede richtige Antwort gibt es 1/𝑛 Punkte.
    Für jede falsche Antwort gibt es −1/𝑛 Punkte.
    Es kann insgesamt nicht weniger als 0 Punkte geben. Wenn Sie also mehr falsche als richtige Antworten auswählen, gibt es insgesamt keine Minuspunkte.
    Falls zu viele Antworten angegeben wurden, gibt es 0 Punkte - auch wenn mehr richtige als falsche Antworten ausgewählt wurden. Achten Sie also darauf, nicht zu viele Antworten einzutragen.
    '''
    
    def evaluate_mctask(self,result, correct, max_points, toManyEquals0:bool):
        '''
        evaluate the given multiple choice task results
        '''    
        amount=max_points/len(correct)
        for ans in result:
            problem=None
            check=f"check {ans}"
            if not ans in correct:
                problem=f" is incorrect"
            self.addScore(amount, check, problem,negativeOnProblem=True)
        # Bei zu vielen angegebenen Antworten mehr falschen als richtigen Antworten: 0 Punkte
        if self.score < 0 or (len(result) > len(correct) and toManyEquals0 == True):
            self.score = 0
        return self.score