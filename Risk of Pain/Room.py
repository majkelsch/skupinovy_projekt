class Room:
    """Reprezentuje jednu místnost v herním světě."""
    def __init__(self, name, enemies=None):
        self.name = name
        self.enemies = enemies if enemies is not None else []

    def has_enemies_remaining(self):
        """Zkontroluje, zda v místnosti zbývají nějací živí nepřátelé."""
        return any(enemy.health > 0 for enemy in self.enemies)

    def get_current_enemy(self):
        """Vrátí prvního živého nepřítele v místnosti."""
        for enemy in self.enemies:
            if enemy.health > 0:
                return enemy
        return None