# game/inventory_screen.rpy
screen inventory():
    tag menu
    use game_menu(_("Inventory"), scroll="viewport"):
        vbox:
            spacing 15
            
            text "Items:" size 30 color gui.accent_color
            
            if len(inventory) == 0:
                text "Your inventory is empty." italic True
            else:
                for item in inventory:
                    hbox:
                        spacing 10
                        if item == "plant_samples":
                            text "🌿 Plant Samples" size 20
                            text "- Poisonous specimens from the greenhouse"
                        elif item == "deadly_poison":
                            text "☠️ Deadly Poison" size 20 color "#ff6666"
                            text "- Concentrated plant extract"
                        elif item == "observatory_key":
                            text "🗝️ Observatory Key" size 20 color "#ffff99"
                            text "- Opens the tower observatory"
                        elif item == "protection_herbs":
                            text "🌱 Protection Herbs" size 20 color "#99ff99"
                            text "- Traditional warding materials"
                        elif item == "passage_map":
                            text "🗺️ Passage Map" size 20
                            text "- Complete layout of hidden routes"
                        elif item == "evidence_package":
                            text "📁 Evidence Package" size 20 color "#99ccff"
                            text "- Detective Mills' investigation files"
                        else:
                            text "📦 [item.replace('_', ' ').title()]" size 20
            
            null height 20
            
            text "Documents:" size 30 color gui.accent_color
            
            if len(documents_found) == 0:
                text "No documents found." italic True
            else:
                for doc in documents_found:
                    hbox:
                        spacing 10
                        if doc == "gardening_journal":
                            text "📖 Gardening Journal" size 20
                            text "- Edmund's plant cultivation notes"
                        elif doc == "margaret_diary":
                            text "📔 Margaret's Diary" size 20 color "#ff99ff"
                            text "- Your great aunt's final thoughts"
                        elif doc == "margarets_lament":
                            text "🎵 Margaret's Lament" size 20
                            text "- Haunting musical composition"
                        elif doc == "margaret_final_note":
                            text "📝 Margaret's Final Note" size 20 color "#ffaaaa"
                            text "- Desperate warning from the panic room"
                        elif doc == "newspaper_archive":
                            text "📰 Newspaper Archive" size 20
                            text "- Historical missing persons reports"
                        else:
                            text "📄 [doc.replace('_', ' ').title()]" size 20
