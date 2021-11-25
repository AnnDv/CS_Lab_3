from tkinter import *
from tkinter import filedialog
import json
from run_audit import check_audit
from enforce_all_audits import enforce_all_audits
from enforce_all_audits import rollback_audits

PATH = '/Users/anadvorac/Documents/FAF/anul3/security and criptografy/lab5/'
PATH_POLICIES = PATH + 'Audit Files/'

start_occurrences = []
end_occurrences = []

index_word = 0
custom_items_to_use = []
number_of_jsons = 0
to_json = {}
extension = ''
current_file = ''
audit_status = []

def save():
    global number_of_jsons
    global to_json
    global extension
    global PATH_POLICIES
    global PATH

    def check():
        global custom_items_to_use
        global number_of_jsons
        global to_json
        global extension
        global current_file
        global PATH_POLICIES
        global PATH

        custom_items_to_use = []
        for i in range(len(chkbuttons)):
            if var[i].get() == 1:
                custom_items_to_use.append(i)
        root_checkbox.destroy()
        if extension == 'audit':
            text_file = filedialog.asksaveasfilename(
                defaultextension = '.*',
                initialdir = PATH_POLICIES,
                title = 'Save File', filetypes = (('All Files', '*.*'), ))
        elif extension == 'json':
            text_file = current_file

        if text_file:
            # Update Status Bars
            name = text_file
            status_bar.config(text = f'{name}       ')
            name = name.replace(PATH_POLICIES, '')
            root.title(f'{name} - Dvorac Ana')

            to_print = []
            for i in custom_items_to_use:
                to_print.append(to_json[i])

            # Save the file
            text_file = open(text_file, 'w')
            json.dump(to_print, text_file, indent = 4)

            # Close the file
            text_file.close()

            if extension == 'json':
                new_file()
                text_file = current_file
                text_file = open(text_file, 'r')
                to_json = json.load(text_file)
                number_of_jsons = len(to_json)
                my_text.insert(END, json.dumps(to_json, indent = 4))
                text_file.close()

    def select_all_():

        for i in range(len(chkbuttons)):
            var[i].set(1)

    def deselect_all_():

        for i in range(len(chkbuttons)):
            var[i].set(0)

    root_checkbox = Tk()
    root_checkbox.title('Select custom item boxes')
    # root_checkbox.iconbitmap(PATH + 'icon.ico')
    sb = Scrollbar(root_checkbox, orient = 'vertical')
    text = Text(root_checkbox, width = 40, height = 20, yscrollcommand = sb.set)
    sb.config(command = text.yview)
    sb.pack(side = 'right', fill = 'y')
    var = []
    for i in range(number_of_jsons):
        var.append(IntVar(root_checkbox))
    text.pack(side = 'top', fill = 'both', expand = True)
    chkbuttons = [Checkbutton(root_checkbox, text="Custom Item Nr.%s" % i, variable = var[i], onvalue = 1, offvalue = 0)
                  for i in range(number_of_jsons)]
    for cb in chkbuttons:
        text.window_create('end', window = cb)
        text.insert('end', '\n')

    submit = Button(root_checkbox, text = 'Submit')
    submit.pack(side = BOTTOM)
    submit.config(command = check)

    select_all = Button(root_checkbox, text = 'Select All')
    select_all.pack(side = TOP)
    select_all.config(command = select_all_)

    deselect_all = Button(root_checkbox, text = 'Deselect All')
    deselect_all.pack(side = TOP)
    deselect_all.config(command = deselect_all_)

    root_checkbox.mainloop()


root = Tk()
root.title('Laboratory 5 - Dvorac Ana')
# root.iconbitmap(PATH + 'icon.ico')
root.geometry('1200x660')

# root window is the parent window
fram = Frame(root)
# adding of single line text box
Label(fram).pack(side = LEFT)
# adding of single line text box
edit = Entry(fram)
# positioning of text box
edit.pack(side = LEFT, fill = BOTH, expand = 1)
# setting focus
edit.focus_set()
# adding of search buttom
butt = Button(fram, text = 'Find')
butt.pack(side = RIGHT)
fram.pack(side = TOP)


#

# Create New File Function
def new_file():
    # Delete previous text
    my_text.delete('1.0', END)

    # Update status bars
    root.title('New File - Dvorac Ana')
    status_bar.config(text = 'New File       ')


def find_all(a_str, sub):
    start = 0
    while True:
        start = a_str.find(sub, start)
        if start == -1: return
        yield start
        start += len(sub)  # use start += 1 to find overlapping matches


# Open Files
def open_file():
    global number_of_jsons
    global to_json
    global extension
    global current_file
    global PATH
    global PATH_POLICIES

    # Delete previous text
    my_text.delete('1.0', END)

    # Grab  Filename
    text_file = filedialog.askopenfilename(
        initialdir = PATH_POLICIES,
        title = 'Open File', filetypes = (('All Files', '*.*'),))

    current_file = text_file

    # Update Status bars
    name = text_file
    status_bar.config(text = f'{name}       ')
    name = name.replace(PATH_POLICIES, '')
    root.title(f'{name} - Dvorac Ana')

    extension = ''
    i = len(name) - 1
    while name[i] != '.':
        extension += name[i]
        i -= 1
    extension = extension[::-1]

    # Open the file
    if extension == 'audit':
        text_file = open(text_file, 'r')
        contents = text_file.read()
        # with open(text_file, 'r') as f:
        #	print(1)
        #	contents = f.read()
        contents = contents.replace('            :', ':')
        contents = contents.replace('           :', ':')
        contents = contents.replace('          :', ':')
        contents = contents.replace('         :', ':')
        contents = contents.replace('        :', ':')
        contents = contents.replace('       :', ':')
        contents = contents.replace('      :', ':')
        contents = contents.replace('     :', ':')
        contents = contents.replace('    :', ':')
        contents = contents.replace('   :', ':')
        contents = contents.replace('  :', ':')
        contents = contents.replace(' :', ':')

        # print(contents)

        start = list(find_all(contents, '<custom_item>'))
        ending = list(find_all(contents, '</custom_item>'))

        custom_item = {}

        custom_item['CMD_EXEC'] = {'type': [], 'description': [], 'cmd': [], 'expect': []}
        custom_item['MACOSX_DEFAULTS_READ'] = {'type': [], 'description': [], 'regex': [], 'plist_item': [],
                                               'plist_name ': [], 'plist_option': []}
        custom_item['FILE_CONTENT_CHECK'] = {'type': [], 'description': []}
        custom_item['FILE_CONTENT'] = {'type': [], 'description': []}
        custom_item['FILE_CONTENT_CHECK_NOT'] = {'type': [], 'description': []}
        custom_item['BANNER_CHECK'] = {'type': [], 'description': []}

        general_custom_item = {}
        general_custom_item_keys = []

        for key in custom_item:
            keys_list = list(custom_item[key])
            for key_x in keys_list:
                if key_x not in general_custom_item_keys:
                    general_custom_item_keys.append(key_x)

        general_custom_item['serial_number_custom_item'] = []

        for key in general_custom_item_keys:
            general_custom_item[key] = []

        general_custom_item['info'] = []
        general_custom_item['reference'] = []
        general_custom_item['solution'] = []
        general_custom_item['see_also'] = []

        for i in range(len(start)):
            content_type_block = contents[start[i] + 13: ending[i]]
            general_custom_item['serial_number_custom_item'].append(i)
            for element in list(general_custom_item.keys()):
                length_of_element = len(element) + 1
                if content_type_block.find(element) != -1:
                    general_custom_item[element].append(content_type_block[content_type_block.find(element + ':') + length_of_element: content_type_block[content_type_block.find(element + ':') + length_of_element :].find('\n') + content_type_block.find(element + ':') + length_of_element ].strip())
                else:
                    if element != 'serial_number_custom_item':
                        general_custom_item[element].append('')

        number_of_jsons = len(general_custom_item['serial_number_custom_item'])

        to_json = []
        for i in range(len(general_custom_item['type'])):
            to_print = {}
            for element in list(general_custom_item.keys()):
                if general_custom_item[element][i] != '':
                    to_print[element] = general_custom_item[element][i]
            to_json.append(to_print)

        my_text.insert(END, json.dumps(to_json, indent = 4))

        # Close the opened file
        text_file.close()

    elif extension == 'json' or extension == 'txt':

        text_file = open(text_file, 'r')
        to_json = json.load(text_file)
        number_of_jsons = len(to_json)
        my_text.insert(END, json.dumps(to_json, indent = 4))
        text_file.close()


# Save As File
def save_as_file():
    global number_of_jsons
    global to_json
    global extension
    global PATH_POLICIES
    global PATH

    def check():
        global custom_items_to_use
        global number_of_jsons
        global to_json
        global extension
        global current_file

        custom_items_to_use = []
        for i in range(len(chkbuttons)):
            if var[i].get() == 1:
                custom_items_to_use.append(i)
        root_checkbox.destroy()

        text_file = filedialog.asksaveasfilename(
            defaultextension = '.*',
            initialdir = PATH_POLICIES,
            title = 'Save File', filetypes = (('All Files', '*.*'),))

        if text_file:
            # Update Status Bars
            name = text_file
            status_bar.config(text = f'{name}       ')
            name = name.replace(PATH_POLICIES, '')
            root.title(f'{name} - Dvorac Ana')

            to_print = []
            for i in custom_items_to_use:
                to_print.append(to_json[i])

            # Save the file
            text_file = open(text_file, 'w')
            json.dump(to_print, text_file, indent = 4)

            # Close the file
            text_file.close()

    def select_all_():

        for i in range(len(chkbuttons)):
            var[i].set(1)

    def deselect_all_():

        for i in range(len(chkbuttons)):
            var[i].set(0)

    root_checkbox = Tk()
    root_checkbox.title('Select custom item boxes')
    # root_checkbox.iconbitmap(PATH + 'icon.ico')
    sb = Scrollbar(root_checkbox, orient = 'vertical')
    text = Text(root_checkbox, width = 40, height = 20, yscrollcommand = sb.set)
    sb.config(command = text.yview)
    sb.pack(side = 'right', fill = 'y')
    var = []
    for i in range(number_of_jsons):
        var.append(IntVar(root_checkbox))
    text.pack(side = 'top', fill = 'both', expand = True)
    chkbuttons = [Checkbutton(root_checkbox, text="Custom Item Nr.%s" % i, variable = var[i], onvalue = 1, offvalue = 0)
                  for i in range(number_of_jsons)]
    for cb in chkbuttons:
        text.window_create('end', window = cb)
        text.insert('end', '\n')

    submit = Button(root_checkbox, text = 'Submit')
    submit.pack(side = BOTTOM)
    submit.config(command = check)

    select_all = Button(root_checkbox, text = 'Select All')
    select_all.pack(side = TOP)
    select_all.config(command = select_all_)

    deselect_all = Button(root_checkbox, text = 'Deselect All')
    deselect_all.pack(side = TOP)
    deselect_all.config(command = deselect_all_)

    root_checkbox.mainloop()


def r_audit():
    global PATH
    global PATH_POLICIES
    global audit_status

    text_file = 'output.json'
    name = 'output.json'
    root.title(f'{name} - Dvorac Ana')
    text_file = open(text_file, 'w')
    text_file.write(my_text.get(1.0, END))

    text_file.close()

    check_audit()

    new_file()

    text_file = 'audit_result.txt'
    text_file = open(text_file, 'r')
    my_text.insert(END, text_file.read())

def enforce_audit():
	global PATH
	global PATH_POLICIES

	text_file = 'to_enforce_audits.json'
	name = 'to_enforce_audits.json'
	root.title(f'{name} - Dvorac Ana')
	text_file = open(text_file, 'w')
	text_file.write(my_text.get(1.0, END))

	text_file.close()

	enforce_all_audits()

	new_file()

	my_text.insert(END, 'DONE! Rerun Run Audit option to check the status!')

def rollback():
	global PATH
	global PATH_POLICIES
	global audit_status

	text_file = 'to_enforce_audits.json'
	name = 'to_enforce_audits.json'
	root.title(f'{name} - Dvorac Ana')
	text_file = open(text_file, 'w')
	text_file.write(my_text.get(1.0, END))

	text_file.close()

	rollback_audits()
	
	new_file()

	my_text.insert(END, 'DONE! Rerun Run Audit option to check the status!')


def export():
    global number_of_jsons
    global to_json
    global extension
    global PATH_POLICIES
    global PATH

    def check():
        global custom_items_to_use
        global number_of_jsons
        global to_json
        global extension
        global current_file
        global PATH_POLICIES
        global PATH

        custom_items_to_use = []
        for i in range(len(chkbuttons)):
            if var[i].get() == 1:
                custom_items_to_use.append(i)
        root_checkbox.destroy()

        text_file = filedialog.asksaveasfilename(
            defaultextension = '.*',
            initialdir = PATH_POLICIES,
            title = 'Save File', filetypes = (('All Files', '*.*'),))

        if text_file:
            # Update Status Bars
            name = text_file
            status_bar.config(text = f'{name}       ')
            name = name.replace(PATH_POLICIES, '')
            root.title(f'{name} - Dvorac Ana')

            text_file = open(text_file, 'w')

            to_print = []
            for i in custom_items_to_use:
                text_file.write('<custom_item>\n')
                for j in to_json[i]:
                    # print('\t' + j + ' : ' + str(to_json[i][j]) + '\n')
                    text_file.write('\t' + j + ' : ' + str(to_json[i][j]) + '\n')
                text_file.write('</custom_item>\n')

            # Close the file
            text_file.close()

    def select_all_():

        for i in range(len(chkbuttons)):
            var[i].set(1)

    def deselect_all_():

        for i in range(len(chkbuttons)):
            var[i].set(0)

    root_checkbox = Tk()
    root_checkbox.title('Select custom item boxes')
    # root_checkbox.iconbitmap(PATH + 'icon.ico')
    sb = Scrollbar(root_checkbox, orient = 'vertical')
    text = Text(root_checkbox, width = 40, height = 20, yscrollcommand = sb.set)
    sb.config(command = text.yview)
    sb.pack(side = 'right', fill = 'y')
    var = []
    for i in range(number_of_jsons):
        var.append(IntVar(root_checkbox))
    text.pack(side = 'top', fill = 'both', expand = True)
    chkbuttons = [Checkbutton(root_checkbox, text="Custom Item Nr.%s" % i, variable = var[i], onvalue = 1, offvalue = 0)
                  for i in range(number_of_jsons)]
    for cb in chkbuttons:
        text.window_create('end', window = cb)
        text.insert('end', '\n')

    submit = Button(root_checkbox, text = 'Submit')
    submit.pack(side = BOTTOM)
    submit.config(command = check)

    select_all = Button(root_checkbox, text = 'Select All')
    select_all.pack(side = TOP)
    select_all.config(command = select_all_)

    deselect_all = Button(root_checkbox, text = 'Deselect All')
    deselect_all.pack(side = TOP)
    deselect_all.config(command = deselect_all_)

    root_checkbox.mainloop()


def find():
    global start_occurrences
    global end_occurrences
    global index_word

    start_occurrences = []
    end_occurrences = []
    index_word = 0

    my_text.tag_remove('found', '1.0', END)

    s = edit.get()

    if s:
        idx = '1.0'
        while 1:
            idx = my_text.search(s, idx, nocase=1,
                                 stopindex=END)
            if not idx: break

            start_occurrences.append(idx)

            lastidx = '%s+%dc' % (idx, len(s))
            end_occurrences.append(lastidx)

            idx = lastidx

        next_word()


def next_word():
    global index_word
    global start_occurrences
    global end_occurrences

    if index_word < len(start_occurrences):
        my_text.tag_remove('found', '1.0', END)
        idx = start_occurrences[index_word]
        lastidx = end_occurrences[index_word]
        my_text.tag_add('found', idx, lastidx)
        to_see = int(idx[0:idx.find('.')])
        my_text.yview(to_see - 10)
        if index_word < (len(start_occurrences) - 1):
            index_word += 1
        my_text.tag_config('found', foreground='black', background = 'red')


def back_word():
    global index_word
    global start_occurrences
    global end_occurrences

    if index_word >= 0:
        my_text.tag_remove('found', '1.0', END)
        idx = start_occurrences[index_word]
        lastidx = end_occurrences[index_word]
        my_text.tag_add('found', idx, lastidx)
        to_see = int(idx[0:idx.find('.')])
        my_text.yview(to_see - 10)
        if (index_word > 0):
            index_word -= 1
        my_text.tag_config('found', foreground='black', background = 'red')


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
file_menu.add_command(label = 'Open', command = open_file)
file_menu.add_command(label = 'Save', command = save)
file_menu.add_command(label = 'Save As', command = save_as_file)
file_menu.add_command(label = 'Export', command = export)
file_menu.add_command(label = 'Run Audit', command = r_audit)
file_menu.add_command(label = 'Enforce Audit', command = enforce_audit)
file_menu.add_command(label = 'Rollback', command = rollback)
file_menu.add_separator()
file_menu.add_command(label = 'Exit', command = root.quit)

back_btn = Button(fram, text = 'Back')
back_btn.pack(side = RIGHT)

next_btn = Button(fram, text = 'Next')
next_btn.pack(side = RIGHT)

next_btn.config(command = next_word)
back_btn.config(command = back_word)
butt.config(command=find)

# Add Status Bar to Bottom
status_bar = Label(root, text = 'Ready     ', anchor = E)
status_bar.pack(fill = X, side = BOTTOM, ipady = 5)
root.mainloop()