import os, requests
from IPython.display import Markdown, display
import sqlite3
from tabulate import tabulate
from Levenshtein import _levenshtein

class Util:
    # https://stackoverflow.com/a/16696317/3151250
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

    def evaluate_sql(path_to_db, query, display_table=True):
        conn = sqlite3.connect(path_to_db)
        cursor = conn.execute(query)
        attributes = [description[0] for description in cursor.description]
        tuples = [list(x) for x in cursor.fetchall()]
        table = tabulate(tuples, attributes, tablefmt="github")
        if display_table:
            display(Markdown(table))
        conn.close()
        return attributes, tuples

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
    def check_sql_solution(query_text,
                           student_dict,
                           solution,
                           no_of_points,
                           partial_score_exact,
                           partial_score_keywords,
                           partial_score_points):
        score = 0
        try:
            # check for exact match
            for x in solution:
                print("checking columns: ", x, " | ", solution[x])
                for y in range(len(solution[x])):
                    print("   checking cell:", y, " | ", solution[x][y])
                    check = _levenshtein.ratio(Util.str_sanitize(solution[x][y]), Util.str_sanitize(student_dict[x][y]))
                    if 0.8 <= check:
                        score += partial_score_exact
                    print("    > ", check, ", score: ", round(score, 4))
        except:
            print('exception caught, aborting')
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
    def permute_list(list, mapping):
        l = list.copy()
        for i in range(0, len(list)):
            list[i] = l[mapping[i]]

    # Returns mapping as list or None
    def get_permutation(list_student, list_solution, elem_name, levenshtein_callback, levenshtein_threshold, quiet):
        res = len(list_student) * []
        a = list_student.copy()
        b = list_solution.copy()
        error = False
        for i in range(0, len(a)):
            best = -1
            best_ratio = -1
            for j in range(0, len(b)):
                if b[j] == None: # Skip elements that were already matched
                    continue
                new_ratio = levenshtein_callback(a[i], b[j])
                if new_ratio >= best_ratio:
                    best_ratio = new_ratio
                    best = j
            if best_ratio >= levenshtein_threshold:
                res.insert(i, best)
                if (best_ratio < 1 and not quiet):
                    print(f"Found {elem_name} '{a[i]}', did you mean '{b[best]}'? Using this instead.")
                b[best] = None # Mark as matched
            else:
                if not quiet:
                    print(f"Wrong {elem_name} '{a[i]}'")
                error = True

        # Check if all items have been used, if not, it was missing in student's solution
        for j in range(0, len(b)):
            if b[j] != None:
                if not quiet:
                    print(f"Missing {elem_name} '{b[j]}'")
                error = True
        if error:
            return None
        return res

    def str_sanitize(s):
        return str(s).lower().strip().replace("ä", "ae").replace("ö", "oe").replace("ü", "ue")

    def levenshtein_str_callback(a, b):
        return _levenshtein.ratio(Util.str_sanitize(a), Util.str_sanitize(b))

    def levenshtein_list_callback(a, b):
        return _levenshtein.seqratio(list(map(Util.str_sanitize, list(a))), list(map(Util.str_sanitize, list(b))))

    def check_table(attributes_solution, tuples_solution, attributes_student, tuples_student, levenshtein_threshold=1, quiet=False):
        # Get permutation according to attributes
        attribute_mapping = Util.get_permutation(attributes_student, attributes_solution, "attribute", Util.levenshtein_str_callback, levenshtein_threshold, quiet)
        if attribute_mapping == None:
            return False

        # Permute solution tuples with found mapping
        # Student's solutions are not changed to explain wrong answers
        Util.permute_list(attributes_solution, attribute_mapping)
        for tuple in tuples_solution:
            Util.permute_list(tuple, attribute_mapping)

        # Check if permutation on tuples can be found
        # If not, some tuples are wrong or missing
        tuple_mapping = Util.get_permutation(tuples_student, tuples_solution, "tuple", Util.levenshtein_list_callback, levenshtein_threshold, quiet)
        if tuple_mapping == None:
            return False
        return True
