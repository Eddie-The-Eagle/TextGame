# Opdracht: Maak een spel met een class en een aantal attributen HP, AV en functie attack
import sys
import os
import random
import time
import msvcrt

os.system('')

# Colors used for text in the console.
red = '\033[1;31;40m'
green = '\033[1;32;40m'
white = '\033[1;37;40m'
yellow = '\033[1;33;40m'
blue = '\033[0;36m'

# Used to wipe a singular line.
def clearPrevLine():
	sys.stdout.write("\033[F")
	sys.stdout.write("\033[K")
	
# Used to wipe the console and create blank lines.
def goBackLines():
	for i in range(21):
		sys.stdout.write("\033[F")
		
# Used to add new breaklines in the console.
def goForwardLines(rangeNumber):
	if rangeNumber > 12:
		rangeNumber -= 11
	for i in range(rangeNumber):
		sys.stdout.write("\033[E")
	
def clearScreen():
	os.system('cls')

class character():
	def __init__(self, name, maxhp, maxmp, strength, agility, magic, defense, level, weaponsList):
		self.name = name
		self.maxhp = maxhp
		self.hp = maxhp
		self.mp = maxmp
		self.maxmp = maxmp
		self.strength = strength
		self.agility = agility
		self.magic = magic
		self.defense = defense
		self.level = level
		self.gear = weaponsList
		self.spellList = []
		self.inventory = {}
		self.effects = {}
		self.xp = 0
		self.gold = 0
	
	# Handels the level up process
	def levelUp(player):
		player.level += 1
		hpincrease = random.randrange(5, 10, 1)
		player.maxhp += hpincrease
		player.hp = player.maxhp
		print(player.name, 'levelled up to level', player.level, '!')
		print(player.name, 'max hp has been increased by', hpincrease, 'to a total of', player.maxhp)
		print(player.name, 'has been fully healed to', player.hp)
		correctInput = True
		while correctInput:
			abilityToUp = input('Choose an ability to level up strength(' + str(player.strength) + '),'+ ' Agility(' + str(player.agility) + '),' + 'Magic(' + str(player.magic) + '),'+' or Defense(' + str(player.defense) + '): ').lower()
			print(abilityToUp)
			if abilityToUp in ('strength', 'agility', 'magic', 'defense'):
				correctInput = False
		if abilityToUp == 'strength':
			player.strength += 1
			print(player.name, 'strength has been increased by 1 to a total of', player.strength)
		elif abilityToUp == 'agility':
			player.agility += 1
			print(player.name, 'agility has been increased by 1 to a total of', player.agility)
		elif abilityToUp == 'magic':
			player.magic += 1
			print(player.name, 'magic has been increased by 1 to a total of', player.magic)
		elif abilityToUp == 'magic':
			player.defense += 1
			print(player.name, 'defense has been increased by 1 to a total of', player.defense)
		player.xp = 0
		
class combat():	
	# Starts a fight and makes sure it doesn't end until a player runs, dies or kills the enemy.
	# Also handles user input.
	def startFight(self, player, enemy):
		fighting, ran = True, True
		while fighting:
			rangeNumber = 0
			clearScreen()
			self.statsOverview(player, enemy, rangeNumber)
			action, metaData = self.actionChoices(player)
			if action == 'attack':
				fighting, rangeNumber = self.attack(enemy, player, green, rangeNumber)
			elif action == 'spell':
				fighting, rangeNumber	= self.castSpell(player, enemy, metaData, rangeNumber)
			elif action == 'potion':
				rangeNumber = self.usePotion(player, enemy, metaData, rangeNumber)
			elif action == 'run':
				fighting = self.run(player, enemy)
				ran = fighting
				if not fighting:
					break
			sys.stdout.write("\033[F")
			rangeNumber += 1
			print('\n')
			if fighting:
				fighting = self.attack(player, enemy, red, rangeNumber)
			if fighting:
				fighting, rangeNumber = self.tickSpell(enemy, rangeNumber)
			msvcrt.getch()
		if not fighting:
			self.endFight(player, enemy, ran)
			
	# Prints the current stats of the player and the enemy
	def statsOverview(self, player, enemy, rangeNumber):
		goBackLines()
		print(white + 'Combat Overview',
					'\n{:30}'.format('Player'), 'Enemy'
					'\n' + '{:30}'.format('Name: ' + str(player1.name)), 'Name:', player2.name, 
					'\n' + '{:30}'.format('Level: ' + str(player1.level)), 'Level:', player2.level, 
					'\n' + '{:30}'.format('HP: ' + str(player1.hp)), 'HP:', player2.hp, 
					'\n' + '{:30}'.format('MP: ' + str(player1.mp)), 'MP:', player2.mp, 
					'\n')
		goForwardLines(rangeNumber)
	
	# Allows the user to choose an action.
	def actionChoices(self, player):
		correctInput = True
		while correctInput:
			action = input('Choose an action (Attack, Spell, Potion, Run) ').lower()
			if action in ('attack, spell, potion, run'):
				metaData = action
				if action == 'spell':
					correctInput = False
					clearPrevLine()
					action, correctInput = self.spellMenu(player, correctInput)
				elif action == 'potion':
					correctInput = False
					clearPrevLine()
					action, correctInput = self.potionMenu(player, correctInput)
				elif action == 'potion' or action == 'attack' or action == 'run':
					correctInput = False
					clearPrevLine()
				else:
					clearPrevLine()
			else:
				clearPrevLine()
		action, metaData = metaData, action
		return action, metaData
	
	# Controls the opening of the spell menu and displays all spells.
	def spellMenu(self, player, correctInput):
		correctInputSpell = True
		while correctInputSpell:
			if player.spellList != []:
				action = input('Choose a spell (' + ', '.join(str(item.name) for item in player.spellList) + ') or type \'Back\' to go back. ').lower()
				if action == 'back':
					correctInputSpell, correctInput = False, True
				elif action in ((', '.join(str(item.name) for item in player.spellList))).lower():
					for item in player.spellList:
						if action in str(item.name).lower():
							action = item
							if player.mp > action.mpCost:
								correctInputSpell = False
							else:
								print('You don\'t have enough MP to use this spell!')
							break
				else:
					clearPrevLine()
		clearPrevLine()
		return action, correctInput 
		
	# Controls opening the potion menu and shows all current potions.
	def potionMenu(self, player, correctInput):
		correctInputPotion = True
		while correctInputPotion:
			if player.inventory != []:
				action = input('Choose a potion (' + ', '.join(str(str(item.name) + str(item.effect) + '[x' + str(player.inventory[item]) + ']') for item in player.inventory) + ') or type \'Back\' to go back. ').lower()
				if action == 'back':
					correctInputPotion, correctInput = False, True
				else:
					for item, v in player.inventory.items():
						if action in str(item.name).lower():
							action = item
							correctInputPotion = False
							break
				clearPrevLine()
		return action, correctInput 
								
	# Controls attacking an enemy or the player with melee. Allows for blocking, parrying and  missing. 
	def attack(self, defender, attacker, color, rangeNumber):
		flag = True
		attacks = self.attackTimes(attacker, defender)
		for hit in attacks:
			if hit == True:
				time.sleep(0.5)
				av = int(round(self.attackDamage(attacker) * (1-self.damageReduction(defender)),0))
				defender.hp = defender.hp - av 
				print(color + attacker.name, 'attacks', defender.name, 'with', attacker.gear[0].name, 'dealing', av, 'damage!')
				rangeNumber += 1
				if defender.hp > 0:
					self.statsOverview(attacker, defender, rangeNumber)
				else:
					print(color + defender.name, 'has fainted' + white)
					flag = False
					return flag, rangeNumber
			elif hit == 'Miss':
				print(yellow + attacker.name, 'misses their attack on', defender.name, 'with', attacker.gear[0].name + white)
				rangeNumber += 1
			elif hit == 'Block':
				print(yellow + defender.name, 'blocked the attack of', attacker.name, 'with', attacker.gear[0].name + white)
				rangeNumber += 1
			elif hit == 'Counter': 
				av = int(round((self.attackDamage(defender) * (1-self.damageReduction(attacker))*0.5),0))
				attacker.hp = attacker.hp - av 
				self.statsOverview(attacker, defender, rangeNumber)
				rangeNumber += 1
				print(yellow + defender.name, 'counter attacked', attacker.name, 'with', defender.gear[0].name, 'dealing', av, 'damage!' + white)
				if attacker.hp > 0:
					pass
				else:
					print(color + attacker.name, 'has fainted\n' + white)
					flag = False
					return flag
		return flag, rangeNumber
	
	# Controls the casting of a spell.
	def castSpell(self, player, enemy, spell, rangeNumber):
		player.mp -= spell.mpCost
		rangeNumber += 1
		print(player.name, 'casts', spell.name, 'on', enemy.name, 'dealing', spell.strength, spell.effect.lower(), 'damage!')
		if spell.effect == 'Burn':
			enemy.hp -= spell.strength
			if enemy.hp > 0:
				enemy.effects[spell] = spell.duration
				rangeNumber += 1
				print(enemy.name, 'is now burning!')
				flag = True
			else:
				rangeNumber += 1
				print(green + enemy.name, 'has fainted\n' + white)
				flag = False
		return flag, rangeNumber
		
	# Controls a DOT effect. 
	def tickSpell(self, enemy, rangeNumber):
		if enemy.effects == {}:
			pass
		else: 
			for spell, duration in enemy.effects.items():
				enemy.hp -= spell.damageOverTime
				enemy.effects[spell] -=  1
				removeSpell = spell
				rangeNumber += 2
				self.statsOverview(player1, enemy, rangeNumber)
				print(enemy.name, str(spell.effect) + 'ed', 'for', spell.damageOverTime, 'damage!')
			if enemy.effects[removeSpell] == 0:
				del enemy.effects[removeSpell]
				rangeNumber += 1
				self.statsOverview(player1, enemy, rangeNumber)
				print(enemy.name, 'is no longer', str(spell.effect) + 'ing!')
		if enemy.hp > 0:
			flag = True
		else:
			flag = False
		return flag, rangeNumber
		
	# Controls the usage of potions
	def usePotion(self, player, enemy, potion, rangeNumber):
		type = potion.potionType 
		if type == 'HPPotion':
			if (player.maxhp - player.hp) > potion.strength:
				player.hp = player.hp + potion.strength
				strength = potion.strength
			else:
				strength = player.maxhp - player.hp
				player.hp = player.maxhp
			print(green + player.name, 'used a', potion.name, 'and healed', strength, 'HP,', player.name, 'now has', player.hp, 'HP')
		elif type == 'MPPotion':
			if (player.maxmp - player.mp) > potion.strength:
				player.mp = player.mp + potion.strength
				strength = potion.strength
			else:
				strength = player.maxmp - player.mp
				player.mp = player.maxmp
			print(green + player.name, 'used a', potion.name, 'and healed for', strength, 'MP,', player.name, 'now has', player.mp, 'MP')
		if player.inventory[potion] > 1:
			player.inventory[potion] -= 1
		else:
			del player.inventory[potion]
		return rangeNumber
	
	def run(self, player, enemy):
		runRandom = random.randrange(0, 100)
		runChance = int(75 + (player.level - enemy.level) * 10)
		if runChance > runRandom:
			return False
		else:
			print('You failed to run away.')
			return True
	
	# Calculates how \many times the player will hit with given weapon
	# Also takes into account the shield of the defender
	def attackTimes(self, attacker, defender):
		attacks = []
		for i in range(0, attacker.gear[0].attackTimes):
			hit = random.randrange(0, 100, 1)
			if hit <= attacker.gear[0].hitChance:
				block = True
				if defender.gear[1] != 'noShield':
					block = self.block(defender)
				if defender.gear[0] != 'Fist':
					block = self.counter(attacker)
				attacks.append(block)
			else:
				attacks.append('Miss')
		return attacks
		
	# Checks if the defender blocks the attack.	
	def block(self, defender):
		blockChance = defender.gear[1].dv * 2
		block = random.randrange(0, 100, 1)
		if block > blockChance:
			return True
		else:
			return 'Block' 
			
	def counter(self, attacker):
		counterChance = attacker.gear[0].counterChance
		counter = random.randrange(0, 100, 1)
		if counter > counterChance:
			return True
		else:
			return 'Counter' 
		
	#Calculates Attack Damage based on the weapon and strength of the attacker
	def attackDamage(self, attacker):
		av = int(attacker.gear[0].av * (1 + (attacker.strength / 50)))
		return av
	
	#Calculates the damage reduction of the defender based on their armor
	def damageReduction(self, defender):
		defense = defender.defense
		if defender.gear[1] != '':
			defense += defender.gear[1].dv
		if defender.gear[2] != '':
			defense += defender.gear[2].dv
		damageReduction = defense * 0.005
		return damageReduction
		
	def endFight(self, player, enemy, ran=True):
		if player.hp > 0 and ran == True:
			self.winFight(player, enemy)
		elif player.hp > 0 and ran == False:
			print('You ran away!')
		else:
			print('You have died, GAME OVER!')
		
	# Gives the player XP and the end of a fight, and checks if he can levelup.
	def winFight(self, player, enemy):
		loot.chance()
		gainedXP = enemy.strength + enemy.agility * 10
		player.xp += gainedXP
		xpToLevel = player.level * 100
		print(blue + player.name, 'has succesfully defeated', enemy.name, 'and gained', str(gainedXP) + ' XP!\n' + str(xpToLevel-player.xp), 'XP is required to level up to level', str(player.level+1) + '!' + white)
		if player.xp >= xpToLevel:
			character.levelUp(player)
		
class weapon():
	def __init__(self, name, av, attackTimes, hitChance, counterChance, dropChance, weaponType):
		self.name = name
		self.av = av
		self.attackTimes = attackTimes
		self.hitChance = hitChance
		self.counterChance = counterChance
		self.dropChance = dropChance
		self.weaponType = weaponType
		
class gear():
	def __init__(self, name, dv, dropChance, gearType):
		self.name = name
		self.dv = dv
		self.dropChance = dropChance
		self.gearType = gearType
		
class spell():
	def __init__(self, name, effect, mpCost, strength, duration, dropChance):
		self.name = name
		self.mpCost = mpCost
		self.effect = effect
		self.strength = strength
		self.duration = duration
		self.damageOverTime = int(strength / duration)
		self.dropChance = dropChance
		
class potion():
	def __init__(self, name, potionType, effect, strength, dropChance):
		self.name = name
		self.potionType = potionType
		self.effect = effect
		self.strength = strength
		self.dropChance = dropChance
		
# Controls the distrubition of loot to the player, per category and item.		
class loot():
	def chance():
		drop = random.randrange(0, 100)
		if drop <= 12: 
			for item in lootList[0]:
				drop = random.randrange(0, 100)
				if drop <= item.dropChance:
					correctInput = True
					while correctInput:
						print('You\'ve found a ' + item.name,
								'\n{:25}'.format('New'), 'Current'
								'\n' + '{:25}'.format('Name: ' + str(item.name)), 'Name:', player1.gear[0].name, 
								'\n' + '{:25}'.format('Damage: ' + str(item.av)), 'Damage:', player1.gear[0].av, 
								'\n' + '{:25}'.format('Attack Chances: ' + str(item.attackTimes)), 'Attack Chances:', player1.gear[0].attackTimes, 
								'\n' + '{:25}'.format('Hit Chance: ' + str(item.hitChance)), 'Hit Chance:', player1.gear[0].hitChance, 
								'\n' + '{:25}'.format('Counter Chance: ' + str(item.counterChance)), 'Counter Chance:', player1.gear[0].counterChance, 
								'\n')
						equipBool = input('Do you want to equip it? (Yes/No)').lower()
						if equipBool in ('yes', 'no'):
							correctInput = False
					if equipBool == 'Yes':
						player1.gear[0] = item
					break
		elif drop > 12 and drop <= 25:
			for item in lootList[1]:
				drop = random.randrange(0, 100)
				if drop <= item.dropChance:
					correctInput = True
					while correctInput:
						print('You\'ve found a ' + item.name,
								'\n{:25}'.format('New'), 'Current'
								'\n' + '{:25}'.format('Name: ' + str(item.name)), 'Name:', player1.gear[1].name, 
								'\n' + '{:25}'.format('Defense: ' + str(item.dv)), 'Defense:', player1.gear[1].dv, 
								'\n' + '{:25}'.format('Block Chance: ' + str(item.dv*2)), 'Block Chance:', player1.gear[1].dv*2, 
								'\n')
						equipBool = input('Do you want to equip it? (Yes/No)').lower()
						if equipBool in ('yes', 'no'):
							correctInput = False
					if equipBool == 'Yes':
						player1.gear[1] = item
					break
		elif drop > 25 and drop <= 40:
			for item in lootList[2]:
					drop = random.randrange(0, 100)
					if drop <= item.dropChance:
						correctInput = True
						while correctInput:
							print('You\'ve found a ' + item.name,
								'\n{:25}'.format('New'), 'Current'
								'\n' + '{:25}'.format('Name: ' + str(item.name)), 'Name:', player1.gear[2].name, 
								'\n' + '{:25}'.format('Defense: ' + str(item.dv)), 'Defense:', player1.gear[2].dv, 
								'\n')
							equipBool = input('Do you want to equip it? (Yes/No)' ).lower()
							if equipBool in ('yes', 'no'):
								correctInput = False
						if equipBool == 'Yes':
							player1.gear[2] = item
						break
		elif drop > 40 and drop <= 70:
			for item in lootList[3]:
					drop = random.randrange(0, 100)
					if drop <= item.dropChance:
						print('You\'ve found a ' + str(item.name) + str(item.effect))
						try:
							player1.inventory[item] += 1
						except KeyError:
							player1.inventory[item] = 1
							break
		value = random.randrange(1, 10)
		player1.gold += value
		print('You\'ve found', value, 'gold, you now have a total of', player1.gold, 'gold!')
		
# Creates all items and enemies in the game.
if __name__ == '__main__':
	fist = weapon('Fists', 0, 5, 60, 0, 0, 'weapon')
	dagger = weapon('Dagger', 6, 3, 75, 5, 20, 'weapon')
	sword = weapon('Sword', 8, 2, 85, 25, 20, 'weapon')
	axe = weapon('Axe', 40, 1, 90, 20, 10, 'weapon')
	test = weapon('test', 1000, 1, 100, 0, 0, 'weapon')

	noShield = gear('None', 0, 0, 'shield')
	shieldWood = gear('Wooden Shield', 10, 20, 'shield')
	shieldIron = gear('Iron Shield', 15, 20, 'shield')

	armorCloth = gear('Cloth Armor', 5, 0, 'armor')
	armorLeather = gear('Leather Armor', 25, 20, 'armor')
	armorIron = gear('Iron Armor', 40, 20, 'armor')
	armorDiamond = gear('Diamond Armor', 50, 20, 'armor')
	
	#Fireball with burn effect deals 20 damage over 4 turn for 30 mp
	fireBall = spell('Fireball', 'Burn', 30, 20, 4, 20)

	healingPotion = potion('Healing Potion', 'HPPotion', ' (+50HP)', 50, 20)
	manaPotion = potion('Mana Potion', 'MPPotion', ' (+50MP)', 50, 20)

	weaponsList = [fist, dagger, sword, axe]
	shieldList = [noShield, shieldWood, shieldIron]
	armorList = [armorLeather, armorIron, armorDiamond]
	potionList = [healingPotion, manaPotion]
	lootList = [weaponsList, shieldList, armorList, potionList]

characterName = input('Enter the name for your champion: ').title()
clearPrevLine()

player1 = character(characterName, 1000, 500, 10, 5, 5, 25, 1, [sword, noShield, armorCloth])
player2 = character('Bandit', 100, 50, 10, 5, 5, 25, 3, [sword, shieldWood, armorLeather])
player1.spellList.append(fireBall)
enemyList = [player2]

playBool = True

# Keeps the game going until the player says no to keep playing
while playBool:
	combat().startFight(player1, player2)
	inputBool = True
	while inputBool:
		playBool = input('Keep playing (Yes/No) ').lower()
		if playBool in ('yes', 'no'):
			inputBool = False
	if playBool.lower() == 'no':
		playBool = False
	player2.hp = player2.maxhp
	
