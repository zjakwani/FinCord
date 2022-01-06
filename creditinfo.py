import csv
from collections import defaultdict

def get_card_info(csv_path):
    card_info = defaultdict(str)
    with open(csv_path, 'r') as f:
        reader = csv.reader(f)
        
        for row in reader:
            name, purchase_rate, transfer_info, annual_fee, credit_level, description = row
            card_info[name] = {'purchase rate': purchase_rate, 'transfer info': transfer_info, 'annual fee': annual_fee, 'credit level': credit_level, 'description': description}
    return card_info