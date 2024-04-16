import random
from color import c
from time import sleep

enemies_for_level = []

goblin_attacks = [
    ['Punch', 10, 1], 
    ['Stab', 20, 0.95], 
    ['Kick', 30, 0.8],
    ['Smash', 50, 0.5]
]

TEK_attacks = [
    ['Laser', 30, 1], 
    ['BOOM BOOM ROBOT', 69, 1]
]

sorcerer_attacks = [
    ['HA HA MAGIC GO BRRRR', 10, 1], 
    ['Gandalf lmao', 10, 1]
]

#Output modifications
def rnum(num):
    return c["red"] + str(num) + c["reset"]


def tcc(color, my_string):
    return c[color] + str(my_string) + c["reset"]


def sp_eff(string, wait):
    for l in string:
        print(l, end='', flush=True)
        sleep(wait)


#Classes
class Enemy:
    def __init__(self, health, attack_list, is_possessed=False):
        self.attacks = [] 
        self.items = []
        self.dropped_objects = []
        self.drop_moves_percentage = 0.8 #default 20% of dropping move
        self._possessed = is_possessed
        self.health = int(health/2) if self._possessed else health

    def weakened_move_damage(self):
        if self._possessed:
            for m in self.attacks:
                m[1] = int(m[1]/2)  #possessed enemies will have their move damages halved

    def fights(self):
        #a is a random attack. Ex. ['Smash', 50, 0.5]
        a = random.choice(self.attacks)
        
        if random.random() < a[2]:  
            print(f"{'Possessed ' if self._possessed else ''}{self.colorname} used {a[0]} and it did {rnum(a[1])} damage!\n")
            return a[1]
        else:
            print(f"{'Possessed ' if self._possessed else ''}{self.colorname} used {a[0]} and it missed...\n")
            return 0 
    
    def drop(self):  #execute this when enemy dies
        if self._possessed:
            pass  #doesn't drop anything
        else:
            p = random.random()
            if self.attacks:  #if there's actually moves in self.attacks
                if p < self.drop_moves_percentage:
                    self.dropped_objects.append(*random.choices(self.attacks))
                
            for item in self.items:
                if p < item[1]:
                    self.dropped_objects.append(item)


class Goblin(Enemy):
    def __init__(self, health, attack_list, is_possessed=False):
        super().__init__(health, attack_list, is_possessed)
        #Takes 1-4 random attacks from the goblin_attacks
        self.attacks.extend(
            random.sample(
              attack_list, 
              random.randint(1, len(goblin_attacks))
            )
        )
        self.colorname = tcc("lightgreen", 'Goblin')
        self.items = [
            ['Coin', 0.8, 'A shiny, golden piece of goblin currency!'],
            ['Knife', 0.8, 'This sharpened blade increases the damage of attacks like Stab and Slash!']
        ]
        

class GoblinBrute(Goblin):
    def __init__(self, health, attack_list, is_possessed=False):
        super().__init__(health, attack_list, is_possessed)
        self.warning_health = health * 0.2
        #Since Goblin Brutes can only have one other basic attack, this sets the list to one random attack
        for _ in range(len(self.attacks) - 1):
            self.attacks.remove(random.choice(self.attacks))
            
        self.attacks.append(['Hit', 15, 0.85])
        self.colorname = tcc("green", 'Goblin Brute')
        
    def fights(self):
        a = random.choice(self.attacks)
        boost = 1

        #Damage increases by 50% when health is low.
        if self.health <= self.warning_health:
            boost = 1.5
            sp_eff(tcc("lightblue", "The Brute's enraged! It's attacks will now be stronger."), 0.05)
            print('\n')
            sleep(1.5)

        if a[0] == 'Hit':
            total_dmg = 0
            return_string = ''
        
            #Three sharp hits, BAM if hits, whoosh if misses.
            for _ in range(3):
                if random.random() < a[2]:
                    total_dmg += a[1] * boost
                    return_string += 'BAM! '
                else:
                    return_string += 'whoosh! '

            total_dmg = round(total_dmg)
            print(
                f'{self.colorname} swiftly attacked! {return_string}It did a total of {rnum(total_dmg)} damage.\n')
            
            return total_dmg
        else:
            if random.random() < a[2]:
                print(
                    f'{self.colorname} used {a[0]} and it did {rnum(round(a[1]*boost))} damage!\n')
                return round(a[1]*boost)
            else:
                print(f'{self.colorname} used {a[0]} and missed...\n')
                return 0


class TEK(Enemy):
    def __init__(self, health, attack_list, is_possessed=False):
        super().__init__(health, attack_list, is_possessed)
        self.attacks.extend(
            random.sample(
                attack_list, 
                random.randint(1, len(TEK_attacks))
            )
        )
        self.colorname = tcc("lightgrey", 'TEK')


class Kruncher(TEK):
    def __init__(self, health, attack_list, is_possessed=False):
        super().__init__(health, attack_list, is_possessed)
        #Kruncher only has one move: the powerful Plasma Ray.
        self.attacks.clear()
        self.attacks.append(
            ['Plasma Ray', 50, 0.7] 
        )
        self.colorname = 'Kruncher'
        self.plasma_acc = 0.7
    
    def death_spawning(self, index):
        #Spawns two TEKs upon death
        print(f'{self.colorname} splits open, revealing two TEKs encased in its metal body...')
        enemies_for_level.insert(index + 1, TEK(random.randint(60, 65), TEK_attacks)) 
        enemies_for_level.insert(index + 1, TEK(random.randint(60, 65), TEK_attacks))
    
    def fights(self):
        if self.plasma_acc > 0:#not recharging
            r = super().fights()
            self.plasma_acc = 0  #has to recharge next turn
            return r
            
        elif self.plasma_acc == 0:
            print(f'The {self.colorname} is recharging...\n')
            self.plasma_acc = 0.7  #done charging
            return 0
        

class Sacrificer(Enemy):
    def __init__(self, health):
        super().__init__(health, attack_list=None)
        self.colorname = '\033[01m\033[31mSacrificer\033[0m'
        self.items = [
            ['Bomb', 0.1, 'KA-BOOM!']
        ]
    
    def fights(self):
        dmg = random.randint(70, 80)
        print(' '*25, 'BOOM!\n')
        sleep(2)
        print(f'The {self.colorname.lower()} blew up in your face! It dealt {dmg} damage.\n')
        self.health = 0 #suicide
        return dmg
        

class Sorcerer(Enemy):
    def __init__(self, health, attack_list, is_possessed=False):
        super().__init__(health, attack_list, is_possessed)
        self.attacks.extend(
            random.sample(
               attack_list, 
               random.randint(1, len(sorcerer_attacks))
            )
        )


class EnergySorcerer(Sorcerer):
    def __init__(self, health, attack_list, is_possessed=False):
        super().__init__(health, attack_list, is_possessed)
        self.attacks.append(
            ['Life Drain', 30, 0.95]
        )
        self.colorname = tcc("yellow", 'Energy Sorcerer')
    
    def fights(self):
        #a is a random attack. Ex. ['Smash', 50, 0.5]
        a = random.choice(self.attacks)

        if a[0] == 'Life Drain':
            if random.random() < a[2]: 
                self.health += a[1]  #'absorbs' health 
                print(f'{self.colorname} used {a[0]} and it absorbed {rnum(a[1])} damage! Its health is now {self.health}.\n')
                return a[1]
            else:
                print(f'{self.colorname} used {a[0]} and it missed...\n')
                return 0 
            
        else:
            if random.random() < a[2]:  
                print(f'{self.colorname} used {a[0]} and it did {rnum(a[1])} damage!\n')
                return a[1]
            else:
                print(f'{self.colorname} used {a[0]} and it missed...\n')
                return 0 

#All possessed enemies
classes = [
    Goblin(random.randint(40, 50), goblin_attacks, True),
    GoblinBrute(random.randint(80, 100), goblin_attacks, True),
    TEK(random.randint(60, 65), TEK_attacks, True),
    Sorcerer(random.randint(30, 40), sorcerer_attacks, True),
    Kruncher(random.randint(95, 105), TEK_attacks, True),
    EnergySorcerer(random.randint(50, 60), sorcerer_attacks, True)
]
enemy_dict = {type(c).__name__: c for c in classes}

class DarkSorcerer(Sorcerer):
    def __init__(self, health, attack_list):
        super().__init__(health, attack_list)
        self.attacks.clear()
        self.attacks.append(['Night Daze', 15, 0.85, 'move_acc_dec'])  #move's accuracy decreases
        self.attacks.append(['Wisp of Doom', 0, 0.75, 'item_gone'])       
        self.colorname = tcc("purple", 'Dark Sorcerer')
        self.drop_moves_percentage = 0
    
    def fights(self):
        #a is a random attack. Ex. ['Smash', 50, 0.5]
        a = random.choice(self.attacks)
        
        if len(a) > 3: #special attack
            if a[3] == 'move_acc_dec':
                print(f"{self.colorname} used Night Daze, dealing {rnum(15)} damage. Strange, foul-smelling smog surround you.")
                sleep(3)
                sp_eff("Your vision begin to weaken, causing a 25% decrease in all of your move's accuracies!", 0.05)
                print('\n')
                return a[1], 'move_acc_dec'
            elif a[3] == 'item_gone':
                sp_eff(f'{self.colorname} shakes violently and wretches a blackish sludge ball. Its eyes glow with malice, and hurls the sludge at your bag...', 0.1)
                print('\n')
                return a[1], 'item_gone'
        else:
            if random.random() < a[2]:  
                print(f'{self.colorname} used {a[0]} and it did {rnum(a[1])} damage!\n')
                return a[1]
            else:
                print(f'{self.colorname} used {a[0]} and it missed...\n')
                return 0 
    
    def dark_spirit(self, current_index):
        found_enemy = False
        for i in range(current_index, -1, -1):
            name = type(enemies_for_level[i]).__name__
            if name in ['DarkSorcerer', 'Sacrificer']:
                pass
            else:
                enemies_for_level.insert(current_index + 1, enemy_dict[name])  
                found_enemy = True
                break  #found a dead enemy suitable for possessing
        
        if found_enemy == False:
            print('The Spirit cannot find any body to take control of.... it fades away.')


class MasterSorcerer(Sorcerer):
    def __init__(self, health, attack_list):
        super().__init__(health, attack_list, is_possessed=False)
        self._effects = ['poison', 'paralyze', 'confuse']
        self.warning_health = health * 0.5
        self.colorname = 'Master Sorcerer'
        self._boost = 1

    def fights(self):
        if self.health <= self.warning_health:
            print('The Master Sorcerer flings away its darts. It reaches in its cloak and brings out a staff! ')
            self._boost = 1.5

            #Sorcerer attack method
            
        else:
            e = random.choice(self._effects)

            if e == 'poison':
                desc1 = 'soaked in a sickly green fluid'
                desc2 = 'poisoning'
            elif e == 'paralyze':
                desc1 = 'charged with electricity'
                desc2 = 'paralyzing'
            elif e == 'confuse':
                desc1 = 'flashing brightly through the dim surroundings'
                desc2 = 'confusing'
            
            print(f'The Master Sorcerer hurls a dart at you, its tip {desc1}. It plunges into your flesh, {desc2} you!\n')

            return 30, e





