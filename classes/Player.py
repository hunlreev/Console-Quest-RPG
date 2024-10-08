'''
Class Name: Player.py
Description: Default Player class of which all other characters will use.
Author: Hunter Reeves
Date: 2024-08-11
'''

from modules.menu import menu_line
from modules.core import console_input, clear_console
from modules.console_art import art_stars

import random
import time

class Player:
    def __init__(self, name, sex, race, birth_sign, player_class, attributes):
        self.name = name
        self.sex = sex
        self.race = race
        self.birth_sign = birth_sign
        self.player_class = player_class
        self.attributes = {attr: max(0, min(100, value)) for attr, value in attributes.items()}
        self.level = 1
        self.experience = 0
        self.next_experience = 100
        self.attribute_points = 0
        self.gold = 0
        self.location = "Small Town"
        self.description = self.player_class
        self.total_kills = 0
        self.total_deaths = 0
        self.inventory = {}
        self.stats = {
            'Health': self.calculate_stat('Endurance', self.level),
            'Mana': self.calculate_stat('Intelligence', self.level),
            'Stamina': self.calculate_stat('Strength', self.level)
        }
        self.max_stats = {
            'Health': self.stats['Health'], 
            'Mana': self.stats['Mana'], 
            'Stamina': self.stats['Stamina']
        }
        self.defense_modifier = 100
        self.physical_attack = round(1.0 + 10.5 * (self.attributes['Strength'] / 100) * (1 + 0.07 * self.level), 0)
        self.magical_attack = round(1.0 + 10.5 * (self.attributes['Intelligence'] / 100) * (1 + 0.07 * self.level), 0)
        self.critical_hit = self.physical_attack + round(2.5 * ((self.attributes['Agility'] * 12) / 100) + 0.08 * self.level, 0)
        self.physical_defense = round(((self.attributes['Endurance'] * 2) / self.defense_modifier) + (0.1 * self.level), 0)
        self.magical_defense = round(((self.attributes['Willpower'] * 2) / self.defense_modifier) + (0.1 * self.level), 0)
        self.stamina_cost = max(8, round(15 * (1.4 - 0.012 * self.attributes['Endurance'] - 0.0005 * self.level), 0))
        self.mana_cost = max(8, round(30 * (1.4 - 0.012 * self.attributes['Willpower'] - 0.0005 * self.level), 0))
        self.dodge_chance = round(self.attributes['Agility'] / 200 + 0.002 * self.level, 2)
        self.critical_chance = round(self.attributes['Agility'] / 400 + 0.002 * self.level, 2)

    def calculate_stat(self, attribute, level, multiplier = 2):
        """
            Handles the math for calculating starting health, mana, and stamina.
    
            Parameters:
                self (object): Player object
                attribute (str): Attribute being used for the current stat.
                multiplier (int): Multiplier for the math in the stat equation.
            
            Returns:
                (int): The stat being calculated.
        """

        return round(self.attributes[attribute] * (multiplier + level * 0.025) - 1, 0)

    def generate_stat_bar(self, current, maximum, length = 50, bar_color = 'white', bracket_color = 'white'):
        """
            Display stats in a bar.
    
            Parameters:
                self (object): Player object
                current (int): Value of the current stat
                maximum (int): Value of the max stat
                length (int): Length of the stat bar
            
            Returns:
                stat_bar (str): The stat bar
                display (str): Stat in parathesis for actual value viewing
        """

        bar_length = int(length * (current / maximum))
        color_code = f"\033[1;{30 + list(('black', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white')).index(bar_color)}m"
        bracket_color_code = f"\033[1;{30 + list(('black', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white')).index(bracket_color)}m"
        stat_bar = f"{bracket_color_code}[{color_code}{'=' * bar_length}{' ' * (length - bar_length)}{bracket_color_code}]\033[0m"
        display = f"({current}/{maximum})".rjust(10)

        return stat_bar, display

    def generate_exp_bar(self, current, maximum, length = 50, bar_color = 'white', bracket_color = 'white'):
        """
            Display experience in a bar.
    
            Parameters:
                self (object): Player object
                current (int): Value of the current stat
                maximum (int): Value of the max stat
                length (int): Length of the stat bar
            
            Returns:
                exp_bar (str): The experience bar
                display (str): Stat in parathesis for actual value viewing
        """

        bar_length = int(length * (current / maximum))
        color_code = f"\033[1;{30 + list(('black', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white')).index(bar_color)}m"
        bracket_color_code = f"\033[1;{30 + list(('black', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white')).index(bracket_color)}m"
        exp_bar = f"{bracket_color_code}[{color_code}{'=' * bar_length}{' ' * (length - bar_length)}{bracket_color_code}]\033[0m"
        display = f"({current}/{maximum})".rjust(5)

        return exp_bar, display

    def rest(self):
        """
            Recovers a random amount for each stat based on the Speed and Agility attributes
    
            Parameters:
                self (object): Player object
            
            Returns:
                seconds_to_wait (float): How long the player must wait between rests (in seconds)
        """

        seconds_to_wait = 100 / self.attributes['Speed']

        max_recovery = int(((self.attributes['Agility'] + self.attributes['Speed']) / 2) * 0.90)
        min_recovery = int(((self.attributes['Agility'] + self.attributes['Speed']) / 2) * 0.50)

        recovery_health = random.randint(min_recovery, max_recovery)
        recovery_mana = random.randint(min_recovery, max_recovery)
        recovery_stamina = random.randint(min_recovery, max_recovery)

        self.stats['Health'] = min(self.max_stats['Health'], self.stats['Health'] + recovery_health)
        self.stats['Mana'] = min(self.max_stats['Mana'], self.stats['Mana'] + recovery_mana)
        self.stats['Stamina'] = min(self.max_stats['Stamina'], self.stats['Stamina'] + recovery_stamina)

        return seconds_to_wait
    
    def level_up(self):
        """
        Level up the player, gain attribute points, and reset experience.

        Parameters:
            None.

        Returns:
            None.
        """

        def get_attribute_name(choice):
            """
            Get the attribute name based on the numeric choice.

            Parameters:
                choice (int): Numeric choice representing an attribute.

            Returns:
                attribute_name (str): Name of the corresponding attribute.
            """

            attribute_mapping = {
                1: 'Strength',
                2: 'Endurance',
                3: 'Intelligence',
                4: 'Willpower',
                5: 'Agility',
                6: 'Speed'
            }

            return attribute_mapping.get(choice)

        clear_console()

        self.attribute_points += 5

        while self.attribute_points > 0:
            art_stars()
            menu_line()
            print(f" ^ Congratulations, {self.name}! You are now Level {self.level + 1}.")
            menu_line()
            print(f" - Attribute Points Remaining: {self.attribute_points}")
            menu_line()
            print(f" 1. Strength     - {self.attributes['Strength']} (Max Stamina, Physical Damage)")
            print(f" 2. Endurance    - {self.attributes['Endurance']} (Max Health, Physical Defense)")
            print(f" 3. Intelligence - {self.attributes['Intelligence']} (Max Mana, Magical Damage)")
            print(f" 4. Willpower    - {self.attributes['Willpower']} (Spell Casting, Magical Defense)")
            print(f" 5. Agility      - {self.attributes['Agility']} (Dodge Chance, Critical Hit)")
            print(f" 6. Speed        - {self.attributes['Speed']} (Run Away, Faster Resting)")
            menu_line()
            print(" * Enter the number of the attribute to increase (0 to save points): ")
            menu_line()

            choice = console_input()

            if choice == '0':
                break
            elif choice in ['1', '2', '3', '4', '5', '6']:
                attribute_name = get_attribute_name(int(choice))

                if self.attributes[attribute_name] < 100:
                    self.attributes[attribute_name] += 1
                    self.attribute_points -= 1
                    menu_line()
                    print(f" - {attribute_name} increased to {self.attributes[attribute_name]}.")
                    clear_console()
                else:
                    menu_line()
                    print(f" - {attribute_name} is already been maxed out. Please try again.")
                    menu_line()
                    time.sleep(2)
                    clear_console()
            else:
                return

        self.experience = round(self.experience % self.next_experience, 0)
        self.level += 1
        self.next_experience = round(self.next_experience * 1.125, 0)
        self.stats = {
            'Health': self.calculate_stat('Endurance', self.level),
            'Mana': self.calculate_stat('Intelligence', self.level),
            'Stamina': self.calculate_stat('Strength', self.level)
        }
        self.max_stats = {
            'Health': self.stats['Health'], 
            'Mana': self.stats['Mana'], 
            'Stamina': self.stats['Stamina']
        }
        self.physical_attack = round(1.0 + 10.5 * (self.attributes['Strength'] / 100) * (1 + 0.07 * self.level), 0)
        self.magical_attack = round(1.0 + 10.5 * (self.attributes['Intelligence'] / 100) * (1 + 0.07 * self.level), 0)
        self.critical_hit = self.physical_attack + round(2.5 * ((self.attributes['Agility'] * 12) / 100) + 0.08 * self.level, 0)
        self.physical_defense = round(((self.attributes['Endurance'] * 2) / self.defense_modifier) + (0.2 * self.level), 0)
        self.magical_defense = round(((self.attributes['Willpower'] * 2) / self.defense_modifier) + (0.2 * self.level), 0)
        self.stamina_cost = max(8, round(15 * (1.4 - 0.012 * self.attributes['Endurance'] - 0.0005 * self.level), 0))
        self.mana_cost = max(8, round(30 * (1.4 - 0.012 * self.attributes['Willpower'] - 0.0005 * self.level), 0))
        self.dodge_chance = round(self.attributes['Agility'] / 200 + 0.002 * self.level, 2)
        self.critical_chance = round(self.attributes['Agility'] / 400 + 0.002 * self.level, 2)