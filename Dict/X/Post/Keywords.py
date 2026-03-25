
# Keyword lists for Kiruna post classification

# Classification 1: Directly related
# Posts that explicitly mention "Kiruna" (any casing)
DIRECT_KEYWORDS = [
    "kiruna",
]

# Classification 2: Indirectly related
# Posts without "Kiruna" but covering related background topics

# Northern Sweden / geography
NORTHERN_SWEDEN_KEYWORDS = [
    "northern sweden", "north sweden",
    "lapland", "lappland",
    "norrland",
    "norrbotten",
    "arctic sweden", "swedish arctic",
    "swedish lapland",
]

# Mining / iron ore / LKAB
MINING_KEYWORDS = [
    "mining", "mine", "miner", "miners",
    "iron ore", "iron mine",
    "lkab",
    "open pit", "underground mine",
    "malmberget",          # nearby LKAB mine town
    "gruvstad",            # Swedish: mine town
    "gruva", "gruvor",     # Swedish: mine / mines
    "järnmalm",            # Swedish: iron ore
]

# Sámi / indigenous culture
SAMI_KEYWORDS = [
    "sami", "sámi", "saami",
    "indigenous sweden", "indigenous lapland",
    "reindeer herding", "reindeer herder",
    "sameby",              # Swedish: Sámi village unit
    "urfolk",              # Swedish: indigenous people
]

# Rare earth metals / critical minerals
RARE_EARTH_KEYWORDS = [
    "rare earth", "rare-earth",
    "critical mineral", "critical minerals",
    "critical metal", "critical metals",
    "lithium", "cobalt", "vanadium",
    "REE", "LREE", "HREE",
    "sällsynta jordartsmetaller",  # Swedish
]

# Swedish town relocation (without mentioning Kiruna)
TOWN_RELOCATION_KEYWORDS = [
    "town relocation", "city relocation",
    "urban relocation", "relocating city",
    "moving a town", "moving a city",
    "relocate town", "relocate city",
    "town moving", "city moving",
    "stad flyttas", "flytta stad",   # Swedish
    "samhällsflytt",                 # Swedish: community relocation
]

# Spam / noise filters
SPAM_SHORT_LINK_PATTERNS = [
    r"bit\.ly/\w+",
    r"infl\.tv/\w+",
    r"reut\.rs/\w+",
    r"t\.co/\w+",
    r"ow\.ly/\w+",
    r"tinyurl\.com/\w+",
]


SPAM_HASHTAG_THRESHOLD = 6   # posts with ≥ this many hashtags + a short link → spam
