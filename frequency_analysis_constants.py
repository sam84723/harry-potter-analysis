
HARRY_POTTER_COMPOUNDS = [
    # People / Entities
    ("you know who", "you-know-who"),
    ("he who must not be named", "he_who_must_not_be_named"),
    # ("the boy who lived", "the_boy_who_lived"),
    # ("the chosen one", "the_chosen_one"),
    ("dark lord", "dark_lord"),
    ("death eater", "death_eater"),
    ("death eaters", "death_eaters"),
    ("order of the phoenix", "order_of_the_phoenix"),
    ("dumbledore's army", "dumbledores_army"),
    ("minister of magic", "minister_of_magic"),
    ("ministry of magic", "ministry_of_magic"),

    # Places
    ("diagon alley", "diagon_alley"),
    ("knockturn alley", "knockturn_alley"),
    ("privet drive", "privet_drive"),
    ("grimmauld place", "grimmauld_place"),
    ("godric's hollow", "godrics_hollow"),
    ("hogsmeade village", "hogsmeade_village"),
    ("little whinging", "little_whinging"),
    ("number twelve", "number_twelve"),
    ("platform nine and three quarters", "platform_nine_three_quarters"),
    ("room of requirement", "room_of_requirement"),
    ("chamber of secrets", "chamber_of_secrets"),
    ("forbidden forest", "forbidden_forest"),
    ("great hall", "great_hall"),
    ("common room", "common_room"),
    ("quidditch pitch", "quidditch_pitch"),

    # Magical objects
    ("elder wand", "elder_wand"),
    ("invisibility cloak", "invisibility_cloak"),
    ("philosopher's stone", "philosophers_stone"),
    ("sorcerer's stone", "sorcerers_stone"),
    ("goblet of fire", "goblet_of_fire"),
    ("pensieve memory", "pensieve_memory"),
    ("time turner", "time_turner"),
    ("marauder's map", "marauders_map"),
    ("sorting hat", "sorting_hat"),
    ("howler letter", "howler_letter"),

    # Spells and magic
    ("avada kedavra", "avada_kedavra"),
    ("expecto patronum", "expecto_patronum"),
    # ("imperio curse", "imperio_curse"),
    # ("cruciatus curse", "cruciatus_curse"),
    # ("unforgivable curse", "unforgivable_curse"),
    # ("unforgivable curses", "unforgivable_curses"),
    # ("killing curse", "killing_curse"),
    # ("dark arts", "dark_arts"),
    # ("dark magic", "dark_magic"),
    # ("defensive magic", "defensive_magic"),

    # Creatures
    ("house elf", "house_elf"),
    ("house elves", "house_elves"),
    # ("dementor's kiss", "dementors_kiss"),
    # ("basilisk fang", "basilisk_fang"),
    # ("phoenix feather", "phoenix_feather"),

    # Concepts
    ("pure blood", "pure_blood"),
    ("half blood", "half_blood"),
    ("mud blood", "mud_blood"),
    ("blood status", "blood_status"),
    ("wizarding world", "wizarding_world"),
    ("muggle world", "muggle_world"),
    ("magical education", "magical_education"),

    # Common expressions
    # ("all right", "all_right"),
    # ("over there", "over_there"),
    # ("right now", "right_now"),
    # ("long time", "long_time"),
    # ("next day", "next_day"),
    # ("last night", "last_night"),
    # ("few minutes", "few_minutes"),
    # ("few seconds", "few_seconds"),
]

# Common English stop words
STOP_WORDS_GENERIC = {
    'a', 'an', 'the', 'and', 'or', 'but', 'if', 'while', 'as', 'because',
    'is', 'are', 'was', 'were', 'be', 'been', 'being',
    'do', 'does', 'did', 'doing',
    'have', 'has', 'had', 'having',
    'of', 'in', 'on', 'at', 'by', 'for', 'to', 'from', 'with', 'about', 'into', 'through',
    'this', 'that', 'these', 'those',
    'it', 'its', 'they', 'them', 'their', 'theirs',
    'he', 'him', 'his', 'she', 'her', 'hers', 'you', 'your', 'yours',
    'we', 'our', 'ours', 'us', 'i', 'me', 'my', 'mine',
    'not', 'no', 'nor', 'only', 'own', 'same', 'so', 'too', 'very',
    'can', 'could', 'would', 'should', 'will', 'shall', 'may', 'might', 'must',
    'then', 'than', 'once', 'when', 'where', 'why', 'how',
    'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such'
}

STOP_WORDS_HP = {
    'said', 'asked', 'told', 'replied',
    'looked', 'looking', 'look', 'watched',
    'went', 'come', 'came', 'going', 'got', 'gone',
    'back', 'down', 'up', 'around', 'over',
    'thought', 'think', 'know', 'knew',
    'saw', 'see', 'seen',
    'still', 'just', 'right', 'well',
    'never', 'ever',
    'now', 'then',
    'first', 'last', 'next',
    'yeh', 'yer',  # Hagrid-specific speech patterns :)
    'yeah', 'oh', 'ah', 'uh'
}



# STOP_WORDS = set(stopwords.words('english'))

STOP_NAMES = {
    # 'harry', 'ron', 'hagrid', 'hermione', 'professor', 'snape', 'dumbledore',
    # 'malfoy', 'potter', 'neville', 'vernon'
}










# Main characters (appear frequently throughout the series)
MAIN_CHARACTERS = [
    "harry", "ron", "hermione", "dumbledore", "snape", "voldemort", 
    "sirius", "lupin", "molly", "arthur", "ginny", "neville", 
    "hagrid", "mcgonagall", "malfoy", "bellatrix", "luna", "cho",
    "dobby", "vernon"
]

# Side characters (appear less frequently)
SIDE_CHARACTERS = [
    "pettigrew", "james", "lily", "fred", "george", "percy", "bill", "charlie",
    "tonks", "kingsley", "moody", "cedric", "fleur", "krum", "lockhart",
    "quirrell", "umbridge", "slughorn", "flitwick", "sprout", "trelawney",
    "binns", "filch", "pomfrey", "hooch", "sirius", "remus", "peter",
    "lucius", "narcissa", "crabbe", "goyle", "pansy", "blaise", "theodore",
    "dean", "seamus", "lavender", "parvati", "padma", "michael", "terry",
    "anthony", "hannah", "susan", "ernie", "justin", "zacharias", "cormac",
    "oliver", "angelina", "katie", "alicia", "lee", "colin", "romilda",
    "marietta", "penelope", "roger", "marcus", "marcus_flint", "graham",
    "millicent", "bloody_baron", "moaning_myrtle", "nearly_headless_nick",
    "fat_friar", "grey_lady", "helena_ravenclaw", "cuthbert_binns",
    "firenze", "alecto", "amycus", "barty_crouch_jr", "charity_burbage",
    "augustus_rookwood", "antonin_dolohov", "corban_yaxley", "walden_macnair",
    "igor_karkaroff", "alice_longbottom", "frank_longbottom", "regulus_black",
    "rodolphus_lestrange", "rabastan_lestrange", "avery", "nott_sr", "yaxley_sr",
    "selwyn", "travers", "dolohov", "rowle", "gibbon", "mcnair", "carrow",
    "peter_pettigrew", "wormtail", "scabbers", "prongs", "moony", "padfoot",
    "snuffles", "the_marauders", "james_potter", "lily_potter", "sirius_black",
    "remus_lupin", "peter_pettigrew", "albus_dumbledore", "minerva_mcgonagall",
    "severus_snape", "rubeus_hagrid", "filius_flitwick", "pomona_sprout",
    "sybill_trelawney", "cuthbert_binns", "argus_filch", "poppy_pomfrey",
    "rolanda_hooch", "aurora_sinistra", "bathsheba_babbling", "charity_burbage",
    "wilhelmina_grubbly_plank", "firenze", "alastor_moody", "kingsley_shacklebolt",
    "nymphadora_tonks", "bill_weasley", "charlie_weasley", "percy_weasley",
    "fred_weasley", "george_weasley", "ginny_weasley", "molly_weasley",
    "arthur_weasley", "cedric_diggory", "cho_chang", "luna_lovegood",
    "marietta_edgecombe", "michael_corner", "anthony_goldstein", "terry_boot",
    "padma_patil", "lisa_turpin", "sue_li", "mandy_brocklehurst",
    "hannah_abbott", "susan_bones", "ernie_macmillan", "justin_finch_fletchley",
    "zacharias_smith", "wayne_hopkins", "megan_jones", "leanne", "kevin_entwhistle",
    "draco_malfoy", "vincent_crabbe", "gregory_goyle", "pansy_parkinson",
    "blaise_zabini", "theodore_nott", "marcus_flint", "graham_montague",
    "millicent_bulstrode", "adrian_pucey", "cassius_warrington", "miles_bletchley",
    "lucius_malfoy", "narcissa_malfoy", "bellatrix_lestrange", "rodolphus_lestrange",
    "rabastan_lestrange", "augustus_rookwood", "antonin_dolohov", "corban_yaxley",
    "walden_macnair", "igor_karkaroff", "barty_crouch_jr", "peter_pettigrew",
    "wormtail", "scabbers", "prongs", "moony", "padfoot", "snuffles"
]

# Character house mapping for visualization coloring
CHARACTER_HOUSES = {
    # Gryffindor
    "harry": "gryffindor", "ron": "gryffindor", "hermione": "gryffindor",
    "dumbledore": "gryffindor", "sirius": "gryffindor", "lupin": "gryffindor",
    "james": "gryffindor", "lily": "gryffindor", "molly": "gryffindor",
    "arthur": "gryffindor", "ginny": "gryffindor", "neville": "gryffindor",
    "fred": "gryffindor", "george": "gryffindor", "percy": "gryffindor",
    "bill": "gryffindor", "charlie": "gryffindor", "mcgonagall": "gryffindor",
    "hagrid": "gryffindor", "dean": "gryffindor", "seamus": "gryffindor",
    "lavender": "gryffindor", "parvati": "gryffindor", "oliver": "gryffindor",
    "angelina": "gryffindor", "katie": "gryffindor", "alicia": "gryffindor",
    "lee": "gryffindor", "colin": "gryffindor", "romilda": "gryffindor",
    "cormac": "gryffindor", "alice_longbottom": "gryffindor", "frank_longbottom": "gryffindor",
    "nearly_headless_nick": "gryffindor", "nick": "gryffindor", "headless_nick": "gryffindor",
    
    # Slytherin
    "voldemort": "slytherin", "snape": "slytherin", "malfoy": "slytherin",
    "bellatrix": "slytherin", "lucius": "slytherin", "narcissa": "slytherin",
    "crabbe": "slytherin", "goyle": "slytherin", "pansy": "slytherin",
    "blaise": "slytherin", "theodore": "slytherin", "marcus_flint": "slytherin",
    "graham": "slytherin", "millicent": "slytherin", "umbridge": "slytherin",
    "slughorn": "slytherin", "pettigrew": "slytherin", "regulus": "slytherin",
    "rodolphus": "slytherin", "rabastan": "slytherin", "augustus_rookwood": "slytherin",
    "antonin_dolohov": "slytherin", "corban_yaxley": "slytherin", "walden_macnair": "slytherin",
    "barty_crouch_jr": "slytherin", "alecto": "slytherin",
    "amycus": "slytherin", "bloody_baron": "slytherin",
    
    # Ravenclaw
    "luna": "ravenclaw", "cho": "ravenclaw", "lockhart": "ravenclaw",
    "flitwick": "ravenclaw", "trelawney": "ravenclaw", "quirrell": "ravenclaw",
    "marietta": "ravenclaw", "michael": "ravenclaw", "terry": "ravenclaw",
    "anthony": "ravenclaw", "padma": "ravenclaw", "penelope": "ravenclaw",
    "roger": "ravenclaw", "marcus_belby": "ravenclaw", "moaning_myrtle": "ravenclaw",
    "helena_ravenclaw": "ravenclaw", "grey_lady": "ravenclaw", "cuthbert_binns": "unknown",
    
    # Hufflepuff
    "cedric": "hufflepuff", "tonks": "hufflepuff", "sprout": "hufflepuff",
    "hannah": "hufflepuff", "susan": "hufflepuff", "ernie": "hufflepuff",
    "justin": "hufflepuff", "zacharias": "hufflepuff", "fat_friar": "hufflepuff",
    "newt_scamander": "hufflepuff", "pomona_sprout": "hufflepuff",
    
    # No house / Unknown
    "moody": "unknown", "kingsley": "unknown", "firenze": "unknown",
    "filch": "unknown", "pomfrey": "unknown", "hooch": "unknown",
    "igor_karkaroff": "unknown", "barty_crouch_sr": "unknown", "cornelius_fudge": "unknown",
    "rufus_scrimgeour": "unknown", "amos_diggory": "unknown", "dedalus_diggle": "unknown",
    "elphias_doge": "unknown", "aberforth": "unknown", "mundungus": "unknown",
    "sturgis": "unknown", "hestia": "unknown", "marlene": "unknown",
    "fabian": "unknown", "gideon": "unknown", "emmeline": "unknown",
    "edgar_bones": "unknown", "dorcas": "unknown", "benjy": "unknown",
    "madame_maxime": "unknown", "gabrielle": "unknown", "viktor": "unknown",
    "petunia": "unknown", "vernon": "unknown", "dudley": "unknown", "marge": "unknown",
    "dobby": "unknown", "kreacher": "unknown", "fenrir": "unknown", "grindelwald": "unknown",
    "albus_severus": "slytherin", "scorpius": "slytherin", "teddy": "hufflepuff",
    "james_sirius": "gryffindor", "rose": "gryffindor", "dennis": "gryffindor"
}

ALIASES = [
    # Voldemort
    ("lord voldemort", "voldemort"),
    ("tom riddle", "voldemort"),
    ("tom marvolo riddle", "voldemort"),
    ("the dark lord", "voldemort"),
    ("you-know-who", "voldemort"),
    ("he-who-must-not-be-named", "voldemort"),
    ("the heir of slytherin", "voldemort"),

    # Harry Potter
    ("harry potter", "harry"),
    ("harry james potter", "harry"),
    ("potter", "harry"),
    ("the boy who lived", "harry"),
    ("the chosen one", "harry"),

    # Ron Weasley
    ("ron weasley", "ron"),
    ("ronald weasley", "ron"),
    ("ronald bilius weasley", "ron"),
    ("weasley", "ron"),

    # Hermione Granger
    ("hermione granger", "hermione"),
    ("hermione jean granger", "hermione"),
    ("granger", "hermione"),

    # Albus Dumbledore
    ("albus dumbledore", "dumbledore"),
    ("albus percival wulfric brian dumbledore", "dumbledore"),
    ("professor dumbledore", "dumbledore"),
    ("headmaster", "dumbledore"),
    ("albus", "dumbledore"),

    # Severus Snape
    ("severus snape", "snape"),
    ("professor snape", "snape"),
    ("severus", "snape"),

    # Sirius Black
    ("sirius black", "sirius"),
    ("black", "sirius"),
    ("padfoot", "sirius"),
    ("snuffles", "sirius"),

    # Remus Lupin
    ("remus lupin", "lupin"),
    ("professor lupin", "lupin"),
    ("moony", "lupin"),

    # Peter Pettigrew
    ("peter pettigrew", "pettigrew"),
    ("wormtail", "pettigrew"),
    ("scabbers", "pettigrew"),

    # James Potter
    ("james potter", "james"),
    ("prongs", "james"),

    # Lily Potter
    ("lily potter", "lily"),
    ("lily evans", "lily"),

    # Molly Weasley
    ("molly weasley", "molly"),
    ("mrs weasley", "molly"),

    # Arthur Weasley
    ("arthur weasley", "arthur"),
    ("mr weasley", "arthur"),

    # Ginny Weasley
    ("ginny weasley", "ginny"),
    ("ginny", "ginny"),
    ("ginevra weasley", "ginny"),

    # Neville Longbottom
    ("neville longbottom", "neville"),
    ("longbottom", "neville"),

    # Rubeus Hagrid
    ("rubeus hagrid", "hagrid"),
    ("hagrid", "hagrid"),

    # Minerva McGonagall
    ("minerva mcgonagall", "mcgonagall"),
    ("professor mcgonagall", "mcgonagall"),
    ("mcgonagall", "mcgonagall"),

    # Draco Malfoy
    ("draco malfoy", "malfoy"),
    ("malfoy", "malfoy"),

    # Bellatrix Lestrange
    ("bellatrix lestrange", "bellatrix"),
    ("lestrange", "bellatrix"),

    # Luna Lovegood
    ("luna lovegood", "luna"),
    ("lovegood", "luna"),

    # Cho Chang
    ("cho chang", "cho"),
    ("chang", "cho"),

    # Cedric Diggory
    ("cedric diggory", "cedric"),
    ("diggory", "cedric"),

    # Nymphadora Tonks
    ("nymphadora tonks", "tonks"),
    ("tonks", "tonks"),

    # Lucius Malfoy
    ("lucius malfoy", "lucius"),
    ("mr malfoy", "lucius"),

    # Narcissa Malfoy
    ("narcissa malfoy", "narcissa"),
    ("mrs malfoy", "narcissa"),

    # Vincent Crabbe
    ("vincent crabbe", "crabbe"),
    ("crabbe", "crabbe"),

    # Gregory Goyle
    ("gregory goyle", "goyle"),
    ("goyle", "goyle"),

    # Pansy Parkinson
    ("pansy parkinson", "pansy"),
    ("parkinson", "pansy"),

    # Blaise Zabini
    ("blaise zabini", "blaise"),
    ("zabini", "blaise"),

    # Theodore Nott
    ("theodore nott", "theodore"),
    ("nott", "theodore"),

    # Fred Weasley
    ("fred weasley", "fred"),

    # George Weasley
    ("george weasley", "george"),

    # Percy Weasley
    ("percy weasley", "percy"),

    # Bill Weasley
    ("bill weasley", "bill"),
    ("william weasley", "bill"),

    # Charlie Weasley
    ("charlie weasley", "charlie"),
    ("charles weasley", "charlie"),

    # Dean Thomas
    ("dean thomas", "dean"),
    ("thomas", "dean"),

    # Seamus Finnigan
    ("seamus finnigan", "seamus"),
    ("finnigan", "seamus"),

    # Lavender Brown
    ("lavender brown", "lavender"),
    ("brown", "lavender"),

    # Parvati Patil
    ("parvati patil", "parvati"),

    # Padma Patil
    ("padma patil", "padma"),

    # Oliver Wood
    ("oliver wood", "oliver"),
    ("wood", "oliver"),

    # Angelina Johnson
    ("angelina johnson", "angelina"),
    ("johnson", "angelina"),

    # Katie Bell
    ("katie bell", "katie"),
    ("bell", "katie"),

    # Alicia Spinnet
    ("alicia spinnet", "alicia"),
    ("spinnet", "alicia"),

    # Lee Jordan
    ("lee jordan", "lee"),
    ("jordan", "lee"),

    # Colin Creevey
    ("colin creevey", "colin"),
    ("creevey", "colin"),

    # Romilda Vane
    ("romilda vane", "romilda"),
    ("vane", "romilda"),

    # Cormac McLaggen
    ("cormac mclaggen", "cormac"),
    ("mclaggen", "cormac"),

    # Hannah Abbott
    ("hannah abbott", "hannah"),
    ("abbott", "hannah"),

    # Susan Bones
    ("susan bones", "susan"),
    ("bones", "susan"),

    # Ernie Macmillan
    ("ernie macmillan", "ernie"),
    ("macmillan", "ernie"),

    # Justin Finch-Fletchley
    ("justin finch-fletchley", "justin"),
    ("finch-fletchley", "justin"),

    # Zacharias Smith
    ("zacharias smith", "zacharias"),
    ("smith", "zacharias"),

    # Marietta Edgecombe
    ("marietta edgecombe", "marietta"),
    ("edgecombe", "marietta"),

    # Michael Corner
    ("michael corner", "michael"),
    ("corner", "michael"),

    # Terry Boot
    ("terry boot", "terry"),
    ("boot", "terry"),

    # Anthony Goldstein
    ("anthony goldstein", "anthony"),
    ("goldstein", "anthony"),

    # Penelope Clearwater
    ("penelope clearwater", "penelope"),
    ("clearwater", "penelope"),

    # Roger Davies
    ("roger davies", "roger"),
    ("davies", "roger"),

    # Marcus Flint
    ("marcus flint", "marcus_flint"),
    ("flint", "marcus_flint"),

    # Graham Montague
    ("graham montague", "graham"),
    ("montague", "graham"),

    # Millicent Bulstrode
    ("millicent bulstrode", "millicent"),
    ("bulstrode", "millicent"),

    # Dolores Umbridge
    ("dolores umbridge", "umbridge"),
    ("professor umbridge", "umbridge"),
    ("umbridge", "umbridge"),

    # Horace Slughorn
    ("horace slughorn", "slughorn"),
    ("professor slughorn", "slughorn"),
    ("slughorn", "slughorn"),

    # Filius Flitwick
    ("filius flitwick", "flitwick"),
    ("professor flitwick", "flitwick"),
    ("flitwick", "flitwick"),

    # Pomona Sprout
    ("pomona sprout", "sprout"),
    ("professor sprout", "sprout"),
    ("sprout", "sprout"),

    # Sybill Trelawney
    ("sybill trelawney", "trelawney"),
    ("professor trelawney", "trelawney"),
    ("trelawney", "trelawney"),

    # Quirinus Quirrell
    ("quirinus quirrell", "quirrell"),
    ("professor quirrell", "quirrell"),
    ("quirrell", "quirrell"),

    # Gilderoy Lockhart
    ("gilderoy lockhart", "lockhart"),
    ("professor lockhart", "lockhart"),
    ("lockhart", "lockhart"),

    # Alastor Moody
    ("alastor moody", "moody"),
    ("mad-eye moody", "moody"),
    ("moody", "moody"),

    # Kingsley Shacklebolt
    ("kingsley shacklebolt", "kingsley"),
    ("shacklebolt", "kingsley"),

    # Nymphadora Tonks
    ("nymphadora tonks", "tonks"),
    ("tonks", "tonks"),

    # Regulus Black
    ("regulus black", "regulus"),
    ("regulus", "regulus"),

    # Rodolphus Lestrange
    ("rodolphus lestrange", "rodolphus"),
    ("rodolphus", "rodolphus"),

    # Rabastan Lestrange
    ("rabastan lestrange", "rabastan"),
    ("rabastan", "rabastan"),

    # Augustus Rookwood
    ("augustus rookwood", "augustus_rookwood"),
    ("rookwood", "augustus_rookwood"),

    # Antonin Dolohov
    ("antonin dolohov", "antonin_dolohov"),
    ("dolohov", "antonin_dolohov"),

    # Corban Yaxley
    ("corban yaxley", "corban_yaxley"),
    ("yaxley", "corban_yaxley"),

    # Walden Macnair
    ("walden macnair", "walden_macnair"),
    ("macnair", "walden_macnair"),

    # Igor Karkaroff
    ("igor karkaroff", "igor_karkaroff"),
    ("karkaroff", "igor_karkaroff"),

    # Barty Crouch Jr.
    ("barty crouch jr", "barty_crouch_jr"),
    ("barty crouch junior", "barty_crouch_jr"),
    ("crouch jr", "barty_crouch_jr"),

    # Alecto Carrow
    ("alecto carrow", "alecto"),
    ("alecto", "alecto"),

    # Amycus Carrow
    ("amycus carrow", "amycus"),
    ("amycus", "amycus"),

    # Bloody Baron
    ("bloody baron", "bloody_baron"),
    ("baron", "bloody_baron"),

    # Moaning Myrtle
    ("moaning myrtle", "moaning_myrtle"),
    ("myrtle", "moaning_myrtle"),
    ("myrtle warren", "moaning_myrtle"),

    # Nearly Headless Nick
    ("nearly headless nick", "nearly_headless_nick"),
    ("sir nicholas", "nearly_headless_nick"),
    ("nick", "nearly_headless_nick"),

    # Fat Friar
    ("fat friar", "fat_friar"),
    ("friar", "fat_friar"),

    # Grey Lady
    ("grey lady", "grey_lady"),
    ("helena ravenclaw", "helena_ravenclaw"),
    ("helena", "helena_ravenclaw"),

    # Cuthbert Binns
    ("cuthbert binns", "cuthbert_binns"),
    ("professor binns", "cuthbert_binns"),
    ("binns", "cuthbert_binns"),

    # Firenze
    ("firenze", "firenze"),

    # Argus Filch
    ("argus filch", "filch"),
    ("filch", "filch"),

    # Poppy Pomfrey
    ("poppy pomfrey", "pomfrey"),
    ("madam pomfrey", "pomfrey"),
    ("pomfrey", "pomfrey"),

    # Rolanda Hooch
    ("rolanda hooch", "hooch"),
    ("madam hooch", "hooch"),
    ("hooch", "hooch"),

    # Alice Longbottom
    ("alice longbottom", "alice_longbottom"),
    ("alice", "alice_longbottom"),

    # Frank Longbottom
    ("frank longbottom", "frank_longbottom"),
    ("frank", "frank_longbottom"),

    # Marauders collective
    ("the marauders", "marauders"),

    # Dobby
    ("dobby", "dobby"),

    # Kreacher
    ("kreacher", "kreacher"),

    # Dursley Family
    ("petunia dursley", "petunia"),
    ("petunia", "petunia"),
    ("aunt petunia", "petunia"),
    ("vernon dursley", "vernon"),
    ("vernon", "vernon"),
    ("uncle vernon", "vernon"),
    ("dudley dursley", "dudley"),
    ("dudley", "dudley"),
    ("marge dursley", "marge"),
    ("aunt marge", "marge"),
    ("marge", "marge"),

    # Nearly Headless Nick
    ("nearly headless nick", "nearly_headless_nick"),
    ("nick", "nearly_headless_nick"),
    ("headless nick", "nearly_headless_nick"),
    ("sir nicholas", "nearly_headless_nick"),
    ("sir nicholas de mimsy-porpington", "nearly_headless_nick"),
    ("nicholas de mimsy-porpington", "nearly_headless_nick"),

    # Igor Karkaroff
    ("igor karkaroff", "igor_karkaroff"),
    ("karkaroff", "igor_karkaroff"),

    # Barty Crouch Sr.
    ("barty crouch", "barty_crouch_sr"),
    ("barty crouch sr", "barty_crouch_sr"),
    ("mr crouch", "barty_crouch_sr"),

    # Cornelius Fudge
    ("cornelius fudge", "cornelius_fudge"),
    ("fudge", "cornelius_fudge"),
    ("minister fudge", "cornelius_fudge"),

    # Rufus Scrimgeour
    ("rufus scrimgeour", "rufus_scrimgeour"),
    ("scrimgeour", "rufus_scrimgeour"),

    # Amos Diggory
    ("amos diggory", "amos_diggory"),
    ("mr diggory", "amos_diggory"),

    # Dedalus Diggle
    ("dedalus diggle", "dedalus_diggle"),
    ("diggle", "dedalus_diggle"),

    # Elphias Doge
    ("elphias doge", "elphias_doge"),
    ("doge", "elphias_doge"),

    # Aberforth Dumbledore
    ("aberforth dumbledore", "aberforth"),
    ("aberforth", "aberforth"),

    # Mundungus Fletcher
    ("mundungus fletcher", "mundungus"),
    ("mundungus", "mundungus"),

    # Sturgis Podmore
    ("sturgis podmore", "sturgis"),
    ("sturgis", "sturgis"),

    # Hestia Jones
    ("hestia jones", "hestia"),
    ("hestia", "hestia"),

    # Marlene McKinnon
    ("marlene mckinnon", "marlene"),
    ("marlene", "marlene"),

    # Fabian Prewett
    ("fabian prewett", "fabian"),
    ("fabian", "fabian"),

    # Gideon Prewett
    ("gideon prewett", "gideon"),
    ("gideon", "gideon"),

    # Emmeline Vance
    ("emmeline vance", "emmeline"),
    ("emmeline", "emmeline"),

    # Edgar Bones
    ("edgar bones", "edgar_bones"),
    ("edgar", "edgar_bones"),

    # Dorcas Meadowes
    ("dorcas meadowes", "dorcas"),
    ("dorcas", "dorcas"),

    # Benjy Fenwick
    ("benjy fenwick", "benjy"),
    ("benjy", "benjy"),

    # Madame Maxime
    ("madame maxime", "madame_maxime"),
    ("olympe maxime", "madame_maxime"),
    ("maxime", "madame_maxime"),

    # Gabrielle Delacour
    ("gabrielle delacour", "gabrielle"),
    ("gabrielle", "gabrielle"),

    # Viktor Krum
    ("viktor krum", "viktor"),
    ("krum", "viktor"),

    # Fenrir Greyback
    ("fenrir greyback", "fenrir"),
    ("greyback", "fenrir"),

    # Gellert Grindelwald
    ("gellert grindelwald", "grindelwald"),
    ("grindelwald", "grindelwald"),

    # Future generation characters
    ("albus severus potter", "albus_severus"),
    ("albus severus", "albus_severus"),
    ("scorpius malfoy", "scorpius"),
    ("scorpius hyperion malfoy", "scorpius"),
    ("scorpius", "scorpius"),
    ("teddy lupin", "teddy"),
    ("edward lupin", "teddy"),
    ("teddy", "teddy"),
    ("james sirius potter", "james_sirius"),
    ("james sirius", "james_sirius"),
    ("rose granger-weasley", "rose"),
    ("rose weasley", "rose"),
    ("rose", "rose"),
    ("dennis creevey", "dennis"),
    ("dennis", "dennis"),
]
