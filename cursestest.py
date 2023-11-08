import curses
from curses import wrapper
import time
import random


longertext = open("longertext.txt", "r")
screen = curses.initscr()


def start_screen(stdscr):
	stdscr.clear()
	stdscr.addstr("Welcome to the Speed Typing Test!")
	stdscr.addstr(3,0, "\nType '1' for hardmode | Press any key for easy mode ")
	stdscr.refresh()
	stdscr.getkey(5,10)



def load_text(stdscr):

	global challenge
	challenge = stdscr.getkey()

	with open("text.txt", "r") as f:
					lines = f.readlines()
					return random.choice(lines).strip()


	'''
	#qus = screen.addstr("Type '1' for level 1, and '2' for level 2: ")
	while True:

			if qus =='1':
				with open("text.txt", "r") as f:
					lines = f.readlines()
					return random.choice(lines).strip()
					break
				
			elif qus =='2':
				with open('longertext.txt', 'r') as f:
					lines = f.readlines()
					return random.choice(lines).strip()	
					break
						
			else:
				stdscr.addstr("\nOnly input '1' or '2'")

	'''


global flag
flag = 0




def display_text(stdscr, target, current, wpm=0):
	stdscr.addstr(target)

	#if qus == '1':
	stdscr.addstr(1, 0, f"WPM: {wpm}")
	
	'''
	elif qus == '2':
		stdscr.addstr(5, 0, f"WPM: {wpm}")
	'''



	for i, char in enumerate(current):
		correct_char = target[i] 
		color = curses.color_pair(1)
		if char != correct_char:
			if challenge == '1':
				stdscr.clear()
				stdscr.addstr(5,0, "You made a mistake! (press the back key)")
			color = curses.color_pair(2)
			flag = 1

		stdscr.addstr(0, i, char, color)




def wpm_test(stdscr):
	screen = curses.initscr()
	target_text = load_text(stdscr)
	current_text = []
	wpm = 0
	start_time = time.time()
	stdscr.nodelay(True)

	while True:
		time_elapsed = max(time.time() - start_time, 1)
		wpm = round((len(current_text) / (time_elapsed / 60)) / 5)

		stdscr.clear()
		display_text(stdscr, target_text, current_text, wpm)
		stdscr.refresh()


		if challenge == '1':
			if "".join(current_text) == target_text:
				stdscr.nodelay(False)
				break
		else:
			if len(("".join(current_text))) == len(target_text):
				stdscr.nodelay(False)
				break

		try:
			key = stdscr.getkey()
		except:
			continue

		if ord(key) == 27:
			print("Ending game")
			break


		if key in ("KEY_BACKSPACE", '\b', "\x7f"):
			if len(current_text) > 0:
				current_text.pop()
		elif len(current_text) < len(target_text):
			current_text.append(key)


def main(stdscr):
	curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
	curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
	curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)

	start_screen(stdscr)
	while True:
		wpm_test(stdscr)
		stdscr.addstr(2, 0, "You completed the text! Press any key to continue.. ")
		key = stdscr.getkey()
		
		if ord(key) == 27:
			break

wrapper(main)