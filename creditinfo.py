import csv
from collections import defaultdict
from tabulate import tabulate

def get_card_info(csv_path):
    card_info = defaultdict(str)
    with open(csv_path, 'r') as f:
        reader = csv.reader(f)
        
        for row in reader:
            name = row[0]
            row[-1] = row[-1].replace('\n', ' ').replace('  ', ' ')
            for i, entry in enumerate(row[:-1]):
                words = entry.split(' ')
                cur = 0
                new_string = ''
                for word in words:
                    cur += len(word)
                    if cur > 20:
                        new_string += '\n'
                        new_string += ' ' + word
                        cur = len(word)
                    else:
                        new_string += ' ' + word
                row[i] = new_string
            card_info[name] = row
    return card_info

def compare_cards(c1, c2, card_info):
    c1_data = card_info[c1]
    c2_data = card_info[c2]
    descrip1 = c1_data[-1]
    descrip2 = c2_data[-1]
    out_str = c1 + ': ' + descrip1 + '\n\n' + c2 + ': ' + descrip2 + '\n\n'
    out_str += tabulate([c1_data[:-1], c2_data[:-1]], headers=["Name", "Purchase Rate", "Transfer Info", "Annual Fee", "Credit Level"])
    return out_str