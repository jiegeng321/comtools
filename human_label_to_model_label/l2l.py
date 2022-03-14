#!/usr/local/bin/python3
# -*- coding:utf-8 -*-
import json
import pandas as pd
excel_file = "./LOGO_1-3_level_label_20210902.xlsx"
model1_label = ['Portland Trail Blazers', 'HID Global', 'Sacramento Kings', 'Sisley', 'palm angels', 'Bottega Veneta', 'Boston Celtics', "Levi's", 'Headshoulders', 'The Fairly Oddparents', 'R4', 'fullips', 'Disney', 'Jimmy Choo', 'breitling', 'Birkenstock', 'Bestway', 'New England Patriots', 'hydro flask', 'Brooklyn Nets', 'Los Angeles Rams', 'Elizabeth Arden', 'Cleveland Cavaliers', 'FIFA', 'Omega', 'swarovski', 'palace', 'Fred Perry', 'Azzaro', 'Rolex', 'Ferrari', 'Philadelphia Eagles', 'Chelsea', 'dsquared2', 'Cincinnati Bengals', 'Ugg', 'dior', 'Cummins', 'coach', 'Hollister Co', 'JUUL', 'iRobot', 'Aspinal of London', 'Asos', 'LINDBERG', 'CAZAL', 'david yurman', 'roor', 'Avengers', 'Seattle Seahawks', 'canada goose', 'alexander wang', 'Cadillac', 'Oakley', 'Tods', 'Buffalo Bills', 'alexander mcqueen', 'Skullcandy', 'supreme', 'Hermes', 'New York Knicks', 'Minnesota Vikings', 'off', 'Houston Rockets', 'Miami Heat', 'lv', 'marc Jacobs', 'Tampa Bay Buccaneers', 'Baby Shark', 'footjoy', 'Benetton', 'Milwaukee Bucks', 'USA Basketball', 'Atletico de Madrid', 'Denver Broncos', 'Arsenal', 'Alcon', 'BVB', 'AS Roma', 'New York Giants', 'Heroes of the Storm', 'Breguet', 'hugo boss', 'ck', 'Detroit Pistons', 'Canon', 'Maui Jim', 'Daniel wellington', 'Alpinestars', 'tommy Hilfiger', 'Los Angeles lakers', 'Allsaints', 'Cards Against Humanity', 'Longines', 'Michael Kors', 'armani', 'CAMELBAK', 'Giuseppe Zanotti', 'Honda', 'Maybelline', 'switch', 'Martin Co', 'DESTINY', 'Starcraft', 'Patek Philippe', 'c1rca', 'Tide', "L'Oreal", 'Bright Bugz', 'AFC Ajax', 'Washington Redskins', 'Asics', 'Denver Nuggets', 'Baltimore Ravens', 'Bunchems', 'bape', 'Cartier', 'burberry', 'CHRISTIAN LOUBOUTIN', 'JBL', 'Oakland Raiders', 'Berluti', 'New Orleans Saints', 'Stussy', 'Orlando Magic', 'Miami Dolphins', 'captain america', 'Jacksonville Jaguars', 'Spyderco', 'audemars piguet', 'SKYLANDERS', 'Audioquest', 'Duracell', 'Rimowa', 'Led Zeppelin', 'dolce', 'Chicago Bears', 'salvatore Ferragamo', 'Bvlgari', 'Herbal Essences', 'Taylormade', 'tag heuer', 'the north face', 'San Francisco 49ers', 'Nickelodeon', 'Charlotte Hornets', 'Big Green Egg', 'prada', 'Columbia', 'Minnesota Timberwolves', 'Dallas Mavericks', 'nfl', 'fendi', 'Houston Texans', 'Kansas City Chiefs', 'Alberta Ferretti', 'Shimmer And Shine', 'Los Angeles Clippers', 'YETI', 'San Antonio Spurs', 'Memphis Grizzlies', 'Carolina Panthers', 'puma', 'Pantene', 'Indianapolis Colts', 'Monchhichi', 'Jurlique', 'tiffany co', 'Apple', 'Beats by Dr.Dre', 'game boy', 'SK', 'NEW BALANCE', 'Alfar Romeo', 'Dallas Cowboys', 'Atlanta Falcons', 'The Killers', 'balmain', 'World of Warcraft', 'Tennessee Titans', 'Scotty Cameron', 'Bakugan', 'kate spade', 'Amiibo', 'Atlanta Hawks', 'New Orleans Pelicans', 'New York Jets', 'Blackberry Smoke', 'Lego', 'BENQ', 'AKG by Harmon', 'Iwc', 'Burts Bees', 'rayban', 'Pittsburgh Steelers', 'lacoste', 'Zelda', 'nike', '7up', 'nba', 'Liverpool FC', 'manolo blahnik', 'Bose', 'goyard', 'Shimano', 'Montblanc', 'Red Bull', 'The Loud House', 'Callaway', 'Moncler', 'versace', 'Phoenix Suns', 'Jaeger', 'Under Armour', 'Green Bay Packers', 'Diablo', 'Arizona Cardinals', 'Hublot', 'Toronto Raptors', 'kobe', 'Benefit', 'Chi', 'balenciaga', 'ralph lauren', 'Ulysse Nardin', 'Betty Boop', 'FILA', 'Nike', 'AWT', 'Washington Wizards', 'Bushnell', 'Gillette', 'Bentley', 'Beretta', 'Indiana Pacers', 'Oklahoma City Thunder', 'Vans', 'Guitar Hero', 'Lancome', 'Sennheiser', 'Cleveland Browns', 'Tissot', 'Specialized', 'Kenzo', 'chanel', 'Utah Jazz', 'Detroit Lions', 'Jack wolfskin', 'The Rolling Stones', 'gucci', 'Tottenham Hotspur', 'Kenan and Kel', 'vivienne westwood', 'Chicago Bulls', 'blu???', 'New Era', 'Adidas', 'CALL OF DUTY GHOSTS', 'Marlboro', 'Celine', 'Golden State Warriors', 'Oral', 'Blizzard', 'Efest', 'golden goose', 'Adobe', 'Gibson', 'Abercrombie Fitch', 'A', 'Carhartt', 'Superdry', 'Givenchy', 'Wallykazam', 'HearthStone', 'Philadelphia 76ers', "Blue's Clues", 'Pampers', 'Van Cleef Arpels', 'Los Angeles Chargers', 'Overwatch', 'Manchester United', 'Manchester City', 'Butterfly', 'ysl']
model2_label = ['MCM', 'Bjorn Borg', 'Babolat', 'Marvel', 'Umbro', 'Hello Kitty', 'Slazenger', 'Wilson', 'Srixon', 'Beachbody', 'Fischer', 'Epson', 'Volkl', 'HEAD', 'tous', 'CLARINS', 'Longchamp', 'Harley Davidson', 'Tonino Lamborghini', 'Clinique', 'Reebok', 'Philipp Plein', 'Evisu', 'Carolina Herrera', 'Ariel', 'FJALLRAVEN', 'helena rubinstein', 'BOSCH', 'DC shoes', 'Tampa Bay Lightning', 'Havaianas', 'Chrome Hearts', 'Blackberry', 'Casio', 'Durex', 'RAW', 'Giro', 'Titoni', 'Pandora', 'DHC', 'Supra', 'Tudor', 'Grenco Science', 'Corum', 'estee lauder', 'Carmex', 'Pxg', '3M', 'Billabong', 'Ozark', 'Crocs', "Jack Daniel's", 'MIFFY', 'Pinarello', 'Samsonite', 'La Martina', 'BMC Racing', 'Valentino Garavani', 'DUCATI', 'Playstation', 'St. Louis Cardinals', 'Cleveland golf', 'Grand Seiko', 'MMS', 'Salomon', 'Everlast', 'DeWALT', 'Volcom', 'Piaget', 'PANERAI', 'Jabra', 'Caterpillar', 'Toronto Maple Leafs', 'DRAGON BALL', 'Minnesota wild', 'VACHERON CONSTANTIN', 'Biotherm', 'Bontrager', 'Audio Technica', 'Chicago Blackhawks', 'San Jose Sharks', 'BRUT', 'Coca', 'Bobbi Brown', 'Titleist', 'Google', 'Detroit Red Wings', 'Jeep', 'Shure', '3T', 'PING', 'Franco Moschino', 'Ritchey', 'Arcteryx', 'Prince', 'GAP', 'Foreo', 'Davidoff', 'Playboy', 'Zumba Fitness', 'JACOB CO', 'Guess', 'Escada', 'Fender', 'belkin', 'Pittsburgh Penguins', 'Ghd', 'Dettol', 'Incipio', 'FC Barcelona(FCB)', 'Pony', 'Bulova', "Kiehl's", 'Montreal Canadiens', 'moose knuckles', 'Buffalo Sabres', 'Batman', 'WWE', 'Dell', 'miu miu', 'Cath Kidston', 'Eotech', '5.11 Tactical', 'ICE Watch', 'Care Bears', 'the punisher', 'KEEN', 'harry winston', 'Facebook', 'Dunhill', 'Ecco', 'Anna Sui', 'Pearl Izumi', 'New Jersey Devils', 'Braun', 'Los Angeles Kings', 'Daiwa', 'Bioderma', 'HP', 'Cisco', 'CND', 'Chloe', 'Movado', 'Chevrolet', 'ENVE', 'Always', 'Fear Of God Essentials', 'VLONE', 'AQUABEADS', 'Edmonton Oilers', 'ac dc', 'ESS', 'PSV Eindhoven', 'Citizen', 'Speck', 'Babyliss', 'Gant', 'Garmin', 'Diesel', 'Sony Ericsson', 'Ibanez', 'Motorola', 'christian audigier', 'Phoenix Coyotes', 'Furla', 'Acer', 'Chevron', 'Barbie', 'M.A.C', 'scooby doo', 'HUF', 'Zara', 'Graham', 'Conair', 'American Eagle', 'Hyundai', 'Tapout', 'Olympique de Marseille', 'Dumbo', 'Nokia', 'MOTORHEAD', 'Juventus', 'Ottawa Senators', 'Max factor', 'Issey Miyake', 'FLEXFIT', 'Hamilton', 'Nashville Predators', 'Toms', 'Bell Ross', 'TECHNOMARINE', 'New York Islanders', 'Anne Klein', 'Juicy Couture', 'BitDefender', 'GoPro', 'West Ham United', 'CLUSE', "D'Addario", 'Agnes B', 'PJ MASKS', 'Jack Jones', 'BeautyBlender', 'Xmen', 'UEFA', 'Def Leppard', 'FURminator', 'Olympus', 'Chopard', 'Bugslock', 'Converse', 'Colgate', 'Glashutte Original', 'Honeywell', 'TRXTraining', 'iron man', 'BMW', 'Philadelphia Phillies', 'JW Anderson', 'Comme Des Garcons', 'Zegna', 'Bed Head', 'Lyle Scott', 'Fossil', 'MLB', 'Tampa Bay Rays', 'Marshall', 'Kingston', 'Anaheim Ducks', 'IMREN', 'Blancpain', 'Sanrio', 'Bally', 'Barbour', 'Xxio', 'Mulberry', 'HTC', 'Mophie', 'Hogan', 'Addicted', 'Bebe', 'Metallica', 'Luke Combs', 'gazelle', 'Grado', 'Fitbit', 'Lululemon', 'New York Rangers', 'Clarisonic', 'Otter box', 'Griffin', 'Concord', 'Guerlain', 'Franck Muller', 'Aquascutum', 'Thomas Sabo', 'Roxy', 'BRABUS', 'DKNY', 'Marcelo Burlon', 'Kipling', 'Nintendo', 'Death Wish Coffee Co.', 'Iron Maiden', 'black panther', 'Pro Kennex', 'Cacharel', 'Pixar', 'CWC', 'Incase', 'SwitchEasy', 'ESP', 'Ariat', 'EOS', 'L.O.L. SURPRISE!', 'UAG', 'Bugatti Veyron', 'Guardians of the Galaxy', 'CHAUMET', 'Visa', 'The Horus Heresy', 'A. Lange Sohne', 'Hunter', 'INFUSIUM', 'jack wills', 'RB Leipzig', 'VOLBEAT', 'Kaporal', 'Desigual', 'Crabs Adjust Humidity', 'Iced Earth', 'Lilo Stitch', 'Roger Vivier', 'Paris Saint Germain', 'Swatch', 'Coty', 'Premier League', 'Bill Blass', 'Audi', 'Daniel Roth', 'Streamlight', 'Zenith', 'S.H.I.E.L.D.', 'Deadpool', 'Muhammad Ali', 'Jacquemus', 'Power Rangers', 'Elvis Presley', 'Breeze Smoke', 'Belstaff', 'U_boat', 'Frida Kahlo', 'Stefano Ricci', 'g_star raw', 'Brazil', 'USA soccer', 'Dean Guitar', 'INSTANTLY AGELESS', 'black widow', 'Smith Wesson', "Carter's", 'THE ALLMAN BROTHERS BAND', 'Fuji film', 'GRUMPY CAT', 'Blackhawk', 'Zimmermann', 'Plantronics', 'Copper Fit', 'Amiri', 'Portugal', 'cole haan', 'Fingerlings', 'MBT', 'Red wing', 'Feyenoord', 'Doctor Strange', 'Games Workshop', 'bunch o balloons', 'PopSockets', 'HM', 'Wrangler', 'dooney bourke', 'Hey Dude', 'Game of Thrones', 'Bubble Guppies', 'Forever 21', 'The Black Crowes', 'Cheap Monday', 'Dr. Martens', 'KOSS', 'Fox Head', 'stan smith', 'Ado Den Haag', 'Creative', 'POCOYO', 'Hexbug', 'AussieBum', 'Toy Watch', 'Lamborghini', 'Brioni', 'Hatchimals', 'KNVB', 'Spibelt', 'Snow White']
model_label = model1_label+model2_label
print(len(model1_label))
print(len(model2_label))
#data = pd.read_excel(excel_file)
data_xls = pd.ExcelFile(excel_file)
level_3_label = data_xls.parse(sheet_name="品牌三级标签")["小写"].values.tolist()
#print(level_3_label)
l2l_dict = {}
for m_label in model_label:
    if m_label.replace("_", "").replace("  ", "_").replace(" ", "_").replace("'", "").replace("!", "").replace("???", "").replace("/", "").replace(".", "").lower() in level_3_label:
        l2l_dict[m_label]="[图像]侵权/品牌/"+m_label.replace("_", "").replace("  ", "_").replace(" ", "_").replace("'", "").replace("!", "").replace("???", "").replace("/", "").replace(".", "").lower()
    elif m_label=="L'Oreal":
        l2l_dict[m_label] = "[图像]侵权/品牌/" + "l_oreal"
    elif m_label=="A COLD WALL":
        l2l_dict[m_label] = "[图像]侵权/品牌/" + "acoldwall"
    elif m_label=="Headshoulders":
        l2l_dict[m_label] = "[图像]侵权/品牌/" + "head_shoulders"
    elif m_label=="lv":
        l2l_dict[m_label] = "[图像]侵权/品牌/" + "louis_vuitton"
    elif m_label=="ck":
        l2l_dict[m_label] = "[图像]侵权/品牌/" + "calvin_klein"
    elif m_label=="FC Barcelona(FCB)":
        l2l_dict[m_label] = "[图像]侵权/品牌/" + "fc_barcelona_fcb"
    elif m_label=="PSV Eindhoven":
        l2l_dict[m_label] = "[图像]侵权/品牌/" + "psv"
    elif m_label=="Olympique de Marseille":
        l2l_dict[m_label] = "[图像]侵权/品牌/" + "olympique_marseille"
    elif m_label == "TRXTraining":
        l2l_dict[m_label] = "[图像]侵权/品牌/" + "trx_training"
    elif m_label == "USA soccer":
        l2l_dict[m_label] = "[图像]侵权/品牌/" + "usa"
    elif m_label == "USA Basketball":
        l2l_dict[m_label] = "[图像]侵权/品牌/" + "usa_basketball"
    elif m_label == "bunch o balloons":
        l2l_dict[m_label] = "[图像]侵权/品牌/" + "bunch_o_ballons"
    elif m_label == "dolce":
        l2l_dict[m_label] = "[图像]侵权/品牌/" + "dolce_gabbana"
    else:
        #l2l_dict[m_label] = "unknow"
        print(m_label)
print(len(model_label))
print(len(l2l_dict))
print(l2l_dict)
with open('l2l_dict.json', 'w') as f:
    json.dump(l2l_dict, f)

with open('l2l_dict.json', 'r') as f:
    data = json.load(f)
print(data)
