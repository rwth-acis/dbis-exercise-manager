
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
        assert Util.check_table(["A"], [[]], ["A"], [[]], 0.5, True) == True

        assert Util.check_table(["A"], [[]], ["B"], [[]], 0.5, True) == False

        assert Util.check_table(
            ["A.Titel","B.Titel","A.Genre"],
            [["Pulp Fiction","Cloud Atlas","Independent"],
            ["Cloud Atlas","Pulp Fiction","Independent"],
            ["Alien","Matrix","Sci-Fi"],
            ["Blade Runner","Matrix","Sci-Fi"]],
            
            ["A.Titel","B.Titel","A.Genre"],
            [["Alien","Matrix","Sci-Fi"],
            ["Pulp Fiction","Cloud Atlas","Independant"],
            ["Cloud Atlas","Pulp Fiction","Independant"],
            ["Blade Runner","Matrix","Sci-Fi"]], 1, True) == False

        assert Util.check_table(
            ["A.Titel","B.Titel","A.Genre"],
            [["Alien","Matrix","Sci-Fi"],
            ["Pulp Fiction","Cloud Atlas","Independent"],
            ["Cloud Atlas","Pulp Fiction","Independent"],
            ["Blade Runner","Matrix","Sci-Fi"]],
            
            ["A.Titel","B.Titel","A.Genre"],
            [["Pulp Fiction","Cloud Atlas","Independant"],
            ["Cloud Atlas","Pulp Fiction","Independant"],
            ["Alien","Matrix","Sci-Fi"],
            ["Blade Runner","Matrix","Sci-Fi"]], 0.8, True) == True

        assert Util.check_table(
            ["Nationalität"],
            [["FRANZÖSISCH"], ["ÖSTERREICHISCH"]],
            ["  nationalitaet     "],
            [["oesterreichisch"], ["     fransoesischh  "]], 0.8, True) == True

        # Complete test of:
        # * umlauts
        # * spelling errors
        # * permutation of attributes
        # * permutation of tuples
        # * whitespace
        # * ints instead of strings
        # * tuples instead of lists
        assert Util.check_table(
            ["Nationalität", "Alter"],
            [["FRANZÖSISCH", "2"], ["ÖSTERREICHISCH", "1"]],

            ["alterr", "  nationalitaet     "],
            [(1, "oesterreichisch"), (2, "     fransoesischh  ")],
            
            0.8, True) == True

        assert Util.check_table(
            ["Vorname", "Nachname"],
            [["Quentin","Tarantino"], ["Robert", "Rodriguez"], ["Ridley", "Scott"], ["Lana", "Wachowski"]],
            ["Vornname", "Nachname"],
            [["Quendin","Tarantino"], ["Robert", "Rodriguez"], ["Ridley", "Scott"], ["Lana", "Wachowski"]],
            0.8,
            False
        ) == True