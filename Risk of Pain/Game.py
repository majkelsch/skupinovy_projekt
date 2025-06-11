from Player import Player
from Settings import *
import pygame
import sys
import random
from Item import Item
from Enemy import Enemy
from Room import Room
import UI
import time

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

        self.inventory_buttons = []  # Přidat tento řádek






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

        # Enemy templates: each enemy type has a list of possible variants (dicts)
        enemy_templates = {
            # Goblin
            "Goblin": [
            {"health": random.randint(10,30), "attack": random.randint(2,10), "defense": random.randint(2,10), "loot": Item("Malý Lék", "potion_health", random.randint(15,30))},
            {"health": random.randint(10,30), "attack": random.randint(2,10), "defense": random.randint(2,10), "loot": Item("Velký Lék", "potion_health", random.randint(40,60))},
            {"health": random.randint(10,30), "attack": random.randint(2,10), "defense": random.randint(2,10), "loot": Item("Vitalita", "potion_vitality", random.randint(10,30))},
            {"health": random.randint(10,30), "attack": random.randint(2,10), "defense": random.randint(2,10), "loot": Item("Špatná Helma", "armor", random.randint(5,10))}
            ],
            # Ork
            "Ork": [
            {"health": random.randint(30,40), "attack": random.randint(10,25), "defense": random.randint(2,10), "loot": Item("Malý Lék", "potion_health", random.randint(15,30))},
            {"health": random.randint(30,40), "attack": random.randint(10,25), "defense": random.randint(2,10), "loot": Item("Velký Lék", "potion_health", random.randint(40,60))},
            {"health": random.randint(30,40), "attack": random.randint(10,25), "defense": random.randint(2,10), "loot": Item("Vitalita", "potion_vitality", random.randint(10,30))},
            {"health": random.randint(30,40), "attack": random.randint(10,25), "defense": random.randint(2,10), "loot": Item("Prošívanice", "armor", random.randint(15,20))},
            {"health": random.randint(30,40), "attack": random.randint(10,25), "defense": random.randint(2,10), "loot": Item("Dobrý Brousek", "weapon", random.randint(10,20))}
            ],
            # Vlkodlak
            "Vlkodlak": [
            {"health": random.randint(40,60), "attack": random.randint(15,30), "defense": random.randint(2,15), "loot": Item("Léčivé Bylinky", "potion_health", random.randint(20,40))},
            {"health": random.randint(40,60), "attack": random.randint(15,30), "defense": random.randint(2,15), "loot": Item("Krystal Života", "potion_health", random.randint(40,60))},
            {"health": random.randint(40,60), "attack": random.randint(15,30), "defense": random.randint(2,15), "loot": Item("Vitalita", "potion_vitality", random.randint(10,30))},
            {"health": random.randint(40,60), "attack": random.randint(15,30), "defense": random.randint(2,15), "loot": Item("Vlčí Kůže", "armor", random.randint(20,30))},
            {"health": random.randint(40,60), "attack": random.randint(15,30), "defense": random.randint(2,15), "loot": Item("Vlčí Drápy", "weapon", random.randint(15,25))},
            {"health": random.randint(40,60), "attack": random.randint(15,30), "defense": random.randint(2,15), "loot": Item("Vlčí Ohon", "artifact", random.randint(5,10))}
            ],
            # Obr
            "Obr": [
            {"health": random.randint(50,100), "attack": random.randint(15,35), "defense": random.randint(2,10), "loot": Item("Pradávný Lék", "potion_health", random.randint(40,80))},
            {"health": random.randint(50,100), "attack": random.randint(15,35), "defense": random.randint(2,10), "loot": Item("Obří Železo", "weapon", random.randint(20,30))},
            {"health": random.randint(50,100), "attack": random.randint(15,35), "defense": random.randint(2,10), "loot": Item("Pochybná Zbroj", "armor", random.randint(10,15))}
            ],
            # Drak (boss, only one variant)
            "Drak": [
            {"health": random.randint(100,250), "attack": random.randint(25,70), "defense": random.randint(50,70), "loot": Item("Dračí Kámen", "artifact", random.randint(30,50))}
            ],
            # Král Goblinů
            "Král Goblinů": [
            {"health": random.randint(50,80), "attack": random.randint(15,30), "defense": random.randint(10,25), "loot": Item("Koruna Goblinů", "armor", random.randint(20,40))},
            {"health": random.randint(50,80), "attack": random.randint(15,30), "defense": random.randint(10,25), "loot": Item("Goblinská Ocel", "weapon", random.randint(20,40))}
            ],
            # Striga
            "Striga": [
            {"health": random.randint(20,40), "attack": random.randint(10,25), "defense": random.randint(10,20), "loot": Item("Lektvar Síly", "potion_strength", random.randint(20,40))},
            {"health": random.randint(20,40), "attack": random.randint(10,25), "defense": random.randint(10,20), "loot": Item("Strigina Kůže", "armor", random.randint(15,30))}
            ],
            # Bojový Mág
            "Bojový Mág": [
            {"health": random.randint(50,80), "attack": random.randint(15,30), "defense": random.randint(5,10), "loot": Item("Kniha Kouzel", "artifact", random.randint(10,20))},
            {"health": random.randint(50,80), "attack": random.randint(15,30), "defense": random.randint(5,10), "loot": Item("Lektvar Magie", "potion_vitality", random.randint(20,40))}
            ],
            # Džin
            "Džin": [
            {"health": random.randint(80,150), "attack": random.randint(20,40), "defense": random.randint(40,80), "loot": Item("Džinova Lampa", "potion_vitality", random.randint(70,100))}
            ]
        }

        # Určení typů nepřátel na základě úrovně místnosti
        possible_enemies = []
        if room_level < 10:
            possible_enemies = ["Goblin", "Striga"]
        elif room_level < 20:
            possible_enemies = ["Goblin", "Ork", "Vlkodlak", "Bojový Mág"]
        elif room_level < 30:
            possible_enemies = ["Goblin", "Ork", "Vlkodlak", "Obr", "Král Goblinů", "Striga"]
        else: # Vyšší úrovně
            possible_enemies = ["Goblin", "Ork", "Vlkodlak", "Obr", "Král Goblinů", "Striga", "Bojový Mág", "Džin"]
            # Šance na "bosse" na každé 5. úrovni (od úrovně 30)
            if room_level % 5 == 0 and room_level > 0:
                possible_enemies.append("Drak")

        for _ in range(num_enemies):
            enemy_type_name = random.choice(possible_enemies)
            template_list = enemy_templates.get(enemy_type_name, enemy_templates["Goblin"]) # Záložní typ
            template = random.choice(template_list)  # Vyber náhodnou variantu nepřítele

            # Škálování statistik nepřátel s úrovní
            health_scale = 1 + room_level * 0.1
            attack_scale = 1 + room_level * 0.08
            defense_scale = 1 + room_level * 0.05

            scaled_health = int(template["health"] * health_scale) + random.randint(-3, 5)
            scaled_attack = int(template["attack"] * attack_scale) + random.randint(-2, 3)
            scaled_defense = int(template["defense"] * defense_scale) + random.randint(-1, 2)

            # Speciální pravidla pro Draka (boss)
            loot = None
            if enemy_type_name == "Drak":
                scaled_health = int(150 * health_scale * 1.5) # Drak je extra odolný
                scaled_attack = int(30 * attack_scale * 1.5)
                scaled_defense = int(10 * defense_scale * 1.5)
                loot = Item("Dračí Kámen", "artifact", 100 + room_level * 10)
            else:
                loot = template["loot"] # Použít kořist ze šablony

            enemies_in_room.append(Enemy(enemy_type_name, scaled_health, scaled_attack, scaled_defense, loot))

        return Room(chosen_name, enemies_in_room)






    def _display_message(self, message, color=WHITE, x=SCREEN_WIDTH//2, y=SCREEN_HEIGHT//2, align="center"):
        """Pomocná funkce pro zobrazení zprávy."""
        text_surface = UI.Label(
            pos=(x, y),
            text=message,
            font=self.small_font,
            color=color,
            align=align
        )
        text_surface.draw(self.screen)







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
                    elif event.key == pygame.K_ESCAPE: # Flee
                        self._flee_from_combat()
                    
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos
                for btn, item in self.inventory_buttons:
                    if btn.rect.collidepoint(mouse_pos):
                        message = item.use(self.player)
                        self.player.messages.append(message)
                        # Pokud chcete item po použití odstranit:
                        if hasattr(item, "item_type") and (item.item_type.startswith("potion") or item.item_type.startswith("weapon") or item.item_type.startswith("armor")):
                            self.player.inventory.remove(item)
                        break

            






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
            if self.combat_active_enemy is not None:
                self.system_messages.append(f"Narazil jsi na: {self.combat_active_enemy.name}!")
            else:
                self.system_messages.append("V této místnosti nejsou žádní nepřátelé. Pokračuj stiskem SPACE.")
        else:
            self.system_messages.append("V této místnosti nejsou žádní nepřátelé. Pokračuj stiskem SPACE.")
        # V nekonečném režimu není stav "vítězství" z vyčerpání místností.







    def _player_turn_attack(self):
        """Logika tahu hráče pro útok."""
        if self.combat_active_enemy and self.combat_active_enemy.health > 0:
            self.player.attack_enemy(self.combat_active_enemy, self.player.current_room_index)
            self._check_combat_status()
            if self.game_state == GAME_STATES["COMBAT"]: # Pokud boj pokračuje, je na řadě nepřítel
                self._enemy_turn()
        else:
            self.player.messages.append("Není na koho útočit.")







    def _player_turn_use_item(self):
        """Logika tahu hráče pro použití předmětu."""
        potion_found = False
        for i, item in enumerate(self.player.inventory):
            if item.item_type == 'potion_health':
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
            self.player.take_damage(damage, self.player.current_room_index) # Poškození závislé na úrovni místnosti
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
                self.player.add_pain_coins(random.randint(1, 10)) # Přidat náhodné Pain Coins za loot
            self.combat_active_enemy = self.current_room.get_current_enemy() # Získat dalšího nepřítele
            if not self.combat_active_enemy:
                self.game_state = GAME_STATES["EXPLORATION"]
                self.system_messages = [f"Všichni nepřátelé v {self.current_room.name} poraženi! Stiskni SPACE pro pokračování."]
                self.player.messages.append("Místnost je volná.")
            else:
                self.player.messages.append(f"Připrav se na dalšího nepřítele: {self.combat_active_enemy.name}!")









    def _rebirth(self):
        """Hráč se rozhodne neriskovat a vrátit se na začátek s mírnými penalizacemi."""
        self.player.clear_messages()
        self.system_messages = ["Rozhodl jsi se neriskovat a vrátit se na začátek."]
        self.player.current_room_index = 0
        self.player.defense = self.player.defense // 2  # Snížení obrany na polovinu
        self.player.attack = self.player.attack // 2
        self.current_room = self._generate_random_room(self.player.current_room_index)  # Generuje novou první místnost
        self.combat_active_enemy = None # Nepřítel, se kterým se aktuálně bojuje
        self.game_state = GAME_STATES["EXPLORATION"]

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

        room_text = UI.Label(
            pos=(SCREEN_WIDTH // 2, 50),
            text=f"Místnost: {self.current_room.name} (Úroveň: {self.player.current_room_index})",
            font=self.font,
            color=WHITE,
            align="center"
        )
        room_text.draw(self.screen)

        # Statistiky hráče
        player_health = UI.HealthSlider(
            pos=(50, SCREEN_HEIGHT - 70),
            size=(300, 40),
            min_value=0,
            max_value=self.player.max_health,
            value=self.player.health,
            bar_color=GREEN,
            bg_color=GREY,
            border_color=WHITE
        )
        player_health.set_value(self.player.health)
        player_health.draw(self.screen)

        player_health_text = UI.Label(
            pos=(50, SCREEN_HEIGHT - 100),
            text=f"Životy: {self.player.health}/{self.player.max_health}",
            font=self.font,
            color=GREEN,
            align="left"
        )

        player_health_text.draw(self.screen)
        player_stats_text = UI.Label(
            pos=(50, SCREEN_HEIGHT - 130),
            text=f"Útok: {self.player.attack} | Obrana: {self.player.defense}",
            font=self.font,
            color=WHITE,
            align="left"
        )
        player_stats_text.draw(self.screen)

        # Inventář
        inventory_text = UI.Label(
            pos=(50, 50),
            text="Inventář:",
            font=self.font,
            color=WHITE,
            align="left"
        )
        inventory_text.draw(self.screen)
        self.inventory_buttons = []  # Reset tlačítek při každém překreslení
        if not self.player.inventory:
            self.screen.blit(self.small_font.render("Prázdný", True, GREY), (50, 80))
        else:
            y_offset = 80
            for item in self.player.inventory:
                item_btn = UI.Button(
                    rect=(50, y_offset, 300, 30),
                    text=f"{item.name} ({item.item_type}, V: {item.value})",
                    font=self.small_font,
                    color=WHITE,
                    text_color=BLACK,
                    align="center"
                )
                item_btn.draw(self.screen)
                self.inventory_buttons.append((item_btn, item))  # Uložit dvojici tlačítko-item
                y_offset += 35

        # Pain Coins
        pain_coins_text = UI.Label(
            pos=(SCREEN_WIDTH - 50, SCREEN_HEIGHT - 50),
            text=f"Pain Coins: {self.player.pain_coins}",
            font=self.font,
            color=RED,
            align="right"
        )
        pain_coins_text.draw(self.screen)








        # Nepřítel v boji (pokud je v boji)
        if self.game_state == GAME_STATES["COMBAT"] and self.combat_active_enemy:
            enemy_name_text = UI.Label(
                pos=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2-250),
                text=f"Nepřítel: {self.combat_active_enemy.name}",
                font=self.font,
                color=RED,
                align="center"
            )
            enemy_name_text.draw(self.screen)


            enemy_health = UI.HealthSlider(
                pos=(SCREEN_WIDTH//2-100, SCREEN_HEIGHT//2-210),
                size=(200, 20),
                min_value=0,
                max_value=self.combat_active_enemy.max_health,
                value=self.combat_active_enemy.health,
                bar_color=RED,
                bg_color=GREY,
                border_color=WHITE
            )
            enemy_health.set_value(self.combat_active_enemy.health)
            enemy_health.draw(self.screen)

            #enemy_health_text = UI.Label(
            #    pos=(SCREEN_WIDTH//2+100, SCREEN_HEIGHT//2-210),
            #    text=f"Životy: {self.combat_active_enemy.health}/{self.combat_active_enemy.max_health}",
            #    font=self.font,
            #    color=RED,
            #    align="center"
            #)
            #enemy_health_text.draw(self.screen)

            #enemy_stats_text = UI.Label(
            #    pos=(SCREEN_WIDTH - 200, SCREEN_HEIGHT - 100),
            #    text=f"Útok: {self.combat_active_enemy.attack} | Obrana: {self.combat_active_enemy.defense}",
            #    font=self.font,
            #    color=RED,
            #    align="right"
            #)
            #enemy_stats_text.draw(self.screen)

            enemy_image = UI.EnemyImage(
                pos=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 50),
                enemy=self.combat_active_enemy,
                max_size=(200, 300),
                align="center"
            )
            enemy_image.draw(self.screen)

        # Zprávy pro hráče (krátkodobé)
        y_offset = SCREEN_HEIGHT - 200
        if len(self.player.messages) > 3:
            self.player.messages.pop(0)  # Omezit počet zpráv na 3
        for msg in reversed(self.player.messages): # Zobrazit nejnovější nahoře
            self._display_message(msg, WHITE, SCREEN_WIDTH//2, y_offset)
            y_offset -= 25

        # Systémové zprávy (delší dobu viditelné instrukce)
        y_offset = SCREEN_HEIGHT - 50
        for msg in self.system_messages:
            self._display_message(msg, YELLOW, y=y_offset)
            y_offset += 25


        # Instrukce pro boj
        if self.game_state == GAME_STATES["COMBAT"]:
            attack_btn = UI.Button(
                rect=(SCREEN_WIDTH//2-100, SCREEN_HEIGHT - 150, 200, 40),
                text="Útok (A)",
                font=self.small_font,
                color=BLACK,
                text_color=WHITE,
                align="center",
                border_color=WHITE,
                border_width=2
            )
            attack_btn.draw(self.screen)

            flee_btn = UI.Button(
                rect=(SCREEN_WIDTH//2-300, SCREEN_HEIGHT - 150, 200, 40),
                text="Útěk (ESC)",
                font=self.small_font,
                color=BLACK,
                text_color=WHITE,
                align="center",
                border_color=WHITE,
                border_width=2
            )
            flee_btn.draw(self.screen)

            rebirth_btn_color = BLACK
            if self.player.pain_coins < 10:  # Pokud hráč nemá dostatek Pain Coins, neriskování nebude dostupné
                rebirth_btn_color = GREY  # Ztlumení tlačítka
            else:
                rebirth_btn_color = BLACK  # Aktivní barva tlačítka
            rebirth_btn = UI.Button(
                rect=(SCREEN_WIDTH//2+100, SCREEN_HEIGHT - 150, 200, 40),
                text="Vrátit se (10 Pain Coins)",
                font=self.small_font,
                color=rebirth_btn_color,
                text_color=WHITE,
                align="center",
                border_color=WHITE,
                border_width=2
            )
            rebirth_btn.draw(self.screen)

            mouse_pressed = pygame.mouse.get_pressed()
            mouse_pos = pygame.mouse.get_pos()
            if mouse_pressed[0] and attack_btn.rect.collidepoint(mouse_pos):
                self._player_turn_attack()
                time.sleep(0.1)
            elif mouse_pressed[0] and flee_btn.rect.collidepoint(mouse_pos):
                self._flee_from_combat()
                time.sleep(0.1)
            elif mouse_pressed[0] and rebirth_btn.rect.collidepoint(mouse_pos):
                if self.player.pain_coins >= 10:
                    self.player.pain_coins -= 10
                    self.system_messages = ["Rozhodl jsi se neriskovat a vrátit se na začátek."]
                    self._rebirth()
                    time.sleep(0.1)

        # Instrukce pro prozkoumávání
        elif self.game_state == GAME_STATES["EXPLORATION"]:
            next_room_btn = UI.Button(
                rect=(SCREEN_WIDTH//2-100, SCREEN_HEIGHT - 150, 200, 40),
                text="Další místnost (SPACE)",
                font=self.small_font,
                color=BLACK,
                text_color=WHITE,
                align="center",
                border_color=WHITE,
                border_width=2
            )
            next_room_btn.draw(self.screen)
            rebirth_btn_color = BLACK
            if self.player.pain_coins < 10:  # Pokud hráč nemá dostatek Pain Coins, neriskování nebude dostupné
                rebirth_btn_color = GREY  # Ztlumení tlačítka
            else:
                rebirth_btn_color = BLACK
            rebirth_btn = UI.Button(
                rect=(SCREEN_WIDTH//2+100, SCREEN_HEIGHT - 150, 200, 40),
                text="Vrátit se (5 Pain Coins)",
                font=self.small_font,
                color=rebirth_btn_color,
                text_color=WHITE,
                align="center",
                border_color=WHITE,
                border_width=2
            )
            rebirth_btn.draw(self.screen)

            mouse_pressed = pygame.mouse.get_pressed()
            mouse_pos = pygame.mouse.get_pos()
            if mouse_pressed[0] and next_room_btn.rect.collidepoint(mouse_pos):
                self._next_room()
                time.sleep(0.2)
            elif mouse_pressed[0] and rebirth_btn.rect.collidepoint(mouse_pos):
                if self.player.pain_coins >= 5:  # Podmínka pro použití neriskování
                    self.player.pain_coins -= 5  # Snížení Pain Coins o 5
                    self.system_messages = ["Rozhodl jsi se neriskovat a vrátit se na začátek."]
                    self._rebirth()
                    time.sleep(0.1)
                else:
                    self.system_messages = ["Nemáš dostatek Pain Coinů! Potřebuješ alespoň 5."]

        # Instrukce pro konec hry / vítězství
        elif self.game_state in [GAME_STATES["GAME_OVER"], GAME_STATES["WIN"]]:
            restart_btn = UI.Button(
                rect=(SCREEN_WIDTH // 2-100, SCREEN_HEIGHT // 2-20, 200, 40),
                text="Restartovat hru",
                font=self.small_font,
                color=BLACK,
                text_color=WHITE,
                align="center",
                border_color=WHITE,
                border_width=2
            )
            restart_btn.draw(self.screen)

            # Check mouse click for restart button using the last event
            mouse_pressed = pygame.mouse.get_pressed()
            mouse_pos = pygame.mouse.get_pos()
            if mouse_pressed[0] and restart_btn.rect.collidepoint(mouse_pos):
                self._reset_game()

        

        pygame.display.flip()

    def run(self):
        """Spustí hlavní herní smyčku."""
        running = True
        while running:
            self._handle_events()
            self._draw_ui()
            self.clock.tick(FPS)

    def intro(self):
        """Zobrazí úvodní obrazovku s fade-in a fade-out efektem a čeká na kliknutí na tlačítko."""
        button_width, button_height = 220, 50
        button_x = SCREEN_WIDTH // 2 - button_width // 2
        button_y = SCREEN_HEIGHT // 2 + 40

        # Fade-in
        alpha_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        alpha_surface.fill(BLACK)
        time.sleep(1)
        for alpha in range(255, -1, -3):
            self.screen.fill(BLACK)
            intro_text = self.font.render("Risk of Pain", True, WHITE)
            self.screen.blit(intro_text, (SCREEN_WIDTH // 2 - intro_text.get_width() // 2, SCREEN_HEIGHT // 2 - 40))

            # Draw button
            mouse_pos = pygame.mouse.get_pos()
            button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
            color = (0, 0, 0) if button_rect.collidepoint(mouse_pos) else BLACK
            pygame.draw.rect(self.screen, color, button_rect)
            pygame.draw.rect(self.screen, WHITE, button_rect, 2)

            button_text = self.small_font.render("Začít hru", True, WHITE)
            self.screen.blit(
                button_text,
                (button_x + button_width // 2 - button_text.get_width() // 2,
                 button_y + button_height // 2 - button_text.get_height() // 2)
            )

            alpha_surface.set_alpha(alpha)
            self.screen.blit(alpha_surface, (0, 0))
            pygame.display.flip()
            self.clock.tick(60)

        # Wait for button click
        button_clicked = False
        while not button_clicked:
            self.screen.fill(BLACK)
            intro_text = self.font.render("Risk of Pain", True, WHITE)
            self.screen.blit(intro_text, (SCREEN_WIDTH // 2 - intro_text.get_width() // 2, SCREEN_HEIGHT // 2 - 40))

            mouse_pos = pygame.mouse.get_pos()
            button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
            color = (0, 0, 0) if button_rect.collidepoint(mouse_pos) else BLACK
            pygame.draw.rect(self.screen, color, button_rect)
            pygame.draw.rect(self.screen, WHITE, button_rect, 2)

            button_text = self.small_font.render("Začít hru", True, WHITE)
            self.screen.blit(
                button_text,
                (button_x + button_width // 2 - button_text.get_width() // 2,
                 button_y + button_height // 2 - button_text.get_height() // 2)
            )

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if button_rect.collidepoint(event.pos):
                        button_clicked = True

            self.clock.tick(60)

        # Fade-out
        for alpha in range(0, 256, 3):
            self.screen.fill(BLACK)
            intro_text = self.font.render("Risk of Pain", True, WHITE)
            self.screen.blit(intro_text, (SCREEN_WIDTH // 2 - intro_text.get_width() // 2, SCREEN_HEIGHT // 2 - 40))

            # Draw button
            mouse_pos = pygame.mouse.get_pos()
            button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
            color = (0, 0, 0) if button_rect.collidepoint(mouse_pos) else BLACK
            pygame.draw.rect(self.screen, color, button_rect)
            pygame.draw.rect(self.screen, WHITE, button_rect, 2)

            button_text = self.small_font.render("Začít hru", True, BLACK)
            self.screen.blit(
                button_text,
                (button_x + button_width // 2 - button_text.get_width() // 2,
                 button_y + button_height // 2 - button_text.get_height() // 2)
            )

            alpha_surface.set_alpha(alpha)
            self.screen.blit(alpha_surface, (0, 0))
            pygame.display.flip()
            self.clock.tick(60)