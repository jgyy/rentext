# game/evidence_board.rpy
screen evidence_board():
    tag menu
    use game_menu(_("Evidence Board"), scroll="viewport"):
        vbox:
            spacing 20
            
            text "Investigation Progress" size 30 color gui.accent_color
            
            text "Path: [investigation_path.title()]" size 24
            
            null height 10
            
            text "Evidence Collected:" size 24 color gui.text_color
            
            if len(evidence_board) == 0:
                text "No evidence collected yet." italic True
            else:
                for evidence, details in evidence_board.items():
                    vbox:
                        spacing 5
                        hbox:
                            text "🔍 [evidence.replace('_', ' ').title()]" size 20 color "#ffff99"
                        hbox:
                            spacing 20
                            text "Location:" size 16
                            text "[details['location'].title()]" size 16 color "#99ccff"
                        hbox:
                            spacing 20
                            text "Significance:" size 16
                            text "[details['significance']]" size 16 color "#99ff99"
                        null height 10
            
            null height 20
            
            text "Theories Formed:" size 24 color gui.text_color
            
            if len(theories_formed) == 0:
                text "No theories yet. Gather more evidence!" italic True
            else:
                for theory in theories_formed:
                    text "💡 [theory]" size 18 color "#ffaa99"
