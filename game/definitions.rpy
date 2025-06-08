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

default visited_locations = set()
default current_location = "mansion_exterior"
default last_location = ""

default completed_actions = set()
default current_scene_visits = {}

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
    def can_visit_location(location):
        """Check if player can visit a location (not just came from there)"""
        return location != current_location
    
    def can_perform_action(action):
        """Check if an action can be performed (hasn't been done recently)"""
        return action not in completed_actions
    
    def mark_action_completed(action):
        """Mark an action as completed to prevent immediate repetition"""
        completed_actions.add(action)
    
    def reset_temporary_actions():
        """Reset actions that can be done again after some time"""
        global completed_actions
        permanent_actions = {"ritual_performed", "curse_broken", "ending_reached"}
        completed_actions = {action for action in completed_actions if action in permanent_actions}
    
    def change_location(new_location):
        """Safely change location and update tracking"""
        global current_location, last_location, visited_locations
        last_location = current_location
        current_location = new_location
        visited_locations.add(new_location)
        
        if new_location not in current_scene_visits:
            current_scene_visits[new_location] = 0
        current_scene_visits[new_location] += 1
    
    def get_scene_visits(location):
        """Get number of times player has visited a scene"""
        return current_scene_visits.get(location, 0)

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
