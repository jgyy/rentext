# game/script.rpy
define narrator = Character(None, kind=nvl)
define player = Character("You", color="#c8ffc8")
define butler = Character("Edmund", color="#a0a0ff")
define ghost = Character("???", color="#ff9999")
define detective = Character("Detective Mills", color="#ffff99")

default has_key = False
default has_flashlight = False
default knows_secret = False
default butler_trust = 0
default rooms_explored = 0
default found_clues = []

default selected_choices = set()

image bg mansion_exterior = "#2c1810"
image bg foyer = "#3d2817"
image bg library = "#4a3423"
image bg dining_room = "#3d2b1a"
image bg cellar = "#1a1a1a"
image bg attic = "#2f2419"
image bg bedroom = "#4a3829"

label start:
    
    scene bg mansion_exterior
    with fade
    
    play music "audio/spooky_ambience.ogg" fadeout 1.0 fadein 2.0
    
    narrator "The rain pounds against your car windshield as you pull up to Ravenshollow Manor."
    narrator "Lightning illuminates the Victorian mansion's Gothic towers and crumbling stonework."
    narrator "You've inherited this place from a great aunt you never knew existed."
    narrator "The lawyer's letter mentioned 'unusual circumstances' surrounding her death..."
    
    player "Well, no turning back now."
    
    narrator "You grab your bag and run through the downpour to the massive oak front door."
    narrator "An ornate brass knocker shaped like a raven's head stares down at you."
    
    menu:
        "{color=#888888}Knock on the door{/color}" if "knock_door" in selected_choices:
            $ selected_choices.add("knock_door")
            jump knock_door
        "Knock on the door" if "knock_door" not in selected_choices:
            $ selected_choices.add("knock_door")
            jump knock_door
        "{color=#888888}Try the door handle{/color}" if "try_handle" in selected_choices:
            $ selected_choices.add("try_handle")
            jump try_handle
        "Try the door handle" if "try_handle" not in selected_choices:
            $ selected_choices.add("try_handle")
            jump try_handle
        "{color=#888888}Look for another entrance{/color}" if "find_entrance" in selected_choices:
            $ selected_choices.add("find_entrance")
            jump find_entrance
        "Look for another entrance" if "find_entrance" not in selected_choices:
            $ selected_choices.add("find_entrance")
            jump find_entrance

label knock_door:
    narrator "The knocker feels ice cold in your hand. Three heavy thuds echo through the manor."
    narrator "After a moment, you hear shuffling footsteps approaching."
    
    show butler at center
    with dissolve
    
    butler "Ah, you must be the new owner. I am Edmund, caretaker of Ravenshollow Manor."
    butler "Lady Margaret spoke of you often, though she never expected... the circumstances of your visit."
    
    player "What happened to her, exactly? The lawyer was vague."
    
    butler "A tragic accident, I'm afraid. She fell down the cellar stairs in the middle of the night."
    butler "Though between you and me... Lady Margaret knew every inch of this house. She never needed light to navigate."
    
    $ butler_trust += 1
    jump enter_manor

label try_handle:
    narrator "The heavy door is unlocked. Strange for such an isolated place."
    narrator "You push it open with a long creak."
    
    scene bg foyer
    with fade
    
    narrator "You step into a grand foyer. Dust motes dance in the dim light filtering through stained glass windows."
    narrator "Suddenly, a voice behind you makes you jump."
    
    show butler at center
    with dissolve
    
    butler "Good evening. I am Edmund, caretaker of this manor."
    butler "You must be Lady Margaret's heir. I've been expecting you."
    
    player "You scared me! I thought the place was empty."
    
    butler "My apologies. I was preparing the manor for your arrival."
    butler "Though I must warn you... this house holds many secrets."
    
    jump enter_manor

label find_entrance:
    narrator "You circle around the mansion, looking for a back door or servant's entrance."
    narrator "Behind an overgrown hedge, you find a small door marked 'CELLAR'."
    narrator "It's slightly ajar, as if someone left in a hurry."
    
    menu:
        "{color=#888888}Enter through the cellar{/color}" if "cellar_entrance" in selected_choices:
            $ selected_choices.add("cellar_entrance")
            jump cellar_entrance
        "Enter through the cellar" if "cellar_entrance" not in selected_choices:
            $ selected_choices.add("cellar_entrance")
            jump cellar_entrance
        "{color=#888888}Go back to the front door{/color}" if "back_front_door" in selected_choices:
            $ selected_choices.add("back_front_door")
            jump knock_door
        "Go back to the front door" if "back_front_door" not in selected_choices:
            $ selected_choices.add("back_front_door")
            jump knock_door

label cellar_entrance:
    scene bg cellar
    with fade
    
    narrator "You push open the cellar door and step into darkness."
    narrator "The air smells of damp stone and something else... something metallic."
    narrator "Your phone's flashlight reveals stone walls and wooden wine racks."
    
    $ has_flashlight = True
    $ found_clues.append("cellar_entry")
    
    narrator "On the floor, you notice dark stains leading to the bottom of a stone staircase."
    narrator "This must be where your great aunt fell..."
    
    narrator "Suddenly, footsteps echo from above. Someone else is in the house."
    
    menu:
        "{color=#888888}Investigate the stains{/color}" if "investigate_stains" in selected_choices:
            $ selected_choices.add("investigate_stains")
            narrator "The stains are definitely blood, but there's something odd about the pattern."
            narrator "They seem to lead FROM the stairs, not TO them..."
            $ found_clues.append("blood_pattern")
            jump investigate_cellar
        "Investigate the stains" if "investigate_stains" not in selected_choices:
            $ selected_choices.add("investigate_stains")
            narrator "The stains are definitely blood, but there's something odd about the pattern."
            narrator "They seem to lead FROM the stairs, not TO them..."
            $ found_clues.append("blood_pattern")
            jump investigate_cellar
        "{color=#888888}Head upstairs immediately{/color}" if "upstairs_immediately" in selected_choices:
            $ selected_choices.add("upstairs_immediately")
            jump cellar_to_foyer
        "Head upstairs immediately" if "upstairs_immediately" not in selected_choices:
            $ selected_choices.add("upstairs_immediately")
            jump cellar_to_foyer
        "{color=#888888}Hide and listen{/color}" if "hide_listen" in selected_choices:
            $ selected_choices.add("hide_listen")
            jump hide_cellar
        "Hide and listen" if "hide_listen" not in selected_choices:
            $ selected_choices.add("hide_listen")
            jump hide_cellar

label enter_manor:
    scene bg foyer
    with fade
    
    narrator "Edmund leads you into the grand foyer."
    narrator "A crystal chandelier hangs overhead, several bulbs flickering ominously."
    narrator "Two curved staircases lead to the upper floors, and doorways branch off in all directions."
    
    butler "Lady Margaret's room has been prepared for you upstairs."
    butler "Though perhaps you'd like to explore first? The manor has quite a history."
    
    player "What kind of history?"
    
    butler "The Ravenshollow family has lived here for over 200 years."
    butler "There have been... incidents. Disappearances. Some say the house itself is cursed."
    
    menu:
        "{color=#888888}Ask about the curse{/color}" if "ask_curse" in selected_choices:
            $ selected_choices.add("ask_curse")
            jump ask_curse
        "Ask about the curse" if "ask_curse" not in selected_choices:
            $ selected_choices.add("ask_curse")
            jump ask_curse
        "{color=#888888}Ask about your great aunt's death{/color}" if "ask_death" in selected_choices:
            $ selected_choices.add("ask_death")
            jump ask_death
        "Ask about your great aunt's death" if "ask_death" not in selected_choices:
            $ selected_choices.add("ask_death")
            jump ask_death
        "{color=#888888}Start exploring the mansion{/color}" if "start_exploring" in selected_choices:
            $ selected_choices.add("start_exploring")
            jump explore_mansion
        "Start exploring the mansion" if "start_exploring" not in selected_choices:
            $ selected_choices.add("start_exploring")
            jump explore_mansion

label ask_curse:
    butler "The locals speak of a family curse dating back to the manor's founding."
    butler "Silas Ravenshollow, your ancestor, was accused of practicing dark arts."
    butler "They say he bound his spirit to this house before he died."
    butler "Every generation since has lost someone to... mysterious circumstances."
    
    $ knows_secret = True
    
    player "And you believe this?"
    
    butler "I've worked here for thirty years. I've seen things that can't be explained."
    butler "Lady Margaret was researching the family history before she died."
    butler "Her journals are in the library, if you're interested."
    
    jump explore_mansion

label ask_death:
    butler "Lady Margaret was found at the bottom of the cellar stairs."
    butler "The official cause was a fall, but..."
    
    player "But what?"
    
    butler "She was fully dressed at 3 AM. And the cellar door was locked from the inside."
    butler "How does one lock a door from the inside and then fall down stairs?"
    
    $ found_clues.append("locked_door")
    
    player "That is strange. Did the police investigate?"
    
    butler "They ruled it an accident. But Detective Mills seemed... unsatisfied with the conclusion."
    butler "He left his card, said to call if anything unusual happened."
    
    jump explore_mansion

label explore_mansion:
    $ rooms_explored += 1
    
    narrator "The manor stretches out before you, full of mysteries waiting to be uncovered."
    
    menu:
        "{color=#888888}Explore the Library{/color}" if "explore_library" in selected_choices:
            $ selected_choices.add("explore_library")
            jump library
        "Explore the Library" if "explore_library" not in selected_choices:
            $ selected_choices.add("explore_library")
            jump library
        "{color=#888888}Visit the Dining Room{/color}" if "visit_dining" in selected_choices:
            $ selected_choices.add("visit_dining")
            jump dining_room
        "Visit the Dining Room" if "visit_dining" not in selected_choices:
            $ selected_choices.add("visit_dining")
            jump dining_room
        "{color=#888888}Go to the Cellar{/color}" if "go_cellar" in selected_choices:
            $ selected_choices.add("go_cellar")
            jump cellar
        "Go to the Cellar" if "go_cellar" not in selected_choices:
            $ selected_choices.add("go_cellar")
            jump cellar
        "{color=#888888}Check the Attic{/color}" if "check_attic" in selected_choices:
            $ selected_choices.add("check_attic")
            jump attic
        "Check the Attic" if "check_attic" not in selected_choices:
            $ selected_choices.add("check_attic")
            jump attic
        "{color=#888888}Rest in the Bedroom{/color}" if "rest_bedroom" in selected_choices:
            if rooms_explored >= 3:
                $ selected_choices.add("rest_bedroom")
                jump bedroom
            else:
                narrator "You're not tired yet. There's too much to explore."
                jump explore_mansion
        "Rest in the Bedroom" if "rest_bedroom" not in selected_choices:
            if rooms_explored >= 3:
                $ selected_choices.add("rest_bedroom")
                jump bedroom
            else:
                narrator "You're not tired yet. There's too much to explore."
                jump explore_mansion

label library:
    scene bg library
    with fade
    
    narrator "Floor-to-ceiling bookshelves line the walls of the vast library."
    narrator "A fireplace crackles softly, though you don't remember anyone lighting it."
    narrator "On a large desk, you find several open books and scattered papers."
    
    if knows_secret:
        narrator "These must be the journals Edmund mentioned."
    
    narrator "The papers contain genealogical charts, newspaper clippings, and handwritten notes."
    narrator "One headline catches your eye: 'THIRD RAVENSHOLLOW HEIR VANISHES MYSTERIOUSLY'"
    
    menu:
        "{color=#888888}Read the journals{/color}" if "read_journals" in selected_choices:
            $ selected_choices.add("read_journals")
            jump read_journals
        "Read the journals" if "read_journals" not in selected_choices:
            $ selected_choices.add("read_journals")
            jump read_journals
        "{color=#888888}Examine the family tree{/color}" if "examine_tree" in selected_choices:
            $ selected_choices.add("examine_tree")
            jump family_tree
        "Examine the family tree" if "examine_tree" not in selected_choices:
            $ selected_choices.add("examine_tree")
            jump family_tree
        "{color=#888888}Search for hidden passages{/color}" if "search_passages" in selected_choices:
            $ selected_choices.add("search_passages")
            jump secret_passage
        "Search for hidden passages" if "search_passages" not in selected_choices:
            $ selected_choices.add("search_passages")
            jump secret_passage

label read_journals:
    narrator "Your great aunt's handwriting is elegant but urgent in her final entries:"
    narrator "'The dreams are getting worse. Silas calls to me nightly.'"
    narrator "'I've found the ritual chamber. The key is hidden where the raven watches.'"
    narrator "'If something happens to me, the heir must complete what I started.'"
    narrator "'The curse can be broken, but only by blood of blood.'"
    
    $ found_clues.append("ritual_chamber")
    $ found_clues.append("raven_key")
    
    narrator "The final entry is dated the night she died."
    
    jump explore_mansion

label family_tree:
    narrator "The family tree shows a disturbing pattern."
    narrator "Every generation for the past 200 years has lost someone around age 30."
    narrator "All died under mysterious circumstances."
    narrator "Your great aunt has circled your name at the bottom of the tree."
    narrator "Next to it, she's written: 'The last hope.'"
    
    $ found_clues.append("family_pattern")
    
    jump explore_mansion

label secret_passage:
    narrator "You run your hands along the bookshelves, looking for hidden mechanisms."
    narrator "Behind a collection of Edgar Allan Poe works, you find a loose book."
    narrator "When you pull it, the shelf swings inward with a grinding sound."
    
    narrator "A narrow stone passage leads into darkness."
    
    if has_flashlight:
        narrator "Your phone's light reveals stone steps leading downward."
        menu:
            "{color=#888888}Enter the passage{/color}" if "enter_passage" in selected_choices:
                $ selected_choices.add("enter_passage")
                jump secret_chamber
            "Enter the passage" if "enter_passage" not in selected_choices:
                $ selected_choices.add("enter_passage")
                jump secret_chamber
            "{color=#888888}Leave it for now{/color}" if "leave_passage" in selected_choices:
                $ selected_choices.add("leave_passage")
                jump explore_mansion
            "Leave it for now" if "leave_passage" not in selected_choices:
                $ selected_choices.add("leave_passage")
                jump explore_mansion
    else:
        narrator "It's too dark to explore safely. You need a light source."
        jump explore_mansion

label dining_room:
    scene bg dining_room
    with fade
    
    narrator "The dining room contains a massive oak table set for one."
    narrator "Fresh flowers sit in a crystal vase, though the petals are black with decay."
    narrator "A portrait of a stern man hangs above the fireplace."
    
    narrator "A brass nameplate reads: 'SILAS RAVENSHOLLOW - PATRIARCH'"
    narrator "His painted eyes seem to follow you around the room."
    
    narrator "On the mantelpiece, you notice a small brass key next to a raven figurine."
    
    if "raven_key" in found_clues:
        narrator "This must be the key your great aunt mentioned!"
        $ has_key = True
        narrator "You pocket the key carefully."
    else:
        menu:
            "{color=#888888}Take the key{/color}" if "take_key" in selected_choices:
                $ selected_choices.add("take_key")
                $ has_key = True
                narrator "The key feels warm in your hand, despite the cold room."
                jump explore_mansion
            "Take the key" if "take_key" not in selected_choices:
                $ selected_choices.add("take_key")
                $ has_key = True
                narrator "The key feels warm in your hand, despite the cold room."
                jump explore_mansion
            "{color=#888888}Leave it alone{/color}" if "leave_key" in selected_choices:
                $ selected_choices.add("leave_key")
                jump explore_mansion
            "Leave it alone" if "leave_key" not in selected_choices:
                $ selected_choices.add("leave_key")
                jump explore_mansion
    
    jump explore_mansion

label cellar:
    scene bg cellar
    with fade
    
    if "cellar_entry" not in found_clues:
        narrator "You descend the stone stairs to the cellar."
        narrator "The air grows colder with each step."
        narrator "At the bottom, you see dark stains on the stone floor."
        
        $ found_clues.append("blood_pattern")
    
    narrator "Wine racks line the walls, but many bottles are empty or broken."
    narrator "In the far corner, you notice a heavy wooden door with iron reinforcements."
    
    if has_key:
        narrator "The brass key from the dining room might fit this lock."
        menu:
            "{color=#888888}Use the key{/color}" if "use_key" in selected_choices:
                $ selected_choices.add("use_key")
                jump locked_room
            "Use the key" if "use_key" not in selected_choices:
                $ selected_choices.add("use_key")
                jump locked_room
            "{color=#888888}Leave the door alone{/color}" if "leave_door" in selected_choices:
                $ selected_choices.add("leave_door")
                jump explore_mansion
            "Leave the door alone" if "leave_door" not in selected_choices:
                $ selected_choices.add("leave_door")
                jump explore_mansion
    else:
        narrator "The door is locked with an old-fashioned brass lock."
        jump explore_mansion

label locked_room:
    narrator "The key turns with a satisfying click."
    narrator "The door swings open to reveal a small stone chamber."
    narrator "Candles line the walls, and strange symbols are carved into the floor."
    narrator "This must be the ritual chamber from your aunt's journal!"
    
    narrator "In the center lies an ornate dagger and an old leather-bound book."
    narrator "The book is written in Latin, but some pages have been translated:"
    narrator "'To break the binding, the blood of Silas must willingly return what was taken.'"
    narrator "'Only then can the spirits find peace.'"
    
    $ found_clues.append("ritual_knowledge")
    
    narrator "Suddenly, the temperature drops dramatically."
    narrator "A translucent figure materializes in the corner."
    
    show ghost at center
    with dissolve
    
    ghost "You... you have his blood. I can sense it."
    
    player "Who are you?"
    
    ghost "I am Margaret, your great aunt. I've been trapped here since my death."
    ghost "Silas killed me when I tried to break the curse. But you... you can finish what I started."
    
    menu:
        "{color=#888888}How do I break the curse?{/color}" if "break_curse_how" in selected_choices:
            $ selected_choices.add("break_curse_how")
            jump break_curse
        "How do I break the curse?" if "break_curse_how" not in selected_choices:
            $ selected_choices.add("break_curse_how")
            jump break_curse
        "{color=#888888}Why didn't you complete the ritual?{/color}" if "why_failed" in selected_choices:
            $ selected_choices.add("why_failed")
            jump why_failed
        "Why didn't you complete the ritual?" if "why_failed" not in selected_choices:
            $ selected_choices.add("why_failed")
            jump why_failed
        "{color=#888888}I don't believe in curses{/color}" if "skeptical" in selected_choices:
            $ selected_choices.add("skeptical")
            jump skeptical
        "I don't believe in curses" if "skeptical" not in selected_choices:
            $ selected_choices.add("skeptical")
            jump skeptical
