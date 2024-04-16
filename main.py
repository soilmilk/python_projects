import random
from time import sleep
import sys
from enemy import*


#Name, Damage, Accuracy
player_attacks = [
    ['Slash', 20, 1], 
    ['Slam', 30, 0.95], 
    ['Punch', 15, 1],
    ['GOGOG', 20, 1],
    ['Test attack', 100, 1]
]


#Level:{Name:Spawnrate percentage}
spawnrates = {
    1: {
        'Goblin': 0,
        'GoblinBrute': 0,
        'TEK': 0,
        'Sorcerer': 0,
        'Sacrificer': 0,
        'Kruncher': 0,
        'EnergySorcerer': 0,
        'DarkSorcerer': 0,
        'MasterSorcerer': 1
    },
    2: {
        'Goblin': 0.2,
        'GoblinBrute': 0.2,
        'TEK': 0.3,
        'Sorcerer': 0.3,
        'Sacrificer': 0,
        'Kruncher': 0,
        'EnergySorcerer': 0,
        'DarkSorcerer': 0,
        'MasterSorcerer': 0
    },
    3: {
        'Goblin': 0.2,
        'GoblinBrute': 0.2,
        'TEK': 0.3,
        'Sorcerer': 0.3,
        'Sacrificer': 0,
        'Kruncher': 0,
        'EnergySorcerer': 0,
        'DarkSorcerer': 0,
        'MasterSorcerer': 0
    },
    4: {
        'Goblin': 0.2,
        'GoblinBrute': 0.2,
        'TEK': 0.3,
        'Sorcerer': 0.3,
        'Sacrificer': 0,
        'Kruncher': 0,
        'EnergySorcerer': 0,
        'DarkSorcerer': 0,
        'MasterSorcerer': 0
    },
    5: {
        'Goblin': 0.2,
        'GoblinBrute': 0.2,
        'TEK': 0.3,
        'Sorcerer': 0.3,
        'Sacrificer': 0,
        'Kruncher': 0,
        'EnergySorcerer': 0,
        'DarkSorcerer': 0,
        'MasterSorcerer': 0
    }

}

#Item, num of items, player's status.
items = []
level = 1


#Checks if user's input is valid or not.
def check_if_correct(
        c_list, v, 
        n_statement='', y_statement= ''):
    
    while v:
        if v in c_list:
            if y_statement:
                print(y_statement)
            else:
                pass 
        
            return v 
            break
        else:
            v = input(n_statement)


def movesdraw():
    print('      Moves  Damage  Accuracy')
    for i, atk in enumerate(player.attacks):
        print(f'{i+1} --> ', end='')
        for my_str in atk:
            print(str(my_str).ljust(9), end='')

        print('\n')


def itemsdraw():
    print('Name     ', 'Number of Item ', 'Description')
    print('------------------------------------------------------')
    #This removes any item that has a count of 0 (or less)
    for item_copy in items.copy():
        if item_copy[3] <= 0:
            items.remove(item_copy)

    for item in items:
        d = divmod(len(item[2].split()), 5) 
        lines = d[0] if d[1] == 0 else d[0]+1
        mid_of_lines = round((lines + 1)/2) if lines % 2 == 1 else round(lines/2)
        split_desc = item[2].split()
        n = 0

        for line in range(1, lines+1):
            if line == mid_of_lines:
                print(item[0],' '*(9 - len(item[0])), end='')
                print(item[3], ' '*(15 - len(str(item[3]))), end='')
                print(*split_desc[n:n+5])
            else:
                print(' '*25, *split_desc[n:n+5])

            n += 5

        print('------------------------------------------------------')


def enemyspawn():
    my_list = random.choices(['g', 'gb', 't', 's', 'sac', 'k', 'es', 'ds', 'ms'], weights = [
        spawnrates[level]['Goblin'], 
        spawnrates[level]['GoblinBrute'],
        spawnrates[level]['TEK'], 
        spawnrates[level]['Sorcerer'],
        spawnrates[level]['Sacrificer'],
        spawnrates[level]['Kruncher'],
        spawnrates[level]['EnergySorcerer'],
        spawnrates[level]['DarkSorcerer'],
        spawnrates[level]['MasterSorcerer']
    ], 
    k = 10)
    for n in my_list:
        if n == 'g':
            enemies_for_level.append(Goblin(random.randint(40, 50), goblin_attacks))
        elif n == 'gb':
            enemies_for_level.append(GoblinBrute(random.randint(80, 100), goblin_attacks))
        elif n == 't':
            enemies_for_level.append(TEK(random.randint(60, 65), TEK_attacks))
        elif n == 's':
            enemies_for_level.append(Sorcerer(random.randint(30, 40), sorcerer_attacks))
        elif n == 'sac':
            enemies_for_level.append(Sacrificer(random.randint(20, 30)))
        elif n == 'k':
            enemies_for_level.append(Kruncher(random.randint(95, 105), TEK_attacks))
        elif n == 'es':
            enemies_for_level.append(EnergySorcerer(random.randint(50, 60), sorcerer_attacks))
        elif n == 'ds':
            enemies_for_level.append(DarkSorcerer(random.randint(40, 55), sorcerer_attacks))
        elif n == 'ms':
            enemies_for_level.append(MasterSorcerer(random.randint(70, 100), sorcerer_attacks))


def player_enemy_fights():
    while current_enemy.health > 0 and player.health > 0:
        p_attacks_yet = False
        while p_attacks_yet == False:
            p_choice = check_if_correct(
                ['i', 'm', 'e', '1', '2', '3', '4'], 
                input('Would would you like to do? Enter "i" if you forgot the keys.'), 
                "That's not a valid answer. Try again.")

            if p_choice == 'i':
                print('\n  1, 2, 3 or 4 to attack. \n  "m" for current moves.\n  "e" for items.\n  "d" for description of encountered enemies.\n')
            elif p_choice == 'm':
                movesdraw()
            elif p_choice == 'e':
                if len(items) == 0:  #empty
                    print("\n  There's no items in your inventory!\n")
                else: 
                    itemsdraw()
            else:
                try:
                    player.attacks[int(p_choice)-1]
                except IndexError:
                    print("There's no move for that slot number! \n")
                else:
                    print(' ', '_'*40)
                    sleep(0.5)
                    dmg = player.fights(int(p_choice)-1)
                    sleep(0.5)
                    current_enemy.health -= dmg
                    current_enemy.health = 0 if current_enemy.health < 0 else current_enemy.health
                    print(f"{'Possessed ' if current_enemy._possessed else ''}{current_enemy.colorname} is left with {current_enemy.health} health ...\n")
                    break #same as attack_yet = True

        #Check if enemy or player is dead. If enemy is dead, break out of this while loop and continue on to the next enemy.
        if current_enemy.health <= 0 or player.health <= 0:
            print(' ', '_'*40)
            break
             
        #Enemy Attacks
        sleep(1)
        #Checking if the enemy's attack is special or not.
        return_obj = current_enemy.fights()

        if isinstance(return_obj, tuple):  #tuples contain damage and status Ex. (50, 'poison')
            player.status = return_obj[1]  
            damage = return_obj[0]

        player.health -= damage
        sleep(1.5)
        player.health = 0 if player.health < 0 else player.health #setting any negative health to 0 health
        print(f'{player.name} is left with {player.health} health ...')
        print(' ', '_'*40, '\n')


def object_procedure():
    if len(current_enemy.dropped_objects) == 0: #dropped nothing
        pass
    else:
        if current_enemy.dropped_objects[0][1] > 1: #checking if it's a move
            print('You found a move! Here it is below:\n')
            print('Move  Damage  Accuracy')
            for my_str in current_enemy.dropped_objects[0]:
                print(str(my_str).ljust(9), end='')
            print('\n')
            sleep(3)
            print('Current Moves:')
            movesdraw()

            if check_if_correct(['y', 'n'], input('Would you like to pick it up?'),"That's not y or n. Try again.") == 'y':
                if len(player.attacks) == 4: #moves are full
                    sleep(1.5)
                    a = input('You have 4 moves already! Please select a move slot(1,2,3,4) to be replaced:')
                    index = int(check_if_correct(['1', '2', '3', '4'], a, "That's not 1, 2, 3, or 4. Try again:"))-1
                    
                    #Replacing the new move with old move
                    print('                           ', end='')
                    sp_eff('.  .  .  .', 0.25)
                    print(f'\n{player.attacks[index][0]} is replaced with {current_enemy.dropped_objects[0][0]}.\n')
                    player.attacks[index] = current_enemy.dropped_objects[0]
                    del current_enemy.dropped_objects[0]  #deleting the move
                    
                else:
                    print('                           ', end='')
                    sp_eff('.  .  .  .', 0.25)
                    print('\nAdded!\n')
                    player.attacks.append(current_enemy.dropped_objects[0])
                    del current_enemy.dropped_objects[0]  #deleting the move
                    
            else:
                print(f'{player.name} left the move behind...\n')
                del current_enemy.dropped_objects[0]  #deleting the move

        
        #Items
        print(f'The {current_enemy.colorname} dropped some items!')
        for item in current_enemy.dropped_objects:
                c = check_if_correct(['y', 'n'], input(f'Do you wanna pick up this {item[0]}?'), 'Nope. Please enter y or n:')
                if c == 'y':
                    print('Picked up!')
                    if len(items) == 0:#no items 
                        item.append(1)
                        items.append(item)   
                    else:
                        inItems = False
                        for i in items:
                            if i[0] == item[0]:#if there's already an item with the same name
                                i[3] += 1
                                inItems = True
                        if inItems == False:#no items in the player inventory has matching names
                            item.append(1)
                            items.append(item)
                            
            
#The basic attack method can be overriden with special attacks - important for sorcerers.
class Player:
    def __init__(self, name, health, attack_list):
        self.attacks = []
        self.name = tcc("bold", name)
        self.health = health
        #Gives the player 2 random starting attacks.
        self.attacks.extend(random.sample(attack_list, 4))
        self.status = 'normal'
    
    def fights(self, index):
        a = self.attacks[index]
        move_acc = a[2]

        if self.status == 'move_acc_dec':
            a[2] *= 0.75 #25% decrease in move accuracy
        elif self.status == 'normal':
            a[2] = move_acc
        elif self.status == 'item_gone':
            if len(items) == 0:
                print('\nYour knapsack is empty, causing the sludge to mournfully collapse into dust...')
                self.status = 'normal'
                sleep(3)
            else:
                i = random.choice(items)
                items[items.index(i)][3] -= 1
                print(f'\nThe sludge wriggles its way into your knapsack, destroying a {tcc("cyan", i[0])}. It disappears after that.')
                self.status = 'normal'
                sleep(2.5)
        elif self.status == 'poison':
            self.health -= 5  #maybe random number? 
            print('You took 5 damage from the poison!')
        elif self.status == 'paralyze':
            if random.random() < 0.5:
                print('As you get ready to attack, a jolt of pain wracks through your body. The paralysis causes you to not move!')
                return 0
            else:
                print('You recover from the paralysis.')
                self.status = 'normal'
        if random.random() < a[2]:  
            print(f'\n{self.name} used {a[0]} and it did {tcc("red", a[1])} damage!\n')
            return a[1]
        else:
            print(f'\n{self.name} used {a[0]} and it missed...\n')
            return 0  


is_alive = None
play = check_if_correct(
    ['y', 'n'], 
    input('Welcome to game! Would you like to play?'), 
    "That's not y or n stupid. Try again.")
    
if play == 'y':
        is_alive = True
        
        #Initialize player
        i = input('What is your name?') or 'Player'
        player = Player(i, 100, player_attacks)
        #enemies_for_level is alreay intialized in classes.       
else:
        is_alive = False
        print('Aw... Well bye then. ')

while is_alive:
    for level in range(1,6):
    
        enemyspawn()

        for current_enemy in enemies_for_level:
            print(type(current_enemy).__name__, level, current_enemy.health)

            player_enemy_fights()
            
            if current_enemy.health <= 0 and player.health > 0:
                sleep(1.5)
                sp_eff(f'{player.name} killed the {current_enemy.colorname}!', 0.05)
                print('\n')

                #Code to check what the player's status is.
                if player.status == 'move_acc_dec':
                    player.status = 'normal'
                    print('The mysterious smog disappears, and your eyesight returns to normal!\n') 
                    sleep(2)

                current_enemy.drop()  #drops loot
                object_procedure()  #asks the user if it wants to pick up the moves/items

                if type(current_enemy).__name__ == 'Kruncher':
                    current_enemy.death_spawning(enemies_for_level.index(current_enemy)) 
                elif type(current_enemy).__name__ == 'DarkSorcerer':
                    print('The Dark Sorcerer falls dead, and his weakened spirit jumps out, seeking a new body to posess. ')
                    current_enemy.dark_spirit(enemies_for_level.index(current_enemy))

                print(enemies_for_level)

            elif current_enemy.health > 0 and player.health <= 0:
                sleep(1.5)
                print("GAME OVER")        
                sys.exit()
            elif current_enemy.health <= 0 and player.health <= 0:
                print('you guys both died.')

        #Resets for next level.    
        enemies_for_level.clear()    


  
            
            
                

        

                

            
            

            

            



            

    
      
      
      

      
      
      
