import random, os, time

#MiddleEarthLife(TestGame)

GAME_DATA = {
    "zones": {
        "forest": {
            "enemies": {
                "forest goblin": {"hp": 50, "at":5, "mana": 100, "xp": 50},
                "forest elf": {"hp": 100, "at": 10, "mana": 100, "xp": 100}
            }
        }
    }
}

def ui_clear():
    os.system('cls' if os.name == 'nt' else 'clear')     
                           
class Character:

    def __init__(self, name, hp, at, mana, xp):
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.at = at
        self.luck = 5
        self.mana = mana
        self.xp = xp
        self.level = 1
        self.xp_required = 100
        self.is_defending = False
        self.sword = False
        self.inventory = ["legend sword"]
      
    def use_item(self, item_name):
         if item_name in self.inventory:
             if item_name == "legend sword" :
                  equip_remove = input("equip/remove: ").lower()
                  if equip_remove == "equip" or equip_remove == "e":
                      ui_clear()
                      print("you equiped the legend sword!")
                      time.sleep(2)
                      ui_clear()
                      self.sword = True
                  elif equip_remove == "remove" or equip_remove == "r":
                      ui_clear()
                      print("you unequiped the legend sword!")
                      time.sleep(2)
                      ui_clear()
                      self.sword = False
         else:
             print("you dont have that item!")
                  
    def level_system(self) :
        if self.sword == True:
            while self.xp >= self.xp_required:
                self.xp -= self.xp_required
                self.level += 1
                self.hp += self.level * 25
                self.max_hp += self.level * 25
                self.at += self.level * 2
                self.xp_required *= 1.5
                print(f"you're now level {self.level}!")
                    
    def is_alive(self):
        return self.hp > 0
      
    def take_damage(self, amount):
        if self.is_defending == True:
            amount //= 2
            time.sleep(2)
            ui_clear()
            self.is_defending = False
        self.hp -= amount
        print(f"{self.name} took {amount} dmg!")
        if self.hp < 0: self.hp = 0
        
    def attack(self, target):
        crit_roll = random.randint(1,100)
        final_dmg = self.at
        
        if crit_roll <= self.luck:
            final_dmg *= 2
            print("---CRITICAL HIT---")
                 
        print(f"| {self.name} attacks {target.name} for {final_dmg}!")    
        target.take_damage(final_dmg)
        time.sleep(2)
        ui_clear()

    def heal(self):
        heal_rec = 20
        if self.mana >= heal_rec:
            self.mana -= heal_rec
            self.hp += 50
            print(f"you got healed! (mana: {self.mana})")
            time.sleep(2)
            ui_clear()
        elif self.mana <= heal_rec:
            print(f"you dont have enough mana! (mana: {self.mana})")
            time.sleep(2)
            ui_clear()
        if self.mana <= 0:
            self.mana = 0
        if self.hp >= self.max_hp:
            self.hp = self.max_hp
            
    def defend(self):
        defend_rec = 20
        if self.mana >= defend_rec:
            self.mana -= defend_rec
            self.is_defending = True
            print(f"you defended! (your mana: {self.mana})")
            time.sleep(2)
            ui_clear()
        elif self.mana <= defend_rec:
            print(f"you dont have enough mana! (mana: {self.mana})")
            time.sleep(2)
            ui_clear()
        if self.mana <= 0:
            self.mana = 0

class GameEngine:
    def __init__(self):
        self.player = Character("name", 200, 20, 200, 0)
       
        self.is_running = True
             
    def spawn_enemy(self):
        name = random.choice(list(GAME_DATA["zones"]["forest"]["enemies"].keys()))
        
        stats = GAME_DATA["zones"]["forest"]["enemies"][name]
        
        return Character(name, stats["hp"], stats["at"], stats["mana"], stats["xp"])
        
    def battle_engine(self):
        enemy = self.spawn_enemy()
        print(f"a wild {enemy.name} sneeked up on you!")
        
        while enemy.is_alive() and self.player.is_alive():
            print("-" * 30)
            print(f"| Player: {self.player.hp} | Enemy: {enemy.hp} |")
            choice = input("(A)ttack, (D)efend, (H)eal, (I)nventory, (R)un? ").lower()
            ui_clear()         
            if choice == 'a':
                self.player.attack(enemy)
                ui_clear()
                if enemy.is_alive():
                    enemy.attack(self.player)
            elif choice == 'd':
                self.player.defend()
                ui_clear()
                if enemy.is_alive():
                    enemy.attack(self.player)
            elif choice == 'h':
                self.player.heal()
                ui_clear()
                if enemy.is_alive():
                    enemy.attack(self.player)
            elif choice == "i":
                use = input(f"what do you want to use? {self.player.inventory} ").lower()
                ui_clear()
                self.player.use_item(use)  
            elif choice == 'r':
                    print("you escaped safely!")
                    time.sleep(2)
                    ui_clear()
                    return
                    
        if not self.player.is_alive():
            self.is_running = False
            print("GAME OVER!")
            respawn = input("do you want to respawn? ")
            if respawn == "yes" or respawn =="y":
                self.is_running = True
                print("you have been respawned by the gods")
                
            else:
                self.is_running = False
                print("Thanks for playing!")
                    
        else:
            print(f"VICTORY! {enemy.name} was slained!")
            self.player.xp += enemy.xp
            self.player.level_system()  
            print(f"your current level: {self.player.level}")
            time.sleep(2)
            ui_clear()
                
    def start(self):
            print("welcome to middle earth! or kind of..")
            while self.is_running:
                print(f"\n|player: {self.player.name} | level: {self.player.level} | hp: {self.player.hp} | base attack: {self.player.at} |")
                cmd = input("| (E)xplore, (Q)uit: ").lower()
                ui_clear()
                if cmd == 'e':
                    self.battle_engine()
                elif cmd == 'q':
                    self.is_running = False
                    print("Thanks for playing!")
                    
if __name__=="__main__":
    player_name = input("whats your name hero? ")
    ui_clear()
    game = GameEngine()
    game.player.name = player_name
    game.start()
