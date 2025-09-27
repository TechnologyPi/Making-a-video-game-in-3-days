import random

def get_three_random_upgrades():
    weapons = ["Sound Blaster", "Slim Glooper", "Dual Rifle", "Laser Blade", "Lazer Rifle", "Physics Breaker Rifle", "Dart Shooter", "Rocket Launcher", "Physics Stafe", "Spinning Hammers", "Pearcing Sniper", "Nacho Boomerang"]
    weapons_weights = [0.7, 0.20, 0.07, 0.02, 0.005, 0.003, 0.001, 0.0005, 0.0003, 0.0001, 0.0000011, 0.0000389]
    print(sum(weapons_weights))

    armors = ["Plastic Jacket", "Wooden Armor", "Cooper Armor", "Iron Armor", "Steel Armor", "Titanium Armor", "Diamond Armor", "Mythril Armor", "Adamantium Armor", "Unobtanium Armor", 'Quantum Armor', 'Dark Matter Armor']
    armors_weights = [0.7, 0.20, 0.07, 0.02, 0.005, 0.003, 0.001, 0.0005, 0.0003, 0.0001, 0.00005, 0.00001]

    weapon = random.choices(weapons, weights=weapons_weights, k=1)[0]
    armor = random.choices(armors, weights=armors_weights, k=1)[0]
    health = "Health Boost"
    return weapon, armor, health