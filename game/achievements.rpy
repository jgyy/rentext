# game/achievements.rpy
init python:
    def unlock_achievement(achievement_name):
        global achievements
        if achievement_name in achievements and not achievements[achievement_name]:
            achievements[achievement_name] = True
            renpy.notify("Achievement Unlocked: " + achievement_name.title().replace("_", " "))
            return True
        return False

    def check_all_achievements():
        return all(achievements.values())

screen achievements():
    tag menu
    use game_menu(_("Achievements"), scroll="viewport"):
        vbox:
            spacing 20
            
            if achievements["detective"]:
                hbox:
                    text "🕵️ Detective" size 24 color "#ffff99"
                    text " - Solved the mystery through investigation"
            else:
                hbox:
                    text "🔒 Detective" size 24 color "#666666"
                    text " - ???"
            
            if achievements["pacifist"]:
                hbox:
                    text "☮️ Pacifist" size 24 color "#99ff99"
                    text " - Resolved conflict without violence"
            else:
                hbox:
                    text "🔒 Pacifist" size 24 color "#666666"
                    text " - ???"
            
            if achievements["scholar"]:
                hbox:
                    text "📚 Scholar" size 24 color "#9999ff"
                    text " - Found all historical documents"
            else:
                hbox:
                    text "🔒 Scholar" size 24 color "#666666"
                    text " - ???"
            
            if achievements["survivor"]:
                hbox:
                    text "🏃 Survivor" size 24 color "#ff9999"
                    text " - Escaped without breaking the curse"
            else:
                hbox:
                    text "🔒 Survivor" size 24 color "#666666"
                    text " - ???"
            
            if achievements["truth_seeker"]:
                hbox:
                    text "🔍 Truth Seeker" size 24 color "#ffaa99"
                    text " - Uncovered the rational explanation"
            else:
                hbox:
                    text "🔒 Truth Seeker" size 24 color "#666666"
                    text " - ???"
            
            if achievements["family_historian"]:
                hbox:
                    text "🏰 Family Historian" size 24 color "#aa99ff"
                    text " - Learned the complete family history"
            else:
                hbox:
                    text "🔒 Family Historian" size 24 color "#666666"
                    text " - ???"
            
            null height 20
            
            if check_all_achievements():
                text "🏆 MASTER OF RAVENSHOLLOW MANOR 🏆" size 30 color "#gold" xalign 0.5
