# Stunt GP

Stunt GP is a radio-controlled car racing video game developed by the UK-based studio Team17, released in 2001.

## How to Play
This Manual APWorld focuses on Stunt GP's Arcade mode. The main feature is randomizing the grid of Arcade mode tracks. Furthermore, Arcade in the vanilla game is completely Sphere 0, so these additional restrictions are in place:
* You must receive cars as multiworld items to start an Arcade run with them
* You must receive tracks as multiworld items to select the route to them

You start with one random car and all three starter tracks (meaning you can first only enter the track of the starter car's class).

## Goal
The goal is to clear Arcade runs ending at different tracks. At each final round track, there is a location that awards the item *Clear* on victory. There is a YAML option that determines how many track clears you need to goal (1 to 6).

## Items
You can receive tracks, which allow you to enter the respective track in Arcade. You can receive cars, which allow you to start Arcade with that car. There are items called *Clear*, which are only for bookkeeping your progress towards the goal.

## Locations
Victory at each track is a location. Each connection between tracks ("Left Entry to ..." or "Right Entry to ...") is a location. You check connection locations as done while in the *Select Route* screen; You check "Left Entry to X" if you're selecting X for the next round and X is the *left* option, and "Right Entry to X" respectively if it is the *right* option.

## Setup
1. Back up your save data (if you don't want playing AP to meddle with it)
1. Add the install location of Stunt GP to `host.yaml` as follows:
    ```yaml
    manual_stuntgp_copyrite_options:
      sgp_path: "C:/Team17/SGP"
    ```
1. (Optional) Back up your `wads/setup.wad`. However, the next step should do it for you automatically.
1. Connect to your slot with the Manual client. In the process, the client will try to locate your `wads/setup.wad` based on the `host.yaml` option. It will take a backup for it (as `wads/setup.wad.bak`) and patch `setup.wad` to contain the configuration of the Arcade grid that the generation rolled.
1. Use the **SGP NOW** cheat: Enter Time Trial, enter **SGP** as your name, return to name entry, enter **NOW** as your name. You now have all cars unlocked.
