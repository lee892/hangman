import pygame
import json
import requests


def get_word():	
	response = requests.get("https://api.wordnik.com/v4/words.json/randomWord?hasDictionaryDef=true&maxCorpusCount=-1&minDictionaryCount=1&maxDictionaryCount=-1&minLength=5&maxLength=-1&api_key=owwfe5vft3yt6pa70tg1sa02isyv2ar4sbgpt0d4oq4vrd8tv")
	word = response.json()['word']
	print(word)
	return word

class Hangman:
	def __init__(self, word):
		pygame.init()
		self.screen = pygame.display.set_mode((1000, 700))
		self.screen.fill((255, 255, 255))
		self.win = False
		self.word = word.lower()
		self.word_length = len(word)
		self.guessed_word_length = 0
		self.man_state = 0
		self.letters = []
		#Letter positions
		self.x_start = 30
		self.y_start = 30
		self.draw_hangstand()
		self.draw_letters()
		self.show_spaces(self.word)

	def draw_hangstand(self):
		hangstand = pygame.image.load('images/hang-stand.png')
		self.screen.blit(hangstand, (200, 150))

	def draw_letters(self):
		x_start = self.x_start
		y_start = self.y_start
		letter_width = 49
		letter_height = 40
		letter_gap = 60
		for letter in range(97, 123):
			character = chr(letter)
			self.screen.blit(pygame.image.load(f'images/{character}.png'), (x_start, y_start))
			self.letters.append((pygame.Rect(x_start, y_start, letter_width, letter_height), letter))
			if letter == 112:
				y_start += letter_gap
				x_start = 30
			else:
				x_start += letter_gap

	def show_spaces(self, word):
		space = pygame.image.load('images/space.png')
		x_start = self.x_start
		y_start = 600
		letter_gap = 60

		for letter in word:
			if letter != ' ':
				self.screen.blit(space, (x_start, y_start))
			else:
				x_start += 10
				self.guessed_word_length += 1
			if x_start + 120 > 1000:
				y_start += letter_gap
				x_start = 30
			else:
				x_start += letter_gap

	def letter_handler(self, event):
		if event.type == pygame.MOUSEBUTTONUP:
			mouse_pos = pygame.mouse.get_pos()

			for letter_rect, letter in self.letters:
				if self.man_state != 9:
					if letter_rect.collidepoint(mouse_pos):
						self.add_letter(letter)
						self.check_win()

	def add_letter(self, letter):
		x_start = 30
		y_start = 560
		letter_gap = 60
		clicked_letter = chr(letter)
		letter_in_word = False
		for character in self.word:
			if character == ' ':
				x_start += 10
			if clicked_letter == character:
				letter_in_word = True
				self.guessed_word_length += 1
				self.screen.blit(pygame.image.load(f'images./{clicked_letter}.png'), (x_start, y_start))
			if x_start + 120 > 1000:
				y_start += letter_gap
				x_start = 30
				continue
			x_start += letter_gap
		if letter_in_word == False:
			self.add_body_part()

	def add_body_part(self):
		self.man_state += 1
		man_part = pygame.image.load(f'images/man_{self.man_state}.png')
		self.screen.blit(man_part, (545, 195))

	def check_win(self):
		if self.guessed_word_length == self.word_length:
			self.win = True
			print("You Win!")
		elif self.man_state == 9:
			print("You lose, reload to try again")


hangman = Hangman(get_word())
	

running = True
#Game loop
while running:

	events = pygame.event.get()
	for event in events:
		if event.type == pygame.QUIT:
			running = False
		hangman.letter_handler(event)
		if hangman.win:
			hangman = Hangman(get_word())
	

	pygame.display.update()
