import random

word_list = [
    "Apple", "Banana", "Cat", "Dog", "Elephant", "Friend", "Happy", "Jump", "Kind", "Laugh", 
    "Mountain", "Nature", "Orange", "Play", "Quick", "Rainbow", "Sun", "Tree", "Umbrella", "Visit",
    "Water", "Xylophone", "Yellow", "Zoo", "Ball", "Book", "Cup", "Dance", "Egg", "Fish",
    "Garden", "Hat", "Ice", "Jump", "Kite", "Lemon", "Moon", "Nest", "Ocean", "Puzzle",
    "Quiet", "Robot", "Star", "Train", "Umbrella", "Volcano", "Wagon", "X-ray", "Yawn", "Zigzag",
    "Bear", "Cake", "Duck", "Fish", "Grass", "Horse", "Island", "Jelly", "Kite", "Lemon",
    "Mango", "Nest", "Ocean", "Piano", "Quilt", "Rain", "Snow", "Tiger", "Umbrella", "Valley",
    "Wave", "Xylophone", "Yellow", "Zebra", "Lamp", "Milk", "Nose", "Owl", "Pencil", "Queen",
    "Robot", "Sun", "Tree", "Umbrella", "Violin", "Wagon", "X-ray", "Yo-yo", "Zigzag"]

randomnum = random.randint(0,99)
word = word_list[randomnum]
lenght = len(word)
word_list = list(word)
guess_list = []

for  i in word:guess_list.append("_")
print(word)
x = 10
while x !=  0:
	guess_word = ''.join(guess_list)
	print("You have a total of ",x," tries.    ",guess_word)
	alphabet = input("\nEnter a alphabat to guess ")
	z = 0
	while z != lenght:
		if alphabet == word_list[z]:
			guess_list[z] = word_list[z]
		z = z+1
	x = x-1

guessed_word = ''.join(guess_list)
if word == guessed_word:
	print("You won!!! The word was ", word)
else:
	print("You lost. The word was ", word)
