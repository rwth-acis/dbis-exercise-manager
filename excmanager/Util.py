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
            