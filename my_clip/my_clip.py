#!/usr/local/bin/python3
# -*- coding:utf-8 -*-
"""
@author: xu.feng
@contact: xfeng_zjut@163.com
"""
import sys
import json
from tqdm import tqdm
from torchsummary import summary
sys.path.append("..")
import numpy as np
import torch
import clip
from PIL import Image
import torch.nn.functional as F
#brand_total = ['3m', '3t', '511_tactical', '7up', 'a_cold_wall', 'a_lange_sohne', 'abercrombie_fitch', 'ac_dc', 'acer', 'addicted', 'adidas', 'ado_den_haag', 'adobe', 'aeronautica_militare', 'afc_ajax', 'agnes_b', 'akg_by_harmon', 'alberta_ferretti', 'alcon', 'alexander_mcqueen', 'alexander_wang', 'alfar_romeo', 'allsaints', 'alpinestars', 'always', 'american_eagle', 'amiibo', 'amiri', 'anaheim_angels', 'anaheim_ducks', 'anna_sui', 'anne_klein', 'apple', 'aquabeads', 'aquascutum', 'arcteryx', 'ariat', 'ariel', 'arizona_cardinals', 'arizona_diamondbacks', 'armani', 'arsenal', 'as_roma', 'asics', 'asos', 'aspinal_of_london', 'atlanta_bravs', 'atlanta_falcons', 'atlanta_hawks', 'atletico_de_madrid', 'audemars_piguet', 'audi', 'audio_technica', 'audioquest', 'aussiebum', 'avengers', 'awt', 'azzaro', 'babolat', 'baby_phat', 'baby_shark', 'babyliss', 'bakugan', 'balenciaga', 'bally', 'balmain', 'baltimore_orioles', 'baltimore_ravens', 'bang_olufsen', 'bape', 'barbie', 'barbour', 'batman', 'baume_et_mercier', 'beachbody', 'beats_by_drdre', 'beautyblender', 'bebe', 'bed_head', 'belkin', 'bell_ross', 'belstaff', 'ben_jerrys', 'benefit', 'benetton', 'benq', 'bentley', 'beretta', 'berluti', 'bestway', 'betty_boop', 'big_green_egg', 'bill_blass', 'billabong', 'bioderma', 'biotherm', 'birkenstock', 'bitdefender', 'bjorn_borg', 'black_panther', 'black_widow', 'blackberry', 'blackberry_smoke', 'blackhawk', 'blancpain', 'blaze_and_the_monster_machines', 'blizzard', 'blu', 'blues_clues', 'bmc_racing', 'bmw', 'bobbi_brown', 'bontrager', 'bosch', 'bose', 'boston_bruins', 'boston_celtics', 'boston_red_sox', 'bottega_veneta', 'brabus', 'braun', 'brazil', 'breeze_smoke', 'breguet', 'breitling', 'bright_bugz', 'brioni', 'brooklyn_nets', 'brut', 'bubble_guppies', 'buffalo_bills', 'buffalo_sabres', 'bugatti_veyron', 'bugslock', 'bulova', 'bunch_o_ballons', 'bunchems', 'burberry', 'burts_bees', 'bushnell', 'butterfly', 'bvb', 'bvlgari', 'c1rca', 'cacharel', 'cadillac', 'calgary_flames', 'call_of_duty_ghosts', 'callaway', 'calvin_klein', 'camelbak', 'canada_goose', 'cannondale', 'canon', 'captain_america', 'cards_against_humanity', 'care_bears', 'carhartt', 'carmex', 'carolina_herrera', 'carolina_hurricanes', 'carolina_panthers', 'carters', 'cartier', 'casio', 'caterpillar', 'cath_kidston', 'cazal', 'celine', 'chanel', 'charlotte_hornets', 'chaumet', 'cheap_monday', 'chelsea', 'chevrolet', 'chevron', 'chi', 'chicago_bears', 'chicago_blackhawks', 'chicago_bulls', 'chicago_cubs', 'chicago_white_sox', 'chloe', 'chopard', 'christian_audigier', 'christian_louboutin', 'chrome_hearts', 'cincinnati_bengals', 'cincinnati_reds', 'cisco', 'citizen', 'clarins', 'clarisonic', 'cleveland_browns', 'cleveland_cavaliers', 'cleveland_golf', 'cleveland_indians', 'clinique', 'cluse', 'cnd', 'coach', 'coca_cola', 'cole_haan', 'colgate', 'colorado_avalanche', 'columbia', 'columbus_blue_jackets', 'comme_des_garcons', 'compaq', 'conair', 'concord', 'converse', 'coogi', 'copper_fit', 'corum', 'coty', 'crabs_adjust_humidity', 'creative', 'crocs', 'crumpler', 'cummins', 'cwc', 'daddario', 'daiwa', 'dallas_cowboys', 'dallas_mavericks', 'dallas_stars', 'daniel_roth', 'daniel_wellington', 'david_yurman', 'davidoff', 'dc_shoes', 'deadpool', 'dean_guitar', 'death_wish_coffee_co', 'def_leppard', 'dell', 'denver_broncos', 'denver_nuggets', 'desigual', 'destiny', 'detroit_lions', 'detroit_pistons', 'detroit_red_wings', 'detroit_tigers', 'dettol', 'dewalt', 'dfb', 'dhc', 'diablo', 'diadora', 'diesel', 'dior', 'disney', 'dkny', 'doctor_strange', 'dolce_gabbana', 'dooney_bourke', 'dr_martens', 'dragon_ball', 'dsquared2', 'ducati', 'dumbo', 'dunhill', 'duracell', 'durex', 'dyson', 'ecco', 'ecko', 'ed_hardy', 'edmonton_oilers', 'efest', 'elementcase', 'elizabeth_arden', 'ellesse', 'elvis_presley', 'england', 'enve', 'eos', 'eotech', 'epson', 'ergobaby', 'escada', 'esp', 'ess', 'estee_lauder', 'everlast', 'evisu', 'facebook', 'fc_barcelona_fcb', 'fc_bayern_munchen', 'fear_of_god_essentials', 'fender', 'fendi', 'ferrari', 'feyenoord', 'fifa', 'fila', 'fingerlings', 'fischer', 'fitbit', 'fjallraven', 'flexfit', 'florida_marlins', 'florida_panthers', 'footjoy', 'foreo', 'forever_21', 'fossil', 'fox_head', 'france', 'franck_muller', 'franco_moschino', 'fred_perry', 'frida_kahlo', 'fuji_film', 'fullips', 'furla', 'furminator', 'game_boy', 'game_of_thrones', 'games_workshop', 'gant', 'gap', 'garmin', 'gazelle', 'ghd', 'gibson', 'gildan', 'gillette', 'girard_perregaux', 'giro', 'giuseppe_zanotti', 'givenchy', 'glashutte_original', 'golden_goose', 'golden_state_warriors', 'golds_gym', 'goo_jit_zu', 'google', 'gopro', 'goyard', 'grado', 'graham', 'grand_seiko', 'green_bay_packers', 'grenco_science', 'griffin', 'grumpy_cat', 'gstar_raw', 'guardians_of_the_galaxy', 'gucci', 'guerlain', 'guess', 'guitar_hero', 'hamann', 'hamilton', 'harley_davidson', 'harry_potter', 'harry_winston', 'hatchimals', 'havaianas', 'head', 'head_shoulders', 'hearthstone', 'helena_rubinstein', 'hello_kitty', 'hennessy', 'herbal_essences', 'hermes', 'heroes_of_the_storm', 'heron_preston', 'hexbug', 'hey_dude', 'hid_global', 'hm', 'hogan', 'hollister_co', 'honda', 'honeywell', 'houston_astros', 'houston_rockets', 'houston_texans', 'hp', 'htc', 'hublot', 'huf', 'hugo_boss', 'hunter', 'hurley', 'hydro_flask', 'hyundai', 'ibanez', 'ice_watch', 'iced_earth', 'imren', 'incase', 'incipio', 'indiana_pacers', 'indianapolis_colts', 'infusium', 'instantly_ageless', 'irobot', 'iron_maiden', 'iron_man', 'issey_miyake', 'iwc', 'jabra', 'jack_daniels', 'jack_jones', 'jack_wills', 'jack_wolfskin', 'jacksonville_jaguars', 'jacob_co', 'jacquemus', 'jaeger_lecoultre', 'jbl', 'jeep', 'jim_beam', 'jimmy_choo', 'john_deere', 'juicy_couture', 'jurlique', 'juul', 'juventus', 'jw_anderson', 'kansas_city_chiefs', 'kansas_royals', 'kaporal', 'kappa', 'kate_spade', 'keen', 'kenan_and_kel', 'kenzo', 'kiehls', 'kingston', 'kipling', 'knvb', 'kobe', 'koss', 'ktm', 'l_oreal', 'la_martina', 'lacoste', 'lamborghini', 'lancome', 'land_rover', 'led_lenser', 'led_zeppelin', 'lego', 'leicester_city_f.c', 'lesmills', 'levis', 'lg', 'lilo_stitch', 'lindberg', 'links_of_london', 'liverpool_fc', 'loewe', 'logitech', 'lol_surprise', 'longchamp', 'longines', 'los_angeles_chargers', 'los_angeles_clippers', 'los_angeles_dodgers', 'los_angeles_kings', 'los_angeles_lakers', 'los_angeles_rams', 'louis_vuitton', 'luke_combs', 'lululemon', 'lyle_scott', 'mac', 'magpul', 'mammut', 'manchester_city', 'manchester_united', 'manolo_blahnik', 'marc_jacobs', 'marcelo_burlon', 'marlboro', 'marshall', 'martin_co', 'marvel', 'maserati', 'maui_jim', 'max_factor', 'maybelline', 'mbt', 'mcm', 'memphis_grizzlies', 'mercedes_benz', 'merrell', 'metallica', 'miami_dolphins', 'miami_heat', 'michael_kors', 'miffy', 'milwaukee_brewers', 'milwaukee_bucks', 'minesota_twins', 'minnesota_timberwolves', 'minnesota_vikings', 'minnesota_wild', 'miu_miu', 'mizuno', 'mlb', 'mms', 'monchhichi', 'moncler', 'monster_energy', 'montblanc', 'montreal_canadiens', 'montreal_expos', 'moose_knuckles', 'mophie', 'motorhead', 'motorola', 'movado', 'muhammad_ali', 'mulberry', 'nasa', 'nashville_predators', 'nba', 'new_balance', 'new_england_patriots', 'new_era', 'new_jersey_devils', 'new_orleans_pelicans', 'new_orleans_saints', 'new_york_giants', 'new_york_islanders', 'new_york_jets', 'new_york_knicks', 'new_york_mets', 'new_york_rangers', 'new_york_yankees', 'nfl', 'nickelodeon', 'nike', 'nintendo', 'nirvana', 'nixon', 'nokia', 'nutribullet', 'oakland_athletics', 'oakland_raiders', 'oakley', 'off_white', 'oklahoma_city_thunder', 'olympique_marseille', 'olympus', 'omega', 'opi', 'oral_b', 'orlando_magic', 'ottawa_senators', 'otter_box', 'overwatch', 'oxo', 'ozark', 'paco_rabanne', 'palace', 'palm_angels', 'pampers', 'pandora', 'panerai', 'pantene', 'paris_saint_germain', 'patagonia', 'patek_philippe', 'paul_frank', 'paul_shark', 'paul_smith', 'pearl_izumi', 'philadelphia_76ers', 'philadelphia_eagles', 'philadelphia_flyers', 'philadelphia_phillies', 'philipp_plein', 'phiten', 'phoenix_coyotes', 'phoenix_suns', 'piaget', 'pinarello', 'ping', 'pink_floyd', 'pinko', 'pittsburgh_penguins', 'pittsburgh_steelers', 'pixar', 'pj_masks', 'plantronics', 'playboy', 'playstation', 'pocoyo', 'pokemon', 'pony', 'popsockets', 'porsche', 'portland_trail_blazers', 'portugal', 'power_rangers', 'prada', 'premier_league', 'prince', 'pro_kennex', 'psv', 'puma', 'pxg', 'r4', 'rado', 'ralph_lauren', 'raw', 'rayban', 'rb_leipzig', 'rcma', 'red_bull', 'reebok', 'rimowa', 'rip_curl', 'ritchey', 'robo_alive', 'robo_fish', 'roger_dubuis', 'roger_vivier', 'rolex', 'romain_jerome', 'roor', 'rosetta_stone', 'roxy', 'sacramento_kings', 'salomon', 'salvatore_ferragamo', 'samantha_thavasa', 'samsonite', 'san_antonio_spurs', 'san_diego_padres', 'san_francisco_49ers', 'san_francisco_giants', 'san_jose_sharks', 'sanrio', 'schwarzkopf', 'scooby_doo', 'scotty_cameron', 'seagate', 'seattle_seahawks', 'sennheiser', 'sephora', 'shaun_the_sheep', 'shield', 'shimano', 'shimmer_and_shine', 'shiseido', 'shopkins', 'shu_uemura', 'shure', 'sisley', 'sk_ii', 'skin79', 'skoda', 'skullcandy', 'skylanders', 'slap_chop', 'slazenger', 'smith_wesson', 'snow_white', 'sons_of_arthritis', 'sony_ericsson', 'specialized', 'speck', 'spibelt', 'spyderco', 'srixon', 'st._louis_blues', 'st._louis_cardinals', 'st_dupont', 'stan_smith', 'starcraft', 'stefano_ricci', 'streamlight', 'stussy', 'superdry', 'supra', 'supreme', 'swarovski', 'swatch', 'swig', 'switch', 'switcheasy', 'tag_heuer', 'tampa_bay_buccaneers', 'tampa_bay_lightning', 'tampa_bay_rays', 'tapout', 'taylormade', 'tech_deck', 'technomarine', 'tennessee_titans', 'texas_rangers', 'the_allman_brothers_band', 'the_black_crowes', 'the_fairly_oddparents', 'the_horus_heresy', 'the_killers', 'the_loud_house', 'the_north_face', 'the_punisher', 'the_rolling_stones', 'thomas_sabo', 'tide', 'tiffany_co', 'timberland', 'tissot', 'titleist', 'titoni', 'tods', 'tommy_hilfiger', 'toms', 'tonino_lamborghini', 'too_faced', 'toppik', 'toronto_blue_jays', 'toronto_maple_leafs', 'toronto_raptors', 'tory_burch', 'tottenham_hotspur', 'tous', 'toy_watch', 'travis_scott', 'true_religion', 'trx_training', 'tudor', 'uag', 'uboat', 'uefa', 'ugg', 'ulysse_nardin', 'umbro', 'under_armour', 'urban_decay', 'usa', 'usa_basketball', 'utah_jazz', 'vacheron_constantin', 'valentino_garavani', 'van_cleef_arpels', 'vancouver_canucks', 'vans', 'vegas_golden_knights', 'versace', 'victorias_secret', 'visa', 'vivienne_westwood', 'vlone', 'volbeat', 'volcom', 'volkl', 'wallykazam', 'washington_capitals', 'washington_redskins', 'washington_wizards', 'west_ham_united', 'western_digital', 'whirlpool', 'wilson', 'winnipeg_jets', 'world_of_warcraft', 'wrangler', 'wwe', 'xmen', 'xxio', 'yeti', 'yonex', 'ysl', 'zara', 'zegna', 'zelda', 'zenith', 'zigzag', 'zimmermann', 'zippo', 'zumba_fitness']
#brand_total = brand_total[:90] + ["allsaints","american_eagle","hamilton","jack&jones","reebok","maybelline","carolina_herrera","aspinal_of_london","iron_maiden","popsockets"]
brand_total = ["a photo of hermes sandal","a photo of hermes slippers","hermes sandal","hermes slippers","a hermes sandal photo","a photo of hermes sandal, a type of sandal","a hermes slippers photo","a photo of hermes slippers, a type of slippers",
               "a photo of adidas yeezy","a photo of adidas yeezy 350, a type of yeezy shoes","a photo of adidas yeezy 450, a type of yeezy shoes","a yeezy photo of adidas","a shoes photo of adidas yeezy","a picture with adidas yeezy","adidas yeezy",
               "a picture with bottega veneta braided pattern","a photo of van cleef arpels",
               "a photo of pig","a photo of power bank","a photo of usb storage device","a photo of battery","a photo of surveillance camera",
               "a photo of smartwatch","a photo of micro sd storage card"]
brand_total_label = ["hermes","hermes-2","hermes-3","hermes-4","hermes-5","hermes-6","hermes-7","hermes-8",
                     "adidas_yeezy","adidas_yeezy-2","adidas_yeezy-3","adidas_yeezy-4","adidas_yeezy-5","adidas_yeezy-6","adidas_yeezy-7",
                     "bottega_veneta","van_cleef_arpels",
                     "禁销宗教猪","禁销电子类违禁产品充电宝","禁销电子类违禁产品存储设备","禁销电子类违禁产品电池相关","禁销电子类违禁产品监视设备",
                     "禁销电子类违禁产品智能手表","禁销电子类违禁产品SD卡"]
brand_total = [["a photo of hermes sandal","a photo of hermes slippers","hermes sandal","hermes slippers","a hermes sandal photo","a photo of hermes sandal, a type of sandal","a hermes slippers photo","a photo of hermes slippers, a type of slippers"],
               ["a photo of adidas yeezy","a photo of adidas yeezy 350, a type of yeezy shoes","a photo of adidas yeezy 450, a type of yeezy shoes","a yeezy photo of adidas","a shoes photo of adidas yeezy","a picture with adidas yeezy","adidas yeezy"],
               ["a picture with bottega veneta braided pattern"], ["a photo of van cleef arpels"],
               ["a photo of pig"], ["a photo of power bank"], ["a photo of usb storage device"], ["a photo of battery"],
               ["a photo of surveillance camera"],
               ["a photo of smartwatch"], ["a photo of micro sd storage card"]
               ]
brand_total_label = ["hermes","adidas_yeezy","bottega_veneta","van_cleef_arpels",
                     "禁销宗教猪","禁销电子类违禁产品充电宝","禁销电子类违禁产品存储设备","禁销电子类违禁产品电池相关","禁销电子类违禁产品监视设备",
                     "禁销电子类违禁产品智能手表","禁销电子类违禁产品SD卡"]


brand_total = ["hermes sandal","adidas yeezy",
               "bottega veneta","van cleef arpels",
               "pig","power bank","usb storage device","battery","surveillance camera",
               "smartwatch","micro sd storage card"]
brand_total_label = ["hermes",
                     "adidas_yeezy",
                     "bottega_veneta","van_cleef_arpels",
                     "禁销宗教猪","禁销电子类违禁产品充电宝","禁销电子类违禁产品存储设备","禁销电子类违禁产品电池相关","禁销电子类违禁产品监视设备",
                     "禁销电子类违禁产品智能手表","禁销电子类违禁产品SD卡"]
brand_total_np = np.array(brand_total_label)
device = "cuda:0" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("RN101.pt", device=device)#['RN50', 'RN101', 'RN50x4', 'RN50x16', 'RN50x64', 'ViT-B/32', 'ViT-B/16', 'ViT-L/14', 'ViT-L/14@336px']
imagenet_templates = [
    'a bad photo of a {}.',
    'a photo of many {}.',
    'a sculpture of a {}.',
    'a photo of the hard to see {}.',
    'a low resolution photo of the {}.',
    'a rendering of a {}.',
    'graffiti of a {}.',
    'a bad photo of the {}.',
    'a cropped photo of the {}.',
    'a tattoo of a {}.',
    'the embroidered {}.',
    'a photo of a hard to see {}.',
    'a bright photo of a {}.',
    'a photo of a clean {}.',
    'a photo of a dirty {}.',
    'a dark photo of the {}.',
    'a drawing of a {}.',
    'a photo of my {}.',
    'the plastic {}.',
    'a photo of the cool {}.',
    'a close-up photo of a {}.',
    'a black and white photo of the {}.',
    'a painting of the {}.',
    'a painting of a {}.',
    'a pixelated photo of the {}.',
    'a sculpture of the {}.',
    'a bright photo of the {}.',
    'a cropped photo of a {}.',
    'a plastic {}.',
    'a photo of the dirty {}.',
    'a jpeg corrupted photo of a {}.',
    'a blurry photo of the {}.',
    'a photo of the {}.',
    'a good photo of the {}.',
    'a rendering of the {}.',
    'a {} in a video game.',
    'a photo of one {}.',
    'a doodle of a {}.',
    'a close-up photo of the {}.',
    'a photo of a {}.',
    'the origami {}.',
    'the {} in a video game.',
    'a sketch of a {}.',
    'a doodle of the {}.',
    'a origami {}.',
    'a low resolution photo of a {}.',
    'the toy {}.',
    'a rendition of the {}.',
    'a photo of the clean {}.',
    'a photo of a large {}.',
    'a rendition of a {}.',
    'a photo of a nice {}.',
    'a photo of a weird {}.',
    'a blurry photo of a {}.',
    'a cartoon {}.',
    'art of a {}.',
    'a sketch of the {}.',
    'a embroidered {}.',
    'a pixelated photo of a {}.',
    'itap of the {}.',
    'a jpeg corrupted photo of the {}.',
    'a good photo of a {}.',
    'a plushie {}.',
    'a photo of the nice {}.',
    'a photo of the small {}.',
    'a photo of the weird {}.',
    'the cartoon {}.',
    'art of the {}.',
    'a drawing of the {}.',
    'a photo of the large {}.',
   'a black and white photo of a {}.',
    'the plushie {}.',
    'a dark photo of a {}.',
    'itap of a {}.',
    'graffiti of the {}.',
    'a toy {}.',
    'itap of my {}.',
    'a photo of a cool {}.',
    'a photo of a small {}.',
    'a tattoo of the {}.',
]
def zeroshot_classifier(classnames, templates):
    with torch.no_grad():
        zeroshot_weights = []
        for classname in tqdm(classnames):
            texts = [template.format(classname) for template in templates] #format with class
            texts = clip.tokenize(texts).cuda() #tokenize
            class_embeddings = model.encode_text(texts) #embed with text encoder
            class_embeddings /= class_embeddings.norm(dim=-1, keepdim=True)
            class_embedding = class_embeddings.mean(dim=0)
            class_embedding /= class_embedding.norm()
            zeroshot_weights.append(class_embedding)
        zeroshot_weights = torch.stack(zeroshot_weights, dim=1).cuda()
    return zeroshot_weights
def zeroshot_classifier2(brand_total):
    with torch.no_grad():
        zeroshot_weights = []
        for classname in tqdm(brand_total):
            texts = classname
            texts = clip.tokenize(texts).cuda() #tokenize
            class_embeddings = model.encode_text(texts) #embed with text encoder
            class_embeddings /= class_embeddings.norm(dim=-1, keepdim=True)
            class_embedding = class_embeddings.mean(dim=0)
            class_embedding /= class_embedding.norm()
            zeroshot_weights.append(class_embedding)
        zeroshot_weights = torch.stack(zeroshot_weights, dim=1).cuda()
    return zeroshot_weights

zeroshot_weights = zeroshot_classifier(brand_total, imagenet_templates)
#zeroshot_weights = zeroshot_classifier2(brand_total)
to_json = {}
for i,v in enumerate(brand_total):
    to_json[v] = zeroshot_weights[:,i].cpu().numpy().tolist()
with open("./RN101_labels.json", 'w') as f:
    json.dump(dict(to_json), f)
#print(zeroshot_weights.shape)

# text = clip.tokenize(brand_total).to(device)
# text_features = model.encode_text(text)
# #text_features = torch.cat((text_features,pic_features),dim=0)
# text_features_nor = F.normalize(text_features,dim=1)
# # text_features /= text_features.norm(dim=-1, keepdim=True)
def clip_func(img,top_n):
    image = preprocess(Image.open(img)).unsqueeze(0).to(device)
    with torch.no_grad():
        logits_per_image, logits_per_text = model(image, text)
        probs = logits_per_image.softmax(dim=-1).cpu().numpy()
        indices = (-probs[0]).argsort()[:top_n]
        res = []
        for logo,score in zip(brand_total_np[indices],probs[0][indices]):
            logo = logo.replace("a photo of ","").replace(" brand","")
            res.append({"logo_name":logo,"score":score})
        return {"res":res}
        # print(image_features.shape,text_features.shape)
        # print(logits_per_image.shape, logits_per_text.shape)
        # print(logits_per_image, logits_per_text)
def clip_func2(img,top_n,soft_max=False):
    image = preprocess(Image.open(img)).unsqueeze(0).to(device)
    with torch.no_grad():
        image_features = model.encode_image(image)
        image_features_nor = F.normalize(image_features)
        # print(image_features.shape,image_features_nor.shape)
        #print(text_features.shape)
        if soft_max:
            cos_sim = (image_features_nor.mm(text_features_nor.T)*100).softmax(dim=-1).cpu().numpy()
            # image_features /= image_features.norm(dim=-1, keepdim=True)
            # cos_sim = (100.0 * image_features @ text_features.T).softmax(dim=-1).cpu().numpy()
        else:
            cos_sim = image_features_nor.mm(text_features_nor.T).cpu().numpy()
        indices = (-cos_sim[0]).argsort()[:top_n]
        res = []
        for logo, score in zip(brand_total_np[indices], cos_sim[0][indices]):
            #logo = logo.replace("a photo of ", "")
            #logo = brand_total_label[brand_total.index(logo)]
            res.append({"logo_name": logo, "score": score})
        return {"res": res}
def clip_func3(img,top_n,soft_max=False):
    image = preprocess(Image.open(img)).unsqueeze(0).to(device)
    #print(type(image),image.shape)
    #print(image.mean())
    with torch.no_grad():
        image_features = model.encode_image(image)
        #print(image_features)
        #print(image_features.mean())
        #image_features_nor = F.normalize(image_features)
        image_features /= image_features.norm(dim=-1, keepdim=True)
        #print(image_features.mean())
        if soft_max:
            #cos_sim = (image_features_nor.mm(text_features_nor.T)*100).softmax(dim=-1).cpu().numpy()
            cos_sim = (100.0 * image_features @ zeroshot_weights).softmax(dim=-1).cpu().numpy()
        else:
            cos_sim = (image_features @ zeroshot_weights).cpu().numpy()
        indices = (-cos_sim[0]).argsort()[:top_n]
        res = []
        for logo, score in zip(brand_total_np[indices], cos_sim[0][indices]):
            #logo = logo.replace("a photo of ", "")
            #logo = brand_total_label[brand_total.index(logo)]
            res.append({"logo_name": logo, "score": score})
        return {"res": res}

if __name__=="__main__":
    img = "/data01/xu.fx/dataset/CLIP_DATASET/fordeal_test_data/brand_labeled/hermes/hermes_0afd8ef7-9866-4f1f-903a-b33c3724f531-1200x1200.jpeg"
    img_dir = "/data01/xu.fx/dataset/CLIP_DATASET/fordeal_test_data/brand_labeled/禁销电子类违禁产品存储设备/"
    #print(clip.available_models())
    res = clip_func3(img, 5,soft_max=False)
    # res2 = clip_func(img, 5)
    print(res)
    # print(res2)

    # for k,i in enumerate(Path(img_dir).rglob("*.*")):
    #     res = clip_func2(str(i),2)
    #     print(k,i.name,res["res"])

    # image_dir =
    # image_list = [p for p in Path(image_dir).rglob('*.*')]
    # for index, image_path in tqdm(enumerate(image_list)):
    #     if not is_img(image_path.name) or image_path.name[0]==".":
    #         continue

# print("Label probs:", probs)  # prints: [[0.9927937  0.00421068 0.00299572]]

