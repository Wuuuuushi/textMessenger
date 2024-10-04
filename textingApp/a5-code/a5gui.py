import tkinter as tk
from tkinter import ttk, filedialog
from datetime import datetime
from pathlib import Path
import time
from Profile import Profile
import ds_messenger


class Body(tk.Frame):
    '''Construct a frame widget with the parent MASTER.'''
    def __init__(self, root, recipient_selected_callback=None):
        tk.Frame.__init__(self, root)
        self.root = root
        self._contacts = [str]
        self._select_callback = recipient_selected_callback
        # After all initialization is complete,
        # call the _draw method to pack the widgets
        # into the Body instance
        self._draw()

    def node_select(self, event):
        '''Selects the body that you are on'''
        index = int(self.posts_tree.selection()[0])
        entry = self._contacts[index]
        if self._select_callback is not None:
            self._select_callback(entry)

    def insert_contact(self, contact: str):
        '''Puts in a contact into the contact tree'''
        if contact not in self._contacts:
            self._contacts.append(contact)
            id = len(self._contacts) - 1
            self._insert_contact_tree(id, contact)
        else:
            pass

    def _insert_contact_tree(self, id, contact: str):
        '''Creates a list using the insert_contact'''
        if contact != None and contact != ' ':
            if len(contact) > 25:
                entry = contact[:24] + "..."
            id = self.posts_tree.insert('', id, id, text=contact)
        else:
            pass

    def insert_user_message(self, message:str):
        '''Inserts the message into the message tree'''
        self.entry_editor.insert(1.0, message + '\n', 'entry-right')
        self.set_text_entry('')

    def insert_contact_message(self, message:str):
        '''Inserts the contact message into the tree'''
        self.entry_editor.insert(1.0, message + '\n', 'entry-left')

    def get_text_entry(self) -> str:
        '''Gets the text entry in the send message box'''
        return self.message_editor.get('1.0', 'end').rstrip()

    def set_text_entry(self, text:str):
        '''Resets the text entry in the send message box'''
        self.message_editor.delete(1.0, tk.END)
        self.message_editor.insert(1.0, text)

    def _draw(self):
        '''Draws the main body work for the send message and recieve message tree'''
        posts_frame = tk.Frame(master=self, width=450, bg = 'green')
        posts_frame.pack(fill=tk.BOTH, side=tk.LEFT)

        self.posts_tree = ttk.Treeview(posts_frame)
        self.posts_tree.bind("<<TreeviewSelect>>", self.node_select)
        self.posts_tree.pack(fill=tk.BOTH, side=tk.TOP,
                             expand=True, padx=5, pady=5)

        entry_frame = tk.Frame(master=self, bg="green")
        entry_frame.pack(fill=tk.BOTH, side=tk.TOP, expand=True)

        editor_frame = tk.Frame(master=entry_frame, bg="red")
        editor_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

        scroll_frame = tk.Frame(master=entry_frame, bg="blue", width=10)
        scroll_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=False)

        message_frame = tk.Frame(master=self, bg="yellow")
        message_frame.pack(fill=tk.BOTH, side=tk.TOP, expand=False)

        self.message_editor = tk.Text(message_frame, width=0, height=5)
        self.message_editor.pack(fill=tk.BOTH, side=tk.LEFT,
                                 expand=True, padx=0, pady=0)

        self.entry_editor = tk.Text(editor_frame, width=0, height=5, bg = 'black')
        self.entry_editor.tag_configure('entry-right', justify='right')
        self.entry_editor.tag_configure('entry-left', justify='left')
        self.entry_editor.pack(fill=tk.BOTH, side=tk.LEFT,
                               expand=True, padx=0, pady=0)

        entry_editor_scrollbar = tk.Scrollbar(master=scroll_frame,
                                              command=self.entry_editor.yview)
        self.entry_editor['yscrollcommand'] = entry_editor_scrollbar.set
        entry_editor_scrollbar.pack(fill=tk.Y, side=tk.LEFT,
                                    expand=False, padx=0, pady=0)


class Footer(tk.Frame):
    '''Frame widget which may contain other widgets and can have a 3D border.
    Construct a frame widget with the parent MASTER.'''
    def __init__(self, root, send_callback=None):
        tk.Frame.__init__(self, root)
        self.root = root
        self._send_callback = send_callback
        self._draw()

    def send_click(self):
        '''Recieve mouse click and sends callback()'''
        if self._send_callback is not None:
            self._send_callback()

    def _draw(self):
        '''Creates a visual send button'''
        save_button = tk.Button(master=self, text="Send", width=20, command = self.send_click, fg = 'green')
        # You must implement this.
        # Here you must configure the button to bind its click to
        # the send_click() function.
        save_button.pack(fill=tk.BOTH, side=tk.RIGHT, padx=5, pady=5)

        self.footer_label = tk.Label(master=self, text="Ready.")
        self.footer_label.pack(fill=tk.BOTH, side=tk.LEFT, padx=5)


class NewContactDialog(tk.simpledialog.Dialog):
    '''Initalizes the account that the user wants to use'''
    def __init__(self, root, title=None, user=None, pwd=None, server=None):
        self.root = root
        self.server = server
        self.user = user
        self.pwd = pwd
        super().__init__(root, title)

    def body(self, frame):
        '''Creates the window that will show where to put the user info'''
        self.server_label = tk.Label(frame, width=30, text="DS Server Address")
        self.server_label.pack()
        self.server_entry = tk.Entry(frame, width=30)
        #self.server_entry.insert(tk.END, self.server)
        self.server_entry.pack()

        self.username_label = tk.Label(frame, width=30, text="Username")
        self.username_label.pack()
        self.username_entry = tk.Entry(frame, width=30)
        #self.username_entry.insert(tk.END, self.user)
        self.username_entry.pack()

        # You need to implement also the region for the user to enter
        # the Password. The code is similar to the Username you see above
        # but you will want to add self.password_entry['show'] = '*'
        # such that when the user types, the only thing that appears are
        # * symbols.
        #self.password...

        self.password_label = tk.Label(frame, width=30, text="Password")
        self.password_label.pack()
        self.password_entry = tk.Entry(frame, width=30)
        #self.password_entry.insert(tk.END, self.pwd)
        self.password_entry.pack()
        self.password_entry['show'] = '*'

    def apply(self):
        '''Sets the username, password, and dsuserver'''
        self.user = self.username_entry.get()
        self.pwd = self.password_entry.get()
        self.server = self.server_entry.get()



class MainApp(tk.Frame):
    '''Main funciton that will store the information and find new contact'''
    def __init__(self, root):
        tk.Frame.__init__(self, root)
        self.root = root
        self.username = None
        self.password = None
        self.server = '168.235.86.101'
        self.recipient = None
        self.file = None
        self.profile = None
        # You must implement this! You must configure and
        # instantiate your DirectMessenger instance after this line.
        #self.direct_messenger = ... continue!
        self.direct_messenger = ds_messenger.DirectMessenger()
        self.direct_messenger.username = self.username
        self.direct_messenger.password = self.password
        self.direct_messenger.server = self.server
        # After all initialization is complete,
        # call the _draw method to pack the widgets
        # into the root frame
        self._draw()


    def send_message(self):
        '''Sends the message to the contact and saves it into a profile'''
        # You must implement this!
        if self.direct_messenger.send(self.body.get_text_entry(), self.recipient) == True:
            save_dict = {'recipient': self.recipient, 'message':self.body.get_text_entry(), 'timestamp':time.time()}
            self.profile.add_my_messages(save_dict)
            self.profile.save_profile(self.file)
            self.publish(self.body.get_text_entry())


    def add_contact(self):
        '''Adds the contact to the contact list'''
        # You must implement this!
        # Hint: check how to use tk.simpledialog.askstring to retrieve
        # the name of the new contact, and then use one of the body
        # methods to add the contact to your contact list
        x = tk.simpledialog.askstring('Add Contact', 'Username')
        if x == '':
            pass
        else:
            return self.body.insert_contact(x)

    def open_file(self):
        '''Opens a file in the folder and uploads previous messages'''
        self.file = filedialog.askopenfilename(title = "Open",filetypes = [("All files", ".dsu")])
        if self.file != None and self.file != '':
            p = Profile()
            p.load_profile(self.file)
            self.profile = p
            self.username = p.username
            self.password = p.password
            for values in self.profile.messages:
                if values['recipient'] not in self.body._contacts:
                    if values['recipient'] != self.username:
                        self.body.insert_contact(values['recipient'])
            for my_values in self.profile.my_messages:
                if my_values['recipient'] not in self.body._contacts:
                    if my_values['recipient'] != self.username:
                        self.body.insert_contact(my_values['recipient'])
            self.direct_messenger.username = self.username
            self.direct_messenger.password = self.password
        else:
            pass

    def create_file(self):
        '''Creates a new file that will stores the
        messages that you sent to other people'''
        file_name = tk.simpledialog.askstring('New', 'Enter Filename (Cancel to Open File)')
        if file_name != None and file_name != "":
            file_location = tk.filedialog.askdirectory()
            file_name = file_name + '.dsu'
            Path(file_location, (file_name)).touch()
            self.file  = file_location + f"/{file_name}"
        else:
            pass

    def time_convertor(self, time:str):
        '''Converts the Epoch time into UTC time'''
        return str(datetime.fromtimestamp(float(time)).strftime('%H:%M:%S'))

    def recipient_selected(self, recipient):
        '''Sets the recipient variable based off of
        the contact taht the user clicked on'''
        self.recipient = recipient
        self.body.entry_editor.delete('1.0', 'end')
        recieve_list = []
        send_list = []
        if self.profile.messages != []:
            for values in self.profile.messages:
                if values['recipient'] == self.recipient:
                    recieve_list.append(values)
            for values in self.profile.my_messages:
                if values['recipient'] == self.recipient:
                    send_list.append(values)
            if len(recieve_list) > len(send_list):
                for values in recieve_list:
                    if send_list != []:
                        try:
                            if float(values['timestamp']) < float(send_list[0]['timestamp']):
                                self.body.insert_contact_message(values['message'])
                                self.body.insert_contact_message(values['recipient'] + ':')
                            while float(send_list[0]['timestamp']) < float(values['timestamp']):
                                self.body.insert_user_message(send_list[0]['message'])
                                send_list.remove(send_list[0])
                        except IndexError:
                            pass
                            
                    else:
                        self.body.insert_contact_message(values['message'])
                        self.body.insert_contact_message(values['recipient'] + ':')
            elif len(recieve_list) == len(send_list):
                for values in recieve_list:
                    if send_list != []:
                        try:
                            if float(values['timestamp']) < float(send_list[0]['timestamp']):
                                self.body.insert_contact_message(values['message'])
                                self.body.insert_contact_message(values['recipient'] + ':')
                            while float(send_list[0]['timestamp']) < float(values['timestamp']):
                                self.body.insert_user_message(send_list[0]['message'])
                                send_list.remove(send_list[0])
                        except IndexError:
                            pass
                    else:
                        self.body.insert_contact_message(values['message'])
                        self.body.insert_contact_message(values['recipient'] + ':')
            else:
                for values in send_list:
                    if recieve_list != []:
                        try:
                            if float(values['timestamp']) < float(recieve_list[0]['timestamp']):
                                self.body.insert_user_message(values['message'])
                            while float(values['timestamp']) > float(recieve_list[0]['timestamp']) and recieve_list != []:
                                self.body.insert_contact_message(recieve_list[0]['message'])
                                self.body.insert_contact_message(values['recipient'] + ':')
                                recieve_list.remove(recieve_list[0])
                        except IndexError:
                            pass
                    else:
                        self.body.insert_user_message(values['message'])
        else:
            for my_values in self.profile.my_messages:
                if my_values['recipient'] == self.recipient:
                    self.body.insert_user_message(my_values['message'])

    def configure_server(self):
        '''Sets the username, password, and server'''
        try:
            ud = NewContactDialog(self.root, "Configure Account",
                                  self.username, self.password, self.server)
            self.create_file()
            p = Profile()
            self.profile = p
            self.username = ud.user
            self.password = ud.pwd
            self.server = ud.server
            # You must implement this!
            # You must configure and instantiate your
            # DirectMessenger instance after this line
            p.username = self.username
            p.password = self.password
            p.dsuserver = self.server
            self.direct_messenger.username = self.username
            self.direct_messenger.password = self.password
            self.direct_messenger.server = self.server
            p.save_profile(self.file)
            self.upload_old()
        except (TypeError, KeyError):
            pass

    def upload_old(self):
        '''Uploads old info from the server to the profile'''
        x = self.direct_messenger.retrieve_all()
        i = 0
        for values in x:
            save_dict = {'recipient': values.recipient[i], 'message':values.message[i], 'timestamp':values.timestamp[i]}
            self.profile.add_message(save_dict)
            self.profile.save_profile(self.file)
            if values.recipient[0] not in self.body._contacts:
                self.body.insert_contact(values.recipient[0])
            if self.recipient == values.recipient[0]:
                self.body.insert_contact_message(values.message[0])
            i += 1

    def publish(self, message:str):
        '''Puts the message into the main body work'''
        # You must implement this!
        self.body.insert_user_message(message)
        pass

    def check_new(self):
        '''Checks for new messages that other users send you'''
        try:
            x = self.direct_messenger.retrieve_new()
            for values in x:
                save_dict = {'recipient': values.recipient[0], 'message':values.message[0], 'timestamp':values.timestamp[0]}
                self.profile.add_message(save_dict)
                self.profile.save_profile(self.file)
                if values.recipient[0] not in self.body._contacts:
                    self.body.insert_contact(values.recipient[0])
                if self.recipient == values.recipient[0]:
                    self.body.insert_contact_message(values.message[0])
                    self.body.insert_contact_message(values.recipient[0] + ':')
        except KeyError:
            pass
        self.after(1000, self.check_new)

    def _draw(self):
        '''Draws the menu for changing the settings,
        opening files and creating new files'''
        # Build a menu and add it to the root frame.
        menu_bar = tk.Menu(self.root)
        self.root['menu'] = menu_bar
        menu_file = tk.Menu(menu_bar)

        menu_bar.add_cascade(menu=menu_file, label='File')
        menu_file.add_command(label='New', command = self.configure_server)
        menu_file.add_command(label='Open...', command = self.open_file)
        menu_file.add_command(label='Close', command = quit)

        settings_file = tk.Menu(menu_bar)
        menu_bar.add_cascade(menu=settings_file, label='Settings')
        settings_file.add_command(label='Add Contact',
                                  command=self.add_contact)
        settings_file.add_command(label='Configure DS Server',
                                  command=self.configure_server)

        # The Body and Footer classes must be initialized and
        # packed into the root window.
        self.body = Body(self.root,
                         recipient_selected_callback=self.recipient_selected)
        self.body.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
        self.footer = Footer(self.root, send_callback = self.send_message)
        self.footer.pack(fill=tk.BOTH, side=tk.BOTTOM)
def main():
    '''Main function that is set to run'''
    # All Tkinter programs start with a root window. We will name ours 'main'.
    main = tk.Tk()

    # 'title' assigns a text value to the Title Bar area of a window.
    main.title("ICS 32 Distributed Social Messenger")

    # This is just an arbitrary starting point. You can change the value
    # around to see how the starting size of the window changes.
    main.geometry("720x480")

    # adding this option removes some legacy behavior with menus that
    # some modern OSes don't support. If you're curious, feel free to comment
    # out and see how the menu changes.
    main.option_add('*tearOff', False)

    # Initialize the MainApp class, which is the starting point for the
    # widgets used in the program. All of the classes that we use,
    # subclass Tk.Frame, since our root frame is main, we initialize
    # the class with it.
    app = MainApp(main)

    # When update is called, we finalize the states of all widgets that
    # have been configured within the root frame. Here, update ensures that
    # we get an accurate width and height reading based on the types of widgets
    # we have used. minsize prevents the root window from resizing too small.
    # Feel free to comment it out and see how the resizing
    # behavior of the window changes.
    main.update()
    main.minsize(main.winfo_width(), main.winfo_height())
    id = main.after(2000, app.check_new)
    print(id)
    # And finally, start up the event loop for the program (you can find
    # more on this in lectures of week 9 and 10).
    main.mainloop()

if __name__ == "__main__":
    main()
