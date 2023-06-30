from dataclasses import dataclass
from typing import Any, List

from Levenshtein import seqratio, setratio

from tests.basetest import Basetest
from excmanager.Util import Util

class TestUtil(Basetest):
    """
    test the Util module
    """
    def setUp(self, debug=False, profile=True):
        return super().setUp(debug, profile)

    def testCheckTable(self):
        """
        test checking tables
        """
        @dataclass
        class TestParam:
            attributes_solution: List[str]
            tuples_solution: List[Any]
            attributes_student: List[str]
            tuples_student: List[Any]
            levenshtein_threshold: float = 1
            quiet: bool = False
            expected_result: bool = True
        test_params = [
            TestParam(["A"], [[]], ["A"], [[]], 0.5, expected_result=True),
            TestParam(["A"], [[]], ["B"], [[]], 0.5, expected_result=False),
            TestParam(
                    attributes_solution=["A.Titel", "B.Titel", "A.Genre"],
                    tuples_solution=[
                        ["Pulp Fiction", "Cloud Atlas", "Independent"],
                        ["Cloud Atlas", "Pulp Fiction", "Independent"],
                        ["Blade Runner", "Matrix", "Sci-Fi"]],
                    attributes_student=["A.Titel", "B.Titel", "A.Genre"],
                    tuples_student=[
                        ["Alien", "Matrix", "Sci-Fi"],
                        ["Pulp Fiction", "Cloud Atlas", "Independant"],
                        ["Cloud Atlas", "Pulp Fiction", "Independant"],
                        ["Blade Runner", "Matrix", "Sci-Fi"]],
                    levenshtein_threshold=1,
                    expected_result=False
            ), TestParam(
                    attributes_solution=["A.Titel", "B.Titel", "A.Genre"],
                    tuples_solution=[
                        ["Alien", "Matrix", "Sci-Fi"],
                        ["Pulp Fiction", "Cloud Atlas", "Independent"],
                        ["Cloud Atlas", "Pulp Fiction", "Independent"],
                        ["Blade Runner", "Matrix", "Sci-Fi"]],
                    attributes_student=["A.Titel", "B.Titel", "A.Genre"],
                    tuples_student=[
                        ["Pulp Fiction","Cloud Atlas","Independant"],
                        ["Cloud Atlas","Pulp Fiction","Independant"],
                        ["Alien","Matrix","Sci-Fi"],
                        ["Blade Runner","Matrix","Sci-Fi"]],
                    levenshtein_threshold=0.8,
                    expected_result=True),
            TestParam(
                    attributes_solution=["Nationalität"],
                    tuples_solution=[["FRANZÖSISCH"], ["ÖSTERREICHISCH"]],
                    attributes_student=["  nationalitaet     "],
                    tuples_student=[["oesterreichisch"], ["     fransoesischh  "]],
                    levenshtein_threshold=0.8,
                    expected_result=True
            ),
            # Complete test of:
            # * umlauts
            # * spelling errors
            # * permutation of attributes
            # * permutation of tuples
            # * whitespace
            # * ints instead of strings
            # * tuples instead of lists
            TestParam(
                    attributes_solution=["Nationalität", "Alter"],
                    tuples_solution=[["FRANZÖSISCH", "2"], ["ÖSTERREICHISCH", "1"]],
                    attributes_student=["alterr", "  nationalitaet     "],
                    tuples_student=[(1, "oesterreichisch"), (2, "     fransoesischh  ")],
                    levenshtein_threshold=0.8,
                    expected_result=True
            ),
            TestParam(
                    attributes_solution=["Vorname", "Nachname"],
                    tuples_solution=[["Quentin","Tarantino"], ["Robert", "Rodriguez"], ["Ridley", "Scott"], ["Lana", "Wachowski"]],
                    attributes_student=["Vornname", "Nachname"],
                    tuples_student=[["Quendin","Tarantino"], ["Robert", "Rodriguez"], ["Ridley", "Scott"], ["Lana", "Wachowski"]],
                    levenshtein_threshold=0.8,
                    expected_result=True
            )
        ]
        for param in test_params:
            with self.subTest(param=param):
                res = Util.check_table(
                        attributes_solution=param.attributes_solution,
                        tuples_solution=param.tuples_solution,
                        attributes_student=param.attributes_student,
                        tuples_student=param.tuples_student,
                        levenshtein_threshold=param.levenshtein_threshold,
                        quiet=param.quiet
                )
                self.assertEqual(res, param.expected_result)


    def test_levenshtein_for_lists(self):
        """
        test levenshtein_list_callback
        """
        test_params = [
            (['pulp fiction', 'cloud atlas', 'independant'], ['pulp fiction', 'cloud atlas', 'independent']),
            (['independant', 'cloud atlas', 'pulp fiction'], ['pulp fiction', 'independent', 'cloud atlas']),
            (['pulp fiction', 'independant', 'cloud atlas'], ['pulp fiction', 'cloud atlas', 'independent']),
            (['independant', 'pulp fiction',  'cloud atlas'], ['pulp fiction', 'cloud atlas', 'independent']),
            (['independant', 'pulp fiction',  'cloud atlas'], ['pulp fiction', 'cloud atlas', 'independence day']),
            (['pulp fiction',  'cloud atlas'], ['pulp fiction', 'cloud atlas', 'independent']),
        ]
        for param in test_params:
            a, b = param
            seq_ratio = seqratio(a, b)
            set_ratio = setratio(a, b)
            print(f"seqratio:{seq_ratio} setratio: {set_ratio} for a={a} and b={b}")

    def test_levenshtein_list_callback(self):
        """
        test levenshtein_list_callback
        """
        test_params = [
            (['pulp fiction', 'cloud atlas', 'independant'], ['pulp fiction', 'cloud atlas', 'independent'], 0.9696969696969697),
            (['independant', 'cloud atlas', 'pulp fiction'], ['pulp fiction', 'independent', 'cloud atlas'], 0.9696969696969697),
            (['pulp fiction', 'independant', 'cloud atlas'], ['pulp fiction', 'cloud atlas', 'independent'], 0.9696969696969697),
            (['independant', 'pulp fiction',  'cloud atlas'], ['pulp fiction', 'cloud atlas', 'independent'], 0.9696969696969697),
            (['independant', 'pulp fiction',  'cloud atlas'], ['pulp fiction', 'cloud atlas', 'independence day'], 0.8888888888888888),
            (['pulp fiction',  'cloud atlas'], ['pulp fiction', 'cloud atlas', 'independent'], 0.8),
            (["tenet"], ["tenet"], 1.0)
        ]
        for param in test_params:
            with self.subTest(param=param):
                a, b, expected_ratio = param
                sr = Util.levenshtein_list_callback(a, b)
                self.assertEqual(expected_ratio, sr)