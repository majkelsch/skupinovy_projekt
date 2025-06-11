import random

class Player:
    """Reprezentuje hráče ve hře."""
    def __init__(self, name="Hrdina", max_health=100, attack=15, defense=5):
        self.name = name
        self.max_health = max_health
        self.health = max_health
        self.attack = attack
        self.defense = defense
        self.inventory = []  # Seznam objektů Item
        self.current_room_index = 0 # Používá se jako indikátor úrovně/progrese
        self.messages = []   # Zprávy pro hráče (např. "Získal jsi loot!")

    def take_damage(self, damage):
        """Hráč utrpí poškození."""
        actual_damage = max(0, damage - self.defense)
        self.health -= actual_damage
        self.messages.append(f"Utrpěl jsi {actual_damage} poškození.")
        if self.health <= 0:
            self.health = 0
            self.messages.append("Byl jsi poražen!")
        return actual_damage

    def attack_enemy(self, enemy):
        """Hráč útočí na nepřítele."""
        damage = random.randint(self.attack - 5, self.attack + 5)
        enemy.take_damage(damage)
        self.messages.append(f"Zaútočil jsi na {enemy.name} za {damage} poškození.")

    def add_item(self, item):
        """Přidá předmět do inventáře hráče."""
        self.inventory.append(item)
        self.messages.append(f"Získal jsi: {item.name}")

    def clear_messages(self):
        """Vymaže zprávy hráče."""
        self.messages = []