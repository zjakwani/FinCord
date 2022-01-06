import csv


# Function will only be run when explicitly ran as a main python file
# since new words may be periodically added

def push_data():
    import firebase_admin
    from firebase_admin import credentials

    from firebase_admin import db

    cred = credentials.Certificate("key.json")

    firebase_admin.initialize_app(cred, {
        'databaseURL': "https://fincord-49cc7-default-rtdb.firebaseio.com/"
    })
    ref = db.reference("/")

    reader = csv.reader(open("financial_terms.csv", "r"))

    for row in reader:
        data_to_send = {

            'term': row[0],
            'definition': row[1]
        }

        ref.push(data_to_send)


if __name__ == '__main__':
    push_data()
