from selenium import webdriver
import csv

dr =  webdriver.Chrome(executable_path='/Users/evanli/NLP/song-project/chromedriver')

dr.get('https://www.nysscpa.org/professional-resources/accounting-terminology-guide#sthash.rzLLuZGo.dpbs')

sections = dr.find_elements_by_css_selector('html > body > form > main > div > div > div > div')

with open('financial_terms.csv', 'w') as f:
    writer = csv.writer(f, delimiter=',')
    for section in sections:
        names = section.find_elements_by_css_selector('h3')
        if names and not names[0].text:
            names = names[1:] #blank h3 header in some random sections
        descriptions = section.find_elements_by_css_selector('p')
        for name, description in zip(names, descriptions):
            name = name.text.replace('\n', '').replace('\t', '').replace('"', '').replace('"', '').strip()
            description = description.text.replace('\n', '').replace('\t', '').replace('\"', '').strip()
            writer.writerow([name, description])
    
