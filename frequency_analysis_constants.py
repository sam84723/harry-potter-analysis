
HARRY_POTTER_COMPOUNDS = [
    # Personnes/Entités
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

    # Lieux
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

    # Objets magiques
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

    # Sorts et magie
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

    # Créatures
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

    # Expressions courantes
    # ("all right", "all_right"),
    # ("over there", "over_there"),
    # ("right now", "right_now"),
    # ("long time", "long_time"),
    # ("next day", "next_day"),
    # ("last night", "last_night"),
    # ("few minutes", "few_minutes"),
    # ("few seconds", "few_seconds"),
]

# Stop words anglais communs
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
    'yeh', 'yer',  # particularités de Hagrid :)
    'yeah', 'oh', 'ah', 'uh'
}



# STOP_WORDS = set(stopwords.words('english'))

STOP_NAMES = {
    # 'harry', 'ron', 'hagrid', 'hermione', 'professor', 'snape', 'dumbledore',
    # 'malfoy', 'potter', 'neville', 'vernon'
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
    ("potter", "harry"),
    ("the boy who lived", "harry"),
    ("the chosen one", "harry"),

    # Albus Dumbledore
    ("albus dumbledore", "dumbledore"),
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


    # Bellatrix Lestrange
    ("bellatrix lestrange", "bellatrix"),
    ("lestrange", "bellatrix"),

    # Collectif Marauders
    ("the marauders", "marauders"),
]
