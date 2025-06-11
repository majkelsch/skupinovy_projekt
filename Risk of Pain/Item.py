class Item:
    """Reprezentuje kořist, kterou hráč může získat."""
    def __init__(self, name, item_type, value):
        self.name = name
        self.item_type = item_type  # např. 'potion', 'weapon', 'armor'
        self.value = value          # např. heal amount, attack bonus, defense bonus

    def use(self, target_player):
        """Použije předmět na cílového hráče."""
        if self.item_type == 'potion_health':
            healed_amount = self.value
            target_player.health = min(target_player.max_health, target_player.health + healed_amount)
            return f"Použil jsi {self.name} a vyléčil se o {healed_amount} životů."
        elif self.item_type == 'potion_vitality':
            target_player.max_health += self.value
            target_player.health = min(target_player.max_health, target_player.health)
            return f"Použil jsi {self.name} a zvýšil jsi své maximální zdraví o {self.value}."
        elif self.item_type == 'potion_strength':
            target_player.attack += self.value
            return f"Použil jsi {self.name} a zvýšil jsi svůj útok o {self.value}."
        elif self.item_type == 'weapon':
            target_player.attack += self.value
            return f"Použil jsi {self.name} a zvýšil jsi svůj útok o {self.value}."
        elif self.item_type == 'armor':
            target_player.defense += self.value
            return f"Použil jsi {self.name} a zvýšil jsi svou obranu o {self.value}."


        return f"Předmět {self.name} nelze použít."