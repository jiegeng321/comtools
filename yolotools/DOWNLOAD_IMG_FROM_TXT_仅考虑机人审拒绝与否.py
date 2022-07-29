#!/usr/local/bin/python3
# -*- coding:utf-8 -*-
#total brand = ['jack_wills', 'puma', 'los_angeles_lakers', 'harley_davidson', 'tods', 'ping', 'timberland', 'afc_ajax', 'coogi', 'breeze_smoke', 'san_jose_sharks', 'led_lenser', 'pxg', 'prince', 'skoda', 'miffy', 'fendi', 'rb_leipzig', 'rolex', 'versace', 'srixon', 'lyle_scott', 'bose', 'anaheim_ducks', 'jacksonville_jaguars', 'comme_des_garcons', 'jim_beam', 'dallas_cowboys', 'bitdefender', 'detroit_tigers', 'jacob_co', 'west_ham_united', 'fred_perry', 'shopkins', 'fingerlings', 'moose_knuckles', 'baby_shark', 'rimowa', 'toppik', 'oxo', 'dior', 'memphis_grizzlies', 'opi', 'estee_lauder', 'vlone', 'cnd', 'ariat', 'head_shoulders', 'flexfit', 'pixar', 'death_wish_coffee_co', 'black_widow', 'coach', 'ariel', 'portland_trail_blazers', 'alexander_wang', 'phoenix_suns', 'cadillac', 'amiri', 'billabong', 'phoenix_coyotes', 'davidoff', 'sennheiser', 'houston_astros', 'romain_jerome', 'american_eagle', 'playboy', 'calvin_klein', 'volcom', 'dunhill', 'the_north_face', 'vacheron_constantin', 'beretta', 'mulberry', 'new_york_knicks', 'burts_bees', 'visa', 'columbus_blue_jackets', 'christian_audigier', '7up', 'aspinal_of_london', 'bobbi_brown', 'stussy', 'leicester_city_f.c', 'speck', 'miami_dolphins', 'ducati', 'nirvana', 'bang_olufsen', 'los_angeles_clippers', 'levis', 'nickelodeon', 'tennessee_titans', 'manchester_city', 'samantha_thavasa', 'paul_frank', 'lg', 'everlast', 'paul_shark', 'new_balance', 'lamborghini', 'diablo', 'fjallraven', 'nba', 'fuji_film', 'winnipeg_jets', 'vivienne_westwood', 'ecco', 'ottawa_senators', 'hugo_boss', 'copper_fit', 'moncler', 'philadelphia_76ers', 'goo_jit_zu', 'incase', 'overwatch', 'skin79', 'bmc_racing', 'hollister_co', 'los_angeles_chargers', 'swatch', 'abercrombie_fitch', 'nfl', 'cisco', 'golden_state_warriors', 'pittsburgh_penguins', 'nutribullet', 'lol_surprise', 'st._louis_blues', 'batman', 'denver_broncos', 'spyderco', 'washington_capitals', 'always', 'umbro', 'golden_goose', 'carolina_herrera', 'valentino_garavani', 'columbia', 'awt', 'black_panther', 'toms', 'dc_shoes', 'cleveland_browns', 'san_antonio_spurs', 'los_angeles_rams', 'herbal_essences', 'jack_daniels', 'bestway', 'cleveland_cavaliers', 'atlanta_hawks', 'gillette', 'manolo_blahnik', 'as_roma', 'robo_alive', 'addicted', 'sephora', 'armani', 'specialized', 'crabs_adjust_humidity', 'hamann', 'detroit_pistons', 'dewalt', 'philadelphia_phillies', 'jw_anderson', 'jimmy_choo', 'vegas_golden_knights', 'colorado_avalanche', 'bjorn_borg', 'sons_of_arthritis', 'hearthstone', 'huf', 'movado', 'st._louis_cardinals', 'celine', 'gucci', 'patagonia', 'bubble_guppies', 'furla', 'zimmermann', 'lancome', 'swig', 'urban_decay', 'jack_wolfskin', 'toronto_blue_jays', 'bosch', 'minnesota_vikings', 'supreme', 'texas_rangers', 'fischer', 'iron_maiden', 'zegna', 'new_york_rangers', 'belkin', 'fox_head', 'new_york_jets', 'philipp_plein', 'luke_combs', 'sacramento_kings', 'los_angeles_kings', 'the_loud_house', 'mms', 'ess', 'cards_against_humanity', 'seattle_seahawks', 'lindberg', 'premier_league', 'aquabeads', 'hamilton', 'duracell', 'coca_cola', 'babyliss', 'supra', 'led_zeppelin', 'chopard', 'jaeger_lecoultre', 'glashutte_original', 'muhammad_ali', 'balmain', 'milwaukee_brewers', 'bill_blass', 'tech_deck', 'thomas_sabo', 'brabus', 'baby_phat', 'compaq', 'alfar_romeo', 'buffalo_sabres', 'boston_celtics', 'kaporal', 'disney', 'hp', 'eotech', 'zumba_fitness', 'red_bull', 'roxy', 'bally', 'bulova', 'the_horus_heresy', 'new_jersey_devils', 'max_factor', 'heroes_of_the_storm', 'breitling', 'gstar_raw', 'toronto_raptors', 'blackberry_smoke', 'doctor_strange', 'kipling', 'mammut', 'yeti', 'cacharel', 'ecko', 'fc_barcelona_fcb', 'kansas_city_chiefs', 'benetton', 'paul_smith', 'bell_ross', 'montreal_canadiens', 'hublot', 'tag_heuer', 'salomon', 'bright_bugz', 'kappa', 'mcm', 'longines', 'bunchems', 'jeep', 'game_boy', 'htc', 'benefit', 'sisley', 'taylormade', 'oakland_athletics', 'issey_miyake', 'daiwa', 'franco_moschino', 'milwaukee_bucks', 'carolina_panthers', 'instantly_ageless', 'captain_america', 'caterpillar', 'jabra', 'clinique', 'washington_redskins', 'stefano_ricci', 'hermes', 'blackhawk', 'ktm', 'panerai', 'power_rangers', 'bentley', 'mercedes_benz', '511_tactical', 'hatchimals', 'avengers', 'feyenoord', 'tissot', 'hexbug', 'alexander_mcqueen', 'creative', 'marshall', 'epson', 'england', 'pearl_izumi', 'footjoy', 'usa', 'iwc', 'guess', 'orlando_magic', 'st_dupont', 'titoni', 'game_of_thrones', 'keen', 'tapout', 'concord', 'buffalo_bills', 'plantronics', 'fc_bayern_munchen', 'monster_energy', 'shure', 'los_angeles_dodgers', 'hid_global', 'new_york_giants', 'bakugan', 'juul', 'ado_den_haag', 'new_era', 'kenzo', 'breguet', 'irobot', 'cleveland_indians', 'land_rover', 'wwe', 'louis_vuitton', 'camelbak', 'porsche', '3m', 'xmen', 'guitar_hero', 'san_francisco_49ers', 'green_bay_packers', 'marvel', 'ugg', 'indiana_pacers', 'bottega_veneta', 'zigzag', 'cincinnati_reds', 'blues_clues', 'the_fairly_oddparents', 'carters', 'citizen', 'hogan', 'clarisonic', 'harry_potter', 'dell', 'boston_bruins', 'rip_curl', 'oklahoma_city_thunder', 'cazal', 'blaze_and_the_monster_machines', 'uboat', 'merrell', 'elementcase', 'swarovski', 'tottenham_hotspur', 'canon', 'miu_miu', 'carmex', 'new_york_yankees', 'benq', 'new_orleans_pelicans', 'infusium', 'motorhead', 'hey_dude', 'motorola', 'world_of_warcraft', 'new_orleans_saints', 'jacquemus', 'sk_ii', 'goyard', 'elizabeth_arden', 'philadelphia_flyers', 'volbeat', 'pink_floyd', 'arizona_diamondbacks', 'iced_earth', 'chicago_bulls', 'the_black_crowes', 'prada', 'fullips', 'montblanc', 'bontrager', 'braun', 'too_faced', 'hennessy', 'zelda', 'wrangler', 'switch', 'pocoyo', 'alpinestars', 'nasa', 'pro_kennex', 'baltimore_ravens', 'enve', 'mophie', 'aquascutum', 'durex', 'david_yurman', 'franck_muller', 'the_allman_brothers_band', 'skylanders', 'knvb', 'big_green_egg', 'callaway', 'dolce_gabbana', 'imren', 'nokia', 'pokemon', 'pinko', 'jack_jones', 'agnes_b', 'calgary_flames', 'efest', 'ice_watch', 'olympique_marseille', 'gopro', 'zenith', 'longchamp', 'liverpool_fc', 'toronto_maple_leafs', 'anna_sui', 'grado', 'new_york_mets', 'psv', 'van_cleef_arpels', 'fender', 'ferrari', 'foreo', 'acer', 'anne_klein', 'kansas_royals', 'hurley', 'houston_texans', 'edmonton_oilers', 'technomarine', 'arsenal', 'cartier', 'diadora', 'koss', 'magpul', 'corum', 'juventus', 'scooby_doo', 'true_religion', 'marc_jacobs', 'boston_red_sox', 'ac_dc', 'barbie', 'trx_training', 'baltimore_orioles', 'dettol', 'zippo', 'bvlgari', 'tampa_bay_buccaneers', 'travis_scott', 'logitech', 'oakland_raiders', 'pampers', 'allsaints', 'audioquest', 'giro', 'griffin', 'havaianas', 'mac', 'shimmer_and_shine', 'rado', 'cole_haan', 'martin_co', 'chelsea', 'givenchy', 'new_england_patriots', 'blu', 'cleveland_golf', 'bmw', 'kiehls', 'deadpool', 'chanel', 'converse', 'sony_ericsson', 'olympus', 'piaget', 'dsquared2', 'lesmills', 'off_white', 'call_of_duty_ghosts', 'kingston', 'minesota_twins', 'scotty_cameron', 'chicago_bears', 'google', 'betty_boop', 'a_cold_wall', 'daniel_roth', 'arizona_cardinals', 'patek_philippe', 'jurlique', 'beats_by_drdre', 'honda', 'cannondale', 'dooney_bourke', 'links_of_london', 'frida_kahlo', 'forever_21', 'azzaro', 'switcheasy', 'christian_louboutin', 'giuseppe_zanotti', 'jbl', 'chaumet', 'michael_kors', 'montreal_expos', 'utah_jazz', 'gap', 'alberta_ferretti', 'heron_preston', 'maserati', 'chloe', 'canada_goose', 'bugatti_veyron', 'smith_wesson', 'mizuno', 'tonino_lamborghini', 'head', 'volkl', 'pandora', 'care_bears', 'gant', 'harry_winston', 'tide', 'san_diego_padres', 'paco_rabanne', 'roor', 'slap_chop', 'detroit_red_wings', 'esp', 'garmin', 'lululemon', 'samsonite', 'ibanez', 'the_killers', 'tory_burch', 'butterfly', 'nixon', 'superdry', 'colgate', 'cincinnati_bengals', 'nashville_predators', 'r4', 'cheap_monday', 'atlanta_bravs', 'kate_spade', 'helena_rubinstein', 'paris_saint_germain', 'hunter', 'blackberry', 'dumbo', 'guerlain', 'roger_dubuis', 'desigual', 'brioni', 'dr_martens', 'barbour', 'hm', 'hyundai', 'blancpain', 'chi', 'grumpy_cat', 'honeywell', 'elvis_presley', 'tous', 'adobe', 'wallykazam', 'philadelphia_eagles', 'apple', 'alcon', 'kenan_and_kel', 'facebook', 'san_francisco_giants', 'arcteryx', 'birkenstock', 'minnesota_wild', 'grand_seiko', 'audemars_piguet', 'skullcandy', 'diesel', 'bunch_o_ballons', 'pittsburgh_steelers', 'houston_rockets', 'shu_uemura', 'salvatore_ferragamo', 'def_leppard', 'mlb', 'dragon_ball', 'ritchey', 'escada', 'hydro_flask', 'guardians_of_the_galaxy', 'carhartt', 'games_workshop', 'bape', 'lacoste', 'gibson', 'a_lange_sohne', 'bed_head', 'shimano', 'stan_smith', 'berluti', 'belstaff', 'tudor', 'brooklyn_nets', 'dallas_mavericks', 'c1rca', 'gazelle', 'lego', 'destiny', 'marlboro', 'ed_hardy', 'charlotte_hornets', 'pony', 'chicago_cubs', 'chicago_white_sox', 'anaheim_angels', 'ellesse', 'john_deere', 'fila', 'detroit_lions', 'daniel_wellington', 'daddario', 'ergobaby', 'new_york_islanders', 'ghd', 'reebok', 'monchhichi', 'asos', 'audi', 'chevron', 'biotherm', 'the_punisher', 'schwarzkopf', 'sanrio', 'maui_jim', 'casio', 'palm_angels', 'minnesota_timberwolves', 'shaun_the_sheep', 'pinarello', 'xxio', 'omega', 'oral_b', 'vancouver_canucks', 'carolina_hurricanes', 'florida_panthers', 'amiibo', 'cath_kidston', 'under_armour', 'denver_nuggets', 'cummins', 'furminator', 'mbt', 'blizzard', '3t', 'indianapolis_colts', 'rcma', 'streamlight', 'whirlpool', 'slazenger', 'starcraft', 'bushnell', 'tampa_bay_rays', 'zara', 'maybelline', 'graham', 'coty', 'juicy_couture', 'manchester_united', 'bioderma', 'iron_man', 'clarins', 'fossil', 'kobe', 'seagate', 'brut', 'tiffany_co', 'chicago_blackhawks', 'palace', 'babolat', 'phiten', 'raw', 'vans', 'dfb', 'miami_heat', 'ben_jerrys', 'robo_fish', 'burberry', 'uefa', 'yonex', 'bugslock', 'incipio', 'dyson', 'gildan', 'shield', 'aussiebum', 'adidas', 'loewe', 'la_martina', 'titleist', 'conair', 'audio_technica', 'fear_of_god_essentials', 'oakley', 'usa_basketball', 'the_rolling_stones', 'florida_marlins', 'brazil', 'girard_perregaux', 'wilson', 'ulysse_nardin', 'rayban', 'evisu', 'playstation', 'portugal', 'ysl', 'bvb', 'cluse', 'eos', 'l_oreal', 'washington_wizards', 'bebe', 'fifa', 'fitbit', 'metallica', 'balenciaga', 'pantene', 'asics', 'victorias_secret', 'shiseido', 'atlanta_falcons', 'chrome_hearts', 'ralph_lauren', 'dkny', 'toy_watch', 'atletico_de_madrid', 'roger_vivier', 'tampa_bay_lightning', 'ozark', 'uag', 'popsockets', 'cwc', 'western_digital', 'hello_kitty', 'nike', 'dean_guitar', 'crocs', 'lilo_stitch', 'tommy_hilfiger', 'marcelo_burlon', 'crumpler', 'dhc', 'grenco_science', 'dallas_stars', 'rosetta_stone', 'chevrolet', 'akg_by_harmon', 'pj_masks', 'otter_box', 'beautyblender']

from pathlib import Path

import requests

from comfunc.funcxml import readxml
import cv2
import random
from comfunc.print_color import bcolors
import os
import shutil
from comfunc.check import check_dir
import ast
txt_paths = ["/data01/xu.fx/dataset/NEW_RAW_INCREASE_DATA/WHOLEE_ONLINE_TXT_DATA/wholee7月5号_7月20日.txt",
]
'''
"/data01/xu.fx/dataset/NEW_RAW_INCREASE_DATA/FORDEAL_ONLINE_TXT_DATA/5月1日_5月31日.txt"
"/data01/xu.fx/dataset/NEW_RAW_INCREASE_DATA/FORDEAL_ONLINE_TXT_DATA/0210-0219.txt",
    "/data01/xu.fx/dataset/NEW_RAW_INCREASE_DATA/FORDEAL_ONLINE_TXT_DATA/0220-0228.txt",
    "/data01/xu.fx/dataset/NEW_RAW_INCREASE_DATA/FORDEAL_ONLINE_TXT_DATA/0301-0309.txt",
    "/data01/xu.fx/dataset/NEW_RAW_INCREASE_DATA/FORDEAL_ONLINE_TXT_DATA/0310-0319.txt",
    "/data01/xu.fx/dataset/NEW_RAW_INCREASE_DATA/FORDEAL_ONLINE_TXT_DATA/0320-0329.txt",
    "/data01/xu.fx/dataset/NEW_RAW_INCREASE_DATA/FORDEAL_ONLINE_TXT_DATA/0401-0409.txt",
    "/data01/xu.fx/dataset/NEW_RAW_INCREASE_DATA/FORDEAL_ONLINE_TXT_DATA/0501-0509.txt",
'''

#txt_paths = txt_paths[::-1]
dst_dir = "/data01/xu.fx/dataset/NEW_RAW_INCREASE_DATA/wholee_for_logo_0725"

total_brand = ['alexander_wang','Hogan','reebok','oakley','umbro','mulberry','dior','christian_audigier','zelda','hamilton',
               'aspinal_of_london','c1rca','coogi','blizzard']
need_brand = {}
for i in total_brand:
    need_brand[i] = 10000

need_brand = {}
donot_need_brand = ['']#['hello_kitty', 'jeep', 'salvatore_ferragamo', 'longines', 'van_cleef_arpels', 'casio', 'playboy', 'prada', 'tory_burch', 'fila', 'mlb', 'versace', 'new_balance', 'nike', 'rolex', 'converse', 'armani', 'franco_moschino', 'miu_miu', 'valentino_garavani', 'under_armour', 'calvin_klein', 'puma', 'vans', 'balenciaga', 'chanel', 'tommy_hilfiger', 'asics', 'supreme', 'patek_philippe', 'omega', 'lacoste', 'hugo_boss', 'louis_vuitton', 'swarovski', 'levis', 'chloe', 'mcm', 'hermes', 'michael_kors', 'moncler', 'loewe', 'the_north_face', 'cartier', 'ralph_lauren', 'alexander_mcqueen', 'bottega_veneta', 'coach', 'mercedes_benz', 'philipp_plein', 'juventus', 'canada_goose', 'celine', 'fendi', 'gucci', 'guess', 'adidas', 'vacheron_constantin', 'zara', 'givenchy', 'christian_louboutin', 'jimmy_choo', 'burberry', 'tiffany_co', 'bape', 'balmain', 'bvlgari', 'reebok', 'fc_barcelona_fcb', 'hublot', 'ellesse', 'panerai', 'lego', 'iwc', 'nba', 'timberland', 'porsche', 'fossil', 'citizen', 'ugg', 'nasa', 'stussy', 'tissot', 'bally', 'pandora', 'audemars_piguet']
other_brand_num = 10000
auto_result_filter = "Accept"#"Reject"# or "Accept"
final_result_filter = "Reject"#"Reject"# or "Reject"

get_brand = {}
data = []
for txt_path in txt_paths:
    with open(txt_path, "r") as f:
        print(txt_path)
        data += f.readlines()
print("total lines :",len(data))
print("need brand :",need_brand)
downloaded_images = 0
for index,line in enumerate(data[:]):
    downloaded_per_list = 0
    dict_brand = ast.literal_eval(line)
    #if dict_brand["finalCheckResult"]=="Reject":#Reject
    img_list = dict_brand["imageCommodityData"]
    #print(index,":",img_list)
    new_get = 0
    for img in img_list:
        try:
            if not ("autoCheckResult" in img and "finalCheckResult" in img):
                print(index,"some img no auto or human result")
                
                continue
            print(img)
            auto_result = img["autoCheckResult"]
            final_result = img["finalCheckResult"]

            if (auto_result == auto_result_filter or auto_result_filter == None) \
                    and (final_result == final_result_filter or final_result_filter==None):
                    #and "侵权/品牌" in img["finalTagHit"]:#ruleHit
                #print(img)
                if "textData" not in img or "finalTagHit" not in img or "ruleHit" not in img: continue
                url = img["textData"]
                if final_result_filter=="Reject" and (auto_result_filter=="Accept" or auto_result_filter==None):
                    #final_brand_raw = list(set(img["finalTagHit"].split(",")))
                    final_brand_raw = list(set(img["finalTagHit"].split(",")))
                    final_brand_list = []
                    for i in final_brand_raw:
                        final_brand_list.append(i.split("/")[-1].split("】")[0])
                    final_brand_raw_auto = list(set(img["ruleHit"].split(",")))
                    final_brand_auto_list = []
                    for i in final_brand_raw_auto:
                        final_brand_auto_list.append(i.split("/")[-1].split("】")[0])
                    rr_match = 0
                    for i in final_brand_auto_list:
                        if i in final_brand_list:
                            rr_match = 1
                            break
                    if rr_match == 1:
                        continue
                    else:
                        final_brand_raw = list(set(img["finalTagHit"].split(",")))
                elif auto_result_filter=="Reject" and (final_result_filter=="Accept" or final_result_filter==None):
                    #final_brand_raw = list(set(img["ruleHit"].split(",")))
                    final_brand_raw = list(set(img["finalTagHit"].split(",")))
                    final_brand_list = []
                    for i in final_brand_raw:
                        final_brand_list.append(i.split("/")[-1].split("】")[0])
                    final_brand_raw_auto = list(set(img["ruleHit"].split(",")))
                    final_brand_auto_list = []
                    for i in final_brand_raw_auto:
                        final_brand_auto_list.append(i.split("/")[-1].split("】")[0])
                    rr_match = 0
                    for i in final_brand_auto_list:
                        if i in final_brand_list:
                            rr_match = 1
                            break
                    if rr_match == 1:
                        continue
                    else:
                        final_brand_raw = list(set(img["ruleHit"].split(",")))
                elif auto_result_filter=="Reject" and final_result_filter=="Reject":
                    final_brand_raw = list(set(img["finalTagHit"].split(",")))
                    final_brand_list = []
                    for i in final_brand_raw:
                        final_brand_list.append(i.split("/")[-1].split("】")[0])
                    final_brand_raw_auto = list(set(img["ruleHit"].split(",")))
                    final_brand_auto_list = []
                    for i in final_brand_raw_auto:
                        final_brand_auto_list.append(i.split("/")[-1].split("】")[0])
                    rr_match = 0
                    for i in final_brand_auto_list:
                        if i in final_brand_list:
                            rr_match = 1
                            break
                    if rr_match==1:
                        continue
                    else:
                        final_brand_raw = list(set(img["ruleHit"].split(",")))
                if final_brand_raw==[]:
                    continue
                final_brand = []
                for brand in final_brand_raw:
                    #print(brand)
                    if "侵权/品牌" in brand:
                        final_brand.append(brand)
                if final_brand==[]:
                    continue
                print_name = final_brand[0].split("/")[-1].split("】")[0]
                if len(final_brand)>=2:
                    for final in final_brand[1:]:
                        print_name += "_"+final.split("/")[-1].split("】")[0]
                final_brand = max(final_brand,key=final_brand.count)
                final_brand = final_brand.split("/")[-1].split("】")[0]
                if final_brand in donot_need_brand or (donot_need_brand == ["all"] and final_brand not in need_brand):
                    continue
                if final_brand in get_brand and final_brand in need_brand and get_brand[final_brand]>=need_brand[final_brand]:
                    print(f"brand {final_brand} is enough,get {get_brand[final_brand]} images")
                    continue
                elif final_brand in get_brand and final_brand not in need_brand and final_brand not in donot_need_brand and get_brand[final_brand]>=other_brand_num:
                    print(f"brand {final_brand} is enough,get {get_brand[final_brand]} images")
                    continue
                else:
                    if final_brand in get_brand:
                        get_brand[final_brand] += 1
                        new_get = 1
                    else:
                        get_brand[final_brand] = 1
                        new_get = 1

                img_name = url.split("/")[-1]
                resq = requests.get(url)
                if len(resq.content) > 50:
                    img_out = os.path.join(dst_dir,final_brand)
                    if not os.path.exists(img_out):
                        os.makedirs(img_out)
                    open(os.path.join(img_out,print_name+"_"+img_name), 'wb').write(resq.content)
                    downloaded_images += 1
                    downloaded_per_list += 1
                else:
                    continue
        except Exception as e:
            print(e)
            continue
    if new_get:
        print(index,"this list has %d images,have downloaded %d/%d,total downloaded %d, new get ID is %s" %(len(img_list),downloaded_per_list,len(img_list),downloaded_images,dict_brand["commodityId"]))
        new_get = 0
    else:
        print(index,"this list has %d images,have downloaded %d/%d,total downloaded %d" %(len(img_list),downloaded_per_list,len(img_list),downloaded_images))
    if index%100==0:
        print(f"get images: {get_brand}")




