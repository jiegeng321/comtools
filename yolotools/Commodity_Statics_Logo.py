#!/usr/local/bin/python3
# -*- coding:utf-8 -*-
"""
@author: xu.feng
@contact: xfeng_zjut@163.com
"""
import ast
import os
import requests
import pandas as pd
from tqdm import tqdm
from sklearn.metrics import classification_report
import argparse

def readtxt(txt_file):
    print("reading txt file")
    try:
        with open(txt_file, 'r') as fr:
            lines = fr.readlines()
        print("reading done")
        return lines
    except Exception as e:
        print(e)
        return None
def save_img_from_url(url,save_dir):
    try:
        img_name = url.split("/")[-1]
        resq = requests.get(url)
        if len(resq.content) > 250:
            if not os.path.exists(save_dir):
                os.makedirs(save_dir)
            open(os.path.join(save_dir, img_name), 'wb').write(resq.content)
            print("save img",os.path.join(save_dir, img_name))
            return True
    except Exception as e:
        print("save img wrong, pass",e)
        return False
#{"autoCheckResult":"Reject","category":"Modelless suit;无模特套装","checkStatus":1,"commodityId":"34436835","commodityPend":0,"crawlTaskId":"0","finalCheckResult":"Reject","finalTagHit":"[图像]侵权/品牌/nike,[文本]侵权/品牌/nike","gmtCreate":1647896413239,"id":"1647896413239724233","imageAutoCheckResult":"Reject","imageCommodityData":[{"autoCheckResult":"Reject","autoCheckTime":1647909792434,"commodityUrlId":"1647896413239724233","crawlTaskId":"0","finalCheckResult":"Reject","finalTagHit":"[图像]侵权/品牌/nike","gmtCreate":1647896413284,"id":"1647896413284396118","imageId":"p-comp/1647909201385000Y8C9F6D2D0030001","imageSize":"224269","isScreenshot":0,"lastChecker":"胡国玉","ruleHit":"图像识别品牌【侵权/品牌/nike】","seqId":"1647909792379000Y8C8F62600030001","status":3,"tagHit":"[图像]侵权/品牌/nike","taskId":"212182","taskUrlId":"0","textData":"https://s3.forcloudcdn.com/item/images/dmc/18c17623-1dc2-4f21-9a6f-ee50151ea537-750x750.jpeg","type":1}
#{"autoCheckResult":"Accept","autoCheckTime":1647909775974,"commodityUrlId":"1647896413239563947","crawlTaskId":"0","finalCheckResult":"Accept","finalTagHit":"","gmtCreate":1647896413284,"id":"1647896413284783127","imageId":"p-comp/1647909229496000Y8C9F52200030001","imageSize":"380863","isScreenshot":0,"lastChecker":"胡国玉","seqId":"1647909775960000Y8C8F30C90030001","status":3,"taskId":"212182","taskUrlId":"0","textData":"https://s3.forcloudcdn.com/item/images/dmc/1b51bbf6-0d47-4bcc-9e31-df4fc5ab119c-1080x1080.jpeg","type":1}

def analyze_data(lines):
    print("analyzing...")
    for line in tqdm(lines):
        dict_brand = ast.literal_eval(line)
        #list_per_pic = dict_brand["imageCommodityData"]#[{"autoCheckResult":"Reject","autoCheckTime":1647909768050,"commodityUrlId":"1647896413239346216","crawlTaskId":"0","finalCheckResult":"Reject","finalTagHit":"[图像]侵权/品牌/prada","gmtCreate":1647896413285,"id":"1647896413285813284","imageId":"p-comp/1647909313939000Y8C9D56080030001","imageSize":"69608","isScreenshot":0,"lastChecker":"胡国玉","ruleHit":"图像识别品牌【侵权/品牌/prada】","seqId":"1647909767954000Y8C8F10810030001","status":3,"tagHit":"[图像]侵权/品牌/prada","taskId":"212182","taskUrlId":"0","textData":"https://s3.forcloudcdn.com/item/images/dmc/97b06a00-3cba-4620-bfb8-c91c85ef4f7f-750x750.jpeg","type":1},{},{},...]
        if "finalTagHit" in dict_brand:
            if dict_brand["autoCheckResult"] == "Accept" and dict_brand["finalCheckResult"] == "Accept":
                auto.append("accept")
                human.append("accept")
                continue
            if pattern in dict_brand["finalTagHit"] or dict_brand["finalTagHit"] == "":#human get result will make sence
                list_per_pic = dict_brand["imageCommodityData"]
                auto_ = []
                for per_pic in list_per_pic:
                    if check_brand:
                        human__ = []
                        if "finalTagHit" in per_pic and pattern in per_pic["finalTagHit"]:
                            for per_brand in per_pic["finalTagHit"].split(","):
                                if pattern in per_brand:
                                    brand = per_brand.split("/")[-1]  # nike
                                    human__.append(brand)
                    if "ruleHit" in per_pic and auto_pattern in per_pic["ruleHit"]:
                        for per_obj in per_pic["ruleHit"].split(","):  # 图像识别品牌【侵权/品牌/prada】
                            if auto_pattern in per_obj:
                                brand = per_obj.split("/")[-1].split("】")[0]
                                auto_.append(brand)  # prada
                                if check_brand and brand in check_brand and brand not in human__ and ((brand in img_get_num and img_get_num[brand]<check_brand[brand]) or brand not in img_get_num):
                                    url = per_pic["textData"]
                                    if save_img_from_url(url,os.path.join(check_brand_img_save_dir,"auto_reject_human_accept",brand)):
                                        if brand not in img_get_num:
                                            img_get_num[brand] = 1
                                        else:
                                            img_get_num[brand] += 1

                    if check_brand:
                        if "finalTagHit" in per_pic and pattern in per_pic["finalTagHit"]:
                            for per_brand in per_pic["finalTagHit"].split(","):
                                if pattern in per_brand:
                                    brand = per_brand.split("/")[-1]  # nike
                                    if brand in check_brand and brand not in auto_ and ((brand in img_get_num and img_get_num[brand] < check_brand[
                                        brand]) or brand not in img_get_num):
                                        url = per_pic["textData"]
                                        if save_img_from_url(url, os.path.join(check_brand_img_save_dir, "human_reject_auto_accept", brand)):
                                            if brand not in img_get_num:
                                                img_get_num[brand] = 1
                                            else:
                                                img_get_num[brand] += 1


                if dict_brand["finalTagHit"] == "":
                    if auto_ == []:
                        auto.append("accept")
                        human.append("accept")
                    else:
                        auto_final = max(auto_, key=auto_.count)
                        auto.append(auto_final)
                        human.append("accept")
                else:
                    human_ = []
                    match = 0
                    for per_brand in dict_brand["finalTagHit"].split(","):#"finalTagHit":"[图像]侵权/品牌/nike,[文本]侵权/品牌/nike"
                        if pattern in per_brand:
                            human_final = per_brand.split("/")[-1]#nike
                            human_.append(human_final)
                            if human_final in auto_:
                                auto.append(human_final)
                                human.append(human_final)
                                match = 1
                                break
                    # if "van_cleef_arpels" in human_:
                    #     print(auto_)
                    #     print(human_)
                    if auto_ == []:
                        auto.append("accept")
                        human.append(max(human_, key=human_.count))
                    elif match == 0:
                        auto.append(max(auto_, key=auto_.count))
                        human.append(max(human_, key=human_.count))

        else:
            pass


if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", type=str, required=True, help="the input txt file path.")
    parser.add_argument("-s", type=str, default="./", help="the save csv path.")
    parser.add_argument("-c", type=str, default=None, help="the check brand.")
    parser.add_argument("-cs", type=str, default=None, help="the check brand save images path.")
    parser.add_argument("-th", type=int, default=20, help="the support th.")
    parser.add_argument("-hp", type=str, default="[图像]侵权/品牌", help="the human result pattern.")
    parser.add_argument("-ap", type=str, default="图像识别品牌", help="the auto result pattern.")
    parser.add_argument("-i", type=str, default="fordeal重点品牌分析详情1028.xlsx", help="the fordeal important brand xlsx file.")
    args = parser.parse_args()

    #线上数据的txt文件
    txt_dir = args.f#"/data01/xu.fx/dataset/NEW_RAW_INCREASE_DATA/FORDEAL_ONLINE_TXT_DATA/0310-0319.txt"
    #具体品牌表格输出目录
    print(args.c)
    save_result_csv_dir = args.s#"./"
    #check品牌配置，品牌：数量
    check_brand = str(args.c)#"{"a":1000,"b":1000}"
    if check_brand:
        check_brand = ast.literal_eval(check_brand)
    #check品牌下载目录，未配置check品牌则无效
    check_brand_img_save_dir = args.cs#"/data01/xu.fx/dataset/NEW_RAW_INCREASE_DATA/tmp3"
    #打印具体指标的出现次数要求，csv结果没有出现次数限制
    total_support_th = args.th
    logo_support_th = args.th
    fordeal_important_support_th = args.th
    #人审过滤字段，可配置logo，爆恐，色情等
    pattern = args.hp
    #机审过滤字段，可配置logo，爆恐，色情等
    auto_pattern = args.ap
    #模型支持品牌配置
    logo_supported = ['spyderco', '3m', 'pampers', 'bentley', 'benq', 'cleveland_indians', 'canada_goose', 'new_york_mets', 'deadpool', 'bape', 'griffin', 'davidoff', 'mlb', 'oxo', 'ping', 'robo_fish', 'akg_by_harmon', 'marc_jacobs', 'a_cold_wall', 'skullcandy', 'eos', 'manolo_blahnik', 'olympus', 'bottega_veneta', 'volbeat', 'utah_jazz', 'bugslock', 'ac_dc', 'prada', 'breitling', 'tide', 'dumbo', 'panerai', 'mcm', 'sennheiser', 'fjallraven', 'raw', 'tag_heuer', 'the_killers', 'awt', 'gillette', 'monster_energy', 'amiibo', 'zegna', 'carters', 'vacheron_constantin', 'martin_co', 'wrangler', 'hamann', 'usa', 'bmc_racing', 'new_york_islanders', 'lego', 'marshall', 'minnesota_wild', 'jw_anderson', 'philadelphia_flyers', 'milwaukee_brewers', 'amiri', 'technomarine', 'flexfit', 'cluse', 'hunter', 'roxy', 'chloe', 'san_francisco_49ers', 'manchester_city', 'maui_jim', 'kingston', 'ergobaby', 'breguet', 'hydro_flask', 'montreal_expos', 'tory_burch', 'too_faced', 'aussiebum', 'a_lange_sohne', 'dfb', 'baltimore_ravens', 'volkl', 'dallas_cowboys', 'shield', 'new_york_rangers', 'fendi', 'dsquared2', 'los_angeles_lakers', 'tottenham_hotspur', 'carolina_hurricanes', 'smith_wesson', 'chopard', 'atlanta_falcons', 'bakugan', 'instantly_ageless', 'fila', 'los_angeles_rams', 'mms', 'butterfly', 'orlando_magic', 'bed_head', 'esp', 'shimmer_and_shine', 'daddario', 'ecko', 'kaporal', 'koss', 'new_orleans_saints', 'alberta_ferretti', 'pocoyo', 'buffalo_bills', 'philadelphia_eagles', 'brioni', 'baby_shark', 'fossil', 'paul_shark', 'phiten', 'washington_wizards', 'dell', 'blues_clues', 'efest', 'hello_kitty', 'bestway', 'guerlain', 'ugg', 'oakley', 'aspinal_of_london', 'care_bears', 'miu_miu', 'sacramento_kings', 'nasa', 'alexander_wang', 'bubble_guppies', 'cincinnati_reds', 'guardians_of_the_galaxy', 'loewe', 'roor', 'liverpool_fc', 'dkny', 'braun', 'goyard', 'hurley', 'celine', 'coogi', 'foreo', 'atlanta_hawks', 'samsonite', 'betty_boop', 'dhc', 'bill_blass', 'shimano', 'scotty_cameron', 'overwatch', 'ktm', 'uboat', 'buffalo_sabres', 'iron_maiden', 'the_allman_brothers_band', 'psv', 'tech_deck', 'wilson', 'black_panther', 'swatch', 'lamborghini', 'true_religion', 'tampa_bay_rays', 'golden_goose', 'new_balance', 'zelda', 'van_cleef_arpels', 'michael_kors', 'slazenger', 'thomas_sabo', 'chicago_cubs', 'philipp_plein', 'david_yurman', 'sk_ii', 'ritchey', 'doctor_strange', 'off_white', 'bulova', 'playstation', 'arizona_diamondbacks', 'biotherm', 'grand_seiko', 'cole_haan', 'hexbug', 'apple', 'kate_spade', 'pearl_izumi', 'zippo', 'zimmermann', 'atlanta_bravs', 'st._louis_blues', 'herbal_essences', 'vancouver_canucks', 'premier_league', 'bobbi_brown', 'luke_combs', 'clarins', 'citizen', 'usa_basketball', 'titleist', 'diablo', 'imren', 'durex', 'batman', 'cleveland_golf', 'streamlight', 'new_york_knicks', 'puma', 'jim_beam', 'links_of_london', 'garmin', 'oklahoma_city_thunder', 'furla', 'tissot', 'max_factor', 'havaianas', 'dooney_bourke', 'levis', 'baby_phat', 'cannondale', 'carolina_panthers', 'converse', 'game_boy', 'lancome', 'harry_winston', 'knvb', 'st._louis_cardinals', 'daniel_wellington', 'stefano_ricci', 'ariel', 'bvlgari', 'monchhichi', 'skylanders', 'ozark', 'guitar_hero', 'toronto_blue_jays', '3t', 'boston_celtics', 'brabus', 'death_wish_coffee_co', 'chevron', 'colgate', 'minnesota_vikings', 'new_england_patriots', 'ed_hardy', 'slap_chop', 'muhammad_ali', 'vivienne_westwood', 'blackberry_smoke', 'desigual', 'louis_vuitton', 'alpinestars', 'pantene', 'the_rolling_stones', 'philadelphia_phillies', 'movado', 'mophie', 'bally', 'harry_potter', 'rimowa', 'burberry', 'bell_ross', 'jeep', 'dallas_mavericks', 'kobe', 'head', 'dr_martens', 'bioderma', 'brooklyn_nets', 'conair', 'paris_saint_germain', 'patek_philippe', 'new_orleans_pelicans', '511_tactical', 'blizzard', 'urban_decay', 'pony', 'victorias_secret', 'robo_alive', 'tampa_bay_buccaneers', 'pj_masks', 'elizabeth_arden', 'bebe', 'bunch_o_ballons', 'ess', 'ecco', 'bright_bugz', 'pxg', 'honeywell', 'jack_jones', 'alexander_mcqueen', 'ulysse_nardin', 'timberland', 'toronto_raptors', 'heroes_of_the_storm', 'pro_kennex', 'edmonton_oilers', 'vlone', 'miami_heat', 'hid_global', 'minnesota_timberwolves', 'bugatti_veyron', 'beautyblender', 'belstaff', 'houston_astros', 'oakland_raiders', 'juul', 'daiwa', 'caterpillar', 'indianapolis_colts', 'sony_ericsson', 'st_dupont', 'epson', 'concord', 'sephora', 'schwarzkopf', 'duracell', 'enve', 'adidas', 'dallas_stars', 'san_antonio_spurs', 'compaq', 'mac', 'toms', 'big_green_egg', 'estee_lauder', 'titoni', 'montblanc', 'houston_rockets', 'milwaukee_bucks', 'uefa', 'detroit_pistons', 'salvatore_ferragamo', 'detroit_lions', 'sisley', 'rcma', 'chicago_white_sox', 'fred_perry', 'hatchimals', 'porsche', 'cleveland_cavaliers', 'anne_klein', 'blackhawk', 'hamilton', 'west_ham_united', 'balmain', 'nashville_predators', 'copper_fit', 'ysl', 'sanrio', 'phoenix_suns', 'xmen', 'ado_den_haag', 'anaheim_angels', 'xxio', 'carmex', 'hermes', 'jacksonville_jaguars', 'green_bay_packers', 'babolat', 'longines', 'the_loud_house', 'boston_bruins', 'rayban', 'merrell', 'lyle_scott', 'franco_moschino', 'fullips', 'arsenal', 'popsockets', 'diadora', 'agnes_b', 'dragon_ball', 'tods', 'kansas_royals', 'crabs_adjust_humidity', 'land_rover', 'frida_kahlo', 'corum', 'juventus', 'elvis_presley', 'ben_jerrys', 'zara', 'supra', 'beats_by_drdre', 'daniel_roth', 'furminator', 'disney', 'captain_america', 'fc_bayern_munchen', 'travis_scott', 'mizuno', 'comme_des_garcons', 'carolina_herrera', 'audio_technica', 'portugal', 'coach', 'lg', 'supreme', 'kenan_and_kel', 'chelsea', 'montreal_canadiens', 'maserati', 'mulberry', 'as_roma', 'miffy', 'ghd', 'philadelphia_76ers', 'moncler', 'fischer', 'plantronics', 'columbus_blue_jackets', 'pokemon', 'asics', 'los_angeles_dodgers', 'tapout', 'vans', 'atletico_de_madrid', 'skin79', 'keen', 'belkin', 'rolex', 'pixar', 'audi', 'winnipeg_jets', 'gopro', 'tonino_lamborghini', 'detroit_tigers', 'gildan', 'heron_preston', 'switcheasy', 'logitech', 'kansas_city_chiefs', 'memphis_grizzlies', 'l_oreal', 'power_rangers', 'washington_capitals', 'cartier', 'prince', 'gant', 'stussy', 'red_bull', 'breeze_smoke', 'bose', 'bushnell', 'audemars_piguet', 'bitdefender', 'gap', 'ibanez', 'ariat', 'chanel', 'alcon', 'opi', 'calgary_flames', 'cincinnati_bengals', 'berluti', 'cards_against_humanity', 'samantha_thavasa', 'san_diego_padres', 'dean_guitar', 'fitbit', 'shiseido', 'pinko', 'volcom', 'cazal', 'portland_trail_blazers', 'evisu', 'fender', 'lesmills', 'christian_audigier', 'allsaints', 'crumpler', 'azzaro', 'brut', 'giuseppe_zanotti', 'jaeger_lecoultre', 'tennessee_titans', 'nutribullet', 'audioquest', 'specialized', 'england', 'gazelle', 'pandora', 'arcteryx', 'toy_watch', 'chicago_blackhawks', 'blancpain', 'nickelodeon', 'wallykazam', 'mercedes_benz', 'blu', 'dunhill', 'speck', 'gucci', 'cummins', 'rip_curl', 'umbro', 'issey_miyake', 'trx_training', 'dior', 'world_of_warcraft', 'barbie', 'starcraft', 'tous', 'franck_muller', 'cnd', 'new_york_yankees', 'balenciaga', 'manchester_united', 'hugo_boss', 'abercrombie_fitch', 'houston_texans', 'crocs', 'birkenstock', 'skoda', 'hey_dude', 'hm', 'moose_knuckles', 'new_era', 'miami_dolphins', 'switch', 'guess', 'paco_rabanne', 'bunchems', 'paul_frank', 'seattle_seahawks', 'jbl', 'pittsburgh_penguins', 'diesel', 'toronto_maple_leafs', 'coty', 'olympique_marseille', 'r4', 'zigzag', 'the_punisher', 'jack_daniels', 'otter_box', 'anaheim_ducks', 'jurlique', 'lindberg', 'colorado_avalanche', 'jimmy_choo', 'chicago_bears', 'escada', 'bosch', 'american_eagle', 'zenith', 'infusium', 'mammut', 'hollister_co', 'arizona_cardinals', 'burts_bees', 'clarisonic', 'ducati', 'benefit', 'the_horus_heresy', 'vegas_golden_knights', 'lol_surprise', 'new_york_giants', 'bmw', 'los_angeles_kings', 'callaway', '7up', 'motorola', 'iwc', 'cacharel', 'asos', 'iced_earth', 'facebook', 'benetton', 'acer', 'motorhead', 'paul_smith', 'lululemon', 'jack_wolfskin', 'avengers', 'nike', 'ellesse', 'calvin_klein', 'playboy', 'dolce_gabbana', 'elementcase', 'gstar_raw', 'google', 'shopkins', 'iron_man', 'magpul', 'grumpy_cat', 'the_fairly_oddparents', 'charlotte_hornets', 'game_of_thrones', 'dyson', 'bang_olufsen', 'head_shoulders', 'romain_jerome', 'hyundai', 'taylormade', 'huf', 'dettol', 'uag', 'creative', 'glashutte_original', 'los_angeles_chargers', 'hp', 'cath_kidston', 'girard_perregaux', 'jacob_co', 'graham', 'irobot', 'omega', 'los_angeles_clippers', 'florida_marlins', 'phoenix_coyotes', 'nirvana', 'kipling', 'yeti', 'cisco', 'swig', 'zumba_fitness', 'led_zeppelin', 'anna_sui', 'columbia', 'fc_barcelona_fcb', 'san_jose_sharks', 'denver_broncos', 'hennessy', 'ralph_lauren', 'honda', 'swarovski', 'pink_floyd', 'srixon', 'visa', 'always', 'gibson', 'palm_angels', 'chaumet', 'john_deere', 'giro', 'rb_leipzig', 'eotech', 'leicester_city_f.c', 'palace', 'coca_cola', 'new_york_jets', 'chrome_hearts', 'forever_21', 'brazil', 'wwe', 'baltimore_orioles', 'juicy_couture', 'boston_red_sox', 'everlast', 'golden_state_warriors', 'jabra', 'piaget', 'blaze_and_the_monster_machines', 'shaun_the_sheep', 'babyliss', 'washington_redskins', 'tampa_bay_lightning', 'beretta', 'versace', 'fingerlings', 'billabong', 'ice_watch', 'ottawa_senators', 'marvel', 'bvb', 'goo_jit_zu', 'feyenoord', 'stan_smith', 'camelbak', 'nokia', 'grado', 'bjorn_borg', 'nfl', 'jack_wills', 'call_of_duty_ghosts', 'clinique', 'whirlpool', 'givenchy', 'pinarello', 'kiehls', 'superdry', 'maybelline', 'blackberry', 'lilo_stitch', 'black_widow', 'aquascutum', 'armani', 'chi', 'roger_vivier', 'roger_dubuis', 'hogan', 'fifa', 'san_francisco_giants', 'addicted', 'valentino_garavani', 'tommy_hilfiger', 'western_digital', 'dc_shoes', 'bontrager', 'incipio', 'under_armour', 'casio', 'aquabeads', 'mbt', 'new_jersey_devils', 'tudor', 'texas_rangers', 'pittsburgh_steelers', 'hublot', 'sons_of_arthritis', 'patagonia', 'fuji_film', 'cadillac', 'helena_rubinstein', 'the_black_crowes', 'denver_nuggets', 'scooby_doo', 'barbour', 'chicago_bulls', 'seagate', 'nixon', 'chevrolet', 'florida_panthers', 'games_workshop', 'grenco_science', 'rado', 'def_leppard', 'tiffany_co', 'nba', 'lacoste', 'kenzo', 'cleveland_browns', 'fox_head', 'rosetta_stone', 'yonex', 'destiny', 'toppik', 'shu_uemura', 'alfar_romeo', 'canon', 'afc_ajax', 'jacquemus', 'salomon', 'minesota_twins', 'adobe', 'indiana_pacers', 'shure', 'incase', 'dewalt', 'detroit_red_wings', 'led_lenser', 'cwc', 'reebok', 'longchamp', 'the_north_face', 'hearthstone', 'christian_louboutin', 'metallica', 'ferrari', 'footjoy', 'kappa', 'marcelo_burlon', 'oakland_athletics', 'c1rca', 'la_martina', 'htc', 'carhartt', 'fear_of_god_essentials', 'marlboro', 'oral_b', 'harley_davidson', 'cheap_monday']
    #fordeal重点品牌配置
    try:
        fordeal_important = pd.read_excel(args.i)
        fordeal_important = fordeal_important.iloc[:,0].tolist()
    except:
        fordeal_important = ['casio', 'puma', 'coach', 'new_balance', 'yves_saint_laurent', 'calvin_klein', 'playboy', 'tory_burch', 'hugo_boss', 'lacoste', 'jeep', 'fossil', 'rolex', 'chloe', 'citizen', 'guess', 'moncler', 'longines', 'jbl', 'dunhill', 'hublot', 'diesel', 'bally', 'caterpillar', 'audemars_piguet', 'escada', 'gant', 'breitling', 'juicy_couture', 'blancpain', 'bose', 'movado', 'breguet', 'zegna', 'gucci', 'louis_vuitton', 'chanel', 'versace', 'armani', 'converse', 'fila', 'celine', 'the_north_face', 'givenchy', 'omega', 'under_armour', 'philipp_plein', 'ugg', 'fred_perry', 'daniel_wellington', 'iwc', 'estee_lauder', 'adidas', 'burberry', 'fendi', 'hermes', 'supreme', 'off_white', 'prada', 'balenciaga', 'disney', 'tommy_hilfiger', 'vans', 'michael_kors', 'mcm', 'air_jordan', 'seiko', 'cartier', 'bottega_veneta', 'loewe', 'bvlgari', 'champion', 'miu_miu', 'kenzo', 'ferrari', 'nba', 'zara', 'christian_louboutin', 'swarovski', 'lamborghini', 'patek_philippe', 'bape', 'police', 'bmw', 'valentino', 'balmain', 'timberland', 'vacheron_constantin', 'pandora']
    auto = []
    human = []
    img_get_num = {}
    lines = readtxt(txt_dir)
    analyze_data(lines)
    class_result = classification_report(human, auto,zero_division=False,output_dict=True)
    new_class_result = {}
    for key,ite in class_result.items():
        if key=="accuracy" or key=="weighted avg" or key == "macro avg":
            continue
        if ite["support"]==0:
            continue
        ite["precision"] = round(ite["precision"],2)
        ite["recall"] = round(ite["recall"], 2)
        ite["f1-score"] = round(ite["f1-score"], 2)
        new_class_result[key] = [ite["support"],ite["recall"],ite["precision"],ite["f1-score"]]
    pd_data = pd.DataFrame(new_class_result,index=["出现次数","召回率","查准率","f1-score"])
    pd_data = pd.DataFrame(pd_data.values.T,index=pd_data.columns,columns=pd_data.index)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)
    pd_data = pd_data.sort_values(by="出现次数",ascending=False)

    print("total test brand have:",len(pd_data[pd_data["出现次数"]>=total_support_th]))
    print("total test num:",pd_data["出现次数"].sum())
    print("recall mean: ", pd_data[pd_data["出现次数"]>=total_support_th]["召回率"].mean())
    print("precision mean: ", pd_data[pd_data["出现次数"]>=total_support_th]["查准率"].mean())
    print(pd_data[pd_data["出现次数"]>=total_support_th])
    if save_result_csv_dir:
        pd_data.to_csv(os.path.join(save_result_csv_dir,"total_brand_result.csv"))
    print("\n")

    logo_supported_ = []
    pd_data_indexs = pd_data.index.tolist()
    for i in logo_supported:
        if i not in pd_data_indexs:
            continue
        logo_supported_.append(i)
    logo_supported_ = pd_data.loc[logo_supported_,:]
    print("model support test brand have:",len(logo_supported_[logo_supported_["出现次数"]>=logo_support_th]))
    print("model support test num:",logo_supported_["出现次数"].sum())
    print("recall mean: ", logo_supported_[logo_supported_["出现次数"]>=logo_support_th]["召回率"].mean())
    print("precision mean: ", logo_supported_[logo_supported_["出现次数"]>=logo_support_th]["查准率"].mean())
    logo_supported_ = logo_supported_.sort_values(by="出现次数",ascending=False)
    print(logo_supported_[logo_supported_["出现次数"]>=logo_support_th])
    if save_result_csv_dir:
        logo_supported_.to_csv(os.path.join(save_result_csv_dir,"model_supported_brand_result.csv"))
    print("\n")

    fordeal_important_ = []
    logo_supported_indexs = logo_supported_.index.tolist()
    for i in fordeal_important:
        if i not in logo_supported_indexs:
            continue
        fordeal_important_.append(i)
    fordeal_important_ = logo_supported_.loc[fordeal_important_,:]
    print("fordeal important test brand have:",len(fordeal_important_[fordeal_important_["出现次数"]>=fordeal_important_support_th]))
    print("fordeal important test num:",fordeal_important_["出现次数"].sum())
    print("recall mean: ", fordeal_important_[fordeal_important_["出现次数"]>=fordeal_important_support_th]["召回率"].mean())
    print("precision mean: ", fordeal_important_[fordeal_important_["出现次数"]>=fordeal_important_support_th]["查准率"].mean())
    fordeal_important_ = fordeal_important_.sort_values(by="出现次数",ascending=False)
    print(fordeal_important_[fordeal_important_["出现次数"]>=fordeal_important_support_th])
    if save_result_csv_dir:
        fordeal_important_.to_csv(os.path.join(save_result_csv_dir,"fordeal_important_brand_result.csv"))
    print("\n")


    total_num = len(lines)
    print("所有商品数量:",total_num)
    def show_detail(auto,human):
        useful_num = len(human)
        auto_accept_num = 0
        human_accept_num = 0
        auto_reject_num = 0
        human_reject_num = 0

        auto_reject_human_accept = 0
        auto_reject_human_reject = 0
        auto_accept_human_accept = 0
        auto_accept_human_reject = 0
        for au,hu in zip(auto,human):
            if au=="accept":
                auto_accept_num += 1
            else:
                auto_reject_num += 1
            if hu=="accept":
                human_accept_num += 1
            else:
                human_reject_num += 1
            if au!="accept" and hu=="accept":
                auto_reject_human_accept += 1
            if au!="accept" and hu!="accept":
                auto_reject_human_reject += 1
            if au=="accept" and hu=="accept":
                auto_accept_human_accept += 1
            if au=="accept" and hu!="accept":
                auto_accept_human_reject += 1
        auto_reject_rate = auto_reject_num/useful_num
        huamn_reject_rate = human_reject_num/useful_num
        auto_reject_right_rate = auto_reject_human_reject/human_reject_num
        auto_reject_wrong_rate = auto_reject_human_accept/auto_reject_num

        print("有效商品数量:",useful_num)

        print(f"机审通过量: {auto_accept_num}")
        print(f"机审拒绝量: {auto_reject_num}")
        print(f"人审通过量: {human_accept_num}")
        print(f"人审拒绝量: {human_reject_num}")
        print(f"机审拒绝，人审拒绝: {auto_reject_human_reject}")
        print(f"机审拒绝，人审通过: {auto_reject_human_accept}")
        print(f"机审通过，人审通过: {auto_accept_human_accept}")
        print(f"机审通过，人审拒绝: {auto_accept_human_reject}")
        print(f"人审拒绝率: {round(huamn_reject_rate*100, 2)}%")
        print(f"机审拒绝率: {round(auto_reject_rate*100, 2)}%")
        print(f"机审拒绝覆盖率: {round(auto_reject_right_rate*100, 2)}%")
        print(f"机审拒绝错误率: {round(auto_reject_wrong_rate*100, 2)}%")

    auto_model_support = []
    human_model_support = []
    for au,hu in zip(auto,human):
        if hu in logo_supported or hu=="accept":
            auto_model_support.append(au)
            human_model_support.append(hu)

    print("所有防控品牌指标结果（指标影响因素：人审主体判断/品牌未支持/人审有误）")
    show_detail(auto,human)
    print("\n")
    print("模型支持品牌指标结果（指标影响因素：人审主体判断/样式未支持/人审有误）")
    show_detail(auto_model_support,human_model_support)
    print("\n")
    print("所有品牌召回查准指标已保存至:",os.path.join(save_result_csv_dir,"total_brand_result.csv"))
    print("模型支持品牌召回查准指标已保存至:",os.path.join(save_result_csv_dir,"model_supported_brand_result.csv"))
    print("fordeal关注品牌召回查准指标已保存至:",os.path.join(save_result_csv_dir,"fordeal_important_brand_result.csv"))
    if check_brand:
        print("已下载图片:",img_get_num)
        print("图片存放地址:",check_brand_img_save_dir)