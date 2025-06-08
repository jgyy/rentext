# game/common_functions.rpy
init python:
    def lose_sanity(amount):
        global sanity, paranoia_level
        sanity = max(0, sanity - amount)
        if sanity < 50:
            paranoia_level += 1
        return sanity
    
    def gain_sanity(amount):
        global sanity
        sanity = min(100, sanity + amount)
        return sanity
    
    def advance_time(hours):
        global current_time, days_survived, edmund_possession_level
        current_time += hours
        if current_time >= 24:
            current_time -= 24
            days_survived += 1
        
        if 22 <= current_time or current_time <= 6:
            edmund_possession_level = min(100, edmund_possession_level + 10)
        else:
            edmund_possession_level = max(0, edmund_possession_level - 5)
    
    def add_evidence(item, location, significance):
        evidence_board[item] = {"location": location, "significance": significance}
    
    def check_edmund_state():
        if edmund_possession_level > 70:
            return "possessed"
        elif edmund_possession_level > 40:
            return "influenced"
        else:
            return "normal"
    
    def unlock_achievement(achievement_name):
        global achievements
        if achievement_name in achievements and not achievements[achievement_name]:
            achievements[achievement_name] = True
            renpy.notify("Achievement Unlocked: " + achievement_name.title().replace("_", " "))
            return True
        return False

    def check_all_achievements():
        return all(achievements.values())
    
    def save_achievement_progress():
        for achievement, unlocked in achievements.items():
            if unlocked:
                persistent.total_achievements[achievement] = True
    
    def track_ending(ending_name):
        persistent.endings_seen.add(ending_name)
        persistent.playthroughs += 1
        save_achievement_progress()

label save_progress:
    $ save_achievement_progress()
    return
