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

    def check_table(attributes, attributes_should, tuples, tuples_should):
        errors = 0
        for i in range(len(attributes_should)):
            if (i >= len(attributes) or attributes[i] != attributes_should[i]):
                print(f"Missing or wrong attribute at position {i}. Expected: {attributes_should[i]}")
                errors += 1
        for i in range(len(tuples_should)):
            if (tuples_should[i] not in tuples):
                print(f"Missing tuple: {tuples_should[i]}")
                errors += 1

        for i in range(len(tuples)):
            if (tuples[i] not in tuples_should):
                print(f"Superfluous tuple: {tuples[i]}")
                errors += 1

        if errors == 0:
            return True
        else:
            return False
            
    # check sql solution
    def check_sql_solution(query_text, 
                        student_dict, 
                        solution, 
                        partial_score_exact, 
                        partial_score_keywords, 
                        partial_score_points):
        score = 0
        try:
            # check for exact match
            for x in solution:
                print( "checking columns: ", x, " | ", solution[x])
                for y in range(len(solution[x])):
                    print( "   checking cell:", y, " | ", solution[x][y])
                    check = solution[x][y] == student_dict[x][y]
                    if check: 
                        score += partial_score_exact
                    print("    > ", check, ", score: ", round(score, 4) )
        except:
            print('exception caught, aborting')
            pass # catch, return
        else:
            # if the solution isn't exact, apply other rules
            # = check for keywords in SQL.
            if round(score,2) < no_of_points: 
                score = 0
                print('partial score')
                for i in partial_score_keywords:
                    if i in query_text.upper(): score += partial_score_points
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
        