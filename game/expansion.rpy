# game/expansion.rpy
init offset = -1

define townsperson = Character("Village Elder", color="#8fbc8f")
define librarian = Character("Ms. Blackwood", color="#dda0dd")
define groundskeeper = Character("Old Tom", color="#cd853f")
define medium = Character("Madame Zelda", color="#9370db")
define historian = Character("Professor Williams", color="#4682b4")
define sarah = Character("Cousin Sarah", color="#f0e68c")

image bg greenhouse = "#2d4a2d"
image bg cemetery = "#1a1a2d"
image bg music_room = "#3d2d4a"
image bg observatory = "#2d2d4a"
image bg town_square = "#4a4a3d"
image bg panic_room = "#1a1a1a"

label enhanced_explore_mansion:
    $ current_edmund_state = check_edmund_state()
    
    narrator "Current time: [current_time]:00. Edmund seems [current_edmund_state]."
    
    if sanity < 30:
        narrator "The walls seem to breathe and shift before your eyes..."
    elif sanity < 60:
        narrator "You feel increasingly on edge. Nothing seems quite right."
    
    menu:
        "Explore the Greenhouse" if "greenhouse" not in selected_choices:
            $ selected_choices.add("greenhouse")
            $ advance_time(1)
            jump greenhouse
        "Visit the Family Cemetery" if "cemetery" not in selected_choices:
            $ selected_choices.add("cemetery")
            $ advance_time(1)
            jump cemetery
        "Investigate the Music Room" if "music_room" not in selected_choices:
            $ selected_choices.add("music_room")
            $ advance_time(1)
            jump music_room
        "Check the Observatory" if "observatory" not in selected_choices and has_key:
            $ selected_choices.add("observatory")
            $ advance_time(1)
            jump observatory
        "Search for Hidden Passages" if "hidden_passages" not in selected_choices:
            $ selected_choices.add("hidden_passages")
            $ advance_time(2)
            jump hidden_passages
        "Go to Town for Information" if days_survived >= 2:
            $ advance_time(3)
            jump town_investigation
        "Rest and Recover" if sanity < 70:
            $ gain_sanity(20)
            $ advance_time(2)
            narrator "You rest for a while and feel somewhat better."
            jump enhanced_explore_mansion
        "Return to Original Areas":
            jump explore_mansion

label greenhouse:
    scene bg greenhouse
    with fade
    
    narrator "The greenhouse is a twisted garden of horrors."
    narrator "Exotic plants with unnatural colors grow in wild profusion."
    narrator "The air is thick with a sickly sweet perfume that makes you dizzy."
    
    $ lose_sanity(5)
    
    menu:
        "Examine the poisonous plants":
            narrator "These are definitely not normal garden varieties."
            narrator "Many bear warning labels in Latin - clearly cultivated for their toxicity."
            $ inventory.append("plant_samples")
            $ add_evidence("poison_garden", "greenhouse", "Someone has been growing deadly plants")
            $ lose_sanity(10)
        
        "Look for Edmund's gardening notes":
            narrator "You find a journal detailing care instructions for various plants."
            narrator "The final entry mentions 'preparing for the ritual moon'."
            $ documents_found.append("gardening_journal")
            $ found_clues.append("ritual_preparation")
        
        "Search for hidden compartments":
            if "plant_samples" in inventory:
                narrator "Behind a particularly large Venus flytrap, you find a hidden panel."
                narrator "Inside is a vial of concentrated plant extract - deadly poison."
                $ inventory.append("deadly_poison")
                narrator "This could be used to defend yourself... or for something darker."
            else:
                narrator "You search but find nothing obvious. Maybe you need to examine the plants first."
        
        "Leave quickly - the air is making you sick":
            narrator "You stumble out of the greenhouse, gasping for fresh air."
            $ lose_sanity(3)
    
    jump enhanced_explore_mansion

label cemetery:
    scene bg cemetery
    with fade
    
    narrator "The family cemetery sits behind the manor, shrouded in perpetual mist."
    narrator "Weathered headstones stretch back centuries, each telling a story of premature death."
    
    if current_time >= 20 or current_time <= 6:
        narrator "In the moonlight, the graves seem to glow with an eerie phosphorescence."
        $ lose_sanity(10)
    
    menu:
        "Study the pattern of deaths":
            narrator "As you examine the dates, a horrifying pattern emerges."
            narrator "Every 25-30 years, someone from the family dies violently."
            narrator "The cycle has been unbroken for over 200 years."
            $ add_evidence("death_pattern", "cemetery", "Systematic elimination of heirs")
            $ investigation_path = "historical"
        
        "Look for Sarah's grave" if sarah_mystery_unlocked:
            narrator "You search for any sign of your cousin Sarah who disappeared five years ago."
            narrator "There's no grave... which means she might still be alive."
            $ found_clues.append("sarah_alive")
        
        "Examine Silas's original grave":
            narrator "The oldest headstone reads: 'SILAS RAVENSHOLLOW - PATRIARCH AND PROTECTOR'"
            narrator "But something's wrong... the grave has been disturbed recently."
            if sanity < 50:
                narrator "You swear you can hear scratching sounds from beneath the soil..."
                $ lose_sanity(15)
            else:
                narrator "Fresh dirt suggests someone has been digging here."
                $ add_evidence("disturbed_grave", "cemetery", "Recent excavation activity")
        
        "Pay respects to Great Aunt Margaret":
            narrator "Margaret's grave is fresh, with wilted flowers."
            narrator "Someone has been visiting regularly... but who?"
            $ gain_sanity(5)
            if "margaret_visitor" not in found_clues:
                narrator "You notice a business card tucked under the flowers - Detective Mills."
                $ found_clues.append("margaret_visitor")
    
    if current_time >= 22:
        narrator "Suddenly, you hear footsteps approaching through the mist."
        menu:
            "Hide behind a large headstone":
                narrator "You crouch behind the Ravenshollow family monument."
                narrator "A figure in a dark coat approaches Margaret's grave."
                if "detective_card" in found_clues:
                    narrator "It's Detective Mills! He places fresh flowers on the grave."
                    narrator "You overhear him whisper: 'I'm sorry I couldn't save you, Margaret.'"
                    $ butler_trust -= 1  
                else:
                    narrator "The figure is too obscured by mist to identify."
                    narrator "They leave something at the grave and disappear."
            
            "Confront the mysterious visitor":
                narrator "You call out to the approaching figure."
                if "detective_card" in found_clues:
                    jump cemetery_detective_meeting
                else:
                    narrator "The figure stops, then runs away into the darkness."
                    $ lose_sanity(10)
    
    jump enhanced_explore_mansion

label cemetery_detective_meeting:
    show detective at center
    with dissolve
    
    detective "I should have known you'd find your way here eventually."
    detective "You're just like Margaret - too curious for your own good."
    
    player "Detective Mills? What are you doing here so late?"
    
    detective "Paying my respects. And keeping watch."
    detective "Margaret and I... we were working together to expose the truth about this place."
    detective "She died before we could finish gathering evidence."
    
    menu:
        "What kind of evidence?":
            detective "Financial records showing Edmund has been using multiple identities."
            detective "Death certificates that don't add up."
            detective "And this..."
            narrator "He shows you a photograph of Edmund from 50 years ago. He looks exactly the same."
            $ add_evidence("edmund_photo", "cemetery", "Edmund hasn't aged in decades")
            $ edmund_possession_level = 100  
        
        "Why didn't you tell me earlier?":
            detective "I needed to see if you were like the others - willing to believe the lies."
            detective "But you're asking the right questions, just like Margaret did."
        
        "Can you help me stop this?":
            detective "I've been trying for years. But I need proof that will hold up in court."
            detective "The supernatural explanation won't work. We need hard evidence."
            $ investigation_path = "criminal"
    
    detective "Meet me tomorrow at the town library. Ms. Blackwood has been keeping records."
    detective "And whatever you do, don't trust Edmund after dark."
    
    jump enhanced_explore_mansion

label music_room:
    scene bg music_room
    with fade
    
    narrator "The music room contains a grand piano covered in dust."
    narrator "Sheet music is scattered across the floor and piano bench."
    
    if current_time >= 20 or current_time <= 6:
        narrator "As you enter, a few piano keys depress by themselves."
        narrator "The ghostly melody sends chills down your spine."
        $ lose_sanity(8)
    
    menu:
        "Examine the sheet music":
            narrator "Most of the music is classical, but one piece stands out."
            narrator "It's handwritten, titled 'Margaret's Lament' and dated just weeks before her death."
            narrator "The melody is haunting, almost hypnotic."
            $ documents_found.append("margarets_lament")
            if sanity < 50:
                narrator "The notes seem to move and rearrange themselves as you watch..."
                $ lose_sanity(5)
        
        "Try to play the piano":
            if "margarets_lament" in documents_found:
                narrator "You attempt to play Margaret's composition."
                narrator "As the melody fills the room, a hidden panel opens in the wall."
                narrator "Inside, you find Margaret's personal diary!"
                $ documents_found.append("margaret_diary")
                $ found_clues.append("diary_location")
                narrator "The diary details her final weeks and her growing fear of Edmund."
            else:
                narrator "You play a few random notes, but nothing happens."
                narrator "Perhaps you need the right sheet music."
        
        "Look for hidden compartments":
            narrator "You search the ornate piano bench and find a secret compartment."
            narrator "Inside is an old key and a note: 'For the Observatory - M'"
            $ inventory.append("observatory_key")
            $ has_key = True  
        
        "Listen carefully for supernatural sounds":
            if sanity < 60:
                narrator "You hear whispers in the walls, voices of the dead..."
                narrator "They're trying to tell you something, but you can't make it out."
                $ lose_sanity(10)
                $ paranoia_level += 1
            else:
                narrator "The room is eerily quiet. Too quiet."
                narrator "You notice the piano pedals are moving slightly, as if pressed by invisible feet."
                $ lose_sanity(5)
    
    jump enhanced_explore_mansion

label observatory:
    scene bg observatory
    with fade
    
    if "observatory_key" not in inventory:
        narrator "The observatory door is locked. You need a key."
        jump enhanced_explore_mansion
    
    narrator "The observatory is Silas's original study, preserved exactly as he left it."
    narrator "Astronomical charts cover the walls, and a large telescope points skyward."
    narrator "Ancient books on astrology and dark magic line the shelves."
    
    menu:
        "Study the astronomical charts":
            narrator "The charts show specific celestial alignments marked in red ink."
            narrator "These correspond to the dates of family deaths over the centuries."
            narrator "Silas was timing the killings to coincide with astrological events!"
            $ add_evidence("celestial_timing", "observatory", "Murders timed to cosmic events")
            $ found_clues.append("astrological_murders")
        
        "Examine Silas's personal grimoire":
            narrator "The ancient book contains detailed instructions for soul binding rituals."
            narrator "One page describes how to transfer consciousness between bodies."
            narrator "This explains how Silas has maintained his existence through different hosts!"
            $ found_clues.append("body_transfer")
            $ investigation_path = "supernatural"
        
        "Use the telescope":
            if current_time >= 20 or current_time <= 6:
                narrator "Through the telescope, you see the moon is almost full."
                narrator "According to the charts, this is when Silas's power peaks."
                narrator "You have perhaps one or two days before the next 'harvest.'"
                $ found_clues.append("lunar_deadline")
            else:
                narrator "The daylight makes astronomical observation impossible."
        
        "Search for the soul transfer ritual":
            if "body_transfer" in found_clues:
                narrator "You find the complete ritual instructions hidden in a false bottom drawer."
                narrator "The process requires the willing participation of the host."
                narrator "This means Edmund agreed to this arrangement... but why?"
                $ found_clues.append("willing_host")
            else:
                narrator "You search but find nothing significant without more context."
    
    jump enhanced_explore_mansion

label hidden_passages:
    narrator "You begin a systematic search for hidden passages throughout the manor."
    narrator "After an hour of pressing panels and examining bookcases, you discover several secret routes."
    
    $ lose_sanity(5)  
    
    narrator "The passages form a network connecting every major room."
    narrator "Someone could move through the house completely unseen."
    
    menu:
        "Follow the passage to the cellar":
            narrator "This passage leads directly to the ritual chamber."
            narrator "You find evidence that it's been used recently - fresh footprints in the dust."
            $ add_evidence("secret_access", "passages", "Recent use of hidden routes")
        
        "Track the passage to Edmund's quarters":
            narrator "The passage leads to a hidden room behind Edmund's quarters."
            narrator "Inside, you find journals dating back decades... in Edmund's handwriting."
            narrator "But the dates span far longer than any human lifetime."
            $ found_clues.append("edmund_journals")
            $ edmund_possession_level = 100
        
        "Explore the passage to the attic":
            narrator "This route connects to a hidden room in the attic."
            jump secret_attic_room
        
        "Map the entire network":
            narrator "You spend considerable time mapping all the passages."
            narrator "The network is extensive - someone spent decades constructing this."
            $ inventory.append("passage_map")
            $ advance_time(1)  
    
    jump enhanced_explore_mansion

label secret_attic_room:
    scene bg panic_room
    with fade
    
    narrator "The hidden attic room appears to be a panic room."
    narrator "It's stocked with food, water, and defensive weapons."
    narrator "Someone was preparing for a siege."
    
    narrator "On a desk, you find a desperate note in Margaret's handwriting:"
    narrator "'He knows I've discovered the truth. I'm running out of time.'"
    narrator "'If anyone finds this, the key to stopping Silas is in the original binding ritual.'"
    narrator "'But it requires a willing sacrifice from the bloodline - or a way to turn his own power against him.'"
    
    $ documents_found.append("margaret_final_note")
    $ found_clues.append("power_reversal")
    
    if "deadly_poison" in inventory:
        narrator "You also find a note about the greenhouse plants:"
        narrator "'The poison from the nightshade can weaken spiritual bonds if properly prepared.'"
        $ found_clues.append("poison_weakness")
    
    jump enhanced_explore_mansion

label town_investigation:
    scene bg town_square
    with fade
    
    narrator "The village of Ravenshollow is small and insular."
    narrator "The locals eye you with a mixture of pity and fear."
    
    menu:
        "Visit the Library":
            jump town_library
        "Talk to the Village Elder":
            jump village_elder
        "Investigate Local Records":
            jump local_records
        "Return to the Manor":
            $ advance_time(1)
            jump enhanced_explore_mansion

label town_library:
    show librarian at center
    with dissolve
    
    librarian "You must be the new Ravenshollow heir. I'm Ms. Blackwood."
    librarian "Detective Mills said you might come by."
    
    player "He mentioned you keep records about the manor?"
    
    librarian "Unofficial records. Things the town doesn't want outsiders to know."
    librarian "Your family... they've been both blessing and curse to this village."
    
    menu:
        "What kind of blessing?":
            librarian "The Ravenshollow fortune has supported this town for generations."
            librarian "Roads, schools, the hospital - all built with family money."
            librarian "But there's always been a price."
        
        "What price?":
            librarian "Every generation, someone disappears. Usually young people."
            librarian "The official stories are always accidents or runaways."
            librarian "But we know better."
            $ town_conspiracy_known = True
        
        "Show me the records":
            if town_conspiracy_known:
                librarian "These are newspaper clippings going back 150 years."
                librarian "Missing persons, unexplained deaths, all connected to the manor."
                $ documents_found.append("newspaper_archive")
                $ add_evidence("missing_persons", "town", "Pattern of disappearances")
            else:
                librarian "I'm sorry, but those records are... restricted."
    
    if "detective_card" in found_clues:
        librarian "Detective Mills left something for you."
        narrator "She hands you a sealed envelope marked 'Evidence Package.'"
        $ inventory.append("evidence_package")
    
    jump town_investigation

label village_elder:
    show townsperson at center
    with dissolve
    
    townsperson "Another Ravenshollow heir. You have the look of your bloodline."
    townsperson "How long do you think you'll last?"
    
    player "That's a strange thing to ask."
    
    townsperson "Is it? Your cousin Sarah lasted three days."
    townsperson "Your great aunt Margaret made it almost a month."
    townsperson "The brave ones always go first."
    
    $ sarah_mystery_unlocked = True
    
    menu:
        "What happened to Sarah?":
            townsperson "She came asking the same questions you probably are."
            townsperson "About the family curse, about Silas, about the deaths."
            townsperson "One morning, we found her car abandoned on the road."
            townsperson "But no body. The manor claimed another heir."
            $ found_clues.append("sarah_disappeared")
        
        "Why doesn't anyone stop this?":
            townsperson "Stop it? Child, we've been trying for generations."
            townsperson "But the manor's influence runs deep. It owns this town."
            townsperson "And some folks... some folks have made deals with the darkness."
            $ town_conspiracy_known = True
        
        "Can you help me?":
            if town_conspiracy_known:
                townsperson "There are a few of us who remember the old ways."
                townsperson "Ways to protect against evil spirits."
                narrator "He gives you a small bag of herbs and salt."
                $ inventory.append("protection_herbs")
                townsperson "Sprinkle this around your room before sleeping."
            else:
                townsperson "Help you? I'm afraid that's not possible."
                townsperson "Some battles must be fought alone."
    
    jump town_investigation

label local_records:
    narrator "You spend time at the town hall examining public records."
    narrator "Birth certificates, death certificates, property transfers..."
    narrator "The pattern becomes clear: the Ravenshollow family has controlled this town for generations."
    narrator "But the records also show unexplained gaps - periods where no one lived in the manor."
    narrator "These gaps always coincide with times when no heirs could be found."
    
    $ add_evidence("control_pattern", "town_hall", "Family has controlled town for generations")
    
    jump town_investigation

label start_enhanced_game:
    jump enhanced_explore_mansion
