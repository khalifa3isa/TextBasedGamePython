import random  
import tkinter as tk  # Importing tkinter for the GUI
from tkinter import (messagebox)  # Importing messagebox from tkinter for pop-up messages used for inventory show

# player data, such as their name, money, health, and points.
player = {
    "name": input("Enter your name: "),
    "money": random.randint(50, 310),
    "health": 100,
    "points": 0,
}
# a function to read the contents of a file.
def read_file(file_name):
    with open(file_name, "r") as f:  # Open the file for reading.
        content = f.read()  # Read the content of the file
    return content  # return the content.


# a function to write content to a file.
def write_file(file_name, content):
    with open(file_name, "w") as f:  # open the file for writing
        f.write(content)  # Write the content to the file


# function to parse or analyze room data from a string 
def Parsing_room_data(RoomData):
    data = {}  # Creating an empty dictionary.
    lines = RoomData.split("\n")  # Split the input string into lines.
    for line in lines:  # Iterates or goes through each line.
        if ":" in line:  # Check if the line contains a colon.
            key, value = line.split(":")  # if yes split the line into key and value.
            data[
                key.strip()
            ] = value.strip()  # Store the key-value pair in the dictionary.
    return data  # Return the dictionary.


# function that to update the room data file with the given data.
def update_room_file(file_name, RoomData):
    content = ""  # Initialize a empty string.
    for (
        key,
        value,
    ) in (
        RoomData.items()
    ): 
        content += f"{key}: {value}\n"  # Add the key value pair to the content string.
    write_file(file_name, content)  # Writes the updated content to the file.


# Function that will to calculate damage and determine if the player can defeat the enemy.
def calculate_damage(WeaponDamage, EnemyDamage, ArmourDurability):
    EnemyDamage = (
        EnemyDamage / ArmourDurability if ArmourDurability else EnemyDamage
    )  # Calculate the enemy damage based on the players armor durability.
    return (WeaponDamage >= EnemyDamage)  # Return True if the players weapon damage is enough to defeat the enemy using less then qual sign


# Function that will clear specific lines from the room data file.
def clear_RoomData(room_file):
    with open(room_file, "r") as file:  
        lines = file.readlines()  # Read all lines in the file.

    with open(room_file, "w") as file:  # Open the room data file for writing.
        for line in lines:  # Iterate through each line.
            if (
                "Weapon description:" not in line
                and "Money description:" not in line
                and "Treasure description:" not in line
                and "HealingPad description:" not in line
            ):  # Checks if the line doesn't contain specific keywords.
                file.write(line)  # Writes the line to the file.


# Function to update a specific key-value pair in the room data file.
def update_RoomData(room_file, key, value):
    with open(room_file, "r") as file: 
        lines = file.readlines()  

    updated = (
        False  # Initializing a flag to track if the key value pair was updated
    )
    with open(room_file, "w") as file: 
        for line in lines: 
            if key in line:  # Check if the line contains the specified key.
                file.write(
                    f"{key}: {value}\n"
                )  # Write the updated key and value to the file.
                updated = True  # Set the updated flag to True.
            else:
                file.write(line)  # Write the original line to the file.

        if not updated:  # Check if the key and value was not updated.
            file.write(
                f"{key}: {value}\n"
            )  # Add the new key value pair to the file.
# Function to handle the process of entering a room.
def enter_room(room_file):
    RoomData = read_file(room_file)  # Read the room data from the file.
    parsed_data = Parsing_room_data(
        RoomData
    )  # Parse the room data into a dictionary.

    RoomName = parsed_data[
        "City Name"
    ]  # Get the City Name from the parsed data

    try:  # Try to extract the enemy information.
        EnemyName, EnemyDamage, EnemyHealth = parsed_data[
            "Enemy description"
        ].split(",")  # Split the enemy information by comma.
        EnemyDamage, EnemyHealth = int(EnemyDamage), int(
            EnemyHealth
        )  # Convert enemy damage and health to integers for the calculations health and demage
    except ValueError:  # If there is an error in the enemy description then print invalid
        print(
            "Enemy description in the room file is invalid."
        )  
        return 
    
    # Extract enemy information after error checking.
    EnemyName, EnemyDamage, EnemyHealth = parsed_data[
        "Enemy description"
    ].split(
        ","
    )  
    EnemyDamage, EnemyHealth = int(EnemyDamage), int(
        EnemyHealth
    )  

    points = int(
        parsed_data["Point description"]
    )  # convert the point description to an integer

    # extract weapon information from the parsed data.
    weapon_name, WeaponDamage, weapon_price = parsed_data[
        "Weapon description"
    ].split(
        ","
    )  
    WeaponDamage, weapon_price = int(WeaponDamage), int(
        weapon_price
    )  

    room_money = int(
        parsed_data["Money description"]
    )  

    # Initialize treasure variables.
    treasure_code, treasure_points = None, None
    # check if there is a treasure description in the parsed data.
    if "Treasure description" in parsed_data:
        # Extract and convert treasure code and points from the treasure description
        treasure_code, treasure_points = map(
            int, parsed_data["Treasure description"].split(",")
        )
    HealingPad = None  # Initialize HealingPad variable
    # Check if there is a HealingPad description in the parsed data then extract and convert the HealingPad description to an integer
    if "HealingPad description" in parsed_data:
        HealingPad = int(
            parsed_data["HealingPad description"]
        )  

    print(
        f"Entering {RoomName}"
    )  # Print the room name the player is going entering then the roomname whichever room it will be.
   
    print(f"Enemy: {EnemyName}, Damage {EnemyDamage}, Health {EnemyHealth}") # Print enem information name damage and health

   
    weapon_choice = input("Choose a weapon from your inventory: ").lower() # Ask the player to choose a weapon from their inventory and .lower to change case sensitivity 

    # Check if the chosen weapon is in the player inventory
    if weapon_choice not in player_inventory["weapons"]:
        # If the weapon is not in the inventory then print a message and leave the room.
        print("You don't have this weapon. Sorry leaving the room.")
        return

    # Ask the player if he wants to use armour or no
    use_armour = input("Do you want to use armour? (yes/no): ").lower()
    ArmourDurability = 1  # Initializing ArmourDurability variable

    # If yes
    if use_armour == "yes":
        # then check if the player has armour in their inventory.
        if player_inventory["armour"]:
            ArmourDurability = player_inventory["armour"][
                0
            ]  # Get the first armour durability value
        else:
            # If the player doesnt have any armour print a message and continue without armour.
            print(
                "unfortunately you don't have any armour. Continuing without armour."
            )

    # Get the player's damage value from the chosen weapon.
    player_damage = player_inventory["weapons"][weapon_choice][0]
    # Calculate the adjusted enemy damage based on the players armour durability.
    adjusted_EnemyDamage = EnemyDamage // ArmourDurability
    # Check if the players damage is greater than or equal to the enemy health
    if player_damage >= EnemyHealth:
        print("You defeated the enemy!")  # Print a message that you won.
        player[
            "points"
        ] += points  # Add the points from the room to the player points.
        player[
            "money"
        ] += room_money  # Add the room money to the players money.
        # Add the weapon from the room to the player inventory
        player_inventory["weapons"][weapon_name] = (
            WeaponDamage,
            weapon_price,
        )

        # Check if there is a treasure and if the player has the corresponding key.
        if (
            treasure_code is not None
            and treasure_code in player_inventory["keys"]
        ):
            player[
                "points"
            ] += treasure_points  # Add the treasure points to the player's points.
            # Print a message about the treasure points gained.
            print(
                f"You opened the treasure and gained {treasure_points} points!"
            )

        # Check if there is a HealingPad in the room.
        if HealingPad is not None:
            player["health"] += (
                50 * HealingPad
            )  # Increase the players health based on the HealingPad value.
            # Print a message about the health gained from the HealingPad.
            print(
                f"Congrats you found a {HealingPad} HealingPad and gained {50 * HealingPad} health!"
            )

        
        clear_RoomData(
            room_file
        )  # Call the clear_RoomData function to remove the room data.
        # If the player damage is less than the enemy health.
    else:
        print(
            "Ops you lost the battle try harder next time."
        )  # Print youre defeated 
        EnemyHealth -= player_damage  # Decrease the enemys health by the players damage.
        player["health"] = 0  # Set the players health to 0.
        player["points"] -= 2  # Deduct 2 points from the player points.

        # Update enemy health in the room file.
        update_RoomData(
            room_file,
            "Enemy description",
            f"{EnemyName},{EnemyDamage},{EnemyHealth}",
        )

    # Remove used weapon and armour from inventory.
    del player_inventory["weapons"][
        weapon_choice
    ]  # Delete the used weapon from the player's inventory.
    # If the player used armour and has armour in the inventory then remove it.
    if use_armour == "yes" and player_inventory["armour"]:
        player_inventory["armour"] = None

    update_gui()  # Update the graphical user interface or GUI to changes.
