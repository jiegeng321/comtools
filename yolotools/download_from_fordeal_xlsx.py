#!/usr/local/bin/python3
# -*- coding:utf-8 -*-
import requests
import json
#import cv2
import os
import numpy as np
import pandas as pd
from tqdm import tqdm
def read_csv(csv_path):
    if csv_path.endswith('.xlsx'):
        csv = pd.read_excel(csv_path, keep_default_na=False)
    elif csv_path.endswith('.csv'):
        csv = pd.read_csv(csv_path, keep_default_na=False)
    else:
        print("the format is Error!")
        exit()
    return csv
def get_img(url_image):
    try:
        resq = requests.get(url_image)
    except:
        return None,None
    imgdata=None
    if len(resq.content) > 100:
        imgdata = resq.content
    file_name = url_image.split("/")[-1]
    return imgdata, file_name
def main(csv_path):
    csv = read_csv(csv_path)[:]
    if need_brand:
        brand_num = {}
        for key, value in need_brand.items():
            brand_num[key] = 0
        for index, item in tqdm(enumerate(csv.itertuples())):
            # if item[5]==0:
            #     continue
            #if index<3172:
            #    continue
            for key, value in brand_num.items():
                print("%s num is %d/%d"%(key,value,need_brand[key]))
            for key, value in need_brand.items():
                human_result = str(item[5])
                #print(item[3])
                item_str = ""
                for it in human_result:
                    item_str+=it
                if key not in item_str:
                    continue
                for data in item:
                    if brand_num[key]>value:
                        print("%s is enough, %d"%(brand_num[key],value))
                        break
                    if not isinstance(data, str) or not data.startswith("https://"):
                        continue
                    img_data, file_name = get_img(data)
                    if img_data is None:
                        continue
                    save_dir = os.path.join(save_main_dir,key)
                    if not os.path.exists(save_dir):
                        os.makedirs(save_dir)
                    with open(os.path.join(save_dir,file_name),"wb") as f:
                        f.write(img_data)
                    brand_num[key]+=1
    else:
        total_num = 0
        for index, item in tqdm(enumerate(csv.itertuples())):
            # if index<1000:
            #    continue
            for data in item:
                if not isinstance(data, str) or not data.startswith("https://"):
                    continue
                img_data, file_name = get_img(data)
                if img_data is None:
                    continue
                if not os.path.exists(save_main_dir):
                    os.makedirs(save_main_dir)
                with open(os.path.join(save_main_dir, file_name), "wb") as f:
                    f.write(img_data)
                total_num += 1

# brand = ['MCM', 'Bjorn Borg', 'Marvel', 'Umbro', 'Hello Kitty', 'Slazenger', 'Wilson', 'Monster Energy', 'Babolat', 'Yonex', 'Ellesse', 'Srixon', 'Fischer', 'Epson', 'Diadora', 'Volkl', 'HEAD', 'tous', 'Longchamp', 'Reebok', 'Harley Davidson', 'Tonino Lamborghini', 'Clinique', 'Philipp Plein', 'ECKO', 'Evisu', 'Carolina Herrera', 'Ariel', 'FJALLRAVEN', 'helena rubinstein', 'BOSCH', 'tory burch', 'Mizuno', 'Tampa Bay Lightning', 'ED Hardy', 'DC shoes', 'Chicago Cubs', 'Havaianas', 'Houston Astros', 'Chrome Hearts', 'Blackberry', 'Durex', 'Casio', 'MLB', 'RAW', 'LG', 'Giro', 'Pandora', 'Supra', 'DHC', 'Titoni', 'CLARINS', 'Tudor', 'Kansas Royals', 'Grenco Science', 'Corum', 'Girard Perregaux', 'Carmex', 'Colorado Avalanche', 'estee lauder', 'Paul frank', 'Pxg', '3M', 'Billabong', 'Ozark', 'Minesota Twins', 'New York Mets', 'Crocs', "Jack Daniel's", 'MIFFY', 'Pinarello', 'La Martina', 'BMC Racing', 'Samsonite', 'St. Louis Cardinals', 'Playstation', 'Valentino Garavani', 'DUCATI', 'Grand Seiko', 'Cleveland golf', 'MMS', 'Timberland', 'Salomon', 'Everlast', 'DeWALT', 'Volcom', 'PANERAI', 'Jabra', 'Toronto Maple Leafs', 'John Deere', 'Caterpillar', 'Minnesota wild', 'DRAGON BALL', 'VACHERON CONSTANTIN', 'Biotherm', 'Bontrager', 'Chicago Blackhawks', 'San Jose Sharks', 'Audio Technica', 'KTM', 'Paul Shark', 'Titleist', 'Coca', 'BRUT', 'Bobbi Brown', 'Ergobaby', 'Dallas Stars', 'Shure', '3T', 'Paco Rabanne', 'Shiseido', 'Detroit Red Wings', 'PING', 'Google', 'Franco Moschino', 'Jeep', 'Ritchey', 'Arcteryx', 'Patagonia', 'Prince', 'Playboy', 'Davidoff', 'GAP', 'Foreo', 'Zumba Fitness', 'Milwaukee Brewers', 'JACOB CO', 'Guess', 'Escada', 'belkin', 'Pittsburgh Penguins', 'New York Yankees', 'Incipio', 'Dettol', 'Pony', 'FC Barcelona(FCB)', 'Bulova', "Kiehl's", 'Buffalo Sabres', 'moose knuckles', 'Montreal Canadiens', 'Dell', 'miu miu', 'Loewe', 'Ghd', 'Boston Bruins', 'Batman', 'Cath Kidston', 'Care Bears', 'ICE Watch', 'Eotech', 'Heron Preston', 'KEEN', 'harry winston', 'the punisher', 'Facebook', 'Nirvana', 'New Jersey Devils', 'Anna Sui', 'Ecco', 'Pearl Izumi', 'Los Angeles Kings', 'Braun', 'Bioderma', 'Dunhill', 'Daiwa', 'Fender', 'WWE', 'Seagate', 'CND', 'HP', 'Cisco', 'Chloe', 'Chevrolet', 'Movado', 'ENVE', 'Always', 'Calgary Flames', '5.11 Tactical', 'Blaze and the Monster Machines', 'England', 'Fear Of God Essentials', 'VLONE', 'AQUABEADS', 'ac/dc', 'Swig', 'Edmonton Oilers', 'ESS', 'PSV Eindhoven', 'Piaget', 'Speck', 'Gant', 'Victorias secret', 'Babyliss', 'Garmin', 'Sony Ericsson', 'Nutribullet', 'Motorola', 'Ibanez', 'Phoenix Coyotes', 'Furla', 'Acer', 'Chevron', 'M.A.C', 'Barbie', 'Zara', 'Diesel', 'Graham', 'Logitech', 'American Eagle', 'Conair', 'scooby doo', 'HUF', 'Tapout', 'OPI', 'Hyundai', 'Oakland Athletics', 'Olympique de Marseille', 'Whirlpool', 'Dumbo', 'Nokia', 'MOTORHEAD', 'Citizen', 'Ottawa Senators', 'Juventus', 'Crumpler', 'Issey Miyake', 'Max factor', 'Mammut', 'FLEXFIT', 'Hamilton', 'Florida Panthers', 'Toms', 'Bell  Ross', 'TECHNOMARINE', 'New York Islanders', 'BitDefender', 'Juicy Couture', 'Nashville Predators', 'West Ham United', "D'Addario", 'PJ MASKS', 'Agnes B', 'Cannondale', 'BeautyBlender', 'CLUSE', 'Xmen', 'UEFA', 'Def Leppard', 'Skoda', 'FURminator', 'Olympus', 'Harry Potter', 'Chopard', 'Anne Klein', 'Jack Jones', 'Bugslock', 'Converse', 'Glashutte Original', 'TRXTraining', 'Honeywell', 'GoPro', 'Colgate', 'iron man', 'BMW', 'Philadelphia Phillies', 'Comme Des Garcons', 'JW Anderson', 'Zegna', 'Bed Head', 'Lyle Scott', 'Carolina Hurricanes', 'Tampa Bay Rays', 'Anaheim Ducks', 'Marshall', 'Kingston', 'dyson', 'IMREN', 'Blancpain', 'Fossil', 'Los Angeles Dodgers', 'Barbour', 'Xxio', 'Mulberry', 'Bally', 'Mophie', 'Hogan', 'Addicted', 'Bebe', 'Pokemon', 'Metallica', 'Luke Combs', 'HTC', 'christian audigier', 'gazelle', 'ElementCase', 'Montreal Expos', 'Fitbit', 'Sanrio', 'Grado', 'Lululemon', 'New York Rangers', 'Clarisonic', 'Otter box', 'Griffin', 'Concord', 'Franck Muller', 'Aquascutum', 'Guerlain', 'Thomas Sabo', 'Roxy', 'BRABUS', 'Marcelo Burlon', 'Kipling', 'Too Faced', 'Death Wish Coffee Co.', 'DKNY', 'Iron Maiden', 'black panther', 'Goo Jit Zu', 'Pro Kennex', 'Pixar', 'Cacharel', 'Incase', 'SwitchEasy', 'CWC', 'ESP', 'Ariat', 'Anaheim Angels', 'UAG', 'L.O.L. SURPRISE!', 'Bugatti Veyron', 'EOS', 'Visa', 'CHAUMET', 'The Horus Heresy', 'Guardians of the Galaxy', 'A. Lange Sohne', 'PINK FLOYD', 'INFUSIUM', 'Hunter', 'jack wills', 'RB Leipzig', 'Desigual', 'Lilo Stitch', 'Iced Earth', 'Paris Saint Germain', 'Paul Smith', 'Swatch', 'VOLBEAT', 'OXO', 'Crabs Adjust Humidity', 'Roger Vivier', 'Coty', 'Premier League', 'Lesmills', 'BEN JERRYS', 'Daniel Roth', 'Bill Blass', 'Kaporal', 'Streamlight', 'Zenith', 'S.H.I.E.L.D.', 'Deadpool', 'Muhammad Ali', 'Jacquemus', 'Breeze Smoke', 'Belstaff', 'U_boat', 'Frida Kahlo', 'Power Rangers', 'Arizona Diamondbacks', 'Stefano Ricci', 'Rip Curl', 'Coogi', 'Brazil', 'USA soccer', 'ROBO FISH', 'g_star raw', 'Links of London', 'Dean Guitar', 'INSTANTLY AGELESS', 'rosetta stone', 'black widow', 'Smith Wesson', "Carter's", 'THE ALLMAN BROTHERS BAND', 'Compaq', 'Fuji film', 'GRUMPY CAT', 'Blackhawk', 'Plantronics', 'Zimmermann', 'Elvis Presley', 'SLAP CHOP', 'Amiri', 'Audi', 'Portugal', 'DFB', 'MBT', 'Fingerlings', 'cole haan', 'Gildan', 'Doctor Strange', 'bunch o balloons', 'Copper Fit', 'True Religion', 'PopSockets', 'HM', 'Cleveland Indians', 'dooney  bourke', 'Feyenoord', 'Hey Dude', 'Samantha Thavasa', 'Game of Thrones', 'Games Workshop', 'RCMA', 'Leicester City F.C', 'Forever 21', 'Bubble Guppies', 'Wrangler', 'The Black Crowes', 'Cheap Monday', 'KOSS', 'Dr. Martens', 'stan smith', 'Ado Den Haag', 'POCOYO', 'Creative', 'Fox Head', 'Hexbug', 'Shaun the sheep', 'AussieBum', 'Toy Watch', 'Lamborghini', 'Brioni', 'Travis Scott', 'SONS OF ARTHRITIS', 'Hatchimals', 'KNVB']
# with open('/data01/xu.fx/comtools/human_label_to_model_label/l2l_dict.json', 'r') as f:
#     data = json.load(f)
#print(data)
need_brand = {"new_york_yankees":2000}#{"nike":1000,"adidas":1000,"gucci":1000,"fendi":1000,"coach":1000,"michael_kors":1000,"louis_vuitton":1000}
# need_brand["0"] = 20000
# for b in brand:
#     if b not in data:
#         need_brand[b.lower().replace(" ","_")] = 500
#         continue
#     need_brand[data[b].split("/")[-1]] = 500

print(need_brand)
#num_per_brand = 4000
save_main_dir = "/data01/xu.fx/dataset/NEW_RAW_INCREASE_DATA/fordeal_1013_for_NewYorkYankees"
#csv_path = "/data01/xu.fx/dataset/NEW_RAW_INCREASE_DATA/fordeal待审核商品0913.xlsx"
csv_path = "/data01/xu.fx/dataset/NEW_RAW_INCREASE_DATA/fordeal待审数据0923.xlsx"
main(csv_path)
