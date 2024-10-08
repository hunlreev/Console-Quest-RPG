'''
Module Name: main.py
Description: Contains the actual gameplay loop and all the pieces that are implemented for it.
Author: Hunter Reeves
Date: 2024-08-12
'''

from modules.menu import console_input, clear_console, main_menu, pause_menu
from modules.game import about_game, new_game, save_game, load_game, delete_game
from modules.console_art import art_planet, art_stars, art_battleaxe, art_skull, art_dragon
from modules.format import menu_line

from classes.Player import Player
from classes.Enemy import Enemy

import time
import random

def shop_menu(player):
    """
    Displays the shop menu where the player can choose to buy items, sell items, or return to the game.

    Parameters:
        player (Player): The character save file that the user goes through the game with.

    Returns:
        None.
    """

    while True:
        clear_console()
        art_planet()
        menu_line()
        print(" ^ The Medieval World Shoppe")
        menu_line()
        print(" 1. Buy Items")
        print(" 2. Sell Items")
        print(" 3. Leave Shop")
        menu_line()

        print(" * Please select an option from the menu above...")
        menu_line()
        choice = console_input()

        if choice == "1":
            buy_items(player)
        elif choice == "2":
            sell_items(player)
        elif choice == "3":
            return
        else:
            return
        
def load_shop_selling_items(file_path='.\\config\\shopSelling.txt'):
    """
    Loads items from the shop file, generating a random buy price for each item.

    Parameters:
        file_path (str): The path to the shop items file.

    Returns:
        items (list): A list of dictionaries representing items available in the shop.
    """
    
    selling_items = []

    with open(file_path, 'r') as file:
        for line in file:
            name, min_price, max_price = line.strip().split(', ')
            min_price, max_price = int(min_price), int(max_price)
            buy_price = random.randint(min_price, max_price)
            selling_items.append({
                'name': name,
                'sell_price': buy_price
            })

    return selling_items

def load_shop_buying_items(file_path='.\\config\\shopBuying.txt'):
    """
    Loads items from the shop file, generating a random sell price for each item.

    Parameters:
        file_path (str): The path to the shop items file.

    Returns:
        items (list): A list of dictionaries representing items available in the shop.
    """

    buying_items = []

    with open(file_path, 'r') as file:
        for line in file:
            name, min_price, max_price = line.strip().split(', ')
            min_price, max_price = int(min_price), int(max_price)
            sell_price = random.randint(min_price, max_price)
            buying_items.append({
                'name': name,
                'sell_price': sell_price
            })

    return buying_items

def buy_items(player):
    """
    Allows the player to buy items from the shop.

    Parameters:
        player (Player): The character save file that the user goes through the game with.

    Returns:
        None.
    """
    
    shop_selling_items = load_shop_selling_items()

    # Randomly select 5 items from the shop selling items
    items_to_display = random.sample(shop_selling_items, min(5, len(shop_selling_items)))

    clear_console()
    art_planet()
    menu_line()
    print(" ^ Buy from the Medieval World Shoppe")
    menu_line()
    print(f" - Gold: {int(player.gold)}")
    menu_line()

    # Loop through the selected items 
    for index, item in enumerate(items_to_display, start=1):
        print(f" {index}. {item['name']} @ {item['sell_price']}g each")

    menu_line()
    # Ask the player what item to buy
    print(f" * Choose an item to buy using the leading number.")
    menu_line()

    item_choice = console_input()

    # Exit if user doesn't enter in a number
    if item_choice == '':
        return

    # Get the selected item
    selected_item = items_to_display[int(item_choice) - 1]
    item_name = selected_item['name']
    item_price = selected_item['sell_price']

    # Ask the player how many of the item they want to buy
    menu_line()
    print(f" * How many {item_name}s do you want to buy?")
    menu_line()
    quantity_choice = console_input()

    try:
        quantity_choice = int(quantity_choice)
        total_cost = item_price * quantity_choice
        
        # Check if the player has enough gold
        if player.gold < total_cost:
            raise ValueError("Not enough gold")

        # Subtract the total cost from the player's gold
        player.gold -= total_cost

        # Add the purchased items to the player's inventory
        if item_name in player.inventory:
            player.inventory[item_name] += quantity_choice
        else:
            player.inventory[item_name] = {'count': quantity_choice}

        menu_line()
        print(f" * You bought {quantity_choice} {item_name}(s) for {total_cost}g!")
        menu_line()
        print(f" - You now have {int(player.gold)}g.")
        menu_line()
        print(" * Press enter to return to the shop menu...")
        menu_line()
        console_input()
    except ValueError:
        print(" * Invalid selection or insufficient funds.")

def sell_items(player):
    """
    Allows the player to sell items from their inventory.

    Parameters:
        player (Player): The character save file that the user goes through the game with.

    Returns:
        None.
    """

    shop_buying_items = load_shop_buying_items()

    clear_console()
    art_planet()
    menu_line()
    print(" ^ Sell to the Medieval World Shoppe")
    menu_line()
    print(f" - Gold: {int(player.gold)}")
    menu_line()
    
    if not player.inventory:
        print(" - Your inventory is currently empty.")
        menu_line()
        print(" * Press enter to return to the shop menu...")
        menu_line()
        console_input()
        return

    # Loop through the inventory items
    for index, (item_name, details) in enumerate(player.inventory.items(), start=1):
        item_count = details['count']

        # Find the corresponding shop item to get the sell price
        shop_item = next((shop_item for shop_item in shop_buying_items if shop_item['name'] == item_name), None)
        if shop_item:
            print(f" {index}. {item_name} (x{item_count}) @ {shop_item['sell_price']}g each")

    menu_line()
    # Ask the player what item to sell
    print(f" * Choose an item to sell using the leading number.")
    menu_line()

    item_choice = console_input()

    try:
        item_choice = int(item_choice) - 1
        if item_choice < 0 or item_choice >= len(player.inventory):
            raise ValueError
    except ValueError:
        return
    
    # Get the selected item
    selected_item_name = list(player.inventory.keys())[item_choice]
    selected_item = player.inventory[selected_item_name]

    # Ask the player how many of the item they want to sell
    max_quantity = selected_item['count']
    menu_line()
    print(f" * How many {selected_item_name} do you want to sell? (1-{max_quantity})")
    menu_line()
    quantity_choice = console_input()

    try:
        quantity_choice = int(quantity_choice)
        if quantity_choice < 1 or quantity_choice > max_quantity:
            raise ValueError
    except ValueError:
        return
    
    # Calculate the gold earned from the sale
    shop_item = next((shop_item for shop_item in shop_buying_items if shop_item['name'] == selected_item_name), None)
    if shop_item:
        total_gold = shop_item['sell_price'] * quantity_choice
        player.gold += total_gold
        player.inventory[selected_item_name]['count'] -= quantity_choice

        # Remove the item from inventory if count reaches zero
        if player.inventory[selected_item_name]['count'] <= 0:
            del player.inventory[selected_item_name]

        menu_line()
        print(f" - You sold {quantity_choice} {selected_item_name} for {total_gold}g.")
        menu_line()
        print(f" - You now have {int(player.gold)}g.")
        menu_line()
        print(" * Press enter to return to the shop menu...")
        menu_line()
        console_input()

def update_enemy_health_bar(enemy):
    """
    Takes enemy health and builds an updated health bar while in combat

    Parameters:
        enemy (object): The enemy.

    Returns:
        None.
    """

    health_bar, health_display = enemy.generate_stat_bar(enemy.stats['Health'], enemy.max_stats['Health'], 50, 'red')
    
    print(f" -  HP: {health_bar} " + health_display)

def update_exp_bar(player):
    """
    Takes player experience and displays an experience bar

    Parameters:
        player (object): The player character.

    Returns:
        None.
    """

    bar_length = 46
    
    exp_bar, exp_display = player.generate_exp_bar(round(player.experience, 2), round(player.next_experience, 2), bar_length, 'yellow')

    print(f" - EXP: {exp_bar} " + exp_display)

def update_stat_bars(player):
    """
    Takes player stats and builds updated stat bars before printing them out.

    Parameters:
        player (object): The player character.

    Returns:
        None.
    """

    bar_length = 50
    
    health_bar, health_display = player.generate_stat_bar(round(player.stats['Health'], 2), round(player.max_stats['Health'], 2), bar_length, 'red')
    mana_bar, mana_display = player.generate_stat_bar(round(player.stats['Mana'], 2), round(player.max_stats['Mana'], 2), bar_length, 'blue')
    stamina_bar, stamina_display = player.generate_stat_bar(round(player.stats['Stamina'], 2), round(player.max_stats['Stamina'], 2),bar_length, 'green')

    print(f" -  HP: {health_bar} " + health_display)
    print(f" -  MP: {mana_bar} " + mana_display)
    print(f" -  SP: {stamina_bar} " + stamina_display)

def recover_stats(player):
    """
    Handles the resting portion of the game.

    Parameters:
        player (Player): The character save file that the user goes through the game with.

    Returns:
        None.
    """

    seconds_to_wait = player.rest()
    menu_line()
    speed = player.attributes['Speed']
    
    if speed < 10:
        print(" - Resting proves to be a challenge as you struggle to find comfort...")
    elif 10 <= speed < 20:
        print(" - You try to rest, but it's a bit of a struggle...")
    elif 20 <= speed < 30:
        print(" - It's not very effective, but you manage to rest anyway...")
    elif 30 <= speed < 40:
        print(" - You relax for a bit, and take your time to recover...")
    elif 40 <= speed < 50:
        print(" - A brief rest leaves you feeling much better than before...")
    elif 50 <= speed < 60:
        print(" - You rest for a short while and feel rejuvenated...")
    elif 60 <= speed < 70:
        print(" - You recover in no time and enjoy your rest...")
    elif 70 <= speed < 80:
        print(" - You rest and recover quickly, thinking about your progress...")
    elif 80 <= speed < 90:
        print(" - Your efficient rest results in near-instant recovery...")
    elif 90 <= speed < 100:
        print(" - You rejoice at the opportunity to restore yourself!")
    elif speed == 100:
        print(" - You recover your health instantly!")
    else:
        print(" - You take some time to rest and recuperate...")

    menu_line()
    time.sleep(seconds_to_wait)

def print_all_stats(player):
    """
    Prints all stats so the player can see their progress

    Parameters:
        player (object): The player

    Returns:
        None.
    """

    clear_console()
    art_stars()
    menu_line()
    print(f" ^ {player.name}'s Stats")
    menu_line()
    print(f" - Available Attribute Points: {player.attribute_points}")
    menu_line()
    print(f" - Strength: {player.attributes['Strength']}")
    print(f" - Endurance: {player.attributes['Endurance']}")
    print(f" - Intelligence: {player.attributes['Intelligence']}")
    print(f" - Willpower: {player.attributes['Willpower']}")
    print(f" - Agility: {player.attributes['Agility']}")
    print(f" - Speed: {player.attributes['Speed']}")
    menu_line()
    print(f" - Physical attack: {player.physical_attack}")
    print(f" - Magical attack: {player.magical_attack}")
    menu_line()
    print(f" - Physical defense: {player.physical_defense}")
    print(f" - Magical defense: {player.magical_defense}")
    menu_line()
    print(f" - Enemies Killed: {player.total_kills}")
    print(f" - Number of Deaths: {player.total_deaths}")
    # Determine KD Ratio
    if player.total_deaths == 0:
        kill_death_ratio = "N/A"
    else:
        kill_death_ratio = round(player.total_kills / player.total_deaths, 1)
    print(f" - Kill/Death Ratio: {kill_death_ratio}")
    menu_line()

def check_dodge(attacker, defender, dodge_threshold):
    """
    Handles the dodge logic during an encounter.

    Parameters:
        attacker (Player or Enemy): The character or enemy attacking.
        defender (Player or Enemy): The character or enemy being attacked.
        dodge_threshold (float): To check if a dodge is executed or not.

    Returns:
        bool (bool): Check if dodge happened or not.
    """

    if dodge_threshold < attacker.dodge_chance:
        return True
    else:
        return False

def run_away(attacker, defender):
    """
    Handles the running away portion of the encounter.

    Parameters:
        attacker (Player or Enemy): The character or enemy attacking.
        defender (Player or Enemy): The character or enemy being attacked.

    Returns:
        message (str): A dynamic message for displaying additional information
    """

    if attacker.attributes['Speed'] > defender.attributes['Speed']:
        return "Run away!"
    else:
        return f" - Oh no, you are too slow! You cannot run from this {defender.description}."

def cast_spell(attacker, defender):
    """
    Handles the spell casting portion of the encounter.

    Parameters:
        attacker (Player or Enemy): The character or enemy attacking.
        defender (Player or Enemy): The character or enemy being attacked.

    Returns:
        message (str): A dynamic message for displaying additional information
    """

    crit_threshold = round(random.random(), 2)
    dodge_threshold = round(random.random(), 2)

    if attacker.stats['Mana'] < attacker.mana_cost:
        return f" - {attacker.description} doesn't have enough mana to cast a spell right now!"

    if crit_threshold < attacker.critical_chance:
        defender.stats['Health'] -= attacker.critical_hit
        attacker.stats['Mana'] -= attacker.mana_cost
        return f" - {attacker.description} landed a critical hit, dealing massive damage!"

    if check_dodge(attacker, defender, dodge_threshold):
        return f" - {defender.description} dodged the {attacker.description}'s spell!"

    defender.stats['Health'] -= max(0, attacker.magical_attack - defender.magical_defense)
    attacker.stats['Mana'] -= attacker.mana_cost
    return f" - {attacker.description} successfully casted a spell at the {defender.description}!"

def attack(attacker, defender):
    """
    Handles the attacking portion of the encounter.

    Parameters:
        attacker (Player or Enemy): The character or enemy attacking.
        defender (Player or Enemy): The character or enemy being attacked.

    Returns:
        message (str): A dynamic message for displaying additional information.
    """

    crit_threshold = round(random.random(), 2)
    dodge_threshold = round(random.random(), 2)

    if attacker.stats['Stamina'] < attacker.stamina_cost:
        damage = max(0, attacker.physical_attack * 0.75 - defender.physical_defense)
        defender.stats['Health'] -= damage
        return f" - {attacker.description} doesn't have enough stamina and isn't as effective!"

    if crit_threshold < attacker.critical_chance:
        defender.stats['Health'] -= attacker.critical_hit
        attacker.stats['Stamina'] -= attacker.stamina_cost
        return f" - {attacker.description} landed a critical hit, dealing massive damage!"

    if check_dodge(attacker, defender, dodge_threshold):
        return f" - {defender.description} dodged the {attacker.description}'s attack!"

    damage = max(0, attacker.physical_attack - defender.physical_defense)
    defender.stats['Health'] -= damage
    attacker.stats['Stamina'] -= attacker.stamina_cost
    return f" - {attacker.description} successfully attacked the {defender.description}!"
    
def enemy_decision(enemy, player):
    """
    Handle the enemy section of combat.

    Parameters:
        player (Player): The character save file that the user goes through the game with.
        enemy (Enemy): The current enemy in the encounter.
        user_input (string): Option the player selected in the previous menu.

    Returns:
        message (str): A dynamic message for displaying additional information
    """

    message = ""
    options = ['1', '2']
    random_selection = random.choice(options)

    if random_selection == options[0]:
        message = attack(enemy, player)
    elif random_selection == options[1]:
        message = cast_spell(enemy, player)
    
    return message

def player_decision(player, enemy, user_input):
    """
    Handles the player section of combat.

    Parameters:
        player (Player): The character save file that the user goes through the game with.
        enemy (Enemy): The current enemy in the encounter.
        user_input (string): Option the player selected in the previous menu.

    Returns:
        message (str): A dynamic message for displaying additional information
    """

    message = ""

    if user_input == '1':
        message = attack(player, enemy)
    elif user_input == '2':
        message = cast_spell(player, enemy)
    elif user_input == '3':
        message = run_away(player, enemy)
    # Debug - for instant killing enemies so I can test my code
    elif user_input == '4':
        message = "Debug"
        enemy.stats['Health'] -= 1000
    
    return message

def enemy_encounter(player, message):
    """
    Handles the enemy encounters when they happen.

    Parameters:
        player (Player): The character save file that the user goes through the game with.
        message (str): A message that displays when updated.

    Returns:
        None.
    """

    def return_to_main_menu_countdown(seconds):
        import sys
        
        for i in range(seconds, 0, -1):
            sys.stdout.write(f"\r ^ Returning to main menu in: {i}")
            sys.stdout.flush()
            time.sleep(1)
        sys.stdout.write("\r ^ Returning to main menu in: 0\n")
        sys.stdout.flush()

    def determine_enemy_drop():
        for item_name, item_info in enemy.dropped_item.items():
            item_name = item_info['name']
            item_count = item_info['count']
            
            if item_count <= 0:
                continue
            
            print(f" - You looted {item_count} {item_name}.")
            
            if item_name in player.inventory:
                player.inventory[item_name]['count'] += item_count
            else:
                player.inventory[item_name] = {'count': item_count}
        
    enemy = Enemy(player.level, 2, player.location)
    turn_counter = 1
    
    if player.attributes['Speed'] >= enemy.attributes['Speed']:
        isPlayerTurn = True
    else:
        isPlayerTurn = False

    while player.stats['Health'] > 0:
        clear_console()
        art_battleaxe()
        menu_line()
        print(f" ^ You encountered a Level {enemy.level} {enemy.type} at {player.location}!")
        menu_line()
        update_enemy_health_bar(enemy)
        menu_line()
        update_stat_bars(player)
        menu_line()
        
        if message != "":
            print(message)
            menu_line()
            
        if turn_counter % 2 == 1 and isPlayerTurn:
            isPlayerTurn = False
            print(" * What would you like to do?")
            menu_line()
            print(" 1. Attack\n 2. Cast Spell\n 3. Run Away")
            menu_line()
            user_input = console_input()
            message = player_decision(player, enemy, user_input)
        elif turn_counter % 2 == 0 and not isPlayerTurn:
            isPlayerTurn = True
            print(f" * {enemy.type} is making a decision...")
            menu_line()
            time.sleep(3)
            message = enemy_decision(enemy, player)

        turn_counter += 1 
        
        mana_recovery = round(player.attributes['Willpower'] * 0.03, 2)
        stamina_recovery = round(player.attributes['Endurance'] * 0.03, 2)
        
        player_mana = player.stats['Mana']
        player_stamina = player.stats['Stamina']
        
        mana_difference = player.max_stats['Mana'] - player.stats['Mana']
        stamina_difference = player.max_stats['Stamina'] - player.stats['Stamina']
                
        player.stats['Mana'] += mana_recovery if player_mana + mana_recovery <= player.max_stats['Mana'] else mana_difference
        player.stats['Stamina'] += stamina_recovery if player_stamina + stamina_recovery <= player.max_stats['Stamina'] else stamina_difference
        
        if message == "Run away!":
            clear_console()
            art_planet()
            menu_line()
            print(f" ^ You managed to run away from the {enemy.type}!")
            menu_line()
            time.sleep(3)
            break
        
        if player.stats['Health'] <= 0:
            player.total_deaths += 1
            player.max_stats['Health'] -= 1
            player.max_stats['Mana'] -= 1
            player.max_stats['Stamina'] -= 1
            health_penalty = round(player.max_stats['Health'] * 0.10, 2)
            player.stats['Health'] = max(health_penalty, 1)
            player.experience -= round(player.experience * 0.5, 2)
            save_game(player)
            clear_console()
            art_skull()
            menu_line()
            print(f" ^ The {enemy.type} killed you! You have lost some progress as a result.")
            menu_line()
            return_to_main_menu_countdown(5)
            break

        if enemy.stats['Health'] <= 0:
            player.total_kills += 1
            clear_console()
            art_stars()
            menu_line()
            print(f" ^ You defeated the {enemy.type}!")
            menu_line()
            level_cap = 50

            if player.level < level_cap:
                print(f" - You have earned {int(enemy.dropped_exp)} experience.")
                player.experience += enemy.dropped_exp
                
            print(f" - You looted {int(enemy.dropped_gold)} gold.")
            determine_enemy_drop()
            menu_line()
            player.gold += enemy.dropped_gold
            time.sleep(4)

            if player.experience >= player.next_experience and player.level < level_cap:
                clear_console()
                player.level_up()
            break

    return_to_game(user_input)

def explore_location(player, locations, encounter_rate):
    """
    Allows the player to explore a randomly selected location.

    Parameters:
        player (Player): The character save file that the user goes through the game with.
        locations (List): A list of locations for the player to explore.
        encounter_rate (Float): A value from 0 to 1 that describes the encounter rate.

    Returns:
        None.
    """
    
    player.location = random.choice(locations)

    exploration_time = random.choice([(1, "a quick adventure"), (2, "a short, nearby exploration"), (3, "a long journey"), (4, "huge campaign and get lost")])

    menu_line()
    print(f" - You set out for {exploration_time[1]}...")
    menu_line()
    time.sleep(exploration_time[0])

    message = ""

    if random.random() < encounter_rate:
        enemy_encounter(player, message)
    else:
        return_to_game("")

def return_to_game(user_input):
    """
    Takes the user back to the main game menu to continue playing.

    Parameters:
        user_input (str): User input.

    Returns:
        user_input (str): Empty string to continue playing.
    """

    user_input = ''

    return user_input

def display_menu(player):
    """
    Display the game menu.

    Parameters:
        player (Player): The character save file that the user goes through the game with.

    Returns:
        str: The user's input.
    """

    clear_console()
    menu_line()
    print(f" ^ Welcome {player.name} the {player.sex} {player.race}!")
    menu_line()
    print(f" - You are a Level {player.level} {player.player_class}, born under {player.birth_sign} sign.")
    menu_line()
    print(f" - Gold: {int(player.gold)}")
    menu_line()
    print(f" - Current Location: {player.location}")
    menu_line()
    update_stat_bars(player)
    menu_line()
    update_exp_bar(player)
    menu_line()
    print(" * What would you like to do?")
    menu_line()

    options = {"Pause Game": 1, "Explore World": 2, "View Stats": 3, "View Inventory": 4, "Visit Shop": 5, "Rest": 6}

    for option, number in options.items():
        print(f" {number}. {option}")

    menu_line()

    return console_input()

def start_game(player):
    """
    The main gameplay loop for Console Quest RPG.

    Parameters:
        player (Player): The character save file that the user goes through the game with.

    Returns:
        None.
    """

    def pause_menu_selection():
        if user_input == '1':
            return_to_game(user_input)
        elif user_input == '2':
            save_game(player)
        elif user_input == '3':
            save_game(player)
            return "Exit"
        elif user_input == '4':
            return "Exit"
        elif user_input == '5':
            delete_game()
        else:
            return_to_game(user_input)

    locations = ["Small Town", "Foggy Forest", "Desolate Cave", "Knoll Mountain", "Sandy Beach", "Abandoned Fort", "Sacked Camp"]

    encounter_rate = 0.67

    if player is None:
        return

    while player.stats['Health'] > 0:
        user_input = display_menu(player)

        if user_input == '1':
            pause_menu()
            user_input = console_input()
            exit = pause_menu_selection()

            if exit == "Exit":
                break
        elif user_input == '2':
            clear_console()
            art_planet()
            explore_location(player, locations, encounter_rate)
        elif user_input == '3':
            print_all_stats(player)
            print(" * Press enter to return to the game...")
            menu_line()
            console_input()
        elif user_input == '4':
            clear_console()
            art_dragon()
            menu_line()

            if not player.inventory:
                print(" ^ Your inventory is currently empty.")
            else:
                print(f" ^ {player.name}'s Inventory:")
                menu_line()
                for item, details in player.inventory.items():
                    print(f" - {item} (x{details['count']})")

            menu_line()
            print(" * Press enter to return to the game...")
            menu_line()
            console_input()
        elif user_input == '5':
            clear_console()
            shop_menu(player)
        elif user_input == '6':
            clear_console()
            art_stars()
            recover_stats(player)
        # Debug - for testing stuff in the game
        elif user_input == '7':
            if player.level >= 50:
                player.experience = player.next_experience
                continue
            player.experience += 2500
            if player.experience >= player.next_experience:
                clear_console()
                player.level_up()
        elif user_input == '8':
            player.stats['Health'] = player.max_stats['Health']
            player.stats['Mana'] = player.max_stats['Mana']
            player.stats['Stamina'] = player.max_stats['Stamina']
        else:
            return_to_game(user_input)
    
def initialize_game():
    """
    Initializes the main menu for Console Quest RPG.
    
    Parameters:
        None.
    
    Returns:
        None.
    """

    while True:
        clear_console()
        main_menu()
        print(" * Select an option from the menu above:")
        menu_line()
        user_input = console_input()

        if user_input == '1':
            name, sex, race, birth_sign, player_class, attributes = new_game()

            player_info = {
                'name': name,
                'sex': sex,
                'race': race,
                'birth_sign': birth_sign,
                'player_class': player_class,
                'attributes': attributes
            }
            player = Player(**player_info)
            start_game(player)
        elif user_input == '2':
            player = load_game()
            start_game(player)
        elif user_input == '3':
            about_game()
        elif user_input == '4':
            break