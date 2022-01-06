import csv
from tabulate import tabulate
import discord

def get_card_info(csv_path):
    card_info = {}
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
                    if cur > 15:
                        new_string += '\n'
                        new_string += ' ' + word
                        cur = len(word)
                    else:
                        new_string += ' ' + word
                row[i] = new_string
            card_info[name] = row
    return card_info

def compare_cards(c1, c2, card_info):
    if c1 not in card_info:
        out_str =  c1 + ' not found'
    elif c2 not in card_info:
        out_str = c2 + ' not found'
    else:
        c1_data = card_info[c1]
        c2_data = card_info[c2]
        data = []
        for c1_, c2_, name in zip(c1_data[1:-1], c2_data[1:-1], ["Purchase Rate", "Transfer Info", "Annual Fee", "Credit Level"]):
            data.append([name, c1_, c2_])
        
        descrip1 = c1_data[-1]
        descrip2 = c2_data[-1]
        out_str = c1 + ': ' + descrip1 + '\n\n' + c2 + ': ' + descrip2 + '\n\n'
        out_str += '```' + tabulate(data, headers=['', c1, c2]) + '```'
    embed = discord.Embed(title = 'Features Comparison', description=out_str)
    return embed
    

#card_info = get_card_info('credit_info.csv')
#print(compare_cards('Venture Rewards', 'Platinum Mastercard', card_info))