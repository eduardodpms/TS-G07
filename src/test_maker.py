import json

def test_maker(json_path):
    while True:
        ID = input("id (string): ")
        T = input("title (string): ")
        C = input("body (string): ")
        F = input("source (string): ")
        P = input("sponsored (bool): ")
        E = input("expected output (string): ")

        new_test = {
            "id": ID,
            "title": T,
            "body": C,
            "source": F,
            "sponsored": P.lower() == 'true',
            "expected": E
        }

        with open(json_path, 'r') as json_file:
            tests = json.load(json_file)

        tests.append(new_test)

        with open(json_path, 'w') as json_file:
            json.dump(tests, json_file, indent=4)

        print(f"\nNew test case saved: ID = {ID}\n{'='*15} Ctrl+C to exit {'='*15}\n")