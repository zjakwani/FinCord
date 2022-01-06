import csv

import firebase_admin
    
from firebase_admin import credentials

from firebase_admin import db

cred = credentials.Certificate("key.json")

# Client code will call this function when the dictionary of financial of terms and 
# their respective definitions will need to be populated. 
def read_data():
    map_dict = {}
   
    url_key = open("api_key.txt").read()
    firebase_admin.initialize_app(cred, {
        'databaseURL': url_key
    })
    ref = db.reference("/")

    snapshot = ref.get()
    for key, val in snapshot.items():
   
        map_dict = {
            'term': str(val.get('term')),
            'definition': str(val.get('definition'))
        }

    return map_dict

# Function will only be run when explicitly ran as a main python file
# since new words may be periodically added
def push_data():

    url_key = open("api_key.txt").read()
    firebase_admin.initialize_app(cred, {
        'databaseURL': url_key
    })
    ref = db.reference("/")

    reader = csv.reader(open("financial_terms.csv", "r"))

    for row in reader:

        if row[1]:
            data_to_send = {

                'term': row[0],
                'definition': row[1]
            }

            ref.push(data_to_send)



if __name__ == '__main__':
    push_data()
