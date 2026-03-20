from ..StuntGP import CARS, TRACKS

# called after the game.json file has been loaded
def after_load_game_file(game_table: dict) -> dict:
    return game_table
# called after the items.json file has been loaded, before any item loading or processing has occurred
# if you need access to the items after processing to add ids, etc., you should use the hooks in World.py
def after_load_item_file(item_table: list) -> list:
    for car in CARS.values():
        item_table.append({
            "name": car["name"],
            "category": ["Car", car["group"]],
            "progression": False if car["group"] == "Team Specials" else True,
        })
    for track in TRACKS.values():
        item_table.append({
            "name": track["name"],
            "category": ["Track"],
            "progression": True,
        })

    item_table.append({
        "name": "Clear",
        "category": ["Goal"],
        "progression": True,
        "useful": True,
        "count": 6,
    })
    return item_table

# NOTE: Progressive items are not currently supported in Manual. Once they are,
#       this hook will provide the ability to meaningfully change those.
def after_load_progressive_item_file(progressive_item_table: list) -> list:
    return progressive_item_table

# called after the locations.json file has been loaded, before any location loading or processing has occurred
# if you need access to the locations after processing to add ids, etc., you should use the hooks in World.py
def after_load_location_file(location_table: list) -> list:
    location_table.append({
        "name": "Goal",
        "category": "Goal",
        "victory": True,
        "requires": "|Clear:1|",
        "region": "Arcade",
    })
    for track in TRACKS.values():
        location_table.append({
            "name": f"{track["name"]} Victory",
            "category": track["name"],
            "region": track["name"],
        })
        location_table.append({
            "name": f"Left Entry to {track["name"]}",
            "category": track["name"],
            "region": track["name"],
        })
        location_table.append({
            "name": f"Right Entry to {track["name"]}",
            "category": track["name"],
            "region": track["name"],
        })
        location_table.append({
            "name": f"{track["name"]} Clear",
            "category": track["name"],
            "region": track["name"],
        })
    return location_table

# called after the locations.json file has been loaded, before any location loading or processing has occurred
# if you need access to the locations after processing to add ids, etc., you should use the hooks in World.py
def after_load_region_file(region_table: dict) -> dict:
    region_table["Arcade"] = {"starting": True}

    for track in TRACKS.values():
        region_table[track["name"]] = {"requires": f"|{track["name"]}|"}
    return region_table

# called after the categories.json file has been loaded
def after_load_category_file(category_table: dict) -> dict:
    category_table["Cars"] = {}
    category_table["Tracks"] = {}

    category_table["Green"] = {}
    category_table["Blue"] = {}
    category_table["Red"] = {}

    category_table["Wild Wheels"] = {}
    category_table["Aero Blasters"] = {}
    category_table["Speed Demons"] = {}
    category_table["Team Specials"] = {}

    for track in TRACKS.values():
        category_table[track["name"]] = {}

    return category_table

# called after the categories.json file has been loaded
def after_load_option_file(option_table: dict) -> dict:
    # option_table["core"] is the dictionary of modification of existing options
    # option_table["user"] is the dictionary of custom options
    return option_table

# called after the meta.json file has been loaded and just before the properties of the apworld are defined. You can use this hook to change what is displayed on the webhost
# for more info check https://github.com/ArchipelagoMW/Archipelago/blob/main/docs/world%20api.md#webworld-class
def after_load_meta_file(meta_table: dict) -> dict:
    return meta_table

# called when an external tool (eg Universal Tracker) ask for slot data to be read
# use this if you want to restore more data
# return True if you want to trigger a regeneration if you changed anything
def hook_interpret_slot_data(world, player: int, slot_data: dict[str, any]) -> dict | bool:
    world.arcade_grid = slot_data["arcade_grid"]
    return slot_data
