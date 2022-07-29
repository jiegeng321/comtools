#!/usr/local/bin/python3
# -*- coding:utf-8 -*-
from pyecharts.charts import *
from pyecharts import options as opts
from pyecharts.globals import CurrentConfig
CurrentConfig.ONLINE_HOST = "https://cdn.kesci.com/lib/pyecharts_assets/"
#learn from https://gallery.pyecharts.org
from pathlib import Path
logo_list = ['3m', 'sk_ii', 'l_oreal', '3t', 'flexfit', 'volbeat', 'leicester_city_f.c', 'ess', 'cleveland_indians', 'movado', 'fila', 'desigual', 'tampa_bay_buccaneers', 'gillette', 'hogan', 'longchamp', 'braun', 'callaway', 'phiten', 'cannondale', 'bally', 'incipio', 'shaun_the_sheep', 'west_ham_united', 'columbia', 'duracell', 'blizzard', 'cards_against_humanity', 'zegna', 'houston_rockets', 'patagonia', 'playboy', 'phoenix_coyotes', 'guitar_hero', 'hydro_flask', 'afc_ajax', 'metallica', 'zumba_fitness', 'chopard', 'anne_klein', 'carhartt', 'esp', 'agnes_b', 'wilson', 'samantha_thavasa', 'mac', 'martin_co', 'bvlgari', '511_tactical', 'gstar_raw', 'heroes_of_the_storm', 'google', 'ferrari', 'cadillac', 'skoda', 'franco_moschino', 'toronto_maple_leafs', 'tampa_bay_lightning', 'land_rover', 'pony', 'avengers', 'davidoff', 'kingston', 'grenco_science', 'cole_haan', 'juul', 'games_workshop', 'lululemon', 'ritchey', 'fischer', 'acer', 'def_leppard', 'usa_basketball', 'graham', 'robo_fish', 'philadelphia_phillies', 'dell', 'florida_panthers', 'grumpy_cat', 'sennheiser', 'ado_den_haag', 'under_armour', 'toronto_blue_jays', 'hublot', 'foreo', 'butterfly', 'rimowa', 'dooney_bourke', 'mammut', 'the_killers', 'death_wish_coffee_co', 'tiffany_co', 'black_widow', 'enve', 'chicago_bears', 'premier_league', 'marlboro', 'miami_dolphins', 'yonex', 'keen', 'cheap_monday', 'titoni', 'beautyblender', 'birkenstock', 'jaeger_lecoultre', 'atlanta_falcons', 'alfar_romeo', 'volkl', 'the_black_crowes', 'panerai', 'harry_winston', 'plantronics', 'louis_vuitton', 'trx_training', 'washington_capitals', 'raw', 'cisco', 'denver_broncos', 'fingerlings', 'guerlain', 'la_martina', 'franck_muller', 'marvel', 'tonino_lamborghini', 'hyundai', 'new_york_giants', 'bell_ross', 'dfb', 'game_of_thrones', 'gibson', 'paco_rabanne', 'oakland_raiders', 'the_loud_house', 'chicago_bulls', 'jacksonville_jaguars', 'berluti', 'arcteryx', 'ben_jerrys', 'detroit_tigers', 'monchhichi', 'baby_phat', 'heron_preston', 'bosch', 'philadelphia_76ers', 'alcon', 'arizona_cardinals', 'blackhawk', 'san_diego_padres', 'green_bay_packers', 'iwc', 'atlanta_hawks', 'bakugan', 'incase', 'ktm', 'new_york_yankees', 'tag_heuer', 'bunch_o_ballons', 'barbour', 'tech_deck', 'memphis_grizzlies', 'ed_hardy', 'shure', 'dallas_mavericks', 'rcma', 'dr_martens', 'seagate', 'chaumet', 'bmc_racing', 'bape', 'hermes', 'cath_kidston', 'jbl', 'ecko', 'los_angeles_rams', 'cleveland_golf', 'havaianas', 'toronto_raptors', 'bang_olufsen', 'indianapolis_colts', 'salvatore_ferragamo', 'spibelt', 'ottawa_senators', 'buffalo_bills', 'baume_et_mercier', 'a_cold_wall', 'blackberry_smoke', 'zimmermann', 'daddario', 'audemars_piguet', 'abercrombie_fitch', 'scotty_cameron', 'led_zeppelin', 'chrome_hearts', 'aussiebum', 'milwaukee_brewers', 'hp', 'power_rangers', 'coach', 'chi', 'swarovski', 'thomas_sabo', 'true_religion', 'girard_perregaux', 'dallas_stars', 'tennessee_titans', 'sons_of_arthritis', 'blues_clues', 'cwc', 'world_of_warcraft', 'garmin', 'michael_kors', 'psv', 'colgate', 'new_jersey_devils', 'tide', 'philipp_plein', 'asics', 'logitech', 'monster_energy', 'golden_state_warriors', 'zigzag', 'dunhill', 'canada_goose', 'cincinnati_bengals', 'fc_bayern_munchen', 'starcraft', 'minnesota_timberwolves', 'paris_saint_germain', 'furminator', 'comme_des_garcons', 'volcom', 'dsquared2', 'bitdefender', 'adobe', 'benq', 'chloe', 'armani', 'pantene', 'links_of_london', 'speck', 'vlone', 'pxg', 'benefit', 'whirlpool', 'tous', 'chicago_white_sox', 'pinko', 'pampers', 'alberta_ferretti', 'florida_marlins', 'skin79', 'carolina_hurricanes', 'oklahoma_city_thunder', 'los_angeles_clippers', 'brioni', 'palm_angels', 'alexander_wang', 'switcheasy', 'aquascutum', 'c1rca', 'fred_perry', 'lilo_stitch', 'escada', 'allsaints', 'tommy_hilfiger', 'eotech', 'bjorn_borg', 'kipling', 'aeronautica_militare', 'stan_smith', 'urban_decay', 'fossil', 'breguet', 'vans', 'the_allman_brothers_band', 'bugslock', 'billabong', 'lyle_scott', 'fc_barcelona_fcb', 'chevrolet', 'brabus', 'iced_earth', 'mizuno', 'manchester_united', 'sanrio', 'nokia', 'gildan', 'salomon', 'tottenham_hotspur', 'opi', 'tods', 'moncler', 'chevron', 'irobot', 'red_bull', 'fjallraven', 'shimano', 'audioquest', 'doctor_strange', 'calvin_klein', 'estee_lauder', 'mms', 'houston_astros', 'maui_jim', 'biotherm', 'the_fairly_oddparents', 'winnipeg_jets', 'aspinal_of_london', 'clarins', 'oral_b', 'kate_spade', 'blackberry', 'tapout', 'grado', 'porsche', 'toy_watch', 'playstation', 'guardians_of_the_galaxy', 'detroit_pistons', 'pink_floyd', 'game_boy', 'amiri', 'shield', 'bed_head', 'always', 'atlanta_bravs', 'brut', 'ibanez', 'juicy_couture', 'shu_uemura', 'dettol', 'atletico_de_madrid', 'bebe', 'tudor', 'washington_redskins', 'clarisonic', 'kansas_royals', 'zenith', 'jack_wolfskin', 'zelda', 'lacoste', 'iron_man', 'blaze_and_the_monster_machines', 'roor', 'max_factor', 'san_antonio_spurs', 'fuji_film', 'washington_wizards', 'jacob_co', 'lego', 'care_bears', 'balmain', 'new_england_patriots', 'carters', 'rolex', 'sephora', 'kenzo', 'palace', 'dc_shoes', 'new_york_mets', 'hollister_co', 'gap', 'hennessy', 'kobe', 'cluse', 'england', 'bright_bugz', 'ecco', 'orlando_magic', 'a_lange_sohne', 'portland_trail_blazers', 'nixon', 'olympique_marseille', 'manolo_blahnik', 'seattle_seahawks', 'eos', 'boston_celtics', 'magpul', 'blu', 'utah_jazz', 'vivienne_westwood', 'levis', 'head_shoulders', 'roger_dubuis', 'los_angeles_dodgers', 'blancpain', 'iron_maiden', 'elizabeth_arden', 'lindberg', 'breeze_smoke', 'crabs_adjust_humidity', 'snow_white', 'mulberry', 'christian_louboutin', 'bottega_veneta', 'camelbak', 'bmw', 'hurley', 'azzaro', 'toppik', 'bubble_guppies', 'huf', 'ergobaby', 'tory_burch', 'benetton', 'romain_jerome', 'the_north_face', 'gopro', 'imren', 'dumbo', 'chicago_cubs', 'muhammad_ali', 'bioderma', 'manchester_city', 'shiseido', 'prada', 'uboat', 'milwaukee_bucks', 'hugo_boss', 'audi', 'swig', 'otter_box', 'dolce_gabbana', 'juventus', 'paul_shark', 'guess', 'shopkins', 'brazil', 'helena_rubinstein', 'minesota_twins', 'srixon', 'kenan_and_kel', 'dean_guitar', 'ghd', 'zara', 'grand_seiko', 'diadora', 'merrell', 'maserati', 'patek_philippe', 'montreal_canadiens', 'aquabeads', 'gucci', 'ellesse', 'nutribullet', 'lamborghini', 'pandora', 'crumpler', 'lol_surprise', 'puma', 'xxio', 'montblanc', 'liverpool_fc', 'marc_jacobs', 'paul_frank', 'cummins', 'bulova', 'shimmer_and_shine', 'dewalt', 'st._louis_cardinals', 'oxo', 'baltimore_ravens', 'diesel', 'burts_bees', 'feyenoord', 'minnesota_wild', 'daniel_roth', 'frida_kahlo', 'bentley', 'wrangler', 'rip_curl', 'montreal_expos', 'ice_watch', 'tampa_bay_rays', 'robo_alive', 'dkny', 'mcm', 'xmen', 'st_dupont', 'balenciaga', 'detroit_lions', 'marshall', 'france', 'barbie', 'motorhead', 'jw_anderson', 'bvb', 'uefa', 'ducati', 'goyard', 'skylanders', 'bushnell', 'goo_jit_zu', 'stefano_ricci', 'alexander_mcqueen', 'supra', 'new_era', 'asos', 'arsenal', 'pearl_izumi', 'jimmy_choo', 'addicted', 'caterpillar', 'pokemon', 'nba', 'versace', 'pro_kennex', 'hunter', 'jacquemus', 'cleveland_browns', 'gazelle', 'buffalo_sabres', 'spyderco', 'hey_dude', 'maybelline', 'rb_leipzig', 'anaheim_angels', 'honda', 'umbro', 'american_eagle', 'longines', 'chicago_blackhawks', 'john_deere', 'sony_ericsson', 'fifa', 'omega', 'san_francisco_giants', 'bestway', 'too_faced', 'burberry', 'swatch', 'daniel_wellington', 'samsonite', 'fox_head', 'skullcandy', 'glashutte_original', 'captain_america', 'facebook', 'cacharel', 'jack_daniels', 'led_lenser', 'new_york_rangers', 'reebok', 'switch', 'head', 'olympus', 'as_roma', 'hid_global', 'christian_audigier', 'tissot', 'pixar', 'columbus_blue_jackets', 'crocs', 'marcelo_burlon', 'fender', 'batman', 'dior', 'call_of_duty_ghosts', 'carmex', 'hm', 'vancouver_canucks', 'jabra', 'philadelphia_flyers', 'black_panther', 'bose', 'david_yurman', 'ariat', 'miffy', 'dhc', 'slap_chop', 'infusium', 'nashville_predators', 'rosetta_stone', 'pocoyo', 'herbal_essences', 'conair', 'technomarine', 'los_angeles_lakers', 'motorola', 'honeywell', 'kiehls', 'minnesota_vikings', 'san_jose_sharks', 'phoenix_suns', 'new_york_jets', 'hearthstone', 'the_punisher', 'hamilton', 'los_angeles_chargers', 'rayban', 'jack_wills', 'nirvana', 'hamann', 'schwarzkopf', 'concord', 'charlotte_hornets', 'roger_vivier', 'wwe', 'r4', 'smith_wesson', 'belkin', 'anaheim_ducks', 'givenchy', 'instantly_ageless', 'bugatti_veyron', 'travis_scott', 'sacramento_kings', 'zippo', 'efest', 'pittsburgh_steelers', 'canon', 'scooby_doo', 'stussy', 'baby_shark', 'jim_beam', 'nintendo', 'the_horus_heresy', 'overwatch', 'new_orleans_pelicans', 'diablo', 'breitling', 'hexbug', 'coty', 'bobbi_brown', 'elvis_presley', 'creative', 'new_balance', 'betty_boop', 'ralph_lauren', 'belstaff', 'dallas_cowboys', 'giuseppe_zanotti', 'awt', 'bill_blass', 'akg_by_harmon', 'denver_nuggets', 'golden_goose', 'colorado_avalanche', 'detroit_red_wings', 'off_white', 'kaporal', 'visa', 'vegas_golden_knights', 'prince', 'beats_by_drdre', 'disney', 'kappa', 'chelsea', 'arizona_diamondbacks', 'oakley', 'st._louis_blues', '7up', 'mercedes_benz', 'houston_texans', 'nfl', 'harley_davidson', 'dragon_ball', 'alpinestars', 'new_york_knicks', 'knvb', 'golds_gym', 'nasa', 'audio_technica', 'calgary_flames', 'los_angeles_kings', 'edmonton_oilers', 'pittsburgh_penguins', 'jurlique', 'citizen', 'ysl', 'ugg', 'giro', 'texas_rangers', 'loewe', 'destiny', 'moose_knuckles', 'san_francisco_49ers', 'casio', 'lancome', 'bunchems', 'toms', 'timberland', 'coogi', 'slazenger', 'carolina_panthers', 'indiana_pacers', 'babolat', 'cazal', 'fear_of_god_essentials', 'everlast', 'kansas_city_chiefs', 'griffin', 'adidas', 'jeep', 'oakland_athletics', 'supreme', 'brooklyn_nets', 'superdry', 'beretta', 'carolina_herrera', 'issey_miyake', 'rado', 'corum', 'forever_21', 'hatchimals', 'nike', 'sisley', 'daiwa', 'jack_jones', 'mophie', 'celine', 'philadelphia_eagles', 'yeti', 'fullips', 'fendi', 'the_rolling_stones', 'boston_bruins', 'vacheron_constantin', 'ulysse_nardin', 'van_cleef_arpels', 'roxy', 'koss', 'compaq', 'streamlight', 'miami_heat', 'new_york_islanders', 'big_green_egg', 'cleveland_cavaliers', 'gant', 'deadpool', 'converse', 'miu_miu', 'babyliss', 'popsockets', 'bontrager', 'portugal', 'usa', 'apple', 'piaget', 'ozark', 'epson', 'dyson', 'htc', 'chanel', 'valentino_garavani', 'ac_dc', 'pj_masks', 'nickelodeon', 'specialized', 'new_orleans_saints', 'copper_fit', 'cincinnati_reds', 'amiibo', 'coca_cola', 'wallykazam', 'boston_red_sox', 'lg', 'cartier', 'fitbit', 'cnd', 'footjoy', 'luke_combs', 'ariel', 'ping', 'durex', 'clinique', 'hello_kitty', 'beachbody', 'paul_smith', 'harry_potter', 'mbt', 'western_digital', 'elementcase', 'taylormade', 'baltimore_orioles', 'anna_sui', 'furla', 'victorias_secret', 'mlb', 'evisu', 'titleist', 'pinarello', 'lesmills', 'uag']
src_dir = Path("/data01/xu.fx/dataset/NEW_RAW_INCREASE_DATA/wholee_for_logo_0725/")
logo_dict = {}
for i in src_dir.glob("*"):
    logo_dict[i.name] = len([j for j in i.iterdir()])
logo_dict = sorted(logo_dict.items(),key=lambda x:x[1],reverse=True)
# TODO test1
not_support_brand_num = 0
not_support_brand_pic_num = 0
cate_not_support = []
data_not_support = []
for i in logo_dict:
    if i[0] not in logo_list:
        print(i[0])
        cate_not_support.append(i[0])
        data_not_support.append(i[1])
        not_support_brand_num += 1
        not_support_brand_pic_num += i[1]
print("total brand:",len(logo_dict))
print("not support brand:",not_support_brand_num)
print("not support pic num:",not_support_brand_pic_num)
cate = []
data = []
for i in logo_dict:
    cate.append(i[0])
    data.append(i[1])
title = ""
# save_name = "./show_tmp.html"



pie = (Pie()
       .add('', [list(z) for z in zip(cate, data)])
       .set_global_opts(title_opts=opts.TitleOpts(title=title),legend_opts = opts.LegendOpts(is_show = False))
       .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c} ({d}%)"))
       )
pie.render("logo_total.html")

pie = (Pie()
       .add('', [list(z) for z in zip(cate_not_support, data_not_support)])
       .set_global_opts(title_opts=opts.TitleOpts(title=title),legend_opts = opts.LegendOpts(is_show = False))
       .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c} ({d}%)"))
       )
pie.render("./not_support.html")

# c = (
#     Bar()
#     .add_xaxis(cate)
#     .add_yaxis("A", data1)
#     .add_yaxis("B", data2)
#     .set_global_opts(
#         title_opts=opts.TitleOpts(title=title, subtitle=""),
#         #brush_opts=opts.BrushOpts(),
#         datazoom_opts=opts.DataZoomOpts(),
#         toolbox_opts=opts.ToolboxOpts()
#     )
#     .render(save_name)
# )