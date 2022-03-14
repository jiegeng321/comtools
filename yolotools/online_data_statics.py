#!/usr/local/bin/python3
# -*- coding:utf-8 -*-
"""
@author: WEW
@contact: wangerwei@tju.edu.cn
"""
import os

import requests
import random
import json
PROXY_INFO = {
    'host': '10.57.22.219',
    'port': 3128
}

cookies = {"_fmdata":"TSlEnN1aCN8WJbfLtrgo8pCY7D69XbTQtN7OrEK4TxmaaVlwqBPJ%2F9%2BT4wAl9P0Yw%2B3cGSysdum9ORITwjsDFfKBC6qCZUGKQkWRjvnshe4%3D",
           "_xid":"bNSmHcKX%2FGcolXI1p8Dva2KjTc062z0mrl8Adr97QFYh8Qm%2FR7x2CUDInXG4Ahh%2FqXC%2B1DlAW9T435KC3vp9qQ%3D%3D",
           "c":"EoBueM0Q-1634026139646-531920bff50a1136116601",
           "NSESSIONID":"ae9f610a-1d2f-41ee-a416-224659705c50",
           "TDCP_US_INNER":"9200852a9ebc94c439897165bea263da5125cafbad0cfab2c67257e16dcbc90e",
           "TDpx":"0",
           "XSRF-TOKEN":"c7dd4868-b655-459d-a5af-1fff90b2d58c"
           }

def load_url(url):
    try:
        response = requests.get(url)
    except:
        return ""
    try:
        res = response.json()
    except:
        return ""
    return res

def get_label(label_str):
    label_str = label_str.split(",")
    first_label = []
    second_label = []
    third_label = []

    for i in label_str:
        i = i.strip("[图像]")
        sd = i.split('/')
        if len(sd)==1:
            first_label.append(sd[0].lower())
        elif len(sd) == 2:
            first_label.append(sd[0].lower())
            second_label.append(sd[1].lower())
        else:
            first_label.append(sd[0].lower())
            second_label.append(sd[1].lower())
            if sd[2].lower()=="new_york_yankees":
                sd[2] = "mlb"
            elif sd[2].lower()=="dolce_gabbana":
                sd[2] = "dolce"
            elif sd[2].lower()=="dior":
                sd[2] = "christian_dior"
            elif sd[2].lower()=="offwhite":
                sd[2] = "off_white"
            else:
                pass
            third_label.append(sd[2].lower())
    return list(set(first_label)), list(set(second_label)), list(set(third_label))


def autoVSfinal(autolabel, finallabel):
    # print(autolabel, "----->", finallabel)
    for a_l in autolabel:
        if a_l in finallabel:
            return True
    return False



def Statics(json_res,dst_dir):
    # pic nums
    data_nums = len(json_res['data'])
    print(data_nums)
    pos_n = 0
    neg_n = 0
    Reject_n = 0
    for p_l in json_res["data"]:
        if "autoCheckResult" in p_l:
            autocheckres = p_l["autoCheckResult"]
        else:
            autocheckres = None
        if "finalCheckResult" in p_l:
            finalcheckres = p_l["finalCheckResult"]
        else:
            finalcheckres = None

        if autocheckres==finalcheckres:
            pos_n += 1
        else:
            neg_n += 1

        # if autocheckres == "Reject":
        #     autostr = p_l["tagHit"]
        #     autofirstlabel, autosecondlabel, autothirdlabel = get_label(autostr)
        # else:
        #     autofirstlabel = None
        if finalcheckres == "Reject":
            #print(p_l)
            Reject_n += 1
            finalstr = p_l["finalTagHit"]
            finalfirstlabel, finalsecondlabel, finalthirdlabel = get_label(finalstr)
            if "侵权" in finalfirstlabel:
                if "品牌" in finalsecondlabel:
                    if finalthirdlabel == [] or not finalthirdlabel:
                        continue
                    try:
                        finalthirdlabel = max(finalthirdlabel, key=finalthirdlabel.count)
                    except:
                        continue
                    if finalthirdlabel in need_brand:
                        if finalthirdlabel in get_brand:
                            if get_brand[finalthirdlabel] >= need_brand[finalthirdlabel]:
                                continue
                            get_brand[finalthirdlabel] += 1
                        else:
                            get_brand[finalthirdlabel] = 1
                    else:
                        continue
                    img_url = p_l["textData"]
                    try:
                        resq = requests.get(img_url)
                    except:
                        continue
                        print("net error")
                    if len(resq.content) > 100:

                            #print(img_url)
                            #print(finalthirdlabel)
                            img_name = finalthirdlabel+"_"+img_url.split("/")[-1]
                            logo_belong = "brand"
                            for b in brand:
                                if b.replace(" ","").lower() == finalthirdlabel.replace("_","").lower():
                                    logo_belong = "brand-tm"
                            img_out = os.path.join(dst_dir,logo_belong, finalthirdlabel)
                            if not os.path.exists(img_out):
                                os.makedirs(img_out)
                            open(os.path.join(img_out,img_name), 'wb').write(resq.content)
                            print(finalthirdlabel + " +1", "total:", get_brand[finalthirdlabel])
                    else:
                        get_brand[finalthirdlabel] -= 1
                        continue
        # elif finalcheckres == "Accept":
        #     if "empty" in get_brand:
        #         if get_brand["empty"] >= need_brand["empty"]:
        #             continue
        #     img_url = p_l["textData"]
        #     try:
        #         resq = requests.get(img_url)
        #     except:
        #         print("net error")
        #     if len(resq.content) > 100:
        #         finalthirdlabel = "empty"
        #         if finalthirdlabel in need_brand:
        #             if finalthirdlabel in get_brand:
        #                 if get_brand[finalthirdlabel] >= need_brand[finalthirdlabel]:
        #                     continue
        #                 get_brand[finalthirdlabel] += 1
        #             else:
        #                 get_brand[finalthirdlabel] = 1
        #             # print(img_url)
        #             # print(finalthirdlabel)
        #             img_name = finalthirdlabel + "_" + img_url.split("/")[-1]
        #             img_out = os.path.join(dst_dir, finalthirdlabel)
        #             if not os.path.exists(img_out):
        #                 os.makedirs(img_out)
        #             open(os.path.join(img_out, img_name), 'wb').write(resq.content)
        #             print(finalthirdlabel+" +1","total:",get_brand[finalthirdlabel])
    return pos_n,neg_n,Reject_n

if __name__=="__main__":
    brand = ['MCM', 'Bjorn Borg', 'Marvel', 'Umbro', 'Hello Kitty', 'Slazenger', 'Wilson', 'Monster Energy', 'Babolat', 'Yonex', 'Ellesse', 'Srixon', 'Fischer', 'Epson', 'Diadora', 'Volkl', 'HEAD', 'tous', 'Longchamp', 'Reebok', 'Harley Davidson', 'Tonino Lamborghini', 'Clinique', 'Philipp Plein', 'ECKO', 'Evisu', 'Carolina Herrera', 'Ariel', 'FJALLRAVEN', 'helena rubinstein', 'BOSCH', 'tory burch', 'Mizuno', 'Tampa Bay Lightning', 'ED Hardy', 'DC shoes', 'Chicago Cubs', 'Havaianas', 'Houston Astros', 'Chrome Hearts', 'Blackberry', 'Durex', 'Casio', 'MLB', 'RAW', 'LG', 'Giro', 'Pandora', 'Supra', 'DHC', 'Titoni', 'CLARINS', 'Tudor', 'Kansas Royals', 'Grenco Science', 'Corum', 'Girard Perregaux', 'Carmex', 'Colorado Avalanche', 'estee lauder', 'Paul frank', 'Pxg', '3M', 'Billabong', 'Ozark', 'Minesota Twins', 'New York Mets', 'Crocs', "Jack Daniel's", 'MIFFY', 'Pinarello', 'La Martina', 'BMC Racing', 'Samsonite', 'St. Louis Cardinals', 'Playstation', 'Valentino Garavani', 'DUCATI', 'Grand Seiko', 'Cleveland golf', 'MMS', 'Timberland', 'Salomon', 'Everlast', 'DeWALT', 'Volcom', 'PANERAI', 'Jabra', 'Toronto Maple Leafs', 'John Deere', 'Caterpillar', 'Minnesota wild', 'DRAGON BALL', 'VACHERON CONSTANTIN', 'Biotherm', 'Bontrager', 'Chicago Blackhawks', 'San Jose Sharks', 'Audio Technica', 'KTM', 'Paul Shark', 'Titleist', 'Coca', 'BRUT', 'Bobbi Brown', 'Ergobaby', 'Dallas Stars', 'Shure', '3T', 'Paco Rabanne', 'Shiseido', 'Detroit Red Wings', 'PING', 'Google', 'Franco Moschino', 'Jeep', 'Ritchey', 'Arcteryx', 'Patagonia', 'Prince', 'Playboy', 'Davidoff', 'GAP', 'Foreo', 'Zumba Fitness', 'Milwaukee Brewers', 'JACOB CO', 'Guess', 'Escada', 'belkin', 'Pittsburgh Penguins', 'New York Yankees', 'Incipio', 'Dettol', 'Pony', 'FC Barcelona(FCB)', 'Bulova', "Kiehl's", 'Buffalo Sabres', 'moose knuckles', 'Montreal Canadiens', 'Dell', 'miu miu', 'Loewe', 'Ghd', 'Boston Bruins', 'Batman', 'Cath Kidston', 'Care Bears', 'ICE Watch', 'Eotech', 'Heron Preston', 'KEEN', 'harry winston', 'the punisher', 'Facebook', 'Nirvana', 'New Jersey Devils', 'Anna Sui', 'Ecco', 'Pearl Izumi', 'Los Angeles Kings', 'Braun', 'Bioderma', 'Dunhill', 'Daiwa', 'Fender', 'WWE', 'Seagate', 'CND', 'HP', 'Cisco', 'Chloe', 'Chevrolet', 'Movado', 'ENVE', 'Always', 'Calgary Flames', '5.11 Tactical', 'Blaze and the Monster Machines', 'England', 'Fear Of God Essentials', 'VLONE', 'AQUABEADS', 'ac/dc', 'Swig', 'Edmonton Oilers', 'ESS', 'PSV Eindhoven', 'Piaget', 'Speck', 'Gant', 'Victorias secret', 'Babyliss', 'Garmin', 'Sony Ericsson', 'Nutribullet', 'Motorola', 'Ibanez', 'Phoenix Coyotes', 'Furla', 'Acer', 'Chevron', 'M.A.C', 'Barbie', 'Zara', 'Diesel', 'Graham', 'Logitech', 'American Eagle', 'Conair', 'scooby doo', 'HUF', 'Tapout', 'OPI', 'Hyundai', 'Oakland Athletics', 'Olympique de Marseille', 'Whirlpool', 'Dumbo', 'Nokia', 'MOTORHEAD', 'Citizen', 'Ottawa Senators', 'Juventus', 'Crumpler', 'Issey Miyake', 'Max factor', 'Mammut', 'FLEXFIT', 'Hamilton', 'Florida Panthers', 'Toms', 'Bell  Ross', 'TECHNOMARINE', 'New York Islanders', 'BitDefender', 'Juicy Couture', 'Nashville Predators', 'West Ham United', "D'Addario", 'PJ MASKS', 'Agnes B', 'Cannondale', 'BeautyBlender', 'CLUSE', 'Xmen', 'UEFA', 'Def Leppard', 'Skoda', 'FURminator', 'Olympus', 'Harry Potter', 'Chopard', 'Anne Klein', 'Jack Jones', 'Bugslock', 'Converse', 'Glashutte Original', 'TRXTraining', 'Honeywell', 'GoPro', 'Colgate', 'iron man', 'BMW', 'Philadelphia Phillies', 'Comme Des Garcons', 'JW Anderson', 'Zegna', 'Bed Head', 'Lyle Scott', 'Carolina Hurricanes', 'Tampa Bay Rays', 'Anaheim Ducks', 'Marshall', 'Kingston', 'dyson', 'IMREN', 'Blancpain', 'Fossil', 'Los Angeles Dodgers', 'Barbour', 'Xxio', 'Mulberry', 'Bally', 'Mophie', 'Hogan', 'Addicted', 'Bebe', 'Pokemon', 'Metallica', 'Luke Combs', 'HTC', 'christian audigier', 'gazelle', 'ElementCase', 'Montreal Expos', 'Fitbit', 'Sanrio', 'Grado', 'Lululemon', 'New York Rangers', 'Clarisonic', 'Otter box', 'Griffin', 'Concord', 'Franck Muller', 'Aquascutum', 'Guerlain', 'Thomas Sabo', 'Roxy', 'BRABUS', 'Marcelo Burlon', 'Kipling', 'Too Faced', 'Death Wish Coffee Co.', 'DKNY', 'Iron Maiden', 'black panther', 'Goo Jit Zu', 'Pro Kennex', 'Pixar', 'Cacharel', 'Incase', 'SwitchEasy', 'CWC', 'ESP', 'Ariat', 'Anaheim Angels', 'UAG', 'L.O.L. SURPRISE!', 'Bugatti Veyron', 'EOS', 'Visa', 'CHAUMET', 'The Horus Heresy', 'Guardians of the Galaxy', 'A. Lange Sohne', 'PINK FLOYD', 'INFUSIUM', 'Hunter', 'jack wills', 'RB Leipzig', 'Desigual', 'Lilo Stitch', 'Iced Earth', 'Paris Saint Germain', 'Paul Smith', 'Swatch', 'VOLBEAT', 'OXO', 'Crabs Adjust Humidity', 'Roger Vivier', 'Coty', 'Premier League', 'Lesmills', 'BEN JERRYS', 'Daniel Roth', 'Bill Blass', 'Kaporal', 'Streamlight', 'Zenith', 'S.H.I.E.L.D.', 'Deadpool', 'Muhammad Ali', 'Jacquemus', 'Breeze Smoke', 'Belstaff', 'U_boat', 'Frida Kahlo', 'Power Rangers', 'Arizona Diamondbacks', 'Stefano Ricci', 'Rip Curl', 'Coogi', 'Brazil', 'USA soccer', 'ROBO FISH', 'g_star raw', 'Links of London', 'Dean Guitar', 'INSTANTLY AGELESS', 'rosetta stone', 'black widow', 'Smith Wesson', "Carter's", 'THE ALLMAN BROTHERS BAND', 'Compaq', 'Fuji film', 'GRUMPY CAT', 'Blackhawk', 'Plantronics', 'Zimmermann', 'Elvis Presley', 'SLAP CHOP', 'Amiri', 'Audi', 'Portugal', 'DFB', 'MBT', 'Fingerlings', 'cole haan', 'Gildan', 'Doctor Strange', 'bunch o balloons', 'Copper Fit', 'True Religion', 'PopSockets', 'HM', 'Cleveland Indians', 'dooney  bourke', 'Feyenoord', 'Hey Dude', 'Samantha Thavasa', 'Game of Thrones', 'Games Workshop', 'RCMA', 'Leicester City F.C', 'Forever 21', 'Bubble Guppies', 'Wrangler', 'The Black Crowes', 'Cheap Monday', 'KOSS', 'Dr. Martens', 'stan smith', 'Ado Den Haag', 'POCOYO', 'Creative', 'Fox Head', 'Hexbug', 'Shaun the sheep', 'AussieBum', 'Toy Watch', 'Lamborghini', 'Brioni', 'Travis Scott', 'SONS OF ARTHRITIS', 'Hatchimals', 'KNVB']
    style2 = ['dior-w-1', 'golden goose-1', 'coach-w-1', 'fendi-1', 'balenciaga-w-1', 'prada-w-1', 'ck-2', 'ysl-w-1', 'ysl-1', 'lv-2', 'lv-1', 'versace-w-1', 'versace-1', 'fendi-w-1', 'dolce-1', 'Givenchy-w-1', 'the north face-1', 'dior-w-2', 'golden goose-2', 'chanel-2', 'chanel-1', 'dolce-w-3', 'dolce-w-2', 'nike-1', 'nike-w-1', 'off-white-w-1', 'burberry-w-1', 'supreme-1', 'gucci-3', 'dsquared2-w-1', 'burberry-1', 'gucci-2', 'ck-1', 'armani-1', 'Michael Kors-1', 'burberry-2', 'Kenzo-1', 'Givenchy-1', 'Hermes-w-1', 'fendi-2', 'Hermes-2', 'Hermes-1', 'Michael Kors-w-1', 'nike-6', 'dior-1', 'Moncler-1', 'Moncler-2', 'off-white-1', 'balenciaga-1', 'Moncler-w-1', 'supreme-2', 'armani-w-1', 'armani-w-2', 'dior-2', 'gucci-1', 'dolce-3', 'the north face-w-1', 'nike-2', 'ck-3', 'dsquared2-w-2', 'nike-5', 'armani-2', 'nike-3', 'dolce-2', 'nike-8', 'nike-4', 'palace-w-1', 'palace-1', 'Hublot-2', 'Hublot-w-1', 'canada goose-1', 'tommy Hilfiger-6', 'tag heuer-1', 'alexander mcqueen-w-2', 'alexander mcqueen-w-1', 'Abercrombie Fitch-w-3', 'Iwc-w-1', 'marc Jacobs-1', 'balmain-w-1', 'ralph lauren-1', 'tommy Hilfiger-w-1', 'audemars piguet-w-1', 'Hublot-3', 'Jaeger-LeCoultre-w-1', 'salvatore Ferragamo-1', 'Van Cleef  Arpels-w-1', 'Van Cleef  Arpels-2', 'Cartier-1', 'Cartier-w-1', 'Montblanc-2', 'New Era-1', 'New Era-w-2', 'NEW BALANCE-1', 'lacoste-w-1', 'lacoste-1', 'palm angels-1', 'Under Armour-1', 'Abercrombie Fitch-2', 'Abercrombie Fitch-w-2', 'NEW BALANCE-w-1', 'Rolex-1', 'Rolex-w-1', 'ralph lauren-w-1', 'Abercrombie Fitch-1', 'Omega-1', 'Omega-w-1', 'NEW BALANCE-2', 'CHRISTIAN LOUBOUTIN-1', 'Bvlgari-w-1', 'audemars piguet-2', 'hugo boss-w-1', 'hugo boss-w-2', 'tag heuer-w-1', 'Adidas-2', 'Adidas-w-1', 'Abercrombie Fitch-w-1', 'Iwc-w-2', 'bape-1', 'New Era-2', 'Adidas-1', 'New Era-w-1', 'marc Jacobs-w-1', 'Montblanc-w-1', 'salvatore Ferragamo-2', 'salvatore Ferragamo-4', 'tommy Hilfiger-w-2', 'canada goose-w-1', 'balmain-w-2', 'salvatore Ferragamo-3', 'balmain-1', 'Adidas-3', 'palm angels-2', 'bape-w-1', 'Van Cleef  Arpels-w-2', 'tommy Hilfiger-1', 'Montblanc-1', 'bape-w-2', 'Under Armour-w-1', 'Cartier-w-2', 'ralph lauren-2', 'bape-2', 'palm angels-3', 'Omega-5', 'Under Armour-2', 'alexander mcqueen-1', 'Omega-4', 'tommy Hilfiger-5', 'Omega-3', 'Omega-2', 'rayban-1', 'Hublot-1', 'Jaeger-LeCoultre-1', 'tommy Hilfiger-4', 'tommy Hilfiger-2', 'FILA-1', 'New Orleans Pelicans-w-2', 'Washington Redskins-1', 'Washington Redskins-w-1', 'Houston Rockets-1', 'Houston Rockets-w-2', 'Houston Rockets-w-3', 'FIFA-w-1', 'Boston Celtics-w-1', 'Pittsburgh Steelers-1', 'Pittsburgh Steelers-w-1', 'Dallas Cowboys-w-1', 'Toronto Raptors-w-1', 'Toronto Raptors-2', 'New Orleans Pelicans-1', 'New Orleans Pelicans-3', 'Brooklyn Nets-w-2', 'Boston Celtics-3', 'Boston Celtics-w-2', 'Los Angeles lakers-w-1', 'Denver Nuggets-w-2', 'Sacramento Kings-1', 'Indiana Pacers-w-2', 'Brooklyn Nets-1', 'Portland Trail Blazers-1', 'nba-w-1', 'nba-1', 'Buffalo Bills-1', 'Buffalo Bills-w-1', 'Sacramento Kings-w-1', 'Indiana Pacers-2', 'Hollister Co-1', 'Tampa Bay Buccaneers-w-1', 'Phoenix Suns-w-3', 'Phoenix Suns-w-2', 'Phoenix Suns-2', 'Houston Texans-1', 'Utah Jazz-1', 'Utah Jazz-w-1', 'david yurman-1', 'david yurman-w-1', 'Miami Heat-w-1', 'Miami Heat-w-2', 'kate spade-w-1', 'Carolina Panthers-1', 'kate spade-1', 'Milwaukee Bucks-1', 'Milwaukee Bucks-w-1', 'Detroit Lions-3', 'Utah Jazz-4', 'Sacramento Kings-3', 'Oklahoma City Thunder-1', 'Oklahoma City Thunder-w-3', 'Jacksonville Jaguars-1', 'Jacksonville Jaguars-w-1', 'San Antonio Spurs-2', 'New Orleans Pelicans-w-1', 'Orlando Magic-2', 'New York Knicks-2', 'Adobe-1', 'Adobe-w-1', 'Philadelphia Eagles-1', 'Memphis Grizzlies-w-1', 'Washington Wizards-w-1', 'Tennessee Titans-w-1', 'HID Global-1', 'CALL OF DUTY GHOSTS-w-2', 'Denver Broncos-w-1', 'Los Angeles Chargers-w-1', 'Chicago Bulls-1', 'Minnesota Timberwolves-w-1', 'Minnesota Timberwolves-w-2', 'Dallas Mavericks-w-1', 'Dallas Mavericks-1', 'Green Bay Packers-w-1', 'Dallas Mavericks-w-3', 'A-COLD-WALL-w-1', 'Indianapolis Colts-1', 'Indianapolis Colts-w-1', 'Atlanta Hawks-1', 'Detroit Lions-1', 'Oklahoma City Thunder-w-2', 'Cleveland Browns-1', 'FILA-2', 'Baltimore Ravens-w-1', 'Cleveland Browns-w-1', 'San Antonio Spurs-1', 'Miami Dolphins-w-1', 'Los Angeles Chargers-1', 'Portland Trail Blazers-w-1', 'Philadelphia 76ers-1', 'Chicago Bears-w-1', 'Orlando Magic-w-1', 'Portland Trail Blazers-w-2', 'Chicago Bears-1', 'Memphis Grizzlies-w-2', 'Hollister Co-w-1', 'New York Knicks-1', 'Washington Wizards-2', 'Tennessee Titans-1', 'Washington Wizards-w-2', 'Houston Texans-w-1', 'Guitar Hero-1', 'New York Giants-1', 'Washington Wizards-3', 'Alcon-w-1', 'Los Angeles lakers-3', 'Denver Nuggets-1', 'Denver Nuggets-2', 'Toronto Raptors-3', 'Brooklyn Nets-2', 'Denver Nuggets-w-1', 'Oakland Raiders-1', 'Oakland Raiders-w-1', 'San Francisco 49ers-1', 'San Francisco 49ers-2', 'Utah Jazz-2', 'Philadelphia 76ers-3', 'Kansas City Chiefs-1', 'Kansas City Chiefs-w-1', 'Miami Heat-1', 'Cleveland Cavaliers-w-1', 'Philadelphia 76ers-2', 'Chicago Bulls-w-1', 'Philadelphia Eagles-w-1', 'Golden State Warriors-1', 'New England Patriots-w-1', 'Chicago Bulls-w-2', 'Memphis Grizzlies-2', 'Memphis Grizzlies-1', 'Golden State Warriors-w-1', 'New England Patriots-1', 'Carolina Panthers-w-1', 'Indiana Pacers-1', 'Dallas Cowboys-w-2', 'Minnesota Vikings-1', 'Atlanta Falcons-1', 'Minnesota Vikings-w-1', 'Boston Celtics-1', 'nfl-w-1', 'nfl-2', 'Los Angeles Clippers-1', 'Miami Dolphins-1', 'Washington Wizards-1', 'Indiana Pacers-w-1', 'Baltimore Ravens-1', 'Sacramento Kings-2', 'Los Angeles lakers-2', 'New York Jets-w-1', 'Cleveland Cavaliers-1', 'Atlanta Hawks-w-1', 'Detroit Pistons-w-1', 'A-COLD-WALL-w-2', 'Orlando Magic-w-2', 'New Orleans Saints-1', 'Oklahoma City Thunder-w-1', 'Denver Broncos-1', 'Cleveland Cavaliers-3', 'Arizona Cardinals-1', 'Arizona Cardinals-w-1', 'Sacramento Kings-4', 'Minnesota Timberwolves-1', 'New York Giants-w-1', 'Los Angeles Clippers-w-1', 'Minnesota Timberwolves-2', 'blu电子烟-1', 'Philadelphia Eagles-w-2', 'Atlanta Hawks-2', 'Toronto Raptors-1', 'Chicago Bulls-w-3', 'Detroit Pistons-1', 'Orlando Magic-1', 'Cleveland Cavaliers-w-2', 'Miami Heat-2', 'Toronto Raptors-w-2', 'Denver Nuggets-4', 'Denver Nuggets-5', 'Los Angeles Rams-2', 'Orlando Magic-3', 'Los Angeles Rams-1', 'Seattle Seahawks-w-1', 'Phoenix Suns-1', 'Dallas Cowboys-w-3', 'Tampa Bay Buccaneers-1', 'Seattle Seahawks-1', 'A-COLD-WALL-1', 'Phoenix Suns-w-1', 'Houston Rockets-2', 'FIFA-1', 'Detroit Lions-w-1', 'Denver Broncos-2', 'Charlotte Hornets-2', 'Charlotte Hornets-w-1', 'Dallas Mavericks-2', 'Buffalo Bills-w-2', 'Cleveland Cavaliers-2', 'Boston Celtics-2', 'Atlanta Falcons-w-1', 'Charlotte Hornets-w-2', 'Charlotte Hornets-3', 'Hollister Co-2', 'Alcon-w-2', 'Denver Nuggets-3', 'Dallas Mavericks-w-4', 'Charlotte Hornets-1', 'Portland Trail Blazers-2', 'Detroit Lions-2', 'Portland Trail Blazers-3', 'Orlando Magic-6', 'Detroit Pistons-2', 'Denver Nuggets-6', 'Los Angeles Clippers-3', 'Los Angeles Clippers-2', 'New Orleans Pelicans-2', 'San Antonio Spurs-3', 'San Antonio Spurs-w-1', 'Toronto Raptors-w-3', 'Cincinnati Bengals-2', 'Cincinnati Bengals-w-1', 'Cincinnati Bengals-1', 'nfl-1', 'Breguet-2', 'Red Bull-1', 'USA Basketball-1', 'Nike-just do it', 'Fred Perry-2', 'Overwatch-2', 'Fred Perry-1', 'tiffany co-1', 'Marlboro-1', 'Ugg-1', 'World of Warcraft-1', 'World of Warcraft-4', 'World of Warcraft-3', 'Disney-2', 'Liverpool FC-2', 'Pantene-2', 'Pantene-1', 'Gibson-1', 'kobe-2', 'Ugg-2', 'Pampers-1', 'Honda-1', 'Breguet-1', 'Red Bull-2', 'Oakley-1', 'Benefit-1', 'Honda-2', 'Benefit-3', 'Butterfly-2', 'Gillette-w-1', 'Gillette-w-2', 'Butterfly-1', 'breitling-1', 'breitling-2', 'Liverpool FC-1', 'Lancome-1', 'Liverpool FC-w-1', 'Daniel wellington-2', 'Daniel wellington-1', 'Longines-1', "Blue's Clues-1", 'Jack wolfskin-1', 'Spyderco-1', 'Spyderco-2', 'Sisley-1', 'game boy-1', 'Starcraft-w-1', "Levi's-w-1", 'Manchester United-1', 'Sisley-2', 'Specialized-w-1', 'Specialized-1', 'Manchester City-1', 'Giuseppe Zanotti-1', 'YETI-1', 'CAZAL-1', 'Tide-1', 'Lancome-2', 'roor-1', 'Columbia-1', 'Columbia-2', 'The Rolling Stones-1', 'The Rolling Stones-w-1', 'Zelda-w-1', 'switch-2', 'switch-1', 'Beats by Dr.Dre-1', 'Overwatch-1', 'Bottega Veneta-1', 'YETI-2', 'Superdry-w-3', 'Superdry-w-2', 'Arsenal-1', 'JBL-1', 'Maui Jim-1', "Levi's-1", 'Nickelodeon-1', 'Shimmer And Shine-1', 'HearthStone-3', 'HearthStone-1', 'Asics-2', 'Lego-1', 'Celine-2', 'SK-II-1', 'Ulysse Nardin-w-1', 'JBL-2', 'Oral-B-1', 'Duracell-w-2', 'Heroes of the Storm-1', 'Honda-3', 'Heroes of the Storm-3', 'R4-1', 'LINDBERG-1', 'Tottenham Hotspur-2', 'Chelsea-1', 'Chelsea-2', 'Bose-1', 'Elizabeth Arden-1', 'Beats by Dr.Dre-w-2', 'Beats by Dr.Dre-w-1', 'breitling-3', 'Zelda-3', 'Duracell-w-1', 'Diablo-1', 'Overwatch-w-1', 'L’Oreal-1', 'Ferrari-2', 'Ferrari-1', 'Tottenham Hotspur-1', 'puma-2', 'Amiibo-1', 'JUUL-1', 'Honda-5', 'Herbal Essences-w-3', 'Herbal Essences-1', 'Herbal Essences-w-1', 'World of Warcraft-w-1', 'Martin Co-1', 'Wallykazam-1', 'DESTINY-w-1', 'DESTINY-1', 'Asics-1', 'Headshoulders-1', 'Headshoulders-w-1', 'Headshoulders-w-2', 'Birkenstock-1', 'Kenan and Kel-1', 'Celine-1', 'alexander wang-w-1', 'Cummins-1', 'Asics-3', 'Honda-4', 'The Fairly Oddparents-1', 'Zelda-2', 'Amiibo-2', 'SKYLANDERS-1', 'Starcraft-2', 'goyard-1', 'Superdry-w-1', 'Apple-1', 'CAZAL-2', 'Benefit-2', 'fullips-2', 'kobe-1', 'Starcraft-1', 'Chi-1', 'fullips-1', 'Blizzard-1', 'World of Warcraft-2', 'Benefit-5', 'Benefit-6', 'Ferrari-3', 'Rimowa-1', 'The Killers-1', 'Apple-w-2', 'Heroes of the Storm-w-1', 'Heroes of the Storm-2', 'goyard-2', 'USA Basketball-2', 'The Loud House-1', 'Duracell-1', 'Starcraft-3', 'iRobot-1', 'Herbal Essences-2', 'Oakley-4', 'Manchester City-2', 'Sisley-3', 'Bose-2', 'puma-1', 'Disney-1', 'Benefit-4', 'HearthStone-2', 'Apple-w-3', 'Shimmer And Shine-2', 'hydro flask-1', 'hydro flask-w-1', 'Bose-3', 'Gibson-2', 'Apple-w-1', 'YETI-3', 'JBL-3', '7up-2', '7up-1', 'Efest-2', 'Efest-1', 'coach-1', 'USA Basketball-1d', 'Tissot-1', 'Stussy-2', 'Stussy-1', 'Blackberry Smoke-1', 'Tods-1', 'Tods-2', 'swarovski-1', 'swarovski-2', 'Skullcandy-1', 'Skullcandy-2', 'Jimmy Choo-1', 'Taylormade-2', 'Taylormade-1', 'Jurlique-1', 'Maybelline-1', 'Vans-1', 'Vans-2', 'Baby Shark-2', 'Scotty Cameron-2', 'Scotty Cameron-3', 'Scotty Cameron-1', 'Scotty Cameron-4', 'Shimano-1', 'manolo blahnik-1', 'vivienne westwood-1', 'vivienne westwood-2', 'Monchhichi-1', 'Sennheiser-2', 'Baby Shark-1', 'Vans-3', 'Shimano-2', 'Maybelline-2', 'Jimmy Choo-2', 'Bright Bugz-2', 'Sennheiser-1', 'Alberta Ferretti-w-1', 'Bright Bugz-1', 'footjoy-2', 'footjoy-w-1', 'Shimano-3', 'Shimano-4', 'Golden State Warriors-w-11', 'BENQ-w-1', 'AWT-1', 'BVB-1', 'AFC Ajax-2', 'AFC Ajax-w-1', 'Asos-w-1', 'Patek Philippe-1', 'Big Green Egg-w-2', 'Big Green Egg-w-1', 'CAMELBAK-w-1', 'Azzaro-w-1', 'Patek Philippe-2', 'AKG by Harmon-2', 'AKG by Harmon-w-1', 'Bestway-w-1', 'Allsaints-2', 'Allsaints-w-1', 'Bakugan-1', 'Beretta-2', 'Beretta-w-1', 'Cadillac-2', 'Led Zeppelin-w-2', 'Alpinestars-w-1', 'Alpinestars-2', 'Carhartt-w-1', 'Bentley-w-1', 'Bentley-2', 'Carhartt-2', 'Callaway-w-1', 'Callaway-2', 'Bushnell-w-1', 'Berluti-w-1', 'Cadillac-w-1', 'Led Zeppelin-1', 'Azzaro-2', 'c1rca-w-2', 'Cards Against Humanity-w-1', 'Avengers-w-1', 'Burts Bees-w-1', 'Canon-1', 'captain america-w-2', 'AS Roma-1', 'Benetton-w-1', 'Benetton-2', 'Atletico de Madrid-1', 'Led Zeppelin-w-3', 'Alfar Romeo-1', 'c1rca-1', 'captain america-w-3', 'Aspinal of London-w-2', 'captain america-w-1', 'Betty Boop-w-2', 'Aspinal of London-w-1', 'Betty Boop-w-1', 'Audioquest-w-1', 'Bunchems-1', 'Betty Boop-w-3', 'Alpinestars-w-3', 'AS Roma-w-2', 'Bentley-3', 'c1rca-3', 'Utah Jazz-3', 'Hennessy-w-1', 'Seattle Seahawks-11', 'Porsche-2', 'puma-w-1', 'Charlotte Hornets', 'Philadelphia 76ers-2d', 'Dallas Mavericks-w-2', 'Detroit Lions-w_1', 'Utah Jazz-1w', 'Los Angeles Clippers-4', 'Phoenix Suns-w-31', 'Bang Olufsen-2', 'Bang Olufsen-w-1', 'Nike-1', 'St Dupont-w-2', 'Merrell-w-1', 'St Dupont-w-1', 'ZigZag-1', 'Nixon-2', 'Urban Decay-3', 'Urban Decay-w-1', 'Urban Decay-w-2', 'captain america-3', 'Phiten-2', 'Texas Rangers-3', 'Texas Rangers-2', 'Texas Rangers-1', 'San Diego Padres-w-1', 'San Diego Padres-2', 'San Francisco Giants-w-1', 'San Francisco Giants-2', 'San Francisco Giants-3', 'San Francisco Giants-w-4', 'Toronto Blue Jays-1', 'Chicago White Sox-1', 'Chicago White Sox-3', 'Chicago White Sox-2', 'Cincinnati Reds-2', 'Cincinnati Reds-1', 'Cincinnati Reds-3', 'Detroit Tigers-1', 'Boston Red Sox-2', 'Boston Red Sox-4', 'Boston Red Sox-1', 'Boston Red Sox-3', 'Atlanta Bravs-1', 'Atlanta Bravs-3', 'Atlanta Bravs-4', 'Atlanta Bravs-2', 'Baltimore Orioles-4', 'Baltimore Orioles-5', 'Baltimore Orioles-2', 'Baltimore Orioles-3', 'Pinko-1', 'Florida Marlins-2', 'Florida Marlins-6', 'Florida Marlins-4', 'Florida Marlins-3', 'Florida Marlins-1', 'Florida Marlins-5', 'Baltimore Orioles-1', 'western digital-w-1', 'western digital-2', 'Hennessy-2', 'Mercedes Benz-2', 'Mercedes Benz-w-1', 'Merrell-2', 'Hennessy-3', 'Zippo-w-1', 'Zippo-2', 'Sephora-w-2', 'Sephora-1', 'Shu Uemura-w-1', 'Schwarzkopf-w-2', 'Skin79-2', 'Philadelphia Flyers-1', 'St. Louis Blues-1', 'Jim Beam-w-1', 'Vegas Golden Knights-1', 'Washington Capitals-2', 'Vancouver Canucks-2', 'Vancouver Canucks-w-3', 'Vancouver Canucks-1', 'Hurley-2', 'Hurley-w-1', 'Winnipeg Jets-1', 'Winnipeg Jets-2', 'Washington Capitals-1', 'Winnipeg Jets-3', 'Hurley-3', 'Washington Capitals-3', 'Maserati-2', 'Maserati-3', 'Hurley-5', 'Hurley-6', 'Magpul-2', 'Hurley-4', 'RADO-2', 'Roger Dubuis-2', 'Roger Dubuis-w-1', 'Romain Jerome-1', 'Kappa-2', 'Baby phat-w-1', 'Baby phat-2', 'Toppik-w-1', 'Land Rover-w-1', 'Land Rover-2', 'LED LENSER-2', 'Robo Alive-w-1', 'Tech Deck-w-1', 'SHOPKINS-w-1', 'Porsche-w-1', 'Maserati-w-1', 'Columbus Blue Jackets-3', 'Columbus Blue Jackets-2', 'FC bayern munchen-1', 'HAMANN-w-2', 'HAMANN-1', 'Nasa-1']
    brand2 = []
    for s in style2:
        brand2.append(s.split("-")[0])
    brand2 = list(set(brand2))
    brand_total = brand+brand2
    with open('/data01/xu.fx/comtools/human_label_to_model_label/l2l_dict.json', 'r') as f:
        data = json.load(f)
    #print(data)
    need_brand = {}
    need_brand["empty"] = 0
    for b in brand_total:
        if b not in data:
            need_brand[b.lower().replace(" ","_")] = 500
            continue
        need_brand[data[b].split("/")[-1]] = 500
    print(len(need_brand))
    for q in ["playboy","converse","tory_burch","mlb","valentino_garavani","mcm","loewe","pokemon"]\
             +["adidas","apple","armani","asics","balenciaga","bottega_veneta","burberry","bvlgari",
               "calvin_klein","cartier","celine","chanel","coach","disney","fendi","fila","givenchy",
               "gucci","hermes","hugo_boss","lacoste","louis_vuitton","michael_kors","new_balance",
               "nike","omega","prada","puma","ralph_lauren","rolex","supreme","the_north_face",
               "tommy_hilfiger","vans","versace"]:
        need_brand.pop(q)
    print(len(need_brand))

    # need_brand = {"playboy":1000,"converse":1000,"mlb":1000,"miu_miu":1000,"mcm":1000,"loewe":1000,"casio":1000,"reebok":1000
    #               ,"lamborghini":1000,"chrome_hearts":1000,"audi":1000,"batman":1000,"roger_vivier":1000,"salomon":1000,"bmw":1000
    #               ,"victorias_secret":1000,"diesel":1000,"zenith":1000,"paul_shark":1000,"franck_muller":1000,"comme_des_garcons":1000,
    #               "timberland":1000,"bally":1000,"vacheron_constantin":1000,"philipp_plein":1000,"valentino_garavani":1000}
    need_brand = {"louis_vuitton":10000}

    print(need_brand)
    get_brand = {}

    Reject = 0
    pos=0
    neg=0
    dst_dir = "/data01/xu.fx/dataset/NEW_RAW_INCREASE_DATA/fordeal1012_1025_for_logo_data"
    #days = ["2021-10-14","2021-10-15","2021-10-16","2021-10-17","2021-10-18","2021-10-19","2021-10-20","2021-10-21","2021-10-22"]
    days = ["2021-10-20","2021-10-21", "2021-10-22", "2021-10-23", "2021-10-24","2021-10-25"]
    days = []
    for i in range(20,30):
        days.append("2021-10-%d"%i)

    for day in days:
        for i in range(1, 1000):
            url = f"https://p-compliance.tongdun.cn/pcompliance/internal/model/data/download?partnerCode=nraqcs&startTime={day} 00:00:00&endTime={day} 23:59:59&pageNum={i}"
            json_res = load_url(url)
            #print(json_res)
            if "data" not in json_res:
                break
            pos_n,neg_n,Reject_n = Statics(json_res, dst_dir)
            pos+=pos_n
            neg+=neg_n
            Reject+=Reject_n
            print("day: ",day,"pagenum: ",i)
            print("get brand:",get_brand)
    print(pos,neg,Reject)