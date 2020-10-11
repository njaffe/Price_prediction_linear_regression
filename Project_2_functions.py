import re


def get_name(soup):
"""
Interacts with Card Kingdom soup object to scrape card name. 

Inputs: soup object.
Outputs: card names as list. 
"""
    name = [link.text.strip() for link in soup.find_all('span', class_ = 'productDetailTitle')]
    return name


def get_expansion_rarity_clean(soup):
"""
Interacts with Card Kingdom soup object to scrape card expansion and rarity. 

Inputs: soup object.
Outputs: expansions as list and card rarity as list. 
"""
    expansion_rarity_long = [link.text for link in soup.find_all('div', class_ = 'productDetailSet')]
    expansion_list = []
    rarity_list = []
    for expansion in expansion_rarity_long:
        expansion_and_rarity = expansion.strip()  # trimming whitespace
        
        expansion_short = expansion_and_rarity[:-4]  # getting only expansion
        expansion_list.append(expansion_short)

        rarity = re.findall("[^()]", expansion_and_rarity[-3:])  # getting only rarity
        rarity_list.append(rarity[0]) # re.findall returns list of lists, so want only first element
        
    return expansion_list, rarity_list

def get_price_clean(soup):
"""
Interacts with Card Kingdom soup object to scrape card price.

Inputs: soup object.
Outputs: card prices as list. 
"""
    price_long = soup.findAll("span", attrs = {"class": "stylePrice"})
    price_list = list()
    for price in price_long:
        x = price.text.strip()
        y = re.findall('\$(\d+.\d+)',x)
        conv_price = float(y[0])
        price_list.append(conv_price)
    return price_list[::4]

def get_mana_costs(soup):
"""
Interacts with Card Kingdom soup object to scrape full card mana cost.

Inputs: soup object.
Outputs: full mana costs as list. 
"""
    all_mana_costs_long = soup.findAll("div", attrs = {"class": "productDetailCastCost"})  # find list of card CMC's as sets of one or more mana symbol images
    cost = []
    for card_cost in all_mana_costs_long:  # iterate through list of all card CMC pic sets
        CMC_list = []
        for mana_symbol in card_cost.find_all('img'): # further iterate through all individual casting cost images (1, g, u, etc)
            CMC_list.append(re.findall('\w+', mana_symbol.get('src'))[4][-1]) # Add to individual card's casting cost
        CMC_str=''
        cost.append(CMC_str.join(CMC_list)) # turn casting cost from list to string
    return cost

def get_converted_cost(soup):
"""
Calls get_mana_costs() and converts to converted cost.

Inputs: soup object.
Outputs: card cmc's as list.
"""
    cmc = []

    for card_cost in get_mana_costs(soup):
        card_cmc=0
        for letter in card_cost:
            if letter.isdigit():
                card_cmc += int(letter)
            else: 
                card_cmc+=1
        cmc.append(card_cmc)
    return cmc

"""
Interacts with Card Kingdom soup object to scrape card color.

Inputs: soup object.
Outputs: card colors as list. 
"""
def get_card_color(soup):
    color = []
    for card_cost in get_mana_costs(soup):
        card_color=[]
        for letter in card_cost:
            if letter != 'x':
                if not letter.isdigit():
                    card_color.append(letter)
                
        if card_color:
            color.append("".join(set(card_color)))
        else: color.append('colorless')
    return color

def get_rules_text(soup):
"""
Interacts with Card Kingdom soup object to scrape card rules text. 

Inputs: soup object.
Outputs: rules text as list of strings.
"""
    all_rules_text_long = soup.findAll("tr", attrs = {"class": "detailFlavortext"})
    
    rules_text = []
    for card_rules in all_rules_text_long:
        rules_text.append(card_rules.td.text.strip().replace('\n', ' '))
    
    return rules_text

def all_scrape_modern():
"""
Calls get_name(), get_expansion_rarity_clean(), get_mana_costs(), get_converted_cost(), get_card_color(), get_rules_text(), and get_price_clean() and uses Selenium to loop through Card Kingdom modern pages and scrape name, expansion, 
rarity, mana cost, cmc, card color, rules text, and price for each card.

Inputs: none; sets driver and first page URL.
Outputs: name, expansion, rarity, mana_cost, cmc, color_identity, rules_text, and price as lists.
"""
    driver = webdriver.Chrome(chromedriver)
    modern_first_page_url = 'https://www.cardkingdom.com/catalog/view?filter%5Bsort%5D=most_popular&filter%5Bsearch%5D=mtg_advanced&filter%5Btab%5D=&filter%5Bname%5D=&filter%5Bcategory_id%5D=2864&filter%5Bmulti%5D%5B0%5D=1&filter%5Btype_mode%5D=any&filter%5Btype_key%5D=&filter%5Bpow1%5D=&filter%5Bpow2%5D=&filter%5Btuf1%5D=&filter%5Btuf2%5D=&filter%5Bconcast1%5D=&filter%5Bconcast2%5D=&filter%5Bprice_op%5D=&filter%5Bprice%5D=&filter%5Bkey_text1%5D=&filter%5Bmanaprod_select%5D=any' 
    url = modern_first_page_url
    driver.get(modern_first_page_url)
    number_of_pages = int(driver.find_element_by_xpath("/html/body/div[4]/div[3]/div[5]/div[2]/ul/li[13]/a").text)
    
    name = []
    expansion = []
    rarity = []
    mana_cost = []
    cmc = []
    color_identity = []
    rules_text = []
    price = []
    
    for i in range(number_of_pages):       
        driver = webdriver.Chrome(chromedriver)
        driver.get(url)
        time.sleep(0.5)
        soup = BeautifulSoup(driver.page_source)


        name_individual = get_name(soup)
        name.extend(name_individual)
        
        expansion_individual, rarity_individual = get_expansion_rarity_clean(soup)
        expansion.extend(expansion_individual)
        rarity.extend(rarity_individual)
        
        mana_cost_individual = get_mana_costs(soup)
        mana_cost.extend(mana_cost_individual)
        
        cmc_individual = get_converted_cost(soup)
        cmc.extend(cmc_individual)
        
        color_identity_individual = get_card_color(soup)
        color_identity.extend(color_identity_individual)
        
        rules_text_individual = get_rules_text(soup)
        rules_text.extend(rules_text_individual)
        
        price_individual = get_price_clean(soup)
        price.extend(price_individual)
        
        
        url = soup.find('ul', class_ = "pagination").find_all('li')[-1].a.get('href')
    
    return name, expansion, rarity, mana_cost, cmc, color_identity, rules_text, price

def get_expansion_names_dates(soup):
"""
Interacts with Wikipedia soup object to scrape expansion names and release dates for Standard-legal MTG sets.

Inputs: soup object.
Outputs: expansion names and release dates as lists.
"""
    expansion_names = []
    set_dates = []

    for set_ in soup.find_all('table', class_ = 'wikitable')[1].find_all('tr')[3:115]: # list of 'tr's goes to ????
        if not set_.td.get('colspan'): # only cycle row tr's have 'colspan' attribute in first 'td' tag
            print(set_.find_all('td')[0].text)
            expansion_names.append(set_.find_all('td')[0].text.strip())

            print(set_.find_all('td')[5].text)
            set_dates.append(set_.find_all('td')[5].text)

            print('\n')
    return expansion_names, set_dates

def remove_bracket_rel_dates(set_dates)
"""
Interacts with output of get_expansion_names_dates function to remove brackets from set dates.

Inputs: set_dates variable from function.
Outputs: set dates as list without brackets.
"""
    set_dates_new = []
    for i in set_dates:
        if '[' in i:
            if i[-5] == '[': # two digits in brackets
                i = i[:-5]
                set_dates_new.append(i)
            else:  # three digits in brackets
                i=i[:-6]
                set_dates_new.append(i)
        else: set_dates_new.append(i)        
    set_dates_new[51] = set_dates_new[51][:-5]
    return set_dates_new

def scrape_core_sets(soup):
"""
Interacts with Wikipedia soup object to scrape expansion names and release dates for Core MTG sets.

Inputs: soup object.
Outputs: expansion names and release dates as lists.
"""
    core_expansion_names = []
    core_set_dates = []

    for set_ in soup.find_all('table', class_ = 'wikitable')[0].find_all('tr')[2:100]: # list of 'tr's goes to ????
        if not set_.td.get('colspan'): # only cycle row tr's have 'colspan' attribute in first 'td' tag
            try: 
                if set_.find('a').text not in core_expansion_names:
                    print(set_.find('a').text)
                    core_expansion_names.append(set_.find('a').text.strip())

                print(set_.find_all('td')[4].text)
                core_set_dates.append(set_.find_all('td')[4].text)
            except: continue
    return core_expansion_names, core_set_dates

def remove_brackets_core_set_list(core_set_dates):
"""
Interacts with output of scrape_core_sets function to remove brackets from set dates.

Inputs: core_set_dates variable from function.
Outputs: set dates as list without brackets.
"""
    core_set_dates_new = []
    for i in core_set_dates:
        if '[' in i:
            if i[-5] == '[': # two digits in brackets
                i = i[:-5]
                core_set_dates_new.append(i)
            else:  # one digits in brackets
                i=i[:-4]
                core_set_dates_new.append(i)
        else: core_set_dates_new.append(i)        

    return core_set_dates_new

def scrape_reprint_comp_sets(soup):
"""
Interacts with Wikipedia soup object to scrape expansion names and release dates for supplemental MTG sets.

Inputs: soup object.
Outputs: expansion names and release dates as lists.
"""
    supp_expansion_names = []
    supp_set_dates = []


    for set_ in soup.find_all('table', class_ = 'wikitable')[4].find_all('tr')[2:100]: # list of 'tr's goes to ????
        if not set_.td.get('colspan'): # only cycle row tr's have 'colspan' attribute in first 'td' tag
            print(set_.find_all('td')[0].text)
            supp_expansion_names.append(set_.find_all('td')[0].text.strip())

            print(set_.find_all('td')[3].text)
            supp_set_dates.append(set_.find_all('td')[3].text.strip())

            print('\n')
    return supp_expansion_names, supp_set_dates

def remove_brackets_supp_sets(supp_set_dates):
"""
Interacts with output of scrape_reprint_comp_sets function to remove brackets from set dates.

Inputs: supp_set_dates variable from function.
Outputs: set dates as list without brackets.
"""
    supp_set_dates_new = []
    for i in supp_set_dates:
        if '[' in i:
            i=i[:-5] # three digits in brackets
            supp_set_dates_new.append(i)
        else: supp_set_dates_new.append(i)        
    return supp_set_dates

def get_days(x):
"""
Loops through modern_df['time_since_release'] and returns dat element of datetime object or nan.
"""
    for i in modern_df['time_since_release']:
        try: 
            return x.days
        except: 
            return np.nan