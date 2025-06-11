class Enemy:
    """Reprezentuje nepřítele ve hře."""
    def __init__(self, name, health, attack, defense, loot_item=None):
        self.name = name
        self.max_health = health
        self.health = self.max_health
        self.attack = attack
        self.defense = defense
        self.loot_item = loot_item  # Objekt Item, který nepřítel upustí
        self.image_path = f"assets/enemies/{name.lower().replace(' ', '_')}.png"

    def take_damage(self, damage, level):
        """Nepřítel utrpí poškození."""
        actual_damage = max(0, damage - int(damage*self.defense//100//(level+1)))
        self.health -= actual_damage
        if self.health <= 0:
            self.health = 0
        return actual_damage

    def drop_loot(self):
        """Vrátí předmět, který nepřítel upustí, pokud existuje."""
        if self.loot_item:
            return self.loot_item
        return None