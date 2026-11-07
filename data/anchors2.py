# Two levels: MACRO region -> list of (state name, lat, lon).
# State names are in Victoria 2's style (historical/regional names), written from memory,
# NOT checked against the game's real state list.
# Map projection fitted from landmarks: x = 8345 + 49*lon ; y = 5073 - 54.8*lat
import math
# Calibrated against 30 real cities in cities.json: x is linear in longitude; y follows a Mercator-like curve,
# corrected by linear interpolation of the residuals at the calibration cities.
_CAL = [(-41.29,7449),(-34.6,6943),(-33.92,6947),(-33.87,6954),(-26.2,6476),(-22.9,6256),(-12.05,5667),(-6.2,5346),
 (-1.29,5121),(1.35,4937),(9.03,4581),(14.69,4274),(21.3,3898),(28.61,3473),(30.04,3402),(35.68,3067),(38.72,2879),
 (38.9,2892),(39.9,2807),(40.42,2774),(41.0,2733),(41.9,2678),(45.42,2487),(48.86,2194),(50.45,2074),(51.5,1992),
 (52.52,1913),(59.33,1315),(59.91,1261)]
def _merc(lat): return 5058 - 2916 * math.log(math.tan(math.pi / 4 + math.radians(lat) / 2))
_RES = sorted((la, y - _merc(la)) for la, y in _CAL)
def _resid(lat):
    if lat <= _RES[0][0]: return _RES[0][1]
    if lat >= _RES[-1][0]: return _RES[-1][1]
    for (a, ra), (b, rb) in zip(_RES, _RES[1:]):
        if a <= lat <= b: return ra + (rb - ra) * (lat - a) / (b - a) if b > a else ra
def proj(lat, lon):
    return 8341.3 + 48.84 * lon, _merc(lat) + _resid(lat)

MACROS = {
"Arctic": [("Greenland",72,-40),("Iceland",65,-18),("Svalbard",78,16),("Jan Mayen",71,-8)],
"Northwest America": [("Alaska",64,-150),("Yukon",64,-135),("Northwest Territories",64,-112),("Arctic Archipelago",74,-95),
   ("British Columbia",54,-125),("Alberta",53,-113),("Pacific Northwest",46,-121)],
"Canada": [("Saskatchewan",52,-105),("Manitoba",51,-97),("Rupert's Land",54,-85),("Labrador",54,-62),("Ontario",47,-80),
   ("Quebec",47,-72),("Maritimes",46,-64),("Newfoundland",48.5,-56)],
"Eastern United States": [("New England",43,-71),("New York",42.5,-75),("Mid-Atlantic",39.5,-77),("Carolinas",35,-80),
   ("Georgia",33,-84),("Florida",28,-82),("Deep South",33,-88),("Ohio Valley",39,-84),("Great Lakes",43,-87),("Tennessee",36,-87),("Louisiana",31,-91.5)],
"Western United States": [("Dakotas",46,-100),("Kansas",38,-98),("Texas",31,-99),("Rocky Mountains",44,-108),
   ("Great Basin",40,-115),("California",37,-120),("Southwest",34,-110),("Hawaii",20.5,-157)],
"Mexico": [("Baja California",28,-113),("Sonora",29,-110),("Chihuahua",28,-106),("Tamaulipas",25,-99),("Jalisco",21,-104),
   ("Mexico",19.5,-99),("Oaxaca",17,-96),("Yucatan",20,-89)],
"Central America": [("Guatemala",15,-90),("Nicaragua",12.5,-85),("Panama",8.5,-80)],
"Caribbean": [("Cuba",22,-79),("Hispaniola",19,-71),("Jamaica",18,-77),("Lesser Antilles",16,-62),("Bahamas",25,-77)],
"Gran Colombia": [("Colombia",5,-74),("Venezuela",8,-66),("Ecuador",-1.5,-78),("Guianas",5,-58)],
"Andes": [("Peru",-9,-75),("Bolivia",-17,-65),("Chile Norte",-23,-69),("Chile Central",-35,-71),("Patagonia",-45,-69),("Tierra del Fuego",-54,-68)],
"Brazil": [("Amazonas",-5,-63),("Para",-3,-52),("Nordeste",-8,-40),("Mato Grosso",-14,-56),("Minas Gerais",-19,-44),("Sao Paulo",-24,-49),("Rio Grande do Sul",-30,-53)],
"River Plate": [("Paraguay",-23,-58),("Uruguay",-33,-56),("Buenos Aires",-35,-62),("Cuyo",-32,-67)],
"Iberia": [("Portugal",39.5,-8),("Castile",40,-4),("Andalusia",37.5,-4.5),("Catalonia",41.5,1.5),("Galicia (Spain)",42.8,-8)],
"France": [("Aquitaine",44,0),("Ile-de-France",48.5,2.5),("Brittany",48,-2.5),("Provence",44,5),("Lorraine",48.5,6),("Normandy",49,0)],
"British Isles": [("England",52.5,-1.5),("Wales",52,-3.5),("Scotland",57,-4),("Ireland",53,-8)],
"Low Countries": [("Belgium",50.8,4.5),("Netherlands",52.3,5)],
"Germany": [("Rhineland",50.5,7.5),("Bavaria",48.5,11.5),("Brandenburg",52.5,13),("Saxony",51,13),("Hanover",52.5,9.5),("Pomerania",54,16),("East Prussia",54,21),("Silesia",51,17)],
"Austria-Hungary": [("Austria",47.8,14),("Bohemia",50,15),("Hungary",47,19),("Galicia",49.7,22.5),("Transylvania",46,25),("Croatia",45,16)],
"Switzerland": [("Switzerland",46.8,8.2)],
"Italy": [("Piedmont",45,8),("Lombardy",45.5,10),("Tuscany",43.5,11),("Papal States",42,13),("Naples",40.5,15),("Sicily",37.5,14),("Sardinia",40,9),("Corsica",42,9)],
"Balkans": [("Serbia",44,21),("Wallachia",44,25),("Bulgaria",42.5,25),("Macedonia",41,22),("Albania",41,20),("Greece",38.5,22)],
"Scandinavia": [("Denmark",56,10),("Norway South",60,9),("Norway North",68,16),("Sweden South",58,14),("Sweden North",64,18),("Finland",62,26)],
"Baltic": [("Livonia",58,25),("Lithuania",55,24),("Poland",52,21)],
"Western Russia": [("Belarus",53.5,28),("Kiev",49.5,31),("Kharkov",49,37),("Bessarabia",46.5,30),("Crimea",45,34),("Don",47,40),
   ("Moscow",55.7,37.6),("St Petersburg",59.9,30),("Karelia",62,34),("Archangelsk",64,41),("Kazan",55.8,49),("Saratov",52,47),("Astrakhan",46,48),("Urals",56,60),("Orenburg",51.5,55)],
"Caucasus": [("Kuban",44,42),("Georgia (Caucasus)",42,44),("Armenia",40,45),("Azerbaijan",40.5,48.5)],
"Anatolia": [("Anatolia West",38.5,30),("Anatolia East",39,39),("Constantinople",41,29)],
"Levant": [("Syria",35,38),("Palestine",32,35.5),("Aleppo",36.5,37.5)],
"Mesopotamia": [("Baghdad",33.3,44),("Basra",30.5,47.5),("Kurdistan",36.5,43)],
"Arabia": [("Hejaz",24,40),("Najd",25,45),("Hasa",25.5,50),("Oman",21,57),("Yemen",15.5,45)],
"Persia": [("Azerbaijan (Persia)",37.5,46),("Tehran",35.7,51.4),("Fars",31,53),("Khorasan",36,59),("Khuzestan",31,49),("Kerman",28,59)],
"Central Asia": [("Kabul",34.5,69),("Kandahar",31.5,65),("Herat",34,62),("Turkmenistan",39,59),("Bukhara",40,66),("Tajikistan",38.5,70.5),
   ("Kazakh West",48,57),("Kazakh Central",48,68),("Semirechye",45,78),("Kyrgyzstan",41.5,75)],
"Xinjiang and Tibet": [("Tarim Basin",40,82),("Dzungaria",44,87),("Tibet",31,90),("Qinghai",36,96)],
"Northern India": [("Sindh",26,68),("Baluchistan",28.5,65),("Punjab",31,74),("Kashmir",34,76),("Rajputana",26.5,73.5),("Delhi",28.6,77),("Oudh",26.5,81),("Bihar",25.5,85),("Nepal",28,84)],
"Eastern India": [("Bengal",23.5,88),("Orissa",20.5,85),("Assam",26,93),("Central Provinces",23,78)],
"Southern India": [("Gujarat",22.5,72),("Maharashtra",19,75),("Hyderabad",17.5,78.5),("Mysore",13.5,76),("Tamil Nadu",11,78.5),("Kerala",10,76.5),("Ceylon",7.5,80.7)],
"Burma": [("Upper Burma",22,96),("Lower Burma",17,96),("Arakan",20,93.5)],
"Indochina": [("Siam",15,101),("Laos",19,102.5),("Tonkin",21.5,105.5),("Annam",16,108),("Cochinchina",10.5,106),("Cambodia",12.5,104.5),("Malaya",4.5,102)],
"Indonesia": [("Sumatra North",3,98),("Sumatra South",-3,104),("West Java",-6.8,107),("East Java",-7.7,112),("Borneo North",3,115),("Borneo South",-1,114),("Celebes",-2,120),("Moluccas",-3,128),("Lesser Sundas",-9,120)],
"Philippines": [("Luzon",16,121),("Mindanao and Visayas",8,125)],
"Mongolia": [("Outer Mongolia North",48,103),("Gobi",43,108),("Inner Mongolia",41,112)],
"Manchuria and Korea": [("Heilongjiang",50,128),("Jilin",45,126),("Liaoning",41.5,123),("Korea North",40,127),("Korea South",36.5,127.5)],
"North China": [("Zhili",39.5,116),("Shandong",36.5,118),("Shanxi",37.5,112),("Shaanxi",34.5,109),("Gansu",37,103),("Henan",34,113)],
"Central China": [("Jiangsu",32,119),("Anhui",31.5,117),("Hubei",31,113),("Hunan",27.5,112),("Jiangxi",28,116),("Zhejiang",29.5,120),("Sichuan",30.5,104)],
"South China": [("Fujian",26,118),("Guangdong",23.5,113),("Guangxi",23.5,108),("Guizhou",26.5,106.5),("Yunnan",25,101),("Hainan",19.5,109.8),("Taiwan",23.7,121)],
"Japan": [("Hokkaido",43,142),("Tohoku",39.5,140.5),("Kanto",36,139.5),("Chubu",36,137),("Kansai",34.8,135.5),("Chugoku",34.8,132.5),("Shikoku",33.7,133.5),("Kyushu",32.8,130.8)],
"Siberia": [("West Siberia",60,70),("Tomsk",57,85),("Krasnoyarsk",62,92),("Irkutsk",53,105),("Yakutia",63,128),("Yakutia North",70,130),("Taymyr",72,100),
   ("Primorye",46,134),("Okhotsk",60,150),("Kamchatka",56,160),("Chukotka",66,172),("Sakhalin",51,143)],
"Australia": [("Western Australia",-26,121),("Northern Territory",-19,133),("Queensland",-22,145),("South Australia",-31,135),("New South Wales",-32,148),("Victoria",-37,144.5),("Tasmania",-42,147)],
"New Zealand": [("North Island",-38,175.5),("South Island",-44,170)],
"Pacific": [("New Guinea West",-4,138),("New Guinea East",-6,146),("Melanesia",-9,160),("Fiji",-17.5,178),("Polynesia",-17,-150),("Micronesia",7,158)],
"Maghreb": [("Morocco",33,-6),("Western Sahara",24,-13),("Oran",35,-0.5),("Algiers",36,3),("Constantine",36,6.5),("Algerian Sahara",28,3),("Tunisia",34.5,9.5)],
"Libya": [("Tripolitania",32.5,13.5),("Cyrenaica",31,21),("Fezzan",27,14),("Kufra",24,23)],
"Egypt and Sudan": [("Lower Egypt",30.5,31),("Upper Egypt",26,32),("Nubia",19,31.5),("Khartoum",14,32),("Kordofan",12.5,29),("Darfur",13,25)],
"Sahel": [("Mauritania",20,-11),("Timbuktu",17,-3),("Bamako",12.5,-7.5),("Niger",16,8),("Chad",14,18),("Tibesti",20,17),("Upper Volta",12.5,-2)],
"West Africa": [("Senegal",14.5,-15),("Guinea",10.5,-12),("Sierra Leone",7,-11),("Ivory Coast",7,-5.5),("Gold Coast",7,-1.5),("Dahomey",8,2),("Sokoto",11.5,7.5),("Yorubaland",7.5,4),("Niger Delta",5.5,7)],
"Central Africa": [("Cameroon",5,12),("Ubangi",6,21),("Gabon",-0.5,11.5),("Middle Congo",-3,15),("Lower Congo",-5,15),("Kasai",-6,22),("Katanga",-10,26),("Kivu",-2,28)],
"Southwest Africa": [("Angola North",-9,15),("Angola South",-14,16),("Ovamboland",-22,17),("Namaqualand",-29,18)],
"Southern Africa": [("Bechuanaland",-22,24),("Rhodesia",-19,30),("Zambia",-14,27),("Nyasaland",-13,34),("Mozambique",-18,35),("Transvaal",-26,28.5),("Natal",-29,30.5),("Orange Free State",-29,26.5),("Cape Colony",-33.5,22)],
"East Africa": [("Tanganyika",-6.5,35),("Uganda",1.5,32.5),("Kenya",0,38),("Zanzibar",-6,39.3),("Rwanda-Urundi",-2.5,30)],
"Horn of Africa": [("Somalia North",9,46),("Somalia South",3,45),("Ethiopia",9,39),("Eritrea",15.5,39),("Ogaden",7,44)],
"Madagascar": [("Madagascar North",-15,48),("Madagascar South",-22,46.5)],
}
ANCHORS = [(state, macro, *proj(lat, lon)) for macro, lst in MACROS.items() for state, lat, lon in lst]
