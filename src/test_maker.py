import json

def test_maker(json_path):
    while True:
        print(">>> New test case:")
        ID = input("id (string): ")
        T = input("title (string): ")
        C = input("body (string): ")
        F = input("source (string): ")
        P = input("sponsored (bool): ")
        E = input("expected output (string - empty if valid class): ")

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

        print(f"\n>>> New test case saved: ID = {ID}\n\n{'='*15} Ctrl+C to exit {'='*15}\n")