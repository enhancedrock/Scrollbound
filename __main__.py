"""game launcher"""
import os
import sys
import json
from rich.console import Console
from rich.prompt import Prompt
from rich_menu import Menu
import game
import copy

NOSAVETODISK = False

console = Console()

TEMPLATESAVE = {
    "hp": 30,
    "max_hp": 30,
    "tp": 2,
    "max_tp": 2,
    "gold": 0,
    "effects": [],
    "floor": 0,
    "biome": "cave",
    "hand": [],
    "stockpile": []
}

if NOSAVETODISK:
    console.print("!! Saving to disk has been disabled in this enviornment !!", style="bold red",
                  justify="center")
    mainMenu = Menu(
        "New Run",
        "Exit",
        title="S C R O L L B O U N D",
        color="bold blue",
        highlight_color="bold white",
    )
else:
    mainMenu = Menu(
        "New Run",
        "Continue Run", 
        "Exit",
        title="S C R O L L B O U N D",
        color="bold blue",
        highlight_color="bold white",
    )

# Get the selection
while True:
    # console.clear() is finnicky, so try the more robust:
    result = os.system('cls' if os.name == 'nt' else 'clear')
    if result != 0:
        # and if that doesn't work, then we'll use it
        console.clear()

    selection = mainMenu.ask(screen = False, esc = False)
    # Handle the selection
    match selection:
        case "New Run":
            BASE = "new-run"
            NEWRUN = BASE
            if os.path.exists("runs"):
                i = 0
                while os.path.exists(os.path.join("runs", f"{NEWRUN}.sbr")):
                    i += 1
                    NEWRUN = f"{BASE}-{i}"
            save_name = Prompt.ask("Enter a name for your run (a-z, A-Z, -, _, 0-9)",
                                   default=NEWRUN)
            if not save_name or any(c not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_" for c in save_name):
                console.print("Invalid save name!", style="bold red")
                continue
            if not os.path.exists("runs"):
                os.makedirs("runs")
            if os.path.exists(os.path.join("runs", f"{save_name}.sbr")):
                overwrite = Prompt.ask(f"A save named '{save_name}' already exists. Overwrite? (y/n)",
                                       choices=["y", "n"], default="n")
                if overwrite == "n":
                    continue
            save_path = os.path.join("runs", f"{save_name}.sbr")
            try:
                save_data = copy.deepcopy(TEMPLATESAVE)
                save_data["name"] = save_name
                with open(save_path, "w", encoding="utf-8") as f:
                    json.dump(save_data, f, ensure_ascii=False, indent=2)
            except OSError as e:
                console.print(f"Failed to create save file: {e}", style="bold red")
                continue
            console.print("Starting new run...", style="italic white")
            game.entry(os.path.join("runs", f"{save_name}.sbr"))
        case "Continue Run":
            SAVEDIREXISTS = os.path.exists("runs")
            if not SAVEDIREXISTS or len([i for i in os.listdir("runs") if i.endswith(".sbr")]) == 0:
                console.print("No saved runs found!", style="bold red")
            else:
                loadSaveMenu = Menu(
                    *sorted(
                        os.path.splitext(i)[0]
                        for i in os.listdir("runs")
                        if i.endswith(".sbr") and os.path.splitext(i)[0]
                    ),
                    "Back",
                    title="Select a run to continue",
                    color="bold blue",
                    highlight_color="bold white",
                )
                selection = loadSaveMenu.ask(screen = False, esc = False)

                if selection == "Back":
                    continue

                console.print("Starting...", style="italic white")
                game.entry(os.path.join("runs", f"{selection}.sbr"))
        case "Exit":
            console.print("Goodbye!", style="italic cyan")
            sys.exit()
