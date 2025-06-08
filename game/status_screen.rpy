# game/status_screen.rpy
screen status():
    tag menu
    use game_menu(_("Status"), scroll="viewport"):
        vbox:
            spacing 20
            
            text "Character Status" size 30 color gui.accent_color
            
            hbox:
                text "Sanity: " size 20
                bar value sanity range 100 xsize 300
                text " [sanity]/100" size 20
                if sanity < 30:
                    text " (Severely Impaired)" color "#ff6666" size 16
                elif sanity < 60:
                    text " (Stressed)" color "#ffaa66" size 16
                else:
                    text " (Stable)" color "#66ff66" size 16
            
            hbox:
                text "Time: " size 20
                text "[current_time]:00" size 20 color "#99ccff"
            
            hbox:
                text "Day: " size 20
                text "[days_survived]" size 20 color "#99ccff"
            
            hbox:
                text "Edmund's State: " size 20
                $ state = check_edmund_state()
                if state == "possessed":
                    text "Possessed" color "#ff6666" size 20
                elif state == "influenced":
                    text "Influenced" color "#ffaa66" size 20
                else:
                    text "Normal" color "#66ff66" size 20
            
            hbox:
                text "Edmund Trust: " size 20
                bar value butler_trust range 10 xsize 200
                text " [butler_trust]/10" size 20
            
            null height 20
            
            text "Progress Tracking" size 24 color gui.accent_color
            
            text "Rooms Explored: [rooms_explored]" size 18
            text "Clues Found: [len(found_clues)]" size 18
            text "Evidence Pieces: [len(evidence_board)]" size 18
            text "Documents: [len(documents_found)]" size 18
            
            if len(found_clues) >= 15:
                text "🏆 Master Detective!" size 20 color "#gold"
            elif len(found_clues) >= 10:
                text "🕵️ Skilled Investigator" size 20 color "#silver"
            elif len(found_clues) >= 5:
                text "🔍 Amateur Sleuth" size 20 color "#bronze"
