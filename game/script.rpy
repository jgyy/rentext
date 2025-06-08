# game/script.rpy
define narrator = Character(None, kind=nvl)
define player = Character("You", color="#c8ffc8")
define butler = Character("Edmund", color="#a0a0ff")
define ghost = Character("???", color="#ff9999")
define detective = Character("Detective Mills", color="#ffff99")

image bg mansion_exterior = "#2c1810"
image bg foyer = "#3d2817"
image bg library = "#4a3423"
image bg dining_room = "#3d2b1a"
image bg cellar = "#1a1a1a"
image bg attic = "#2f2419"
image bg bedroom = "#4a3829"

label start:
    jump enhanced_start

label enhanced_start:
    call save_progress from _call_save_progress
    
    if persistent.playthroughs > 0:
        menu:
            "Would you like to play the enhanced version with your accumulated knowledge?"
            "Enhanced Version (Recommended)":
                jump new_game_plus
            "Original Experience":
                jump original_start
    else:
        jump start_enhanced_game

label new_game_plus:
    narrator "You begin your return to Ravenshollow Manor, but this time with the wisdom of experience..."
    
    if persistent.total_achievements.get("detective", False):
        $ found_clues.append("detective_knowledge")
        narrator "Your previous investigative experience serves you well."
    
    jump start_enhanced_game

label original_start:
    jump knock_door

label random_manor_events:
    $ import random
    $ event_chance = random.randint(1, 10)
    
    if event_chance <= 3 and current_time >= 22:
        jump midnight_wanderer
    elif event_chance <= 5 and "protection_herbs" in inventory:
        jump herb_reaction
    elif event_chance <= 7 and sanity < 50:
        jump sanity_episode
    else:
        return

label midnight_wanderer:
    narrator "You hear footsteps in the hallway outside your room."
    narrator "They stop right outside your door..."
    
    menu:
        "Investigate the sound":
            narrator "You open the door to find the hallway empty."
            narrator "But wet footprints lead toward the cellar."
            $ lose_sanity(5)
            $ found_clues.append("mysterious_footprints")
        
        "Stay hidden and listen":
            narrator "The footsteps continue past your room."
            narrator "You hear a door creak open somewhere in the distance."
            $ gain_sanity(2)  # Avoided confrontation
    
    return

label herb_reaction:
    narrator "The protective herbs in your inventory begin to glow faintly."
    narrator "Something supernatural is near..."
    
    $ lose_sanity(3)
    narrator "The herbs have warned you of danger."
    
    return

label sanity_episode:
    narrator "Reality becomes unstable. The walls breathe, shadows move independently."
    narrator "You question what's real and what's in your mind."
    
    menu:
        "Ground yourself in reality":
            narrator "You focus on physical sensations - your heartbeat, the floor beneath your feet."
            narrator "Slowly, the hallucinations fade."
            $ gain_sanity(5)
        
        "Embrace the visions":
            narrator "You let the supernatural perceptions wash over you."
            narrator "Perhaps madness offers its own kind of insight..."
            $ lose_sanity(10)
            $ found_clues.append("madness_insight")
    
    return

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
        "{s}Enter through the cellar{/s}" if "cellar_entrance" in selected_choices:
            $ selected_choices.add("cellar_entrance")
            jump cellar_entrance
        "Enter through the cellar" if "cellar_entrance" not in selected_choices:
            $ selected_choices.add("cellar_entrance")
            jump cellar_entrance
        "{s}Go back to the front door{/s}" if "back_front_door" in selected_choices:
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
        "{s}Investigate the stains{/s}" if "investigate_stains" in selected_choices:
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
        "{s}Head upstairs immediately{/s}" if "upstairs_immediately" in selected_choices:
            $ selected_choices.add("upstairs_immediately")
            jump cellar_to_foyer
        "Head upstairs immediately" if "upstairs_immediately" not in selected_choices:
            $ selected_choices.add("upstairs_immediately")
            jump cellar_to_foyer
        "{s}Hide and listen{/s}" if "hide_listen" in selected_choices:
            $ selected_choices.add("hide_listen")
            jump hide_cellar
        "Hide and listen" if "hide_listen" not in selected_choices:
            $ selected_choices.add("hide_listen")
            jump hide_cellar

label investigate_cellar:
    narrator "As you examine the bloodstains more closely, you hear the footsteps getting closer."
    narrator "You also notice scratches on the cellar wall, as if someone was dragged."
    
    $ found_clues.append("scratch_marks")
    
    narrator "The cellar door creaks open above you."
    
    show butler at center
    with dissolve
    
    butler "Ah, there you are. I was wondering where you'd gone."
    butler "I see you've found the... scene of the accident."
    
    player "These bloodstains don't look like they came from a simple fall."
    
    butler "The police investigated thoroughly. Lady Margaret was found at the bottom of the stairs."
    butler "Though I admit, some details never sat right with me either."
    
    $ butler_trust += 1
    
    jump enter_manor

label cellar_to_foyer:
    narrator "You quickly climb the cellar stairs and emerge into the manor's main level."
    
    scene bg foyer
    with fade
    
    narrator "The foyer is dimly lit by flickering candles."
    narrator "You hear movement in the kitchen area."
    
    show butler at center
    with dissolve
    
    butler "Ah, you found your way in through the cellar. I hope you didn't disturb anything down there."
    butler "I am Edmund, caretaker of Ravenshollow Manor."
    
    player "I saw bloodstains on the floor. That's where she died, isn't it?"
    
    butler "Yes, a terrible tragedy. Lady Margaret was investigating something in the cellar that night."
    butler "She never told me what she was looking for."
    
    jump enter_manor

label hide_cellar:
    narrator "You duck behind a large wine rack and listen carefully."
    narrator "The footsteps above move slowly, deliberately, as if searching for something."
    narrator "After several tense minutes, they fade away."
    
    narrator "You emerge from hiding and notice something you missed before:"
    narrator "Fresh footprints in the dust leading to a hidden door behind the wine racks."
    
    $ found_clues.append("hidden_door")
    
    narrator "Someone else knows about the secret passages in this house."
    
    jump cellar_to_foyer

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
        "{s}Ask about the curse{/s}" if "ask_curse" in selected_choices:
            $ selected_choices.add("ask_curse")
            jump ask_curse
        "Ask about the curse" if "ask_curse" not in selected_choices:
            $ selected_choices.add("ask_curse")
            jump ask_curse
        "{s}Ask about your great aunt's death{/s}" if "ask_death" in selected_choices:
            $ selected_choices.add("ask_death")
            jump ask_death
        "Ask about your great aunt's death" if "ask_death" not in selected_choices:
            $ selected_choices.add("ask_death")
            jump ask_death
        "{s}Start exploring the mansion{/s}" if "start_exploring" in selected_choices:
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
    $ change_location("foyer")
    $ rooms_explored += 1
    
    # Reset temporary actions every few room changes
    if rooms_explored % 3 == 0:
        $ reset_temporary_actions()
    
    narrator "The manor stretches out before you, full of mysteries waiting to be uncovered."
    
    # Show different options based on what's been done and current state
    menu:
        "Explore the Library" if can_visit_location("library"):
            $ mark_action_completed("chose_library")
            jump library
            
        "Visit the Dining Room" if can_visit_location("dining_room"):
            $ mark_action_completed("chose_dining")
            jump dining_room
            
        "Go to the Cellar" if can_visit_location("cellar"):
            $ mark_action_completed("chose_cellar")
            jump cellar
            
        "Check the Attic" if can_visit_location("attic"):
            $ mark_action_completed("chose_attic")
            jump attic
            
        "Rest in the Bedroom" if rooms_explored >= 3 and can_visit_location("bedroom"):
            $ mark_action_completed("chose_bedroom")
            jump bedroom
            
        "Use Enhanced Exploration Options" if rooms_explored >= 2:
            jump enhanced_explore_mansion
            
        "Review Evidence and Plan Next Move" if len(found_clues) >= 3:
            jump review_progress

label library:
    $ change_location("library")
    
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
        "Read the journals" if can_perform_action("read_journals"):
            $ mark_action_completed("read_journals")
            jump read_journals
            
        "Examine the family tree" if can_perform_action("examine_tree"):
            $ mark_action_completed("examine_tree")
            jump family_tree
            
        "Search for hidden passages" if can_perform_action("search_passages"):
            $ mark_action_completed("search_passages")
            jump secret_passage
            
        "Return to exploring other areas":
            jump explore_mansion

label read_journals:
    if get_scene_visits("library") > 3:
        narrator "You've already thoroughly read these journals. There's nothing new to discover here."
        jump explore_mansion
    
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
    if get_scene_visits("library") > 3:
        narrator "You've already studied the family tree extensively."
        jump explore_mansion
        
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
            "{s}Enter the passage{/s}" if "enter_passage" in selected_choices:
                $ selected_choices.add("enter_passage")
                jump secret_chamber
            "Enter the passage" if "enter_passage" not in selected_choices:
                $ selected_choices.add("enter_passage")
                jump secret_chamber
            "{s}Leave it for now{/s}" if "leave_passage" in selected_choices:
                $ selected_choices.add("leave_passage")
                jump explore_mansion
            "Leave it for now" if "leave_passage" not in selected_choices:
                $ selected_choices.add("leave_passage")
                jump explore_mansion
    else:
        narrator "It's too dark to explore safely. You need a light source."
        jump explore_mansion

label dining_room:
    $ change_location("dining_room")
    
    scene bg dining_room
    with fade
    
    narrator "The dining room contains a massive oak table set for one."
    narrator "Fresh flowers sit in a crystal vase, though the petals are black with decay."
    narrator "A portrait of a stern man hangs above the fireplace."
    
    narrator "A brass nameplate reads: 'SILAS RAVENSHOLLOW - PATRIARCH'"
    narrator "His painted eyes seem to follow you around the room."
    
    if not has_key:
        narrator "On the mantelpiece, you notice a small brass key next to a raven figurine."
        
        if "raven_key" in found_clues:
            narrator "This must be the key your great aunt mentioned!"
            $ has_key = True
            $ mark_action_completed("took_raven_key")
            narrator "You pocket the key carefully."
        else:
            menu:
                "Take the key" if can_perform_action("take_key"):
                    $ has_key = True
                    $ mark_action_completed("take_key")
                    narrator "The key feels warm in your hand, despite the cold room."
                    
                "Leave it alone" if can_perform_action("leave_key"):
                    $ mark_action_completed("leave_key")
                    narrator "You decide to leave the key for now."
    else:
        narrator "You already have the brass key from this room."
    
    menu:
        "Examine the portrait more closely" if can_perform_action("examine_portrait"):
            $ mark_action_completed("examine_portrait")
            narrator "The portrait's eyes seem to track your movement. Unsettling."
            narrator "You notice a small inscription: 'He who watches, never dies.'"
            $ found_clues.append("portrait_inscription")
            
        "Return to exploring other areas":
            jump explore_mansion

label enhanced_explore_mansion:
    $ change_location("foyer_enhanced")
    $ current_edmund_state = check_edmund_state()
    
    narrator "Current time: [current_time]:00. Edmund seems [current_edmund_state]."
    
    if sanity < 30:
        narrator "The walls seem to breathe and shift before your eyes..."
    elif sanity < 60:
        narrator "You feel increasingly on edge. Nothing seems quite right."
    
    menu:
        "Explore the Greenhouse" if can_visit_location("greenhouse"):
            $ advance_time(1)
            jump greenhouse
            
        "Visit the Family Cemetery" if can_visit_location("cemetery"):
            $ advance_time(1)
            jump cemetery
            
        "Investigate the Music Room" if can_visit_location("music_room"):
            $ advance_time(1)
            jump music_room
            
        "Check the Observatory" if can_visit_location("observatory") and has_key:
            $ advance_time(1)
            jump observatory
            
        "Search for Hidden Passages" if can_perform_action("search_hidden_passages"):
            $ mark_action_completed("search_hidden_passages")
            $ advance_time(2)
            jump hidden_passages
            
        "Go to Town for Information" if days_survived >= 2 and can_perform_action("town_visit"):
            $ mark_action_completed("town_visit")
            $ advance_time(3)
            jump town_investigation
            
        "Rest and Recover" if sanity < 70 and can_perform_action("rest_recover"):
            $ mark_action_completed("rest_recover")
            $ gain_sanity(20)
            $ advance_time(2)
            narrator "You rest for a while and feel somewhat better."
            jump enhanced_explore_mansion
            
        "Return to Basic Exploration":
            jump explore_mansion

label review_progress:
    narrator "You take a moment to review everything you've discovered so far."
    narrator "Clues found: [len(found_clues)]"
    narrator "Evidence collected: [len(evidence_board)]"
    narrator "Documents discovered: [len(documents_found)]"
    
    if len(found_clues) >= 8:
        narrator "You feel like you're close to understanding the truth."
        narrator "Perhaps it's time to take decisive action."
        
        menu:
            "Proceed to final confrontation" if "ritual_knowledge" in found_clues:
                jump final_confrontation
                
            "Continue investigating" if can_perform_action("continue_investigating"):
                $ mark_action_completed("continue_investigating")
                jump explore_mansion
                
            "Call Detective Mills" if "detective_card" in found_clues and can_perform_action("call_mills"):
                $ mark_action_completed("call_mills")
                jump call_detective
    else:
        narrator "You need to gather more information before making any major decisions."
        jump explore_mansion

label cellar:
    $ change_location("cellar")
    
    scene bg cellar
    with fade
    
    if "cellar_entry" not in found_clues:
        narrator "You descend the stone stairs to the cellar."
        narrator "The air grows colder with each step."
        narrator "At the bottom, you see dark stains on the stone floor."
        $ found_clues.append("blood_pattern")
    else:
        narrator "You return to the cellar where your great aunt died."
    
    narrator "Wine racks line the walls, but many bottles are empty or broken."
    narrator "In the far corner, you notice a heavy wooden door with iron reinforcements."
    
    if has_key and can_perform_action("use_cellar_key"):
        narrator "The brass key from the dining room might fit this lock."
        menu:
            "Use the key":
                $ mark_action_completed("use_cellar_key")
                jump locked_room
            "Leave the door alone":
                jump explore_mansion
    elif has_key:
        narrator "You've already unlocked this door."
        menu:
            "Enter the ritual chamber":
                jump locked_room
            "Leave":
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
        "{s}How do I break the curse?{/s}" if "break_curse_how" in selected_choices:
            $ selected_choices.add("break_curse_how")
            jump break_curse
        "How do I break the curse?" if "break_curse_how" not in selected_choices:
            $ selected_choices.add("break_curse_how")
            jump break_curse
        "{s}Why didn't you complete the ritual?{/s}" if "why_failed" in selected_choices:
            $ selected_choices.add("why_failed")
            jump why_failed
        "Why didn't you complete the ritual?" if "why_failed" not in selected_choices:
            $ selected_choices.add("why_failed")
            jump why_failed
        "{s}I don't believe in curses{/s}" if "skeptical" in selected_choices:
            $ selected_choices.add("skeptical")
            jump skeptical
        "I don't believe in curses" if "skeptical" not in selected_choices:
            $ selected_choices.add("skeptical")
            jump skeptical

label break_curse:
    if get_scene_visits("ritual_chamber") > 2:
        narrator "You've already discussed this thoroughly with Margaret's spirit."
        narrator "It's time to make a decision."
        
        menu:
            "Perform the ritual":
                jump good_ending
            "Refuse to do the ritual":
                jump bad_ending
            "Leave and think more":
                jump explore_mansion
        return
    
    ghost "The ritual requires a willing sacrifice of blood from Silas's bloodline."
    ghost "You must cut your palm with the ceremonial dagger and let three drops fall on the ritual circle."
    ghost "Then speak the words: 'I release what was bound, I free what was chained.'"
    
    player "What happens to me if I do this?"
    
    ghost "The curse will be broken, and all the trapped spirits will be freed."
    ghost "Including myself. We can finally find peace."
    ghost "You will inherit the manor truly, free of its dark influence."
    
    menu:
        "Perform the ritual":
            jump good_ending
        "Refuse to do the ritual":
            jump bad_ending
        "Ask for more time to think":
            jump explore_mansion

label why_failed:
    ghost "I was so close... I had gathered everything needed for the ritual."
    ghost "But Silas's spirit is stronger at night. He possessed Edmund and used him to stop me."
    ghost "I was pushed down the cellar stairs before I could complete the ceremony."
    
    player "Edmund? But he seems so helpful..."
    
    ghost "During the day, Edmund is himself. But at night, Silas takes control."
    ghost "You must complete the ritual during daylight hours, when Silas is weakest."
    ghost "And whatever you do, don't trust Edmund after dark."
    
    $ found_clues.append("edmund_possessed")
    
    jump break_curse

label skeptical:
    player "This is all nonsense. There's a rational explanation for everything."
    
    ghost "You sound just like the detective who investigated my death."
    ghost "Very well. Leave this place then. But know this - the curse will follow you."
    ghost "You cannot escape your bloodline, no matter how far you run."
    
    narrator "The ghost fades away, leaving you alone in the ritual chamber."
    narrator "Suddenly, you hear heavy footsteps approaching from the cellar."
    
    show butler at center
    with dissolve
    
    butler "Ah, you found the old chamber. Lady Margaret spent her final night here."
    butler "Fascinating woman, always chasing shadows and legends."
    
    narrator "Something about Edmund's smile seems... different."
    
    menu:
        "{s}Confront Edmund about the possession{/s}" if "confront_edmund" in selected_choices and "edmund_possessed" in found_clues:
            $ selected_choices.add("confront_edmund")
            jump confront_possession
        "Confront Edmund about the possession" if "confront_edmund" not in selected_choices and "edmund_possessed" in found_clues:
            $ selected_choices.add("confront_edmund")
            jump confront_possession
        "{s}Leave the chamber immediately{/s}" if "leave_chamber" in selected_choices:
            $ selected_choices.add("leave_chamber")
            jump escape_attempt
        "Leave the chamber immediately" if "leave_chamber" not in selected_choices:
            $ selected_choices.add("leave_chamber")
            jump escape_attempt
        "{s}Reconsider the ritual{/s}" if "reconsider" in selected_choices:
            $ selected_choices.add("reconsider")
            jump break_curse
        "Reconsider the ritual" if "reconsider" not in selected_choices:
            $ selected_choices.add("reconsider")
            jump break_curse

label attic:
    scene bg attic
    with fade
    
    $ rooms_explored += 1
    
    narrator "The attic is filled with dusty furniture covered by white sheets."
    narrator "Moonlight streams through a circular window, casting eerie shadows."
    narrator "Old portraits line the walls - generations of Ravenshollow family members."
    
    narrator "In the corner, you find a trunk filled with old letters and documents."
    narrator "One letter catches your attention - it's addressed to you, written in your great aunt's hand."
    
    narrator "'My dear heir, if you're reading this, then I have failed and the burden falls to you.'"
    narrator "'The truth about our family is darker than you know. Silas didn't just practice dark magic - he IS dark magic now.'"
    narrator "'He feeds on the life force of our bloodline to maintain his existence.'"
    narrator "'Break the cycle, or become his next victim.'"
    
    $ found_clues.append("final_letter")
    
    jump explore_mansion

label bedroom:
    $ change_location("bedroom")
    
    scene bg bedroom
    with fade
    
    narrator "Lady Margaret's bedroom is preserved exactly as she left it."
    narrator "Personal effects lie scattered on the vanity table."
    narrator "The bed is still unmade, as if she left in a hurry that final night."
    
    if "detective_card" not in found_clues:
        narrator "On the nightstand, you find Detective Mills' business card and a note:"
        narrator "'Call Mills if anything strange happens. He knows the truth.'"
        $ found_clues.append("detective_card")
    
    if len(found_clues) >= 5 and can_perform_action("first_sleep"):
        narrator "You're exhausted from exploring and learning the dark secrets of the manor."
        narrator "As you lie down on the bed, you notice the temperature dropping rapidly."
        
        menu:
            "Try to sleep":
                $ mark_action_completed("first_sleep")
                jump nightmare_sequence
                
            "Stay awake and call Detective Mills" if "detective_card" in found_clues:
                $ mark_action_completed("call_detective_bedroom")
                jump call_detective
                
            "Go back to exploring":
                jump explore_mansion
                
    elif "first_sleep" in completed_actions:
        narrator "You've already rested here. The bedroom holds no more secrets for now."
        menu:
            "Return to exploring":
                jump explore_mansion
    else:
        narrator "You're not ready to rest yet. There's still too much to discover."
        jump explore_mansion

label secret_chamber:
    narrator "The secret passage leads to an underground chamber beneath the house."
    narrator "This room is older than the rest of the manor, with rough stone walls and primitive carvings."
    narrator "In the center stands an ancient altar stained with what looks like dried blood."
    
    narrator "This must be Silas's original ritual chamber, where he first bound his spirit to the house."
    narrator "The air itself feels thick with malevolent energy."
    
    if has_key:
        narrator "You notice a small alcove that might be opened with your key."
        menu:
            "{s}Use the key on the alcove{/s}" if "use_key_alcove" in selected_choices:
                $ selected_choices.add("use_key_alcove")
                jump hidden_treasure
            "Use the key on the alcove" if "use_key_alcove" not in selected_choices:
                $ selected_choices.add("use_key_alcove")
                jump hidden_treasure
            "{s}Leave this place{/s}" if "leave_secret" in selected_choices:
                $ selected_choices.add("leave_secret")
                jump explore_mansion
            "Leave this place" if "leave_secret" not in selected_choices:
                $ selected_choices.add("leave_secret")
                jump explore_mansion
    else:
        narrator "You feel like something important is hidden here, but you need the right key."
        jump explore_mansion

label hidden_treasure:
    narrator "The alcove opens to reveal ancient scrolls and a crystal pendant."
    narrator "The pendant pulses with a soft blue light - it's clearly magical."
    narrator "The scrolls contain the original binding ritual and its counter-spell."
    
    $ found_clues.append("counter_spell")
    $ found_clues.append("magic_pendant")
    
    narrator "With this pendant, you might be able to protect yourself from Silas's influence."
    narrator "And the counter-spell provides an alternative to the blood ritual."
    
    jump explore_mansion

label good_ending:
    if "ending_reached" in completed_actions:
        narrator "You've already completed this path."
        return
        
    $ mark_action_completed("ending_reached")
    
    narrator "You pick up the ceremonial dagger with trembling hands."
    narrator "The blade is surprisingly sharp and seems to hum with energy."
    
    player "I release what was bound, I free what was chained."
    
    narrator "You slice across your palm and let three drops of blood fall onto the ritual circle."
    narrator "Immediately, the chamber fills with blinding white light."
    
    narrator "You hear the sound of chains breaking and tortured spirits crying out in relief."
    narrator "The oppressive atmosphere that has hung over the manor begins to lift."
    
    show ghost at center
    with dissolve
    
    ghost "Thank you... the curse is broken. We are finally free."
    ghost "The manor is yours now, truly yours, without the taint of dark magic."
    ghost "Live well, and remember us kindly."
    
    narrator "Margaret's spirit fades away with a peaceful smile."
    narrator "The chamber grows warm and welcoming for the first time in centuries."
    
    scene bg mansion_exterior
    with fade
    
    narrator "Six months later, you've restored Ravenshollow Manor to its former glory."
    narrator "The locals no longer speak of curses or mysterious disappearances."
    narrator "You've broken a cycle of death that lasted two hundred years."
    narrator "The manor is finally at peace... and so are you."
    
    $ unlock_achievement("truth_seeker")
    $ track_ending("good_ending")
    
    narrator "THE END - CURSE BROKEN"
    
    return

label bad_ending:
    if "ending_reached" in completed_actions:
        narrator "You've already completed this path."
        return
        
    $ mark_action_completed("ending_reached")
    
    player "I'm sorry, but I can't do this. There has to be another way."
    
    ghost "You fool! You've doomed yourself and all future generations!"
    ghost "Silas will never let you leave this place alive!"
    
    narrator "Margaret's spirit flickers and fades, her expression one of profound disappointment."
    narrator "The chamber grows cold again, and you hear malevolent laughter echoing from the walls."
    
    narrator "Suddenly, the ritual chamber door slams shut behind you."
    narrator "The candles go out one by one, plunging you into darkness."
    
    narrator "In the distance, you hear Edmund's voice, but it sounds different... older, more commanding."
    
    butler "Welcome to your new home, descendant. You'll never leave here alive."
    butler "Just like all the others..."
    
    narrator "The darkness closes in around you."
    narrator "You've become the latest victim of the Ravenshollow curse."
    
    $ track_ending("bad_ending")
    
    narrator "THE END - CURSE CONTINUES"
    
    return

label nightmare_sequence:
    narrator "You drift off to sleep, exhausted by the day's revelations."
    narrator "But your dreams are far from peaceful..."
    
    scene bg cellar
    with fade
    
    narrator "In your dream, you're standing in the cellar."
    narrator "Your great aunt Margaret appears before you, looking exactly as she did in life."
    
    ghost "You're running out of time. Silas grows stronger each night."
    ghost "Complete the ritual at dawn, or join me in eternal bondage to this cursed place."
    
    narrator "The dream shifts, and you see flashes of the past:"
    narrator "Silas Ravenshollow performing dark rituals..."
    narrator "Family members disappearing one by one over the centuries..."
    narrator "Your great aunt discovering the truth too late..."
    
    narrator "You wake with a start. Dawn is breaking outside the window."
    narrator "This is your chance - you must act now while Silas is weakest."
    
    menu:
        "{s}Rush to the ritual chamber{/s}" if "rush_ritual" in selected_choices:
            $ selected_choices.add("rush_ritual")
            jump final_confrontation
        "Rush to the ritual chamber" if "rush_ritual" not in selected_choices:
            $ selected_choices.add("rush_ritual")
            jump final_confrontation
        "{s}Try to escape the manor{/s}" if "escape_manor" in selected_choices:
            $ selected_choices.add("escape_manor")
            jump escape_attempt
        "Try to escape the manor" if "escape_manor" not in selected_choices:
            $ selected_choices.add("escape_manor")
            jump escape_attempt

label call_detective:
    narrator "You dial Detective Mills' number with shaking fingers."
    narrator "He answers on the first ring, as if he'd been waiting for your call."
    
    show detective at center
    with dissolve
    
    detective "You're at the manor, aren't you? I can hear it in your voice."
    detective "Listen carefully - you're in danger. Margaret called me the night she died."
    detective "She'd discovered something about the family curse. Something that got her killed."
    
    player "Edmund... is he possessed?"
    
    detective "So you know. Yes, at night, he becomes someone else entirely."
    detective "Margaret found evidence that Edmund has been the caretaker here for far longer than he claims."
    detective "I think he might be Silas himself, using different identities over the centuries."
    
    $ found_clues.append("edmund_is_silas")
    
    detective "Get out of there now, while you still can!"
    
    narrator "Suddenly, the phone line goes dead."
    narrator "You hear heavy footsteps in the hallway outside."
    
    jump final_confrontation

label escape_attempt:
    narrator "You run through the manor toward the front door."
    narrator "But every door you try is locked, and the windows won't budge."
    narrator "The house itself seems to be holding you prisoner."
    
    show butler at center
    with dissolve
    
    butler "Leaving so soon? But you've only just arrived."
    butler "And we have so much to discuss... descendant."
    
    narrator "Edmund's voice has changed. It's older now, more refined."
    narrator "His eyes glow with an unnatural light."
    
    player "You're not Edmund, are you? You're Silas."
    
    butler "Clever child. Yes, I am Silas Ravenshollow, founder of this house."
    butler "I've been waiting so long for you to arrive."
    butler "Every generation, I require fresh blood to maintain my existence."
    butler "And you, dear heir, are the strongest of the bloodline yet."
    
    menu:
        "{s}Fight back with the magic pendant{/s}" if "fight_pendant" in selected_choices and "magic_pendant" in found_clues:
            $ selected_choices.add("fight_pendant")
            jump pendant_fight
        "Fight back with the magic pendant" if "fight_pendant" not in selected_choices and "magic_pendant" in found_clues:
            $ selected_choices.add("fight_pendant")
            jump pendant_fight
        "{s}Try to reason with him{/s}" if "reason_silas" in selected_choices:
            $ selected_choices.add("reason_silas")
            jump reason_with_silas
        "Try to reason with him" if "reason_silas" not in selected_choices:
            $ selected_choices.add("reason_silas")
            jump reason_with_silas
        "{s}Run to the ritual chamber{/s}" if "run_ritual" in selected_choices:
            $ selected_choices.add("run_ritual")
            jump final_confrontation
        "Run to the ritual chamber" if "run_ritual" not in selected_choices:
            $ selected_choices.add("run_ritual")
            jump final_confrontation

label confront_possession:
    player "I know what you are, Silas. My great aunt told me everything."
    
    butler "Ah, so Margaret managed to speak to you from beyond the grave."
    butler "How... inconvenient."
    
    narrator "Edmund's facade drops completely. His form begins to shimmer and change."
    narrator "The kindly butler is replaced by a tall, gaunt figure in Victorian dress."
    
    butler "I am Silas Ravenshollow, and this is MY house!"
    butler "Every brick, every stone is bound to my will!"
    butler "You cannot escape your destiny, child. Your blood belongs to me!"
    
    jump final_confrontation

label final_confrontation:
    scene bg cellar
    with fade
    
    narrator "You race down to the ritual chamber, with Silas close behind."
    narrator "The room is filled with swirling shadows and unnatural cold."
    
    if "magic_pendant" in found_clues:
        narrator "The crystal pendant around your neck glows brightly, holding back the darkness."
        narrator "This gives you the protection you need to complete the ritual."
        
        menu:
            "{s}Use the counter-spell from the scrolls{/s}" if "counter_spell" in found_clues:
                jump counter_spell_ending
            "Perform the blood ritual":
                jump good_ending
    else:
        narrator "The oppressive magical energy in the room is overwhelming."
        narrator "You struggle to focus as Silas's power washes over you."
        
        menu:
            "Perform the blood ritual quickly":
                jump rushed_ending
            "Try to fight Silas directly":
                jump combat_ending

label pendant_fight:
    narrator "You hold up the crystal pendant, and it blazes with protective light."
    narrator "Silas recoils, hissing like a serpent."
    
    butler "Impossible! Where did you find that accursed thing?"
    
    player "Your own ritual chamber. You should have hidden it better."
    
    narrator "The pendant's light grows stronger, and Silas's form begins to waver."
    narrator "This is your chance to reach the ritual chamber and break the curse permanently."
    
    jump final_confrontation

label reason_with_silas:
    player "Wait! We're family. Surely there's another way."
    player "You don't have to keep killing your own descendants."
    
    butler "Family? Child, I've consumed the life force of dozens of my 'family' over the centuries."
    butler "You're nothing but cattle to me now."
    butler "Your blood will give me another century of existence."
    
    narrator "Reasoning with him is hopeless. You'll have to find another way."
    
    jump final_confrontation

label counter_spell_ending:
    narrator "You unroll the ancient scrolls and begin reading the counter-spell."
    narrator "The words are in Old Latin, but somehow you understand their meaning."
    
    player "By the power of blood and bone, I break the bonds that bind thee!"
    player "Return to dust, Silas Ravenshollow! Your time is ended!"
    
    narrator "Golden light fills the chamber as the counter-spell takes effect."
    narrator "Silas screams in rage and terror as his essence is torn from the house."
    
    butler "No! I will not be banished! This house is MINE!"
    
    narrator "But the ancient magic is too strong. Silas's spirit is finally destroyed."
    narrator "The curse is broken without requiring your blood sacrifice."
    narrator "The crystal pendant crumbles to dust, its purpose fulfilled."
    
    scene bg mansion_exterior
    with fade
    
    narrator "With Silas gone and the curse broken, Ravenshollow Manor is finally at peace."
    narrator "You've not only survived but found a way to end the cycle without sacrifice."
    narrator "The knowledge and artifacts you've discovered make you wealthy beyond measure."
    narrator "You've achieved the perfect ending - victory without loss."
    
    narrator "THE END - PERFECT VICTORY"
    
    return

label rushed_ending:
    narrator "Without the pendant's protection, you struggle against Silas's influence."
    narrator "You manage to cut your palm and complete the blood ritual, but at great cost."
    
    narrator "The curse is broken, but you're severely weakened by the magical backlash."
    narrator "You survive, but you'll never fully recover from the ordeal."
    
    narrator "THE END - PYRRHIC VICTORY"
    
    return

label combat_ending:
    narrator "You try to fight Silas directly, but without magical protection, you're no match for him."
    narrator "His dark magic overwhelms you, and you become another victim of the Ravenshollow curse."
    narrator "THE END - DEFEAT"
    return
