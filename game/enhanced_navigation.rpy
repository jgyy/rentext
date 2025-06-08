# game/enhanced_navigation.rpy
screen enhanced_navigation():
    vbox:
        style_prefix "navigation"
        xpos gui.navigation_xpos
        yalign 0.5
        spacing gui.navigation_spacing

        if main_menu:
            textbutton _("New Game") action Start()
            textbutton _("Continue Enhanced") action Start("start_enhanced_game")
        else:
            textbutton _("History") action ShowMenu("history")
            textbutton _("Save") action ShowMenu("save")

        textbutton _("Load") action ShowMenu("load")
        textbutton _("Inventory") action ShowMenu("inventory")
        textbutton _("Evidence Board") action ShowMenu("evidence_board")
        textbutton _("Status") action ShowMenu("status")
        textbutton _("Achievements") action ShowMenu("achievements")
        textbutton _("Preferences") action ShowMenu("preferences")

        if _in_replay:
            textbutton _("End Replay") action EndReplay(confirm=True)
        elif not main_menu:
            textbutton _("Main Menu") action MainMenu()

        textbutton _("About") action ShowMenu("about")

        if renpy.variant("pc") or (renpy.variant("web") and not renpy.variant("mobile")):
            textbutton _("Help") action ShowMenu("help")

        if renpy.variant("pc"):
            textbutton _("Quit") action Quit(confirm=not main_menu)

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
    
    def save_achievement_progress():
        for achievement, unlocked in achievements.items():
            if unlocked:
                persistent.total_achievements[achievement] = True

label save_progress:
    $ save_achievement_progress()
    return

init python:
    def track_ending(ending_name):
        persistent.endings_seen.add(ending_name)
        persistent.playthroughs += 1
        save_achievement_progress()

label tracked_good_ending:
    call good_ending
    $ track_ending("curse_broken")
    return

label tracked_bad_ending:
    call bad_ending
    $ track_ending("curse_continues")
    return

label tracked_perfect_ending:
    call perfect_knowledge_ending
    $ track_ending("perfect_resolution")
    return

label new_game_plus:
    if persistent.playthroughs > 0:
        narrator "Welcome back to Ravenshollow Manor."
        narrator "Your previous experiences echo in your mind..."
        
        if persistent.total_achievements["detective"]:
            $ found_clues.append("detective_instincts")
            narrator "Your investigative instincts are sharper this time."
        
        if persistent.total_achievements["scholar"]:
            $ gain_sanity(20)
            narrator "Your knowledge of the family history provides some comfort."
        
        if len(persistent.endings_seen) >= 3:
            narrator "The paths through this nightmare are becoming clearer."
            $ sanity = min(100, sanity + 10)
    
    jump start_enhanced_game
