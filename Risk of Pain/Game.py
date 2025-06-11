from Player import Player
from Settings import *
import pygame
import sys
import random
from Item import Item
from Enemy import Enemy
from Room import Room

class Game:
    """Hlavní třída pro ovládání herní logiky a zobrazení."""
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36) # Standardní font
        self.small_font = pygame.font.Font(None, 24)

        self.game_state = GAME_STATES["EXPLORATION"]
        self.player = Player()
        self.player.current_room_index = 0 # Počáteční úroveň místnosti
        self.current_room = self._generate_random_room(self.player.current_room_index) # Generuje první místnost
        self.combat_turn_message = "" # Zpráva o tahu v boji
        self.combat_active_enemy = None # Nepřítel, se kterým se aktuálně bojuje

        # Zprávy pro zobrazení na obrazovce
        self.system_messages = ["Vítej v žaláři, hrdino! Stiskni SPACE pro pokračování."]

    def _generate_random_room(self, room_level):
        """Generuje náhodnou místnost s nepřáteli na základě úrovně místnosti."""
        room_names = [
            "Prašný Sklep", "Zapomenutá Chodba", "Hmyzí Doupě",
            "Místnost s Pastí", "Vlhký Sál", "Starověká Svatyně",
            "Jeskyně Ozvěn", "Tajemná Komora", "Síně Stínů",
            "Ztracená Knihovna", "Kovárna Zapomnění", "Hrobka Hrdinů",
            "Zamrzlá Jeskyně", "Ohnivá Propast", "Zelený Labyrint",
            "Křišťálová Jeskyně", "Zlatý Sál", "Místnost s Iluzemi",
        ]
        chosen_name = random.choice(room_names)

        enemies_in_room = []
        # Počet nepřátel se zvyšuje s úrovní, max 4 nepřátelé
        num_enemies = random.randint(1, min(4, 1 + room_level // 2))

        enemy_templates = {
            "Goblin": {"health": 30, "attack": 10, "defense": 2, "loot": Item("Malý Lék", "potion_health", 20)},
            "Ork": {"health": 50, "attack": 18, "defense": 5, "loot": Item("Meč", "weapon", 10)},
            "Vlkodlak": {"health": 70, "attack": 25, "defense": 8, "loot": Item("Silný Lék", "potion_health", 40)},
            "Obr": {"health": 100, "attack": 35, "defense": 12, "loot": Item("Velký Meč", "weapon", 15)},
            "Drak": {"health": 150, "attack": 30, "defense": 10, "loot": Item("Dračí Kámen", "artifact", 100)},
            "Král Goblinů": {"health": 80, "attack": 20, "defense": 6, "loot": Item("Koruna Goblinů", "armor", 20)},
            "Striga": {"health": 90, "attack": 22, "defense": 7, "loot": Item("Lektvar Síly", "potion_strength", 30)},
            "Bojový Mág": {"health": 60, "attack": 15, "defense": 4, "loot": Item("Kniha Kouzel", "artifact", 70)},
            "Džin": {"health": 120, "attack": 28, "defense": 9, "loot": Item("Džinova Lampa", "potion_vitality", 50)},

        }

        # Určení typů nepřátel na základě úrovně místnosti
        possible_enemies = []
        if room_level < 3:
            possible_enemies = ["Goblin"]
        elif room_level < 6:
            possible_enemies = ["Goblin", "Ork"]
        elif room_level < 10:
            possible_enemies = ["Goblin", "Ork", "Vlkodlak"]
        else: # Vyšší úrovně
            possible_enemies = ["Goblin", "Ork", "Vlkodlak", "Obr"]
            # Šance na "bosse" na každé 5. úrovni (od úrovně 5)
            if room_level % 5 == 0 and room_level > 0:
                 possible_enemies.append("Drak")

        for _ in range(num_enemies):
            enemy_type_name = random.choice(possible_enemies)
            template = enemy_templates.get(enemy_type_name, enemy_templates["Goblin"]) # Záložní typ

            # Škálování statistik nepřátel s úrovní
            health_scale = 1 + room_level * 0.1
            attack_scale = 1 + room_level * 0.08
            defense_scale = 1 + room_level * 0.05

            scaled_health = int(template["health"] * health_scale)
            scaled_attack = int(template["attack"] * attack_scale)
            scaled_defense = int(template["defense"] * defense_scale)

            # Speciální pravidla pro Draka (boss)
            loot = None
            if enemy_type_name == "Drak":
                scaled_health = int(150 * health_scale * 1.5) # Drak je extra odolný
                scaled_attack = int(30 * attack_scale * 1.5)
                scaled_defense = int(10 * defense_scale * 1.5)
                loot = Item("Dračí Kámen", "artifact", 100 + room_level * 10)
            else:
                loot = template.get("loot") # Použít kořist ze šablony

            enemies_in_room.append(Enemy(enemy_type_name, scaled_health, scaled_attack, scaled_defense, loot))

        return Room(chosen_name, enemies_in_room)


    def _display_message(self, message, color=WHITE, x=10, y=500):
        """Pomocná funkce pro zobrazení zprávy."""
        text_surface = self.small_font.render(message, True, color)
        self.screen.blit(text_surface, (x, y))

    def _handle_events(self):
        """Zpracovává uživatelské vstupy."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if self.game_state == GAME_STATES["EXPLORATION"]:
                    if event.key == pygame.K_SPACE:
                        self._next_room()
                elif self.game_state == GAME_STATES["COMBAT"]:
                    if event.key == pygame.K_a: # Attack
                        self._player_turn_attack()
                    elif event.key == pygame.K_u: # Use Item (použij první lektvar v inventáři)
                        self._player_turn_use_item()
                    elif event.key == pygame.K_ESCAPE: # Flee
                        self._flee_from_combat()
                elif self.game_state in [GAME_STATES["GAME_OVER"], GAME_STATES["WIN"]]:
                    if event.key == pygame.K_r: # Restart
                        self._reset_game()

    def _next_room(self):
        """Generuje další místnost a přesune hráče do ní."""
        self.player.clear_messages()
        # Zkontrolovat, zda v aktuální místnosti nejsou žádní nepřátelé
        if self.current_room.has_enemies_remaining():
            self.system_messages = ["V této místnosti jsou stále nepřátelé! Musíš je porazit."]
            self.game_state = GAME_STATES["COMBAT"] # Zůstat v boji, pokud jsou nepřátelé
            self.combat_active_enemy = self.current_room.get_current_enemy()
            return

        self.player.current_room_index += 1 # Zvýšení úrovně místnosti
        self.current_room = self._generate_random_room(self.player.current_room_index) # Generuje zbrusu novou místnost
        self.system_messages = [f"Vstoupil jsi do: {self.current_room.name} (Úroveň: {self.player.current_room_index})"]
        if self.current_room.has_enemies_remaining():
            self.game_state = GAME_STATES["COMBAT"]
            self.combat_active_enemy = self.current_room.get_current_enemy()
            self.system_messages.append(f"Narazil jsi na: {self.combat_active_enemy.name}!")
        else:
            self.system_messages.append("V této místnosti nejsou žádní nepřátelé. Pokračuj stiskem SPACE.")
        # V nekonečném režimu není stav "vítězství" z vyčerpání místností.


    def _player_turn_attack(self):
        """Logika tahu hráče pro útok."""
        if self.combat_active_enemy and self.combat_active_enemy.health > 0:
            self.player.attack_enemy(self.combat_active_enemy)
            self._check_combat_status()
            if self.game_state == GAME_STATES["COMBAT"]: # Pokud boj pokračuje, je na řadě nepřítel
                self._enemy_turn()
        else:
            self.player.messages.append("Není na koho útočit.")

    def _player_turn_use_item(self):
        """Logika tahu hráče pro použití předmětu."""
        potion_found = False
        for i, item in enumerate(self.player.inventory):
            if item.item_type == 'potion':
                message = item.use(self.player)
                self.player.messages.append(message)
                self.player.inventory.pop(i) # Odebrat použitý předmět
                potion_found = True
                break
        if not potion_found:
            self.player.messages.append("Nemáš žádné lektvary k použití.")

        self._check_combat_status()
        if self.game_state == GAME_STATES["COMBAT"]:
            self._enemy_turn()

    def _flee_from_combat(self):
        """Pokusí se utéct z boje."""
        if random.random() > 0.5: # 50% šance na útěk
            self.player.messages.append("Úspěšně jsi utekl z boje!")
            self.combat_active_enemy = None
            # Při útěku hráč efektivně opustí aktuální místnost.
            # Generujeme novou místnost na předchozí úrovni.
            self.player.current_room_index = max(0, self.player.current_room_index - 1)
            self.current_room = self._generate_random_room(self.player.current_room_index) # Generuje novou místnost pro předchozí úroveň
            self.game_state = GAME_STATES["EXPLORATION"]
            self.system_messages = ["Útěk úspěšný! Vrátil ses do předchozího stavu. Stiskni SPACE pro pokračování."]
        else:
            self.player.messages.append("Nepodařilo se ti utéct!")
            self._enemy_turn() # Pokud útěk selhal, nepřítel stále zaútočí

    def _enemy_turn(self):
        """Logika tahu nepřítele."""
        if self.combat_active_enemy and self.combat_active_enemy.health > 0:
            damage = random.randint(self.combat_active_enemy.attack - 5, self.combat_active_enemy.attack + 5)
            self.player.take_damage(damage)
            self.player.messages.append(f"{self.combat_active_enemy.name} zaútočil na tebe za {damage} poškození.")
            self._check_combat_status()
        else:
            self.player.messages.append("Nepřítel již není schopen boje.")

    def _check_combat_status(self):
        """Zkontroluje stav boje po tahu."""
        if self.player.health <= 0:
            self.game_state = GAME_STATES["GAME_OVER"]
            self.system_messages = ["KONEC HRY! Byl jsi poražen. Stiskni 'R' pro restart."]
            return

        if self.combat_active_enemy and self.combat_active_enemy.health <= 0:
            self.player.messages.append(f"Porazil jsi {self.combat_active_enemy.name}!")
            loot = self.combat_active_enemy.drop_loot()
            if loot:
                self.player.add_item(loot)
            self.combat_active_enemy = self.current_room.get_current_enemy() # Získat dalšího nepřítele
            if not self.combat_active_enemy:
                self.game_state = GAME_STATES["EXPLORATION"]
                self.system_messages = [f"Všichni nepřátelé v {self.current_room.name} poraženi! Stiskni SPACE pro pokračování."]
                self.player.messages.append("Místnost je volná.")
            else:
                self.player.messages.append(f"Připrav se na dalšího nepřítele: {self.combat_active_enemy.name}!")

    def _reset_game(self):
        """Restartuje hru do počátečního stavu."""
        self.player = Player()
        self.player.current_room_index = 0 # Resetování úrovně místnosti
        self.current_room = self._generate_random_room(self.player.current_room_index) # Generuje novou první místnost
        self.game_state = GAME_STATES["EXPLORATION"]
        self.system_messages = ["Hra restartována. Vítej v žaláři! Stiskni SPACE pro pokračování."]
        self.player.clear_messages()
        self.combat_active_enemy = None


    def _draw_ui(self):
        """Kreslí uživatelské rozhraní."""
        self.screen.fill(BLACK)

        # Aktuální místnost a úroveň
        room_text = self.font.render(f"Místnost: {self.current_room.name} (Úroveň: {self.player.current_room_index})", True, WHITE)
        self.screen.blit(room_text, (10, 10))

        # Statistiky hráče
        player_health_text = self.font.render(f"Životy: {self.player.health}/{self.player.max_health}", True, GREEN)
        self.screen.blit(player_health_text, (10, 50))
        player_stats_text = self.font.render(f"Útok: {self.player.attack} | Obrana: {self.player.defense}", True, WHITE)
        self.screen.blit(player_stats_text, (10, 90))

        # Inventář
        inventory_text = self.font.render("Inventář:", True, YELLOW)
        self.screen.blit(inventory_text, (10, 130))
        if not self.player.inventory:
            self.screen.blit(self.small_font.render("Prázdný", True, GREY), (20, 160))
        else:
            y_offset = 160
            for item in self.player.inventory:
                item_str = f"- {item.name} ({item.item_type}, V: {item.value})"
                self.screen.blit(self.small_font.render(item_str, True, WHITE), (20, y_offset))
                y_offset += 25

        # Nepřítel v boji (pokud je v boji)
        if self.game_state == GAME_STATES["COMBAT"] and self.combat_active_enemy:
            enemy_name_text = self.font.render(f"Nepřítel: {self.combat_active_enemy.name}", True, RED)
            self.screen.blit(enemy_name_text, (SCREEN_WIDTH - enemy_name_text.get_width() - 10, 10))
            enemy_health_text = self.font.render(f"Životy: {self.combat_active_enemy.health}", True, RED)
            self.screen.blit(enemy_health_text, (SCREEN_WIDTH - enemy_health_text.get_width() - 10, 50))
            enemy_stats_text = self.font.render(f"Útok: {self.combat_active_enemy.attack} | Obrana: {self.combat_active_enemy.defense}", True, RED)
            self.screen.blit(enemy_stats_text, (SCREEN_WIDTH - enemy_stats_text.get_width() - 10, 90))

        # Zprávy pro hráče (krátkodobé)
        y_offset = SCREEN_HEIGHT - 100
        for msg in reversed(self.player.messages): # Zobrazit nejnovější nahoře
            self._display_message(msg, WHITE, SCREEN_WIDTH//2, y_offset)
            y_offset -= 25

        # Systémové zprávy (delší dobu viditelné instrukce)
        y_offset = SCREEN_HEIGHT - 100
        for msg in self.system_messages:
            self._display_message(msg, YELLOW, 10, y_offset)
            y_offset += 25


        # Instrukce pro boj
        if self.game_state == GAME_STATES["COMBAT"]:
            instructions = [
                "Bojové instrukce:",
                "  A: Útok",
                "  U: Použít předmět (lektvar)",
                "  ESC: Pokusit se utéct"
            ]
            y_offset_combat = SCREEN_HEIGHT // 2 - 50
            for instruction in instructions:
                self._display_message(instruction, WHITE, 10, y_offset_combat)
                y_offset_combat += 25

        # Instrukce pro prozkoumávání
        elif self.game_state == GAME_STATES["EXPLORATION"]:
            self._display_message("Stiskni SPACE pro pokračování do další místnosti.", WHITE, 10, SCREEN_HEIGHT // 2)

        # Instrukce pro konec hry / vítězství
        elif self.game_state in [GAME_STATES["GAME_OVER"], GAME_STATES["WIN"]]:
            self._display_message("Stiskni 'R' pro restart.", WHITE, 10, SCREEN_HEIGHT // 2)

        pygame.display.flip()

    def run(self):
        """Spustí hlavní herní smyčku."""
        running = True
        while running:
            self._handle_events()
            self._draw_ui()
            self.clock.tick(FPS)