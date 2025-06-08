# game/definitions.rpy
define narrator = Character(None, kind=nvl)
define player = Character("You", color="#c8ffc8")
define butler = Character("Edmund", color="#a0a0ff")
define ghost = Character("???", color="#ff9999")
define detective = Character("Detective Mills", color="#ffff99")

define townsperson = Character("Village Elder", color="#8fbc8f")
define librarian = Character("Ms. Blackwood", color="#dda0dd")
define groundskeeper = Character("Old Tom", color="#cd853f")
define medium = Character("Madame Zelda", color="#9370db")
define historian = Character("Professor Williams", color="#4682b4")
define sarah = Character("Cousin Sarah", color="#f0e68c")

image bg mansion_exterior = "#2c1810"
image bg foyer = "#3d2817"
image bg library = "#4a3423"
image bg dining_room = "#3d2b1a"
image bg cellar = "#1a1a1a"
image bg attic = "#2f2419"
image bg bedroom = "#4a3829"
image bg greenhouse = "#2d4a2d"
image bg cemetery = "#1a1a2d"
image bg music_room = "#3d2d4a"
image bg observatory = "#2d2d4a"
image bg town_square = "#4a4a3d"
image bg panic_room = "#1a1a1a"

default has_key = False
default has_flashlight = False
default knows_secret = False
default butler_trust = 0
default rooms_explored = 0
default found_clues = []
default selected_choices = set()

default sanity = 100
default paranoia_level = 0
default current_time = 18
default days_survived = 1
default inventory = []
default documents_found = []
default edmund_possession_level = 0
default can_trust_edmund = True
default sarah_mystery_unlocked = False
default town_conspiracy_known = False

default evidence_board = {}
default investigation_path = "none"
default theories_formed = []

default achievements = {
    "detective": False,
    "pacifist": False,
    "scholar": False,
    "survivor": False,
    "truth_seeker": False,
    "family_historian": False
}

init python:
    if persistent.total_achievements is None:
        persistent.total_achievements = {
            "detective": False,
            "pacifist": False,
            "scholar": False,
            "survivor": False,
            "truth_seeker": False,
            "family_historian": False
        }
    
    if persistent.playthroughs is None:
        persistent.playthroughs = 0
    
    if persistent.endings_seen is None:
        persistent.endings_seen = set()
