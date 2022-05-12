#!/usr/local/bin/python3
# -*- coding:utf-8 -*-

import random
from tqdm import tqdm
import hashlib
from pathlib import Path
from PIL import Image
import shutil
import xml.etree.ElementTree as ET
from comfunc.path import ospathjoin
from comfunc.check import check_dir
from multiprocessing import Pool, Manager
import cv2
import os
import numpy as np
import pandas as pd
from comfunc.print_color import bcolors
import warnings
# warnings.filterwarnings("error", category=UserWarning)
# Image.warnings.simplefilter('error', Image.DecompressionBombWarning)
from comfunc.tools import is_img
#main_data_dir为数据总目录，建议该目录下包含名为checked的目录然后该目录下为xml与图片混合的数据，之后全自动生成yolo数据集和相关数据集统计信息

be_merged_dir = None#"dataset/LOGO_DATASET/D14"
white_sample_dir_list = {}
white_sample_dir_list["/data01/xu.fx/dataset/LOGO_DATASET/white_data/logo_white_data_from_fordeal_high_quality"] = 0
white_sample_dir_list["/data01/xu.fx/dataset/LOGO_DATASET/white_data/logo_white_data_from_fordeal_high_quality_2nd"] = 0

show_data_info = False
use_effective_brand = False
use_class_brand = True

random_seed = 1
train_val_test_ratio = [0.99, 0.01, 0.0]
MAX_NUM_PER_BRAND = None
MAX_OBJ_NUM_PER_BRAND = 2000
#WHITE_SAMPLE_COUNT = 0
detect_num = 2
export_data_info_csv = True
WORKERS = 30

main_data_dir = "dataset/LOGO_DATASET/comb_data"
yolo_dataset_name = "yolodataset_logo_784bs_1392ks_0415"

######################################################## WEW #########################################
CLASS_list_wew = ['dior-w-1', 'golden goose-1', 'coach-w-1', 'fendi-1', 'balenciaga-w-1', 'prada-w-1', 'ck-2', 'ysl-w-1', 'ysl-1', 'lv-2', 'lv-1', 'versace-w-1', 'versace-1', 'fendi-w-1', 'dolce-1', 'Givenchy-w-1', 'the north face-1', 'golden goose-2', 'chanel-2', 'chanel-1', 'dolce-w-3', 'dolce-w-2', 'nike-1', 'nike-w-1', 'off white-w-1', 'burberry-w-1', 'supreme-1', 'gucci-3', 'dsquared2-w-1', 'burberry-1', 'gucci-2', 'ck-1', 'armani-1', 'Michael Kors-1', 'burberry-2', 'Kenzo-1', 'Givenchy-1', 'Hermes-w-1', 'fendi-2', 'Hermes-2', 'Hermes-1', 'Michael Kors-w-1', 'nike-6', 'dior-1', 'Moncler-1', 'Moncler-2', 'off white-1', 'balenciaga-1', 'Moncler-w-1', 'supreme-2', 'armani-w-1', 'armani-w-2', 'dior-2', 'gucci-1', 'dolce-3', 'nike-2', 'palace-w-1', 'palace-1', 'Hublot-2', 'Hublot-w-1', 'canada goose-1', 'tommy Hilfiger-1', 'tag heuer-1', 'alexander mcqueen-w-2', 'alexander mcqueen-w-1', 'Abercrombie Fitch-w-3', 'Iwc-w-1', 'marc Jacobs-1', 'balmain-w-1', 'ralph lauren-1', 'tommy Hilfiger-w-1', 'audemars piguet-w-1', 'Jaeger LeCoultre-w-1', 'salvatore Ferragamo-1', 'Van Cleef Arpels-w-1', 'Van Cleef Arpels-2', 'Cartier-1', 'Cartier-w-1', 'Montblanc-2', 'New Era-1', 'New Era-w-2', 'NEW BALANCE-1', 'lacoste-w-1', 'lacoste-1', 'palm angels-1', 'Under Armour-1', 'Abercrombie Fitch-2', 'Abercrombie Fitch-w-2', 'NEW BALANCE-w-1', 'Rolex-1', 'Rolex-w-1', 'ralph lauren-w-1', 'Abercrombie Fitch-1', 'Omega-1', 'Omega-w-1', 'NEW BALANCE-2', 'CHRISTIAN LOUBOUTIN-1', 'Bvlgari-w-1', 'audemars piguet-2', 'hugo boss-w-1', 'hugo boss-w-2', 'tag heuer-w-1', 'Adidas-2', 'Adidas-w-1', 'Abercrombie Fitch-w-1', 'Iwc-w-2', 'bape-1', 'bape-2', 'New Era-2', 'Adidas-1', 'New Era-w-1', 'marc Jacobs-w-1', 'Montblanc-w-1', 'salvatore Ferragamo-2', 'salvatore Ferragamo-4', 'tommy Hilfiger-w-2', 'canada goose-w-1', 'salvatore Ferragamo-3', 'balmain-1', 'palm angels-2', 'bape-w-1', 'bape-w-2', 'Under Armour-w-1', 'Cartier-w-2', 'alexander mcqueen-1', 'rayban-1', 'FILA-1', 'New Orleans Pelicans-w-2', 'Washington Redskins-1', 'Washington Redskins-w-1', 'Houston Rockets-1', 'Houston Rockets-w-2', 'Houston Rockets-w-3', 'FIFA-w-1', 'Boston Celtics-w-1', 'Pittsburgh Steelers-1', 'Pittsburgh Steelers-w-1', 'Dallas Cowboys-w-1', 'Toronto Raptors-w-1', 'Toronto Raptors-2', 'New Orleans Pelicans-1', 'New Orleans Pelicans-3', 'Brooklyn Nets-w-2', 'Boston Celtics-3', 'Boston Celtics-w-2', 'Los Angeles lakers-w-1', 'Denver Nuggets-w-2', 'Sacramento Kings-1', 'Indiana Pacers-w-2', 'Brooklyn Nets-1', 'Portland Trail Blazers-1', 'nba-w-1', 'nba-1', 'Buffalo Bills-1', 'Buffalo Bills-w-1', 'Sacramento Kings-w-1', 'Indiana Pacers-2', 'Hollister Co-1', 'Tampa Bay Buccaneers-w-1', 'Phoenix Suns-w-3', 'Phoenix Suns-w-2', 'Phoenix Suns-2', 'Houston Texans-1', 'Utah Jazz-1', 'Utah Jazz-w-1', 'david yurman-1', 'david yurman-w-1', 'Miami Heat-w-1', 'Miami Heat-w-2', 'kate spade-w-1', 'Carolina Panthers-1', 'kate spade-1', 'Milwaukee Bucks-1', 'Milwaukee Bucks-w-1', 'Detroit Lions-3', 'Utah Jazz-4', 'Sacramento Kings-3', 'Oklahoma City Thunder-1', 'Oklahoma City Thunder-w-3', 'Jacksonville Jaguars-1', 'Jacksonville Jaguars-w-1', 'San Antonio Spurs-2', 'New Orleans Pelicans-w-1', 'Orlando Magic-2', 'New York Knicks-2', 'Adobe-1', 'Adobe-w-1', 'Philadelphia Eagles-1', 'Memphis Grizzlies-w-1', 'Washington Wizards-w-1', 'Tennessee Titans-w-1', 'HID Global-1', 'CALL OF DUTY GHOSTS-w-2', 'Denver Broncos-w-1', 'Los Angeles Chargers-w-1', 'Chicago Bulls-1', 'Minnesota Timberwolves-w-1', 'Minnesota Timberwolves-w-2', 'Dallas Mavericks-w-1', 'Dallas Mavericks-1', 'Green Bay Packers-w-1', 'Dallas Mavericks-w-3', 'A COLD WALL-w-1', 'Indianapolis Colts-1', 'Indianapolis Colts-w-1', 'Atlanta Hawks-1', 'Detroit Lions-1', 'Oklahoma City Thunder-w-2', 'Cleveland Browns-1', 'FILA-2', 'Baltimore Ravens-w-1', 'Cleveland Browns-w-1', 'San Antonio Spurs-1', 'Miami Dolphins-w-1', 'Los Angeles Chargers-1', 'Portland Trail Blazers-w-1', 'Philadelphia 76ers-1', 'Chicago Bears-w-1', 'Orlando Magic-w-1', 'Portland Trail Blazers-w-2', 'Chicago Bears-1', 'Memphis Grizzlies-w-2', 'Hollister Co-w-1', 'New York Knicks-1', 'Washington Wizards-2', 'Tennessee Titans-1', 'Houston Texans-w-1', 'Guitar Hero-1', 'New York Giants-1', 'Washington Wizards-3', 'Alcon-w-1', 'Los Angeles lakers-3', 'Denver Nuggets-1', 'Denver Nuggets-2', 'Toronto Raptors-3', 'Brooklyn Nets-2', 'Denver Nuggets-w-1', 'Oakland Raiders-1', 'Oakland Raiders-w-1', 'San Francisco 49ers-1', 'San Francisco 49ers-2', 'Utah Jazz-2', 'Philadelphia 76ers-3', 'Kansas City Chiefs-1', 'Kansas City Chiefs-w-1', 'Miami Heat-1', 'Cleveland Cavaliers-w-1', 'Philadelphia 76ers-2', 'Chicago Bulls-w-1', 'Philadelphia Eagles-w-1', 'Golden State Warriors-1', 'New England Patriots-w-1', 'Chicago Bulls-w-2', 'Memphis Grizzlies-2', 'Memphis Grizzlies-1', 'Golden State Warriors-w-1', 'New England Patriots-1', 'Carolina Panthers-w-1', 'Indiana Pacers-1', 'Dallas Cowboys-w-2', 'Minnesota Vikings-1', 'Atlanta Falcons-1', 'Minnesota Vikings-w-1', 'Boston Celtics-1', 'nfl-w-1', 'nfl-2', 'Los Angeles Clippers-1', 'Miami Dolphins-1', 'Washington Wizards-1', 'Indiana Pacers-w-1', 'Baltimore Ravens-1', 'Sacramento Kings-2', 'Los Angeles lakers-2', 'New York Jets-w-1', 'Cleveland Cavaliers-1', 'Atlanta Hawks-w-1', 'Detroit Pistons-w-1', 'A COLD WALL-w-2', 'Orlando Magic-w-2', 'New Orleans Saints-1', 'Oklahoma City Thunder-w-1', 'Denver Broncos-1', 'Cleveland Cavaliers-3', 'Arizona Cardinals-1', 'Arizona Cardinals-w-1', 'Sacramento Kings-4', 'Minnesota Timberwolves-1', 'New York Giants-w-1', 'Los Angeles Clippers-w-1', 'Minnesota Timberwolves-2', 'blu-1', 'Philadelphia Eagles-w-2', 'Atlanta Hawks-2', 'Toronto Raptors-1', 'Chicago Bulls-w-3', 'Detroit Pistons-1', 'Orlando Magic-1', 'Cleveland Cavaliers-w-2', 'Miami Heat-2', 'Toronto Raptors-w-2', 'Denver Nuggets-4', 'Denver Nuggets-5', 'Los Angeles Rams-2', 'Los Angeles Rams-1', 'Seattle Seahawks-w-1', 'Phoenix Suns-1', 'Dallas Cowboys-w-3', 'Tampa Bay Buccaneers-1', 'Seattle Seahawks-1', 'Phoenix Suns-w-1', 'Houston Rockets-2', 'FIFA-1', 'Detroit Lions-w-1', 'Charlotte Hornets-2', 'Charlotte Hornets-w-1', 'Dallas Mavericks-2', 'Buffalo Bills-w-2', 'Cleveland Cavaliers-2', 'Atlanta Falcons-w-1', 'Charlotte Hornets-w-2', 'Alcon-w-2', 'Charlotte Hornets-1', 'Cincinnati Bengals-2', 'Cincinnati Bengals-w-1', 'Cincinnati Bengals-1', 'Breguet-2', 'Red Bull-1', 'USA Basketball-1', 'nike-w-2', 'Fred Perry-2', 'Overwatch-2', 'Fred Perry-1', 'tiffany co-1', 'Marlboro-1', 'Ugg-1', 'World of Warcraft-1', 'World of Warcraft-4', 'World of Warcraft-3', 'Disney-2', 'Liverpool FC-2', 'Pantene-2', 'Pantene-1', 'Gibson-1', 'kobe-2', 'Pampers-1', 'Honda-1', 'Breguet-1', 'Red Bull-2', 'Oakley-1', 'Benefit-1', 'Honda-2', 'Benefit-3', 'Butterfly-2', 'Gillette-w-1', 'Gillette-w-2', 'Butterfly-1', 'breitling-1', 'breitling-2', 'Liverpool FC-1', 'Lancome-1', 'Liverpool FC-w-1', 'Daniel wellington-2', 'Daniel wellington-1', 'Longines-1', "Blue's Clues-1", 'Jack wolfskin-1', 'Spyderco-1', 'Spyderco-2', 'Sisley-1', 'game boy-1', 'Starcraft-w-1', "Levi's-w-1", 'Manchester United-1', 'Sisley-2', 'Specialized-w-1', 'Specialized-1', 'Manchester City-1', 'Giuseppe Zanotti-1', 'YETI-1', 'CAZAL-1', 'Tide-1', 'Lancome-2', 'roor-1', 'Columbia-1', 'Columbia-2', 'The Rolling Stones-1', 'The Rolling Stones-w-1', 'Zelda-w-1', 'switch-2', 'switch-1', 'Beats by Dr.Dre-1', 'Overwatch-1', 'Bottega Veneta-1', 'YETI-2', 'Superdry-w-3', 'Superdry-w-2', 'Arsenal-1', 'JBL-1', 'Maui Jim-1', "Levi's-1", 'Nickelodeon-1', 'Shimmer And Shine-1', 'HearthStone-3', 'HearthStone-1', 'Asics-2', 'Lego-1', 'Celine-2', 'SK II-1', 'Ulysse Nardin-w-1', 'Oral B-1', 'Duracell-w-2', 'Heroes of the Storm-1', 'Honda-3', 'Heroes of the Storm-3', 'R4-1', 'LINDBERG-1', 'Tottenham Hotspur-2', 'Chelsea-1', 'Chelsea-2', 'Bose-1', 'Elizabeth Arden-1', 'Beats by Dr.Dre-w-2', 'Beats by Dr.Dre-w-1', 'breitling-3', 'Zelda-3', 'Duracell-w-1', 'Diablo-1', 'Overwatch-w-1', 'L Oreal-1', 'Ferrari-2', 'Ferrari-1', 'Tottenham Hotspur-1', 'puma-2', 'Amiibo-1', 'JUUL-1', 'Honda-5', 'Herbal Essences-w-3', 'Herbal Essences-1', 'Herbal Essences-w-1', 'World of Warcraft-w-1', 'Martin Co-1', 'Wallykazam-1', 'DESTINY-w-1', 'DESTINY-1', 'Asics-1', 'Headshoulders-1', 'Headshoulders-w-1', 'Headshoulders-w-2', 'Birkenstock-1', 'Kenan and Kel-1', 'Celine-1', 'alexander wang-w-1', 'Cummins-1', 'Asics-3', 'Honda-4', 'The Fairly Oddparents-1', 'Zelda-2', 'Amiibo-2', 'SKYLANDERS-1', 'Starcraft-2', 'goyard-1', 'Superdry-w-1', 'Apple-1', 'Benefit-2', 'fullips-2', 'kobe-1', 'Starcraft-1', 'Chi-1', 'fullips-1', 'Blizzard-1', 'World of Warcraft-2', 'Ferrari-3', 'Rimowa-1', 'The Killers-1', 'goyard-2', 'USA Basketball-2', 'The Loud House-1', 'Starcraft-3', 'iRobot-1', 'Herbal Essences-2', 'Manchester City-2', 'Sisley-3', 'puma-1', 'Disney-1', 'HearthStone-2', 'Apple-w-3', 'hydro flask-1', 'hydro flask-w-1', 'Gibson-2', '7up-2', '7up-1', 'Efest-2', 'Efest-1', 'Tissot-w-1', 'Stussy-2', 'Stussy-1', 'Blackberry Smoke-1', 'Tods-1', 'Tods-2', 'SWAROVSKI-w-1', 'SWAROVSKI-2', 'Skullcandy-1', 'Skullcandy-2', 'Jimmy Choo-1', 'Taylormade-2', 'Taylormade-1', 'Jurlique-1', 'Maybelline-1', 'Vans-1', 'Vans-2', 'Baby Shark-w-2', 'Scotty Cameron-2', 'Scotty Cameron-3', 'Scotty Cameron-1', 'Scotty Cameron-4', 'Shimano-1', 'manolo blahnik-1', 'vivienne westwood-1', 'vivienne westwood-2', 'Monchhichi-1', 'Sennheiser-2', 'Baby Shark-w-1', 'Vans-3', 'Shimano-2', 'Maybelline-2', 'Jimmy Choo-2', 'Bright Bugz-2', 'Sennheiser-w-1', 'Alberta Ferretti-w-1', 'Bright Bugz-1', 'footjoy-2', 'footjoy-w-1', 'BENQ-w-1', 'AWT-1', 'BVB-1', 'AFC Ajax-2', 'AFC Ajax-w-1', 'Asos-w-1', 'Patek Philippe-1', 'Big Green Egg-w-2', 'Big Green Egg-w-1', 'CAMELBAK-w-1', 'Azzaro-w-1', 'Patek Philippe-2', 'AKG by Harmon-2', 'AKG by Harmon-w-1', 'Bestway-w-1', 'Allsaints-w-1', 'Bakugan-1', 'Beretta-2', 'Beretta-w-1', 'Cadillac-2', 'Led Zeppelin-w-2', 'Alpinestars-w-1', 'Alpinestars-2', 'Carhartt-w-1', 'Bentley-w-1', 'Bentley-2', 'Carhartt-2', 'Callaway-w-1', 'Callaway-2', 'Bushnell-w-1', 'Berluti-w-1', 'Cadillac-w-1', 'Led Zeppelin-1', 'Azzaro-2', 'c1rca-w-2', 'Cards Against Humanity-w-1', 'Avengers-w-1', 'Burts Bees-w-1', 'Canon-1', 'captain america-w-2', 'AS Roma-1', 'Benetton-w-1', 'Benetton-2', 'Atletico de Madrid-1', 'Led Zeppelin-w-3', 'Alfar Romeo-1', 'c1rca-1', 'captain america-w-3', 'Aspinal of London-w-2', 'captain america-w-1', 'Betty Boop-w-2', 'Aspinal of London-w-1', 'Betty Boop-w-1', 'Audioquest-w-1', 'Bunchems-1', 'Betty Boop-w-3', 'Alpinestars-w-3', 'AS Roma-w-2', 'Hennessy-w-1', 'Porsche-2', 'puma-w-1', 'Bang Olufsen-2', 'Bang Olufsen-w-1', 'St Dupont-w-2', 'Merrell-w-1', 'ZigZag-1', 'Nixon-2', 'Urban Decay-3', 'Urban Decay-w-1', 'Urban Decay-w-2', 'captain america-3', 'Phiten-2', 'Texas Rangers-3', 'Texas Rangers-2', 'Texas Rangers-1', 'San Diego Padres-w-1', 'San Diego Padres-2', 'San Francisco Giants-w-1', 'San Francisco Giants-2', 'San Francisco Giants-3', 'San Francisco Giants-w-4', 'Toronto Blue Jays-1', 'Chicago White Sox-1', 'Chicago White Sox-3', 'Chicago White Sox-2', 'Cincinnati Reds-2', 'Cincinnati Reds-1', 'Detroit Tigers-1', 'Boston Red Sox-2', 'Boston Red Sox-4', 'Boston Red Sox-1', 'Boston Red Sox-3', 'Atlanta Bravs-1', 'Atlanta Bravs-3', 'Atlanta Bravs-4', 'Atlanta Bravs-2', 'Baltimore Orioles-4', 'Baltimore Orioles-5', 'Baltimore Orioles-2', 'Baltimore Orioles-3', 'Pinko-1', 'Florida Marlins-2', 'Florida Marlins-6', 'Florida Marlins-4', 'Florida Marlins-3', 'Florida Marlins-1', 'Florida Marlins-5', 'western digital-w-1', 'western digital-2', 'Hennessy-2', 'Mercedes Benz-2', 'Mercedes Benz-w-1', 'Merrell-2', 'Zippo-w-1', 'Zippo-2', 'Sephora-w-2', 'Sephora-1', 'Shu Uemura-w-1', 'Schwarzkopf-w-2', 'Skin79-2', 'Philadelphia Flyers-1', 'St. Louis Blues-1', 'Jim Beam-w-1', 'Vegas Golden Knights-1', 'Washington Capitals-2', 'Vancouver Canucks-2', 'Vancouver Canucks-w-3', 'Vancouver Canucks-1', 'Hurley-2', 'Hurley-w-1', 'Winnipeg Jets-1', 'Winnipeg Jets-2', 'Washington Capitals-1', 'Maserati-2', 'Maserati-3', 'Hurley-6', 'Magpul-2', 'RADO-2', 'Roger Dubuis-2', 'Roger Dubuis-w-1', 'Romain Jerome-1', 'Kappa-2', 'Baby phat-w-1', 'Baby phat-2', 'Toppik-w-1', 'Land Rover-w-1', 'Land Rover-2', 'LED LENSER-2', 'Robo Alive-w-1', 'Tech Deck-w-1', 'SHOPKINS-w-1', 'Porsche-w-1', 'Columbus Blue Jackets-3', 'Columbus Blue Jackets-2', 'FC bayern munchen-1', 'HAMANN-w-2', 'HAMANN-1', 'Nasa-1']
######################################################## WEW ########################################
######################################################## FX #########################################
CLASS_list_fx = ['3M-1', '3T-1', '5.11 Tactical-2', 'A. Lange Sohne-w-1', 'ac dc-w-1', 'Acer-w-1', 'Addicted-w-1', 'Ado Den Haag-1', 'Agnes B-w-1', 'Always-w-1', 'American Eagle-1', 'American Eagle-w-2', 'Amiri-1', 'Anaheim Angels-1', 'Anaheim Angels-2', 'Anaheim Ducks-1', 'Anaheim Ducks-2', 'Anaheim Ducks-3', 'Anna Sui-w-1', 'Anne Klein-2', 'Anne Klein-w-1', 'AQUABEADS-w-1', 'Aquascutum-2', 'Aquascutum-w-1', 'Arcteryx-1', 'Arcteryx-w-2', 'Ariat-2', 'Ariat-w-1', 'Ariel-2', 'Ariel-w-1', 'Arizona Diamondbacks-1', 'Arizona Diamondbacks-4', 'Arizona Diamondbacks-w-2', 'Audi-2', 'Audio Technica-1', 'Audio Technica-w-2', 'AussieBum-w-1', 'AussieBum-w-2', 'Babolat-1', 'Babolat-w-2', 'Babyliss-1', 'Bally-w-1', 'Barbie-1', 'Barbie-2', 'Barbour-w-1', 'Batman-2', 'Batman-w-1', 'BeautyBlender-2', 'BeautyBlender-w-1', 'Bebe-w-1', 'Bed Head-w-1', 'belkin-2', 'belkin-w-1', 'Bell Ross-w-1', 'Bell Ross-w-2', 'Belstaff-2', 'Belstaff-w-1', 'BEN JERRYS-w-1', 'Bill Blass-2', 'Bill Blass-w-1', 'Billabong-2', 'Billabong-w-1', 'Bioderma-w-1', 'Biotherm-w-1', 'BitDefender-2', 'BitDefender-w-1', 'Bjorn Borg-w-1', 'Bjorn Borg-w-3', 'black panther-w-1', 'black panther-w-2', 'black widow-w-1', 'black widow-w-2', 'Blackberry-2', 'Blackberry-w-1', 'Blackhawk-2', 'Blackhawk-w-1', 'Blancpain-w-1', 'Blaze and the Monster Machines-1', 'Blaze and the Monster Machines-2', 'BMC Racing-1', 'BMW-1', 'Bobbi Brown-2', 'Bobbi Brown-w-1', 'Bobbi Brown-w-3', 'Bontrager-2', 'Bontrager-w-1', 'BOSCH-2', 'BOSCH-w-1', 'Boston Bruins-2', 'Boston Bruins-3', 'BRABUS-w-1', 'Braun-w-1', 'Brazil-1', 'Breeze Smoke-w-1', 'Brioni-1', 'BRUT-w-1', 'Bubble Guppies-1', 'Buffalo Sabres-2', 'Buffalo Sabres-3', 'Buffalo Sabres-w-1', 'Bugatti Veyron-1', 'Bugatti Veyron-2', 'Bugslock-w-1', 'Bulova-2', 'Bulova-w-1', 'bunch o balloons-w-1', 'Cacharel-w-1', 'Calgary Flames-3', 'Cannondale-2', 'Cannondale-w-1', 'Care Bears-1', 'Carmex-w-1', 'Carolina Herrera-2', 'Carolina Herrera-w-1', 'Carolina Hurricanes-2', "Carter's-w-1", 'Casio-w-1', 'Casio-w-2', 'Caterpillar-2', 'Caterpillar-w-1', 'Cath Kidston-1', 'CHAUMET-w-1', 'Cheap Monday-2', 'Cheap Monday-w-1', 'Chevrolet-2', 'Chevrolet-w-1', 'Chevron-1', 'Chevron-w-2', 'Chicago Blackhawks-2', 'Chicago Blackhawks-3', 'Chicago Cubs-1', 'Chicago Cubs-2', 'Chloe-w-1', 'Chopard-w-1', 'Chopard-w-2', 'christian audigier-3',  'Chrome Hearts-2', 'Chrome Hearts-w-1', 'Chrome Hearts-w-3', 'Cisco-2', 'Cisco-w-1', 'Citizen-w-1', 'CLARINS-w-1', 'Clarisonic-w-1', 'Clarisonic-w-2', 'Cleveland golf-2', 'Cleveland golf-w-1', 'Cleveland Indians-1', 'Cleveland Indians-2', 'Clinique-1', 'Clinique-w-2', 'CLUSE-w-1', 'CND-1', 'Coca Cola-1', 'cole haan-w-1', 'Colgate-w-1', 'Colorado Avalanche-2', 'Colorado Avalanche-3', 'Colorado Avalanche-w-1', 'Comme Des Garcons-2', 'Comme Des Garcons-w-1', 'Compaq-1', 'Compaq-w-2', 'Conair-w-1', 'Concord-2', 'Concord-w-1', 'Converse-1', 'Converse-3', 'Converse-w-2', 'Coogi-w-1', 'Copper Fit-1', 'Corum-2', 'Corum-w-1', 'Coty-2', 'Coty-w-1', 'Crabs Adjust Humidity-1', 'Crabs Adjust Humidity-w-3', 'Creative-1', 'Crocs-2', 'Crocs-w-1', 'Crumpler-1', 'Crumpler-2', 'CWC-1', "D'Addario-w-1", 'Daiwa-1', 'Daiwa-2', 'Dallas Stars-1', 'Dallas Stars-2', 'Daniel Roth-w-1', 'Daniel Roth-w-2', 'Davidoff-2', 'Davidoff-3', 'Davidoff-w-1', 'DC shoes-1', 'DC shoes-w-1', 'Deadpool-w-1', 'Dean Guitar-1', 'Death Wish Coffee Co.-1', 'Def Leppard-1', 'Def Leppard-w-2', 'Dell-1', 'Desigual-w-1', 'Detroit Red Wings-1', 'Dettol-w-1', 'DeWALT-w-1', 'DFB-1', 'DHC-w-1', 'Diadora-2', 'Diadora-3', 'Diesel-w-1', 'DKNY-w-2', 'Doctor Strange-w-1', 'Doctor Strange-w-2', 'dooney bourke-2', 'dooney bourke-w-1', 'Dr. Martens-w-1', 'DRAGON BALL-1', 'DRAGON BALL-w-2', 'DUCATI-1', 'DUCATI-w-2', 'Dumbo-1', 'Dunhill-1', 'Dunhill-w-2', 'Durex-w-1', 'dyson-1', 'Ecco-w-1', 'ECKO-2', 'ECKO-w-1', 'ED Hardy-2', 'ED Hardy-w-1', 'Edmonton Oilers-1', 'ElementCase-2', 'ElementCase-w-1', 'Ellesse-1', 'Ellesse-w-2', 'Elvis Presley-2', 'England-1', 'ENVE-1', 'EOS-w-1', 'Eotech-1', 'Eotech-3', 'Eotech-w-2', 'Epson-w-1', 'Ergobaby-2', 'Ergobaby-w-1', 'Escada-w-1', 'ESP-1', 'ESS-w-1', 'estee lauder-2', 'estee lauder-w-1', 'Everlast-2', 'Everlast-w-1', 'Evisu-1', 'Evisu-w-2', 'Facebook-1', 'Facebook-w-2', 'FC Barcelona(FCB)-1', 'Fear Of God Essentials-w-1', 'Fear Of God Essentials-w-2', 'Fear Of God Essentials-w-3', 'Fender-1', 'Feyenoord-1', 'Fingerlings-1', 'Fischer-1', 'Fischer-w-2', 'Fitbit-2', 'Fitbit-w-1', 'FJALLRAVEN-1', 'FJALLRAVEN-w-2', 'FLEXFIT-2', 'FLEXFIT-w-1', 'Florida Panthers-1', 'Florida Panthers-3', 'Foreo-w-1', 'Forever 21-w-1', 'Fossil-w-1', 'Fox Head-2', 'Franck Muller-2', 'Franck Muller-w-1', 'Franco Moschino-w-1', 'Frida Kahlo-1', 'Fuji film-w-1', 'Furla-w-1', 'FURminator-w-1', 'g_star raw-2', 'g_star raw-w-1', 'Game of Thrones-1', 'Game of Thrones-2', 'Games Workshop-w-2', 'Gant-w-1', 'GAP-w-1', 'Garmin-w-1', 'gazelle-w-1', 'Ghd-1', 'Gildan-w-1', 'Girard Perregaux-2', 'Girard Perregaux-w-1', 'Giro-2', 'Giro-w-1', 'Glashutte Original-1', 'Glashutte Original-2', 'Goo Jit Zu-1', 'Google-w-1', 'GoPro-w-1', 'Grado-w-1', 'Graham-w-1', 'Grand Seiko-1', 'Grand Seiko-2', 'Grenco Science-2', 'Grenco Science-3', 'Grenco Science-w-1', 'Griffin-3', 'Griffin-w-1', 'Griffin-w-2', 'GRUMPY CAT-w-1', 'Guardians of the Galaxy-w-1', 'Guerlain-w-1', 'Guess-1', 'Guess-w-2', 'Hamilton-w-1', 'Harley Davidson-1', 'Harley Davidson-2', 'Harry Potter-1', 'harry winston-1', 'harry winston-w-2', 'harry winston-w-3', 'harry winston-w-4', 'Hatchimals-1', 'Havaianas-w-1', 'HEAD-2', 'HEAD-w-1', 'helena rubinstein-w-1', 'helena rubinstein-w-2', 'Hello Kitty-2', 'Hello Kitty-w-1', 'Heron Preston-1', 'Heron Preston-2', 'Heron Preston-3', 'Hexbug-w-1', 'Hey Dude-w-1', 'HM-1', 'Hogan-1', 'Honeywell-w-1', 'Houston Astros-1', 'Houston Astros-2', 'HP-1', 'HTC-1', 'HUF-2', 'HUF-w-1', 'Hunter-w-1', 'Hyundai-2', 'Hyundai-w-1', 'Ibanez-w-1', 'ICE Watch-w-1', 'ICE Watch-w-2', 'Iced Earth-1', 'IMREN-2', 'IMREN-w-1', 'Incase-1', 'Incipio-2', 'Incipio-w-1', 'INFUSIUM-w-1', 'INSTANTLY AGELESS-1', 'Iron Maiden-1', 'iron man-w-1', 'Issey Miyake-w-1', 'Jabra-w-1', "Jack Daniel's-w-1", 'Jack Jones-w-1', 'Jack Jones-w-3', 'jack wills-w-1', 'jack wills-w-2', 'JACOB CO-3', 'JACOB CO-w-1', 'Jacquemus-w-1', 'Jeep-w-1', 'John Deere-2', 'John Deere-w-1', 'John Deere-w-3', 'Juicy Couture-1', 'Juicy Couture-2', 'Juicy Couture-4', 'Juventus-2', 'Juventus-3', 'JW Anderson-2', 'JW Anderson-w-1', 'Kansas Royals-1', 'Kansas Royals-2', 'Kansas Royals-3', 'Kaporal-2', 'Kaporal-w-1', 'KEEN-1', "Kiehl's-1", 'Kingston-2', 'Kipling-1', 'KNVB-2', 'KNVB-3', 'KOSS-2', 'KTM-1', 'L.O.L. SURPRISE!-1', 'La Martina-2', 'La Martina-w-1', 'Lamborghini-1', 'Leicester City F.C-1', 'Lesmills-w-1', 'LG-2', 'LG-w-1', 'Lilo Stitch-1', 'Links of London-2', 'Links of London-w-1', 'Loewe-1', 'Loewe-w-2', 'Logitech-3', 'Logitech-4', 'Logitech-w-1', 'Logitech-w-2', 'Longchamp-w-1', 'Longchamp-2', 'Los Angeles Dodgers-1', 'Los Angeles Dodgers-2', 'Los Angeles Kings-1', 'Los Angeles Kings-2', 'Luke Combs-1', 'Luke Combs-2', 'Lululemon-2', 'Lyle Scott-2', 'Lyle Scott-w-1', 'M.A.C-1', 'Mammut-2', 'Marcelo Burlon-2', 'Marshall-1', 'Marshall-2', 'Marvel-w-1', 'Max factor-w-1', 'Max factor-w-2', 'MBT-1', 'MCM-1', 'MCM-w-2', 'Metallica-1', 'MIFFY-1', 'MIFFY-2', 'Milwaukee Brewers-1', 'Milwaukee Brewers-2', 'Milwaukee Brewers-3', 'Milwaukee Brewers-4', 'Minesota Twins-1', 'Minesota Twins-2', 'Minesota Twins-3', 'Minnesota wild-1', 'Minnesota wild-2', 'miu miu-1', 'Mizuno-1', 'Mizuno-2', 'MLB-1', 'MLB-2', 'MMS-1', 'Monster Energy-1', 'Monster Energy-2', 'Montreal Canadiens-1', 'Montreal Expos-1', 'Montreal Expos-2', 'Montreal Expos-3', 'moose knuckles-1', 'moose knuckles-2', 'Mophie-2', 'MOTORHEAD-1', 'Motorola-2', 'Movado-1', 'Muhammad Ali-w-1', 'Mulberry-2', 'Nashville Predators-1', 'New Jersey Devils-1', 'New York Islanders-1', 'New York Islanders-2', 'New York Mets-1', 'New York Mets-2', 'New York Rangers-2', 'New York Rangers-3', 'New York Yankees-1', 'New York Yankees-2', 'New York Yankees-3', 'Nirvana-2', 'Nirvana-3', 'Nokia-w-1', 'Nutribullet-w-1', 'Nutribullet-w-2', 'Oakland Athletics-1', 'Oakland Athletics-2', 'Olympique de Marseille-2', 'Olympus-w-1', 'OPI-w-1', 'Ottawa Senators-1', 'Ottawa Senators-2', 'Otter box-2', 'Otter box-w-1', 'Otter box-w-3', 'OXO-2', 'Ozark-2', 'Ozark-w-1', 'Paco Rabanne-2', 'Paco Rabanne-w-1', 'Pandora-1', 'Pandora-2', 'Pandora-w-3', 'PANERAI-1', 'PANERAI-2', 'Paris Saint Germain-1', 'Patagonia-2', 'paul frank-2', 'Paul Shark-1', 'Paul Shark-2', 'Paul Smith-1', 'Paul Smith-2', 'Pearl Izumi-2', 'Pearl Izumi-w-1', 'Philadelphia Phillies-2', 'Philadelphia Phillies-3', 'Philadelphia Phillies-w-1', 'Philipp Plein-w-1', 'Philipp Plein-2', 'Philipp Plein-w-4', 'Phoenix Coyotes-1', 'Phoenix Coyotes-4', 'Piaget-w-1', 'Pinarello-2', 'Pinarello-w-1', 'PING-w-1', 'PINK FLOYD-2', 'PINK FLOYD-3', 'Pittsburgh Penguins-1', 'Pixar-1', 'Pixar-2', 'PJ MASKS-1', 'Plantronics-2', 'Plantronics-w-1', 'Playboy-2', 'Playstation-2', 'Playstation-w-1', 'POCOYO-w-1', 'Pony-2', 'Pony-3', 'PopSockets-1', 'PopSockets-3', 'Portugal-1', 'Power Rangers-2', 'Power Rangers-4', 'Premier League-3', 'Premier League-w-1', 'Premier League-w-2', 'Prince-2', 'Prince-w-1', 'Pro Kennex-2', 'Pro Kennex-w-1', 'PSV Eindhoven-1', 'PSV Eindhoven-w-2', 'Pxg-1', 'RAW-1', 'RB Leipzig-2', 'RCMA-w-1', 'Reebok-2', 'Reebok-3', 'Reebok-w-1', 'Rip Curl-2', 'Rip Curl-4', 'Ritchey-2', 'Ritchey-3', 'Ritchey-w-1', 'ROBO FISH-w-1', 'Roger Vivier-1', 'Roger Vivier-2', 'rosetta stone-1', 'Roxy-1', 'S.H.I.E.L.D.-1', 'S.H.I.E.L.D.-3', 'Salomon-2', 'Salomon-w-1', 'Samantha Thavasa-2', 'Samantha Thavasa-w-3', 'Samsonite-1', 'Samsonite-3', 'San Jose Sharks-1', 'Sanrio-1', 'scooby doo-1', 'scooby doo-w-2', 'Seagate-1', 'Seagate-2', 'Shaun the sheep-w-3', 'Shaun the sheep-w-4', 'Shiseido-1', 'Shure-w-1', 'Skoda-2', 'SLAP CHOP-w-1', 'Slazenger-2', 'Slazenger-w-1', 'Smith Wesson-2', 'Smith Wesson-w-1', 'SONS OF ARTHRITIS-w-1', 'Sony Ericsson-1', 'Sony Ericsson-w-2', 'Speck-2', 'Speck-3', 'Speck-w-1', 'Srixon-1', 'Srixon-2', 'St. Louis Cardinals-1', 'St. Louis Cardinals-2', 'St. Louis Cardinals-4', 'St. Louis Cardinals-w-3', 'stan smith-w-1', 'Stefano Ricci-1', 'Stefano Ricci-3', 'Streamlight-1', 'Streamlight-2', 'Supra-2', 'Supra-w-1', 'Swatch-w-1', 'Swig-2', 'SwitchEasy-1', 'SwitchEasy-w-2', 'Tampa Bay Lightning-1', 'Tampa Bay Lightning-w-2', 'Tampa Bay Rays-2', 'Tampa Bay Rays-w-1', 'Tapout-1', 'TECHNOMARINE-1', 'TECHNOMARINE-w-1', 'THE ALLMAN BROTHERS BAND-2', 'THE ALLMAN BROTHERS BAND-3', 'The Black Crowes-2', 'The Black Crowes-w-1', 'The Horus Heresy-w-1', 'the punisher-1', 'the punisher-2', 'Thomas Sabo-w-1', 'Thomas Sabo-w-2', 'Timberland-2', 'Timberland-w-1', 'Titleist-1', 'Titoni-3', 'Titoni-w-2', 'Toms-w-1', 'Tonino Lamborghini-1', 'Tonino Lamborghini-2', 'Too Faced-w-1', 'Toronto Maple Leafs-1', 'Toronto Maple Leafs-2', 'tory burch-1', 'tory burch-w-2', 'tous-w-1', 'tous-2', 'tous-3', 'Toy Watch-1', 'Travis Scott-2', 'True Religion-2', 'True Religion-w-1', 'TRXTraining-w-1', 'Tudor-1', 'Tudor-w-2', 'U_boat-w-1', 'UAG-1', 'UEFA-2', 'UEFA-3', 'UEFA-w-1', 'Umbro-2', 'Umbro-w-1', 'USA soccer-1', 'USA soccer-2', 'VACHERON CONSTANTIN-1', 'VACHERON CONSTANTIN-w-2', 'Valentino Garavani-1', 'Valentino Garavani-2', 'Valentino Garavani-3', 'Victorias secret-2', 'Victorias secret-w-1', 'Visa-w-1', 'VLONE-2', 'VLONE-w-1', 'VOLBEAT-3', 'VOLBEAT-w-1', 'Volcom-2', 'Volcom-w-1', 'Volkl-2', 'Volkl-w-1', 'West Ham United-1', 'West Ham United-2', 'Whirlpool-w-1', 'Wilson-2', 'Wilson-w-1', 'Wrangler-w-1', 'WWE-2', 'Xmen-2', 'Xmen-w-1', 'Xxio-1', 'Yonex-1', 'Yonex-2', 'Zara-2', 'Zara-w-1', 'Zegna-1', 'Zegna-2', 'Zenith-w-1', 'Zimmermann-w-1', 'Zumba Fitness-2', 'Zumba Fitness-w-1',"Pokemon-1","Audi-w-1","BMW-2","BMW-w-3","Lamborghini-2","MCM-h-1","Reebok-h-4"]
######################################################## FX #########################################
quit_list = ["Maserati-3","Sephora-1","Chicago White Sox-3","Bang Olufsen-w-1","puma-w-1","AS Roma-w-2","Alpinestars-w-3",
             "Aspinal of London-w-2","Big Green Egg-w-2","AFC Ajax-w-1","Shimano-2","Sisley-3","Cincinnati Bengals-1",
             "Charlotte Hornets-1","Alcon-w-2","Charlotte Hornets-w-2","Buffalo Bills-w-2","Detroit Lions-w-1","Denver Nuggets-2",
             "Cartier-w-2","New Era-w-1","nike-6","Samantha Thavasa-2","Def Leppard-w-2"
             ]
D11 = ["Aeronautica Militare-1","Aeronautica Militare-w-2","Baume et Mercier-w-1","Baume et Mercier-2","Beachbody-w-1","Beachbody-2",
       "France-1","France-2","Golds Gym-w-1","Golds Gym-2","Golds Gym-3","Nintendo-w-1","Nintendo-2","Spibelt-1","Spibelt-2","Snow White-1"]
#brand_names = brand_names_fx+brand_names_wew
CLASS_list_ = CLASS_list_fx+CLASS_list_wew+D11
CLASS_list = []
for c in CLASS_list_:
    if c not in quit_list:
        CLASS_list.append(c)
brand_names = []
for c in CLASS_list:
    brand = c.split("-")[0]
    if brand not in brand_names:
        brand_names.append(brand)

print(CLASS_list)
print(len(CLASS_list))
#CLASS_list = None
# brand_names_exist = brand_names1+brand_names2+brand_names3+brand_names4+brand_names5+brand_names6+brand_names7+brand_names8
# for i in brand_names:
#     if i.replace(" ","").lower() in [j.replace(" ","").lower() for j in brand_names_exist]:
#         print("%s is exist"%i)
#split img data
# export_dataset_flag = True

WORKERS_get_class = WORKERS
WORKERS_xml = WORKERS
WORKERS_spilt = WORKERS
WORKERS_gif_mv = WORKERS
WORKERS_md5_mv = WORKERS
WORKERS_not_pair_mv = WORKERS
WORKERS_empty_mv = WORKERS
if be_merged_dir:
    be_merged_dir = "/data01/xu.fx/" + be_merged_dir + "/checked"
src_dir = "/data01/xu.fx/"+main_data_dir+"/checked"
yolo_dataset_dir = "/data02/xu.fx/"+main_data_dir+"/"+yolo_dataset_name+"/"
detect_img_dir = "/data02/xu.fx/"+main_data_dir+"/"+yolo_dataset_name+"/test_detect_img"

empty_dir = src_dir + "_empty"
same_dir = src_dir + "_same_md5"
gif_dir = src_dir + "_gif"
error_dir = src_dir + "_error"
not_pair_dir = src_dir + "_not_pair"
wrong_xml_dir = src_dir + "_wrong_xml"
warning_dir = src_dir + "_warning"
effective_brandname = Manager().list(brand_names)

def merge_data(src_dir,dst_dir):
    print("before merged data info:")
    print("merge to dir file num:", int(len(os.listdir(dst_dir))/2))
    print("be merged dir file num:", int(len(os.listdir(src_dir))/2))
    for file in tqdm(os.listdir(src_dir)):
        shutil.copy(os.path.join(src_dir,file),dst_dir)
    print("\nafter merged data info:")
    print("merge to dir file num:", int(len(os.listdir(dst_dir)) / 2))
    print("be merged dir file num:", int(len(os.listdir(src_dir)) / 2))

def not_pair_mv_func(files):
    check_pair = dict()
    not_pair_num = 0
    xml_num = 0
    for file in tqdm(files):
        if file.split('.')[-1]=='xml':
            xml_num+=1
        file_ = ''
        for i in file.split('.')[:-1]:
            file_ += i
        if file_ not in check_pair:
            check_pair[file_] = 1
        else:
            check_pair[file_] += 1
    total_num = len(files)
    print('total num: ',total_num)
    print('xml num: ',xml_num)
    if xml_num!=int(total_num/2):
        print('xml and pic is not pair')
    else:
        print('xml and pic is pair')
    for key,value in tqdm(check_pair.items()):
        if value>=3:
            not_pair_num += 1
            for file_i in files:
                file_ = ''
                for i in file_i.split('.')[:-1]:
                    file_ += i
                if file_ == key:
                    if not os.path.exists(not_pair_dir):
                        os.mkdir(not_pair_dir)
                    shutil.move(ospathjoin([src_dir, file_i]), not_pair_dir)
                    print("%s is not pair" % file_i)
    print('not_pair_num: ',not_pair_num)
def not_pair_mv(src_dir):
    files = os.listdir(src_dir)
    pool = Pool(processes=WORKERS_not_pair_mv)
    for i in range(0, WORKERS_not_pair_mv):
        files_ = files[i:len(files):WORKERS_not_pair_mv]
        pool.apply_async(not_pair_mv_func, (files_,))
    pool.close()
    pool.join()
def empty_mv_func(files):
    empty_num = 0
    for file_i in tqdm(files):
        if file_i.split('.')[-1] in ['jpg','png','jpeg','JPG','PNG','JPEG']:
            xml_str = ospathjoin([src_dir, file_i[:-(len(file_i.split('.')[-1]))]+'xml'])
            if not os.path.exists(xml_str):
                print(xml_str)
                if not os.path.exists(empty_dir):
                    os.mkdir(empty_dir)
                shutil.move(ospathjoin([src_dir, file_i]), empty_dir)
                print("%s is empty"%file_i)
                empty_num+=1

        if file_i.endswith('.xml'):
            jpg_str = ospathjoin([src_dir, file_i[:-(len(file_i.split('.')[-1]))]+'jpg'])
            png_str = ospathjoin([src_dir, file_i[:-(len(file_i.split('.')[-1]))]+'png'])
            jpeg_str = ospathjoin([src_dir, file_i[:-(len(file_i.split('.')[-1]))]+'jpeg'])
            JPG_str = ospathjoin([src_dir, file_i[:-(len(file_i.split('.')[-1]))]+'JPG'])
            PNG_str = ospathjoin([src_dir, file_i[:-(len(file_i.split('.')[-1]))]+'PNG'])
            JPEG_str = ospathjoin([src_dir, file_i[:-(len(file_i.split('.')[-1]))]+'JPEG'])
            if not os.path.exists(jpg_str) and not os.path.exists(png_str) and not os.path.exists(jpeg_str) and\
                    not os.path.exists(JPG_str) and not os.path.exists(PNG_str) and not os.path.exists(JPEG_str):
                if not os.path.exists(empty_dir):
                    os.mkdir(empty_dir)
                shutil.move(ospathjoin([src_dir, file_i]), empty_dir)
                print("%s is empty"%file_i)
                empty_num+=1
    print("empty_num: ",empty_num)
def empty_mv(src_dir):
    files = os.listdir(src_dir)
    pool = Pool(processes=WORKERS_empty_mv)
    for i in range(0, WORKERS_empty_mv):
        files_ = files[i:len(files):WORKERS_empty_mv]
        pool.apply_async(empty_mv_func, (files_,))
    pool.close()
    pool.join()

def dataset_check(yolo_dataset_dir):
    train_img = yolo_dataset_dir+'/'+'JPEGImages/train/images'
    eval_img = yolo_dataset_dir+'/'+'JPEGImages/eval/images'
    test_detect_img = yolo_dataset_dir + '/' + 'test_detect_img'
    test_img = yolo_dataset_dir + '/' + 'JPEGImages/test/images'
    label_train = yolo_dataset_dir+'/'+'JPEGImages/train/labels'
    label_eval = yolo_dataset_dir + '/' + 'JPEGImages/eval/labels'
    label_test = yolo_dataset_dir + '/' + 'JPEGImages/test/labels'
    test_detect_img_num = len(os.listdir(test_detect_img))
    train_img_num = len(os.listdir(train_img))
    eval_img_num = len(os.listdir(eval_img))
    test_img_num = len(os.listdir(test_img))
    train_img_white_num = len([i for i in os.listdir(train_img) if "WhiteSample" in i])
    eval_img_white_num = len([i for i in os.listdir(eval_img) if "WhiteSample" in i])
    test_img_white_num = len([i for i in os.listdir(test_img) if "WhiteSample" in i])
    label_train_num = len(os.listdir(label_train))
    label_eval_num = len(os.listdir(label_eval))
    label_test_num = len(os.listdir(label_test))
    print("train img and label num: ", train_img_num,label_train_num,"with white sample: ",train_img_white_num)
    print("eval img and label num: ", eval_img_num,label_eval_num,"with white sample: ",eval_img_white_num)
    print("test img and label num: ", test_img_num,label_test_num,"with white sample: ",test_img_white_num)
    print("detect img num: ", test_detect_img_num)
    if train_img_num==label_train_num and eval_img_num==label_eval_num and test_img_num==label_test_num:
        print(bcolors.OKGREEN+"the dataset is all right"+bcolors.ENDC)
def get_brands_and_labels(src_dir):
    xml_paths = [xml_file for xml_file in walk_xml(src_dir)]
    pool = Pool(processes=WORKERS_get_class)
    class_list = Manager().list()
    file_list = Manager().list()
    not_class_list = Manager().list()
    for i in range(0, WORKERS_get_class):
        xmls = xml_paths[i:len(xml_paths):WORKERS_get_class]
        pool.apply_async(get_brands_and_labels_func, (xmls, class_list,file_list,not_class_list,))
    pool.close()
    pool.join()
    brand_list = []
    class_num = {}
    not_class_num = {}
    file_num = {}
    brand_num = {}
    print('in the class analysis phase')
    for cls in tqdm(class_list):
        if cls in class_num:
            class_num[cls] += 1
        else:
            class_num[cls] = 1
        if cls.split('-')[0] in brand_list:
            brand_num[cls.split('-')[0]] += 1
            pass
        else:
            brand_num[cls.split('-')[0]] = 1
            brand_list.append(cls.split('-')[0])
    print('in the file analysis phase')
    for fil in tqdm(file_list):
        if fil in file_num:
            file_num[fil] += 1
        else:
            file_num[fil] = 1

    print('in the not class analysis phase')
    for cls in tqdm(not_class_list):
        if cls in not_class_num:
            not_class_num[cls] += 1
        else:
            not_class_num[cls] = 1

    print('not classes num list:', end=" ")
    for item in sorted(not_class_num, key=lambda a: not_class_num[a], reverse=True):
        print((item, not_class_num[item]), end=" ")
    print(f"\nnot in class num: {len(not_class_num)}")


    brand_list = list(set(brand_list))
    brand_list.sort(key=str.lower)
    print('classes num list:', end=" ")
    for item in sorted(class_num, key=lambda a: class_num[a], reverse=True):
        print((item, class_num[item]), end=" ")
    print("\nclasses num: ", len(class_num))


    print(bcolors.OKGREEN + 'file num list:' + bcolors.ENDC, end=" ")
    for item in sorted(file_num, key=lambda a: file_num[a], reverse=True):
        print(bcolors.OKGREEN + "(%s" % item + ", " + "%d)" % file_num[item] + bcolors.ENDC, end=" ")
    print(bcolors.OKGREEN + "\nfile num: " + bcolors.ENDC, len(file_num))

    print('brand num list:', end=" ")
    brand_list_sort = []
    for item in sorted(brand_num.items(), key=lambda kv: (kv[1], kv[0]), reverse=True):
        print(item, end =" ")
        brand_list_sort.append(item[0])
    print("\nbrand num: ", len(brand_list))
    print("\n")
    print('classes list: ', sorted(class_num,key=str.lower))
    print('brand list: ', brand_list_sort)
    return sorted(class_num,key=str.lower),brand_list
def get_brands_and_labels_func(xml_ps,class_list,file_list,not_class_list):
    for anno_file in tqdm(xml_ps):
        try:
            tree = ET.parse(anno_file)
            root = tree.getroot()
        except:
            continue
        file_list.append(anno_file.split("/")[-1].split("_")[0])
        for obj in root.iter('object'):
            cls = obj.find('name').text
            if cls is None:
                continue
            cls = cls.strip()
            if use_effective_brand:
                if cls.split('-')[0] not in effective_brandname:
                    continue
            if use_class_brand:
                if cls not in CLASS_list:
                    not_class_list.append(cls)
                    print(f"{cls} not in CLASS_list")
                    continue
            class_list.append(cls)

def get_xml_obj_num(anno_file):
    try:
        tree = ET.parse(anno_file)
        root = tree.getroot()
        objs = root.iter('object')
        size = root.find('size')
    except Exception as e:
        print(e)
        objs,size = -1
    return objs,size
def xml2txt(out_file,cls_boxes,size,class_list_sts):
    w = float(size.find('width').text)
    h = float(size.find('height').text)
    box_list = []
    with open(out_file, 'w') as fw:
        for obj in cls_boxes:
            cls = obj[0]
            if cls is None:
                print(out_file,"get None on name")
                continue
            cls = cls.strip()
            if cls not in classes_list:
                continue
            cls_id = classes_list.index(cls)
            xmin, xmax, ymin, ymax = obj[1],obj[2],obj[3],obj[4]
            b = [np.clip(min(xmin, xmax), 0, w), np.clip(max(xmin, xmax), 0, w), np.clip(min(ymin, ymax), 0, h),
                 np.clip(max(ymin, ymax), 0, h)]
            if b not in box_list:
                box_list.append(b)
            else:
                continue
            bb = convert((w, h), b)
            if bb[0] <= 0 or bb[0] >= 1 or bb[1] <= 0 or bb[1] >= 1 or bb[2] <= 0 or bb[3] <= 0:
                print("it's wrong box is", bb)
                print(out_file)
                print(b, bb, w, h)
                print("-" * 60)
                continue

            if bb[1] > 1 or bb[3] > 1 or bb[2] > 1 or bb[0] > 1:
                print("it's wrong box is", bb)
                print(out_file)
                print(b, bb, w, h)
                print("-" * 60)
                continue
            if None in [str(i) for i in bb]:
                print("it's wrong box is", bb)
                print(out_file)
                print(b, bb, w, h)
                print("-" * 60)
                continue
            class_list_sts.append(cls)
            fw.write(str(cls_id) + " " + " ".join([str(a) if a > 0 else str(-a) for a in bb]) + '\n')
def split_data_and_rename_func(src_dir,brand_files,class_list_sts,class_list_sts_total,file_num,file_num_total):
    get_obj_dict = {}
    for i, files in enumerate(brand_files):
        if i%10 == 0:
            print("-"*50,i,"/",len(brand_files))
        random.seed(random_seed)
        random.shuffle(files)
        for file in files:
            file_num_total.append(file)
            xml_file = Path(os.path.join(src_dir,file))
            objs,size = get_xml_obj_num(xml_file)
            if objs == -1:
                continue
            for obj in objs:
                cls = obj.find('name').text
                if cls!=None:
                    class_list_sts_total.append(cls.strip())
        if MAX_NUM_PER_BRAND:
            files = files[:MAX_NUM_PER_BRAND]
        val_num = int(len(files) * train_val_test_ratio[1])
        test_num = int(len(files) * train_val_test_ratio[2])
        for index, file_i in tqdm(enumerate(files)):
            xml_file = Path(os.path.join(src_dir,file_i))
            objs,size = get_xml_obj_num(xml_file)
            if objs == -1:
                continue
            cls_boxes = []
            for obj in objs:
                cls = obj.find('name').text
                if cls == None:
                    continue
                xmlbox = obj.find('bndbox')
                xmin, xmax, ymin, ymax = xmlbox.find('xmin').text, xmlbox.find('xmax').text, \
                                         xmlbox.find('ymin').text, xmlbox.find('ymax').text
                if None in [xmin, xmax, ymin, ymax]:
                    continue
                cls_boxes.append([cls, float(xmin), float(xmax), float(ymin), float(ymax)])
                if cls not in get_obj_dict:
                    get_obj_dict[cls] = 1
                else:
                    get_obj_dict[cls] += 1
            if MAX_OBJ_NUM_PER_BRAND:
                donot_need = 1
                cls_per_img = set([i[0] for i in cls_boxes if i[0] in classes_list])
                for cl in cls_per_img:
                    if get_obj_dict[cl] < MAX_OBJ_NUM_PER_BRAND:
                        donot_need = 0
                if donot_need:
                    print("enough,",file_i,"is donot need")
                    continue
            # annotiaon_file = xml_file
            # fr = open(annotiaon_file, 'rb')
            # data = fr.read()
            # dst_annotion_file = ospathjoin([yolo_dataset_dir, "Annotations",
            #                                 xml_file.parent.name.replace(' ', '').replace("'", "").replace('&', '') + "_" + file_i.replace(
            #                                     '-', '').replace(' ', '').replace('&', '')])
            # cp images
            xml_file_temp = str(xml_file)
            if os.path.exists(xml_file_temp.replace('.xml', '.jpg')):
                img_path = xml_file_temp.replace('.xml', '.jpg')
            elif os.path.exists(xml_file_temp.replace('.xml', '.jpeg')):
                img_path = xml_file_temp.replace('.xml', '.jpeg')
            elif os.path.exists(xml_file_temp.replace('.xml', '.JPG')):
                img_path = xml_file_temp.replace('.xml', '.JPG')
            elif os.path.exists(xml_file_temp.replace('.xml', '.JPEG')):
                img_path = xml_file_temp.replace('.xml', '.JPEG')
            elif os.path.exists(xml_file_temp.replace('.xml', '.png')):
                img_path = xml_file_temp.replace('.xml', '.png')
            elif os.path.exists(xml_file_temp.replace('.xml', '.PNG')):
                img_path = xml_file_temp.replace('.xml', '.PNG')
            else:
                print('Image File Not Found')
                continue
            file_num.append(file_i)
            fimg = open(img_path, 'rb')
            img_data = fimg.read()
            fimg.close()
            eval_txt_path = ospathjoin([yolo_dataset_dir, 'JPEGImages/eval/labels',xml_file.parent.name.replace(' ', '').replace("'", "").replace('&','') + "_" +xml_file.name.replace('-', '').replace(' ', '').replace('&', '').replace(".xml",".txt")])
            if index < val_num:
                if index<detect_num and detect_img_dir!=None:
                    detect_img_path = ospathjoin([detect_img_dir,
                                               xml_file.parent.name.replace(' ', '').replace("'", "").replace('&', '') + "_" +
                                               img_path.split('/')[-1].replace('-', '').replace(' ', '').replace('&','')])

                    with open(detect_img_path, 'wb') as fw:
                        fw.write(img_data)
                    # detect_annotion_file = ospathjoin([detect_img_dir, "Annotations",
                    #                                    xml_file.parent.name.replace(' ', '').replace("'", "").replace('&', '') + "_" +
                    #                                    file_i.replace('-', '').replace(' ', '').replace('&', '')])
                    # annotiaon_file = xml_file
                    # fr = open(annotiaon_file, 'rb')
                    # data = fr.read()
                    # with open(detect_annotion_file, 'wb') as fw:
                    #     fw.write(data)

                dst_img_path = ospathjoin([yolo_dataset_dir, 'JPEGImages/eval/images',
                                           xml_file.parent.name.replace(' ', '').replace("'", "").replace('&', '') + "_" +
                                           img_path.split('/')[-1].replace('-', '').replace(' ', '').replace('&', '')])
                with open(dst_img_path, 'wb') as fw:
                    fw.write(img_data)
                xml2txt(eval_txt_path,cls_boxes,size,class_list_sts)

            elif index>=val_num and index<(val_num+test_num):
                dst_img_path = ospathjoin([yolo_dataset_dir, 'JPEGImages/test/images',
                                           xml_file.parent.name.replace(' ', '').replace("'", "").replace('&',
                                                                                                          '') + "_" +
                                           img_path.split('/')[-1].replace('-', '').replace(' ', '').replace('&', '')])
                with open(dst_img_path, 'wb') as fw:
                    fw.write(img_data)
                test_txt_path = eval_txt_path.replace('eval', 'test')
                xml2txt(test_txt_path, cls_boxes, size, class_list_sts)

            else:
                dst_img_path = ospathjoin([yolo_dataset_dir, 'JPEGImages/train/images',
                                           xml_file.parent.name.replace(' ', '').replace("'", "").replace('&', '') + "_" +
                                           img_path.split('/')[-1].replace('-', '').replace(' ', '').replace('&', '')])
                with open(dst_img_path, 'wb') as fw:
                    fw.write(img_data)
                train_txt_path = eval_txt_path.replace('eval', 'train')
                xml2txt(train_txt_path, cls_boxes, size, class_list_sts)
def split_data_and_rename(src_dir):

    if detect_img_dir:
        detect_dir = Path(detect_img_dir)
        check_dir(detect_dir)
    yolo_dataset_dir_path = Path(yolo_dataset_dir)
    check_dir(yolo_dataset_dir_path)
    check_dir(yolo_dataset_dir_path / "JPEGImages/train/images")
    check_dir(yolo_dataset_dir_path / "JPEGImages/eval/images")
    check_dir(yolo_dataset_dir_path / "JPEGImages/test/images")
    check_dir(yolo_dataset_dir_path / "JPEGImages/train/labels")
    check_dir(yolo_dataset_dir_path / "JPEGImages/eval/labels")
    check_dir(yolo_dataset_dir_path / "JPEGImages/test/labels")
    brand_files = {}
    files = os.listdir(src_dir)
    for f in files:
        if f.split(".")[-1]=="xml":
            if f.find("_") != -1:
                brand = f.split("_")[0]
                if brand not in brand_files:
                    brand_files[brand] = []
                    brand_files[brand].append(f)
                else:
                    brand_files[brand].append(f)
            else:
                if "other" not in brand_files:
                    brand_files["other"] = []
                else:
                    brand_files["other"].append(f)
    brand_lists = []
    for k, v in brand_files.items():
        brand_lists.append(v)
    all_nums = int(len(files)/2)
    print("all Datasets file num is: ", all_nums)
    val_nums = int(all_nums * train_val_test_ratio[1])
    test_nums = int(all_nums * train_val_test_ratio[2])
    print("train file num is: ", all_nums - val_nums - test_nums)
    print("val file num is: ", val_nums)
    print("test file num is: ", test_nums)
    print("detect file num is: ", detect_num)

    WORKERS_spilt_ = WORKERS_spilt
    if len(brand_lists) < WORKERS_spilt:
        WORKERS_spilt_ = len(brand_lists)
    file_num = Manager().list()
    class_list_sts = Manager().list()
    file_num_total = Manager().list()
    class_list_sts_total = Manager().list()
    #get_obj_dict = Manager().dict()
    pool = Pool(processes=WORKERS_spilt_)
    for i in range(0, WORKERS_spilt_):
        xmls = brand_lists[i:len(brand_lists):WORKERS_spilt_]
        pool.apply_async(split_data_and_rename_func, (src_dir, xmls,class_list_sts,class_list_sts_total,file_num,file_num_total,))
    pool.close()
    pool.join()

    #print(get_obj_dict)
    print("all labels: ", classes_list)
    print("all labels's nums: ", len(classes_list))
    assert len(classes_list) == len(set(classes_list)), "reapeat labels error."

    file_num_dict = dict()
    for file in file_num:
        if len(file.split('_')) <= 1:
            continue
        mid = file.split('_')[0]
        if mid not in file_num_dict:
            file_num_dict[mid] = 1
        else:
            file_num_dict[mid] += 1

    file_num_dict_total = dict()
    for file in file_num_total:
        if len(file.split('_')) <= 1:
            continue
        mid = file.split('_')[0]
        if mid not in file_num_dict_total:
            file_num_dict_total[mid] = 1
        else:
            file_num_dict_total[mid] += 1

    brand_names = set()
    check_brand = dict()
    check_label = dict()
    check_brand_total = dict()
    check_label_total = dict()

    for name_i in classes_list:
        bname = name_i.split('-')[0]
        brand_names.add(bname)

    res = list(brand_names)
    res.sort(key=str.lower)
    print("brand name: ", res)
    print("brand num: ", len(brand_names))
    print("total object num:", len(class_list_sts))
    for cls_i in class_list_sts:
        if cls_i not in check_label:
            check_label[cls_i] = 1
        else:
            check_label[cls_i] += 1
        bname = cls_i.split('-')[0]
        if bname not in check_brand:
            check_brand[bname] = 1
        else:
            check_brand[bname] += 1

    for cls_i in class_list_sts_total:
        if cls_i not in check_label_total:
            check_label_total[cls_i] = 1
        else:
            check_label_total[cls_i] += 1
        bname = cls_i.split('-')[0]
        if bname not in check_brand_total:
            check_brand_total[bname] = 1
        else:
            check_brand_total[bname] += 1

    if export_data_info_csv:
        pd_label = pd.DataFrame(check_label, index=["dataset_style_num"]).T
        pd_brand = pd.DataFrame(check_brand, index=["dataset_brand_num"]).T
        pd_file_num = pd.DataFrame(file_num_dict, index=["dataset_file_num"]).T

        pd_label_total = pd.DataFrame(check_label_total, index=["total_style_num"]).T
        pd_brand_total = pd.DataFrame(check_brand_total, index=["total_brand_num"]).T
        pd_file_num_total = pd.DataFrame(file_num_dict_total, index=["total_file_num"]).T

        pd_label_merge = pd.concat([pd_label_total,pd_label], axis=1)#.fillna(0, inplace=True)
        pd_brand_merge = pd.concat([pd_brand_total, pd_brand], axis=1)#.fillna(0, inplace=True)
        pd_file_merge = pd.concat([pd_file_num_total, pd_file_num], axis=1)#.fillna(0, inplace=True)

        pd_label_merge.to_csv("./data_info/%s_label_info.csv" % yolo_dataset_name.replace("yolo_dataset_", ""))
        pd_brand_merge.to_csv("./data_info/%s_brand_info.csv" % yolo_dataset_name.replace("yolo_dataset_", ""))
        pd_file_merge.to_csv("./data_info/%s_file_num_info.csv" % yolo_dataset_name.replace("yolo_dataset_", ""))

    print("checkout_brand", check_brand.keys())
    print("this dataset has brands:", len(list(check_brand.keys())))
    # assert len(list(check_brand.keys())) == len(res)
    # for key, value in check_brand.items():
    #     print("brand name : {}, num: {}".format(key, value))
    #     if value < 20:
    #         print("{} is in trouble.".format(key))
    #     else:
    #         pass
# def makeyolodir(voc_dir):
#     train_label_path = os.path.join(voc_dir, 'JPEGImages/train/labels/')
#     check_dir(train_label_path)
#     val_label_path = train_label_path.replace('train', 'eval')
#     check_dir(val_label_path)
#     test_label_path = train_label_path.replace('train', 'test')
#     check_dir(test_label_path)
#     return
def walk_xml(xml_dir):
    for root, dirs, files in os.walk(xml_dir, topdown=False):
        for name in files:
            xml_str = os.path.join(root, name)
            post_str = os.path.splitext(xml_str)[-1]
            if post_str == ".xml":
                yield xml_str
    return
# def get_xml(xml_dir):
#     for xml_file in os.listdir(xml_dir):
#         xml_str = os.path.join(xml_dir, xml_file)
#         post_str = os.path.splitext(xml_str)[-1]
#         if post_str == ".xml":
#             yield xml_str
#         else:
#             pass
#     return
def convert(size, box):
    x = ((box[0] + box[1]) / 2.0) / size[0]
    y = ((box[2] + box[3]) / 2.0) / size[1]
    w = (box[1] - box[0]) / size[0]
    h = (box[3] - box[2]) / size[1]
    return (x, y, w, h)
def wrong_xml_mv(src_dir):
    files = [file_xml for file_xml in walk_xml(src_dir)]
    pool = Pool(processes=WORKERS_xml)
    wrong_list = Manager().list()
    for i in range(0, WORKERS_xml):
        xmls = files[i:len(files):WORKERS_xml]
        pool.apply_async(wrong_xml_mv_func, (xmls,wrong_list))
    pool.close()
    pool.join()
    print("wrong_num: ",len(wrong_list))
def wrong_xml_mv_func(xml_ps,wrong_list):
    #print(len(xml_ps))
    for anno_file in tqdm(xml_ps):
        try:
            root = ET.parse(anno_file).getroot()
        except:
            if not os.path.exists(wrong_xml_dir):
                os.mkdir(wrong_xml_dir)
            wrong_list.append(anno_file)
            shutil.move(anno_file, wrong_xml_dir)
            print("find wrong xml: ", anno_file.split('/')[-1])

def add_white_sample_func(yolo_dataset_dir,white_sample_list):
    train_img = yolo_dataset_dir + '/' + 'JPEGImages/train/images'
    eval_img = yolo_dataset_dir + '/' + 'JPEGImages/eval/images'
    test_img = yolo_dataset_dir + '/' + 'JPEGImages/test/images'
    label_train = yolo_dataset_dir + '/' + 'JPEGImages/train/labels'
    label_eval = yolo_dataset_dir + '/' + 'JPEGImages/eval/labels'
    label_test = yolo_dataset_dir + '/' + 'JPEGImages/test/labels'
    #print(white_sample_dir)
    #white_sample_list = os.listdir(white_sample_dir)
    white_sample_num = len(white_sample_list)
    train_white_num = int(white_sample_num * train_val_test_ratio[0])
    eval_white_num = int(white_sample_num * train_val_test_ratio[1])
    test_white_num = white_sample_num - train_white_num - eval_white_num
    for i in tqdm(range(white_sample_num)):
        if not is_img(white_sample_list[i]):
            continue
        if i < test_white_num:
            shutil.copy(white_sample_list[i],
                        os.path.join(test_img, "checked_WhiteSample_" + white_sample_list[i].name))
            with open(os.path.join(label_test, "checked_WhiteSample_" + white_sample_list[i].name[:-(
                    len(white_sample_list[i].name.split('.')[-1]))] + 'txt'), 'w') as f:
                pass
        elif i < test_white_num + eval_white_num:
            shutil.copy(white_sample_list[i],
                        os.path.join(eval_img, "checked_WhiteSample_" + white_sample_list[i].name))
            with open(os.path.join(label_eval, "checked_WhiteSample_" + white_sample_list[i].name[:-(
                    len(white_sample_list[i].name.split('.')[-1]))] + 'txt'), 'w') as f:
                pass
        else:
            shutil.copy(white_sample_list[i],
                        os.path.join(train_img, "checked_WhiteSample_" + white_sample_list[i].name))
            with open(os.path.join(label_train, "checked_WhiteSample_" + white_sample_list[i].name[:-(
                    len(white_sample_list[i].name.split('.')[-1]))] + 'txt'), 'w') as f:
                pass

def add_white_sample(yolo_dataset_dir,white_sample_dir_list,WHITE_SAMPLE_COUNT):

    image_list_total = []
    for white_sample_dir in white_sample_dir_list:
        white_sample_list = os.listdir(white_sample_dir)
        if os.path.isdir(os.path.join(white_sample_dir,white_sample_list[0])):
            for dir in white_sample_list:
                white_sample_dir_ = os.path.join(white_sample_dir,dir)
                image_list_total += [p for p in Path(white_sample_dir_).rglob('*.*')]
        else:
            image_list_total += [p for p in Path(white_sample_dir).rglob('*.*')]
    random.shuffle(image_list_total)
    print("white samples total:",len(image_list_total))
    print("we need:",WHITE_SAMPLE_COUNT)
    image_list_total = image_list_total[:WHITE_SAMPLE_COUNT]
    add_white_sample_func(yolo_dataset_dir, image_list_total)

if show_data_info:
    if be_merged_dir:
        print("-" * 20 + "merge data start" + "-" * 20)
        merge_data(be_merged_dir, src_dir)
        print("-" * 20 + "merge data end" + "-" * 20)
    print("-"*20+"wrong xml search start"+"-"*20)
    #wrong_xml_mv(src_dir)
    print("-"*20+"wrong xml search end"+"-"*20)

    print("-"*20+"empty search start"+"-"*20)
    #empty_mv(src_dir)
    print("-"*20+"empty search end"+"-"*20)

    print("-" * 20 + "label & brand search start" + "-" * 20)
    class_list, _ = get_brands_and_labels(src_dir)
    print("-" * 20 + "label & brand search end" + "-" * 20)
else:
    if be_merged_dir:
        print("-" * 20 + "merge data start" + "-" * 20)
        merge_data(be_merged_dir, src_dir)
        print("-" * 20 + "merge data end" + "-" * 20)

    print("-"*20+"wrong xml search start"+"-"*20)
    #wrong_xml_mv(src_dir)
    print("-"*20+"wrong xml search end"+"-"*20)

    print("-"*20+"not pair search start"+"-"*20)
    #not_pair_mv(src_dir)
    print("-"*20+"not pair search end"+"-"*20)

    print("-"*20+"empty search start"+"-"*20)
    empty_mv(src_dir)
    print("-"*20+"empty search end"+"-"*20)

    print("-"*20+"label & brand search start"+"-"*20)
    if CLASS_list:
        classes_list = CLASS_list
        print("use defined:",classes_list)
        print(len(classes_list))
    else:
        classes_list, _ = get_brands_and_labels(src_dir)
    print("-"*20+"label & brand search end"+"-"*20)


    print("-"*20+"split data and rename start"+"-"*20)
    split_data_and_rename(src_dir)
    print("-" * 20 + "split data and rename start" + "-" * 20)

    if white_sample_dir_list:
        for white_sample_dir, num in white_sample_dir_list.items():
            print("-" * 20 + "add white sample start" + "-" * 20)
            add_white_sample(yolo_dataset_dir,[white_sample_dir],num)
            print("-" * 20 + "add white sample end" + "-" * 20)

    print("-"*20+"dataset check start"+"-"*20)
    dataset_check(yolo_dataset_dir)
    print("-"*20+"dataset check end"+"-"*20)
