import os, requests
from typing import Any, Callable, List, Optional, Union

from IPython.display import Markdown, display
import sqlite3
from tabulate import tabulate
from Levenshtein import ratio,seqratio, setratio

class Util:
    '''
    Utilities
    '''
    # https://stackoverflow.com/a/16696317/3151250
    @staticmethod
    def download_file(url, folder):
        local_filename = url.split('/')[-1]
        full_path = os.path.join(folder, local_filename)
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(full_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        print(f"Downloaded and placed file at {full_path}")
        return local_filename

    @staticmethod
    def evaluate_sql(path_to_db, query, display_table=True):
        if not os.path.exists(path_to_db):
            raise FileNotFoundError()
        conn = sqlite3.connect(path_to_db)
        cursor = conn.execute(query)
        attributes = [description[0] for description in cursor.description]
        tuples = [list(x) for x in cursor.fetchall()]
        table = tabulate(tuples, attributes, tablefmt="github")
        if display_table:
            display(Markdown(table))
        conn.close()
        return attributes, tuples

    @staticmethod
    def transform_pgsql_resultset_to_list_of_lists(result):
        result_list = []
        for row_dicts in result.dicts():
            row_list = []
            for attribute, value in row_dicts.items():
                row_list.append(str(value))
            result_list.append(row_list)
        attributes = result.field_names
        return attributes, result_list

    # check sql solution
    @staticmethod
    def check_sql_solution(
            query_text,
            student_dict,
            solution,
            no_of_points,
            partial_score_exact,
            partial_score_keywords,
            partial_score_points
    ):
        score = 0
        try:
            solution = {Util.str_sanitize(k): v for k, v in solution.items()}
            student_dict = {Util.str_sanitize(k): v for k, v in student_dict.items()}
            # check for exact match
            for x in solution:
                print("checking columns: ", x, " | ", solution[x])
                for y in range(len(solution[x])):
                    print("   checking cell:", y, " | ", solution[x][y])
                    check = Util.levenshtein_str_callback(solution[x][y], student_dict[x][y])
                    if 0.8 <= check:
                        score += partial_score_exact
                    print("    > ", check, ", score: ", round(score, 4))
        except Exception as e:
            print('exception caught, aborting')
            print(f'  {type(e).__name__} {e} ')
            if type(e).__name__ == "KeyError":
                print("  ... this error message likely means that a column name is misspelled or that a column was not found.")
            pass  # catch, return
        else:
            # if the solution isn't exact, apply other rules
            # = check for keywords in SQL.
            if round(score, 2) < no_of_points:
                score = 0
                print('partial score')
                for i in partial_score_keywords:
                    if i in query_text.upper():
                        score += partial_score_points
        return score

    # count solution cells in result array
    @staticmethod
    def get_solution_count(solution):
        count = 0
        for x in solution:
            for y in range(len(solution[x])):
                count += 1
        if count == 0:
            count = 1
        return count

###############################################################################################################
# CHECK TABLE & HELPER FUNCTIONS
###############################################################################################################

    # Mapping: Index of new list -> Index of old list
    @staticmethod
    def permute_list(data: list, mapping: list):
        l = data.copy()
        for i in range(0, len(data)):
            data[i] = l[mapping[i]]

    # Returns mapping as list or None
    @staticmethod
    def get_permutation(
            list_student: List[Any],
            list_solution: List[Any],
            elem_name: str,
            levenshtein_callback: Callable,
            levenshtein_threshold: float,
            quiet: bool = True
    ) -> Optional[List[Any]]:
        res = len(list_student) * []
        a = list_student.copy()
        b = list_solution.copy()
        error = False
        for i, student_answer in enumerate(a):
            best = -1
            best_ratio = -1
            for j, expected_answer in enumerate(b):
                if expected_answer is None:  # Skip elements that were already matched
                    continue
                new_ratio = levenshtein_callback(student_answer, expected_answer)
                if new_ratio >= best_ratio:
                    best_ratio = new_ratio
                    best = j
            if best_ratio >= levenshtein_threshold:
                res.insert(i, best)
                if best_ratio < 1 and not quiet:
                    print(f"Found {elem_name} '{student_answer}', did you mean '{b[best]}'? Using this instead.")
                b[best] = None  # Mark as matched
            else:
                if not quiet:
                    print(f"Wrong {elem_name} '{student_answer}'")
                error = True

        # Check if all items have been used, if not, it was missing in student's solution
        for j in range(0, len(b)):
            if b[j] is not None:
                if not quiet:
                    print(f"Missing {elem_name} '{b[j]}'")
                error = True
        if error:
            return None
        return res

    @staticmethod
    def str_sanitize(s: str) -> str:
        """
        Sanitize given string by converting it to lowercase and replacing umlauts to corresponding counterparts
        Args:
            s: string to sanitize
        Returns:
            str: sanitized string
        """
        return str(s).lower().strip().replace("ä", "ae").replace("ö", "oe").replace("ü", "ue")

    @staticmethod
    def levenshtein_str_callback(a: str, b: str) -> float:
        """
        Compare the given strings with each other with Levenshtein
        Args:
            a: string to compare
            b: string to compare
        Returns:
            float: Levenshtein distance ratio of given strings
        """
        r = ratio(Util.str_sanitize(a), Util.str_sanitize(b))
        return r

    @staticmethod
    def levenshtein_list_callback(a: List[str], b: List[str]) -> float:
        """
        Compare the given list of strings with each other with Levenshtein
        Args:
            a: list of strings
            b: list of strings
        Returns:
            float: Levenshtein set ratio of the given lists of strings
        """
        strlist1 = list(map(Util.str_sanitize, list(a)))
        strlist2 = list(map(Util.str_sanitize, list(b)))
        sr = setratio(strlist1, strlist2)
        return sr

    @staticmethod
    def check_table(
            attributes_solution: List[str],
            tuples_solution: List[Any],
            attributes_student: List[str],
            tuples_student: List[Any],
            levenshtein_threshold: float = 1,
            quiet: bool = False
    ):
        # Get permutation according to attributes
        attribute_mapping = Util.get_permutation(
                list_student=attributes_student,
                list_solution=attributes_solution,
                elem_name="attribute",
                levenshtein_callback=Util.levenshtein_str_callback,
                levenshtein_threshold=levenshtein_threshold,
                quiet=quiet
        )
        if attribute_mapping is None:
            return False

        # Permute solution tuples with found mapping
        # Student's solutions are not changed to explain wrong answers
        Util.permute_list(attributes_solution, attribute_mapping)
        for tuple in tuples_solution:
            Util.permute_list(tuple, attribute_mapping)

        # Check if permutation on tuples can be found
        # If not, some tuples are wrong or missing
        tuple_mapping = Util.get_permutation(
                list_student=tuples_student,
                list_solution=tuples_solution,
                elem_name="tuple",
                levenshtein_callback=Util.levenshtein_list_callback,
                levenshtein_threshold=levenshtein_threshold,
                quiet=quiet
        )
        if tuple_mapping is None:
            return False
        return True
