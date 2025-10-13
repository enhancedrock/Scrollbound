"""main game engine/framework"""
import os
import json
import random
import copy
from typing import List, Dict, Any
from rich.console import Console
from rich.prompt import Prompt
from rich_menu import Menu

CARDS: List[Dict[str, Any]] = []
SCROLLS: List[Dict[str, Any]] = []
ENEMIES: List[Dict[str, Any]] = []
SAVE = {}

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
                    string += f"[bold blue]{opt.get('name')}[/bold blue]\n"
                    # add gray description
                    string += f"[bright black]{opt.get('description')}[/bright black]\n"
                    # add yellow tp cost
                    string += f"[yellow]{str(opt.get('tp'))}TP[/yellow]"
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

    descend()

def build_enemies() -> List[Dict[str, Any]]:
    """Generate enemies for the current floor"""
    potential_enemies = []
    enemies = []
    for enemy in ENEMIES:
        if enemy.get("from", 0) <= SAVE["floor"]: 
            potential_enemies.append(enemy)
    if not potential_enemies:
        SAVE["floor"] += 1
        return build_enemies()

    # add first anemone
    first_enemy = random.choice(potential_enemies)
    enemies.append(copy.deepcopy(first_enemy))

    # 25% chance to add another anemone
    if random.random() < 0.25:
        second_enemy = random.choice(potential_enemies)
        while second_enemy == first_enemy and len(potential_enemies) > 1:
            second_enemy = random.choice(potential_enemies)
        enemies.append(copy.deepcopy(second_enemy))

        # further 25% chance to add a third anemone
        if random.random() < 0.25:
            third_enemy = random.choice(potential_enemies)
            while (third_enemy in (first_enemy, second_enemy)) and len(potential_enemies) > 2:
                third_enemy = random.choice(potential_enemies)
            enemies.append(copy.deepcopy(third_enemy))

    # wait that's not how you spell enemy
    # don't code at 1AM :tongue:
    #
    # also why does VSCode complain about trailing whitespaces if it's
    # the one putting them there
    #
    # https://www.youtube.com/watch?v=RSUEno09yHs

    return enemies

def build_effects(effects):
    """Format effects list for display"""
    finallist = []
    for effect in effects:
        effect_str = " - " + f"[{effect.get('style', 'bold white')}] "
        effect_str += effect.get('type', '???')
        effect_str += " " + str(effect.get('duration')) if effect.get('duration') or effect.get('duration') != 0 else ""
        effect_str += " [/" + effect.get('style', 'bold white') + "]"
        finallist.append(effect_str)
    return "".join(finallist)

def descend():
    """Main game loop - handles floor progression and combat"""
    while True:
        # build enemies for the floor
        enemies = build_enemies()

        # main combat loop
        while True:
            # cum on the screen rq (coinpon reference)
            result = os.system('cls' if os.name == 'nt' else 'clear')
            if result != 0:
                console.clear()

            # print enemies
            for enemy in enemies:
                if not enemy.get('effects'):
                    enemy['effects'] = []
                console.print(f"- [bold red]{enemy.get('name')}[/bold red] ({enemy.get('hp')}{build_effects(enemy.get('effects'))})", style="bold white")

            # print cards
            cards = SAVE.get("hand", [])
            for card in cards:
                string = ""
                string += f"[bold blue]{card.get('name')}[/bold blue]\n"
                string += f"[bright black]{card.get('description')}[/bright black]\n"
                string += f"[yellow]{str(card.get('tp'))}TP[/yellow]"
                console.print(string)

            # print player stats
            console.print(f"\n[blue]FLOOR: {SAVE.get('floor')}[/blue], [yellow]TP: {SAVE.get('tp', 0)}/{SAVE.get('max_tp', 0)}[/yellow], [green]HP: {SAVE.get('hp', 0)}/{SAVE.get('max_hp', 0)}[/green], EFFECTS: {build_effects(SAVE['effects'])}\n")

            # pick whatchu wanna do ho
            card_picker_menu = Menu(
                *sorted(str(i + 1) for i in range(len(SAVE.get("hand", [])))),
                "End Turn",
                title="What card will you use?",
                color="bold blue",
                highlight_color="bold white"
            )

            chosen_card = card_picker_menu.ask(screen=False, esc=False)

            # regen TP on end of turn
            if chosen_card == "End Turn":
                console.print("You end your turn.", style="bold white")
                SAVE["tp"] = SAVE.get("max_tp", 2)
                continue

            # get chosen card
            chosen_card = SAVE.get("hand", [])[int(chosen_card)-1]

            # check if player has enough TP
            if chosen_card.get("tp", 0) > SAVE.get("tp", 0):
                console.print("You do not have enough TP to play that card.", style="bold red")
                Prompt.ask("Press Enter to continue...")
                continue

            # card go brrrrrr
            SAVE["tp"] -= chosen_card.get("tp", 0)
            targets_remaining = chosen_card.get("targets", 1)

            # pick targets
            while targets_remaining > 0 and len(enemies) > 0:
                enemy_picker_menu = Menu(
                    *sorted(str(i + 1) for i in range(len(enemies))),
                    title=f"Which enemy will you target? ({targets_remaining}/{chosen_card.get('targets', 1)})",
                    color="bold red",
                    highlight_color="bold white"
                )
                chosen_enemy = enemies[int(enemy_picker_menu.ask(screen=False, esc=False))-1]

                # apply damage
                chosen_enemy['hp'] -= chosen_card.get("damage", 0)

                # and effects
                if len(chosen_card.get("effects", [])) > 0:
                    if not chosen_enemy.get('effects'):
                        chosen_enemy['effects'] = []
                    for effect in chosen_card.get("effects", []):
                        if effect not in chosen_enemy['effects']:
                            chosen_enemy['effects'].append(effect)

                targets_remaining -= 1

                # kablamo
                if chosen_enemy['hp'] <= 0:
                    enemies.remove(chosen_enemy)
                    SAVE["gold"] += chosen_enemy.get("gold", 0)

            # aw man that was a scroll
            if chosen_card.get("scroll", False):
                SAVE["hand"].remove(chosen_card)

            # mega kablamo?
            if len(enemies) == 0:
                console.print("You have defeated all enemies on this floor!", style="bold green")
                SAVE["floor"] += 1
                SAVE["tp"] = SAVE.get("max_tp", 2)
                Prompt.ask("Press Enter to continue...")
                break  # mega kablamo.

# TODO handle end of turn effects, enemy attacks, scroll shop, voucher shop, etc.