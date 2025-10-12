"""main game engine/framework"""
import os
import json
import random
from typing import List, Dict, Any
from rich.console import Console
from rich.prompt import Prompt
from rich_menu import Menu

CARDS: List[Dict[str, Any]] = []
SCROLLS: List[Dict[str, Any]] = []
ENEMIES: List[Dict[str, Any]] = []
SAVE = {}
savepath = ""

with open("cards.json", "r", encoding="utf-8") as cards_json:
    CARDS = json.load(cards_json)
with open("scrolls.json", "r", encoding="utf-8") as scrolls_json:
    SCROLLS = json.load(scrolls_json)
with open("enemies.json", "r", encoding="utf-8") as enemies_json:
    ENEMIES = json.load(enemies_json)

console = Console()

def entry(inputsavepath: str):
    """entry point for the game"""
    global SAVE
    savepath = inputsavepath
    if not os.path.exists(savepath):
        raise FileNotFoundError(f"Save file {savepath} does not exist.")
    with open(savepath, "r", encoding="utf-8") as savefile:
        SAVE = json.load(savefile)
    if SAVE["floor"] == 0:
        def pick_cards():
            # get random cards (up to 5, or all available if fewer)
            sample_size = min(5, len(CARDS))
            options: List[Dict[str, Any]] = random.sample(CARDS, k=sample_size)
            # format options for display
            choice_options = []
            
            def show_cards():
                choice_options.clear()  # Clear the list before rebuilding it
                for opt in options:
                    # start with empty string
                    string = ""
                    # add bold blue name
                    string += f"[bold blue]{opt.get('name')}[/bold blue]\n"
                    # add gray description
                    string += f"[bright black]{opt.get('description')}[/bright black]\n"
                    # add yellow tp cost
                    string += f"[yellow]{str(opt.get('tp'))}TP[/yellow]"
                    # a
                    console.print(string)
                    choice_options.append(opt.get('name'))
            
            # remove one instance of the chosen card from options
            def pick_card_menu():
                # console.clear() is finnicky, so try the more robust:
                result = os.system('cls' if os.name == 'nt' else 'clear')
                if result != 0:
                    # and if that doesn't work, then we'll use it
                    console.clear()
                show_cards()
                choose_card_menu = Menu(
                    *sorted(choice_options),
                    title="^ Choose a starting card ^",
                    color="bold blue"
                )
                chosen_card = choose_card_menu.ask(screen = False, esc = False)
                for i, opt in enumerate(options):
                    if opt.get("name") == chosen_card:
                        SAVE["hand"].append(opt)
                        options.pop(i)
                        choice_options.remove(chosen_card)
                        break
            
            # pick first card
            pick_card_menu()
            # pick second card if possible
            if len(options) > 0:
                pick_card_menu()
        def pick_scrolls():
            # get random cards (up to 5, or all available if fewer)
            sample_size = min(5, len(SCROLLS))
            options: List[Dict[str, Any]] = random.sample(SCROLLS, k=sample_size)
            # format options for display
            choice_options = []
            
            def show_scrolls():
                choice_options.clear()  # Clear the list before rebuilding it
                for opt in options:
                    # start with empty string
                    string = ""
                    # add bold blue name
                    string += f"[bold blue]{opt.get('name')}[/bold blue]\n" # type: ignore
                    # add gray description
                    string += f"[bright black]{opt.get('description')}[/bright black]\n" # type: ignore
                    # add yellow tp cost
                    string += f"[yellow]{str(opt.get('tp'))}TP[/yellow]" # type: ignore
                    # a
                    console.print(string)
                    choice_options.append(opt.get('name'))
            
            # remove one instance of the chosen card from options
            def pick_scroll_menu():
                # console.clear() is finnicky, so try the more robust:
                result = os.system('cls' if os.name == 'nt' else 'clear')
                if result != 0:
                    # and if that doesn't work, then we'll use it
                    console.clear()
                show_scrolls()
                choose_card_menu = Menu(
                    *sorted(choice_options),
                    title="^ Choose a starting scroll ^",
                    color="bold blue"
                )
                chosen_card = choose_card_menu.ask(screen = False, esc = False)
                for i, opt in enumerate(options):
                    if opt.get("name") == chosen_card:
                        SAVE["hand"].append(opt)
                        options.pop(i)
                        choice_options.remove(chosen_card)
                        break
            
            # pick first scroll
            pick_scroll_menu()
            # pick second scroll if possible
            if len(options) > 0:
                pick_scroll_menu()
                # pick third scroll if possible
                if len(options) > 0:
                    pick_scroll_menu()
            
        pick_cards()
        pick_scrolls()
        SAVE["floor"] += 1
        # save the updated game state
        with open(savepath, "w", encoding="utf-8") as savefile:
            json.dump(SAVE, savefile, indent=2)

        print(SAVE)
        descend()

def descend():
    potential_enemies = []
    enemies = []
    for enemy in ENEMIES:
        if enemy.get("from", 0) <= SAVE["floor"]: 
            potential_enemies.append(enemy)
    if not potential_enemies:
        SAVE["floor"] += 1
        return
    enemies.append(random.choice(potential_enemies))
    if random.random() < 0.25:  # 25% chance to add a second enemy
        second_enemy = random.choice(potential_enemies)
        while second_enemy == enemies[0] and len(potential_enemies) > 1:
            second_enemy = random.choice(potential_enemies)
        enemies.append(second_enemy)
        if random.random() < 0.25: # further 25% chance to add a third enemy
            third_enemy = random.choice(potential_enemies)
            while third_enemy in enemies and len(potential_enemies) > len(enemies):
                third_enemy = random.choice(potential_enemies)
            enemies.append(third_enemy)
    console.print(f"You descend to floor {SAVE['floor']}...", style="italic white")
    console.print("You encounter:", style="bold white")
    def build_effects(effects: list):
        finallist = []
        for effect in effects:
            effect_str = " - " + f"[{effect.get('style', 'bold white')}] "  # Changed from 'str' to 'effect_str'
            effect_str += effect.get('type', '???')
            effect_str += " " + str(effect.get('duration')) if effect.get('duration') or effect.get('duration') != 0 else ""
            effect_str += " [/" + effect.get('style', 'bold white') + "]"
            finallist.append(effect_str)
        return ", ".join(finallist)
            
    while True:
        # console.clear() is finnicky, so try the more robust:
        result = os.system('cls' if os.name == 'nt' else 'clear')
        if result != 0:
            # and if that doesn't work, then we'll use it
            console.clear()
        for enemy in enemies:
            if not enemy.get('effects'):
                enemy['effects'] = []
            console.print(f"- [bold red]{enemy.get('name')}[/bold red] ({enemy.get('hp')}{build_effects(enemy.get('effects'))})", style="bold white")
        cards = SAVE.get("hand", [])
        cardopts = []
        for card in cards:
            # start with empty string
            string = ""
            # add bold blue name
            string += f"[bold blue]{card.get('name')}[/bold blue]\n" # type: ignore
            # add gray description
            string += f"[bright black]{card.get('description')}[/bright black]\n" # type: ignore
            # add yellow tp cost
            string += f"[yellow]{str(card.get('tp'))}TP[/yellow]" # type: ignore
            # a
            console.print(string)
            cardopts.append(card.get('name'))
        
        console.print(f"\n[yellow]TP: {SAVE.get('tp', 0)}/{SAVE.get('max_tp', 0)}[/yellow], [green]HP: {SAVE.get('hp', 0)}/{SAVE.get('max_hp', 0)}[/green], EFFECTS: {build_effects(SAVE['effects'])}\n")
        
        card_picker_menu = Menu(
            *sorted(cardopts),
            "End Turn",
            title="What card will you use?",
            color="bold blue",
            highlight_color="bold white"
        )
        
        chosen_card = card_picker_menu.ask(screen = False, esc = False)
        
        enemy_picker_menu = Menu(
            *sorted([enemy.get('name') for enemy in enemies]),
            title="Which enemy will you target?",
            color="bold red",
            highlight_color="bold white"
        )

        chosen_enemy = enemy_picker_menu.ask(screen = False, esc = False)

        # TODO apply card damage and effect, discard card if scroll, decrease TP, when turn end, enemy attack turn, 
        # pick enemy attack, apply damage & effect, etc.