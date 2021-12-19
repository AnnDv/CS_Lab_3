from tkinter import *
from tkinter import filedialog
from tkinter import font
import json
from os import listdir
from os.path import isfile, join
from functools import partial
from read_database import is_correct_log_in
from read_database import read_data

root = Tk()
root.title('Laboratory 7 - Dvorac Ana')
root.geometry('1200x660')

is_logged_in = False

username_x = StringVar()
password_y = StringVar()

# Create New File Function
def new_file():
	# Delete previous text
	my_text.delete('1.0', END)
	
	# Update status bars 
	root.title('New File - Dvorac Ana')
	status_bar.config(text = 'New File       ')


def exit_db():
	global username_x
	global password_y
	global is_logged_in

	username_x = ''
	password_y = ''
	is_logged_in = False

	my_text.delete('1.0', END)


def connect():
	global username_x
	global password_y
	global is_logged_in

	def validateLogin(username, password):

		global username_x
		global password_y
		global is_logged_in

		username_x =  username.get()
		password_y =  password.get()
		
		is_logged_in = is_correct_log_in(username_x, password_y)

		connect_window.destroy()
		return

	def logout():

		global username_x
		global password_y
		global is_logged_in

		username_x =  ''
		password_y =  ''
		
		is_logged_in = False

		my_text.delete('1.0', END)

		connect_window.destroy()
		return

	def okey():
		
		connect_window.destroy()

		return




	#connect_window = Tk()
	#connect_window.title('Sign In to Database')

	if is_logged_in == False:
	
		connect_window = Tk()
		connect_window.title('Sign In to Database')

		username_label = Label(connect_window, text = 'Username:').grid(row = 0, column = 0)
		username = StringVar(connect_window)
		username_entry = Entry(connect_window, textvariable = username, width = 50).grid(row = 0, column = 1)


		password_label = Label(connect_window, text = 'Password:').grid(row = 1, column = 0)
		password = StringVar(connect_window)
		password_entry = Entry(connect_window, textvariable = password, width = 50, show = '*').grid(row = 1, column = 1)


		validateLogin = partial(validateLogin, username, password)

		submit = Button(connect_window, text = 'Submit' ,command = validateLogin).grid(row = 4, column = 0)
	
		connect_window.mainloop()

	else:
		connect_window = Tk()
		connect_window.title('Sign In to Database')

		no_label = Label(connect_window, text = 'You are logged in!').grid(row = 0, column = 0)
		
		okey = partial(okey)

		ok = Button(connect_window, text = 'Ok', command = okey).grid(row = 1, column = 0)

		logout = partial(logout)

		log_out = Button(connect_window, text = 'Log out', command = logout).grid(row = 1, column = 1)


		connect_window.mainloop()


def view_data():
	global username_x
	global password_y
	global is_logged_in

	if is_logged_in: 
		nr_persons, list_persons = read_data(username_x, password_y)
		
		#print(nr_persons)
		
		#for person in list_persons:
		#	print(person, end = '\n')

		my_text.delete('1.0', END)
		for person in list_persons:
			my_text.insert(END, json.dumps(person, indent = 4))
	
	else:
		connect()



# Create Main Frame
my_frame = Frame(root)
my_frame.pack(pady = 5)

# Create out Scollbar For the Text Box
text_scroll = Scrollbar(my_frame)
text_scroll.pack(side = RIGHT, fill = Y)

# Create Text Box
my_text = Text(my_frame, width = 97, height = 25,
			 font = ('Helvetica', 16), selectbackground = 'yellow',
			 selectforeground = 'black', undo = True,
			 yscrollcommand = text_scroll.set)
my_text.pack()

# Configure out Scrollbar
text_scroll.config(command = my_text.yview)

# Create Menu
my_menu = Menu(root)
root.config(menu = my_menu)

# Add File Menu
file_menu = Menu(my_menu, tearoff = False)
my_menu.add_cascade(label = 'File', menu = file_menu)
file_menu.add_command(label = 'New', command = new_file)
file_menu.add_command(label = 'Connect to Database', command = connect)
file_menu.add_command(label = 'View data', command = view_data)
file_menu.add_command(label = 'Log out', command = exit_db)
file_menu.add_separator()
file_menu.add_command(label = 'Exit', command = root.quit)

# Add Status Bar to Bottom
status_bar = Label(root, text = 'Ready     ', anchor = E)
status_bar.pack(fill = X, side = BOTTOM, ipady = 5)
root.mainloop()