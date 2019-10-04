#!/usr/bin/env python3

"""This module contains the gui.

"""

import dbconnection as db
import dbqueries as dbq
import frame_func as ffunc
from tkinter import LabelFrame, Button, Label, Entry, OptionMenu, StringVar, \
    PhotoImage, messagebox, END, Scrollbar, font, Menu, Toplevel
from tkinter.ttk import *
from os import getcwd

class Frames:
    def __init__(self, master, frameName):
        """Contains global flags along with which frame to show initially."""

        self.master = master
        self.showPassword = False
        self.passwordResetFrame = False
        self.newPasswordFrame = False
        self.TreeFrameEdit = False
        self.eyeImage = PhotoImage(file="imgs/eye.png")
        self.checkImage = PhotoImage(file="imgs/checkmark.png")
        self.cwd = getcwd()

        if frameName == 'setup':
            self.setup()
        else:
            self.login()

    # frames
    def setup(self):
        """Frame for first time using the Password Manager."""

        # security questions
        SECQUESTIONS = [
            'What was your childhood nickname?',
            'In what city or town did your mother and father meet?',
            'What is your favorite team?',
            'What was your favorite food as a child?',
            'What was the name of the hospital where you were born?',
            'What school did you attend for sixth grade?'
        ]

        # frame
        setupFrame = LabelFrame(self.master, text='Setup Your Account')
        setupFrame.pack()

        # widget init
        SecQvar = StringVar(setupFrame)
        SecQvar.set(SECQUESTIONS[0])

        # widget
        mPassLabel = Label(setupFrame, text='Create a master password*: ')
        mPassEntry = Entry(setupFrame, width=45, show='*')
        previewBtn = Button(setupFrame, image=self.eyeImage,
            command=lambda: self.previewPassword(mPassEntry))
        spacer = Label(setupFrame, text='')
        mSecLabel = Label(setupFrame, text='Choose a security question: ')
        mSecQs = OptionMenu(setupFrame, SecQvar, *SECQUESTIONS)
        mSecAnsLabel = Label(setupFrame, text='Answer to security question**: ')
        mSecAnsEntry = Entry(setupFrame, width=45)
        spacer = Label(setupFrame, text='')
        confBtn = Button(setupFrame, text='Sign Up', width=10, 
            command=lambda: self.signUpSubmit(
                mPassEntry.get(), 
                SecQvar.get(), 
                mSecAnsEntry.get(), 
                setupFrame, 
                'login'))
        spacer = Label(setupFrame, text='')
        star1 = Label(setupFrame, 
            text='* 6-20 characters, 1 UPPER, 1 lower, 1 num, no space.')
        star2 = Label(setupFrame, text='** Capitalization and spacing counts.')

        # widget pack
        mPassLabel.grid(row=0 , column=0, sticky='e')
        mPassEntry.grid(row=0, column=1)
        previewBtn.grid(row=0, column=1, sticky='e')
        spacer.grid(row=1, column=0)
        mSecLabel.grid(row=2 , column=0, sticky='e')
        mSecQs.grid(row=2, column=1, sticky='w')
        mSecAnsLabel.grid(row=3 , column=0, sticky='e')
        mSecAnsEntry.grid(row=3, column=1)
        spacer.grid(row=4, column=1)
        confBtn.grid(row=5, column=1, sticky='e')
        spacer.grid(row=6, column=1)
        star1.grid(row=7, column=1, sticky='e')
        star2.grid(row=8, column=1, sticky='e')

        # widget bind
        previewBtn.image = self.eyeImage
        mPassEntry.bind('<Return>', lambda x: self.signUpSubmit(
            mPassEntry.get(), 
            SecQvar.get(), 
            mSecAnsEntry.get(), 
            setupFrame, 
            'login'))
        mSecAnsEntry.bind('<Return>', lambda x: self.signUpSubmit(
            mPassEntry.get(),
            SecQvar.get(),
            mSecAnsEntry.get(),
            setupFrame,
            'login'))

    def login(self):
        """Frame for logging into Password Manager using master password."""

        # frame
        loginFrame = LabelFrame(self.master, text='Login To Your Account')
        loginFrame.pack()

        # widget
        loginLabel = Label(loginFrame, text='Enter your master password: ')
        mLoginEntry = Entry(loginFrame, width=45, show='*')
        Spacer = Label(loginFrame, text='')
        loginBtn = Button(loginFrame, text='Log In',
            command=lambda: self.loginCheck(
                mLoginEntry.get(),
                loginFrame))
        loginResetBtn = Button(loginFrame, text='Reset Password',
            command=lambda: self.showPasswordReset())

        # widget pack
        loginLabel.grid(row=0 , column=0)
        mLoginEntry.grid(row=0, column=1)
        Spacer.grid(row=1, column=0)
        loginBtn.grid(row=2, column=1, sticky='e')
        loginResetBtn.grid(row=2, column=0, sticky='w')

        # widget bind
        mLoginEntry.bind('<Return>', lambda x: self.loginCheck(
            mLoginEntry.get(),
            loginFrame))

    def resetPassword(self):
        """Frame for checking security answer for new master password."""

        self.passwordResetFrame = True
        
        # frame
        self.resetPassFrame = LabelFrame(self.master, text='Password Reset')
        self.resetPassFrame.pack()

        # widget
        showSecQ = Label(self.resetPassFrame, text=ffunc.getSecQ())
        spacer = Label(self.resetPassFrame, text='')
        secAnsLabel = Label(self.resetPassFrame, text='Answer:')
        secAnsEntry = Entry(self.resetPassFrame, width=50)
        resetCheckBtn = Button(self.resetPassFrame, text='Check',
            command=lambda: self.secCheck(secAnsEntry.get()))

        # widget pack
        showSecQ.grid(row=0, column=1)
        spacer.grid(row=1, column=2)
        secAnsLabel.grid(row=2, column=0)
        secAnsEntry.grid(row=2, column=1)
        resetCheckBtn.grid(row=2, column=3)

        # widget bind
        secAnsEntry.bind('<Return>', lambda x: self.secCheck(secAnsEntry.get()))

    def newPassword(self):
        """Frame for creating new master password."""

        self.newPasswordFrame = True

        # frame
        self.newPassFrame = LabelFrame(self.master, text='Make A New Password')
        self.newPassFrame.pack()

        # widget
        newPassLabel = Label(self.newPassFrame,
            text='Create A New Master Password*')
        spacer = Label(self.newPassFrame, text='')
        newPassEntry = Entry(self.newPassFrame, width=45, show='*')
        previewBtn = Button(self.newPassFrame, image=self.eyeImage,
            command=lambda: self.previewPassword(newPassEntry))
        submitBtn = Button(self.newPassFrame, text='Submit',
            command=lambda: self.resetSubmit(newPassEntry.get()))
        spacer = Label(self.newPassFrame, text='')
        starLabel = Label(self.newPassFrame, 
            text='* 6-20 characters, 1 UPPER, 1 lower, 1 num, no space.')

        # widget pack
        newPassLabel.grid(row=0 , column=0)
        spacer.grid(row=1, column=0)
        newPassEntry.grid(row=2, column=0)
        previewBtn.grid(row=2, column=1)
        submitBtn.grid(row=3, column=0, sticky='e')
        spacer.grid(row=4, column=0)
        starLabel.grid(row=5, column=0, sticky='w')

        # widget bind
        newPassEntry.bind('<Return>', 
            lambda x: self.resetSubmit(newPassEntry.get()))

    def home(self):
        """Frames for creating and storing entries."""

        # frame - adding entries
        self.homeFrame = LabelFrame(self.master, text='Add An Entry')
        self.homeFrame.grid(row=0, column=0)

        # widget - adding entries
        webLabel = Label(self.homeFrame, text='Website')
        userLabel = Label(self.homeFrame, text='Username')
        passLabel = Label(self.homeFrame, text='Password')
        webEntry = Entry(self.homeFrame, width=30)
        userEntry = Entry(self.homeFrame, width=30)
        passEntry = Entry(self.homeFrame, width=30)
        addEntryBtn = Button(self.homeFrame, image=self.checkImage,
            command=lambda: self.checkEntry(
                webEntry.get(),
                userEntry.get(),
                passEntry.get()))

        # widget pack - adding entries
        webLabel.grid(row=0, column=0)
        userLabel.grid(row=0, column=1)
        passLabel.grid(row=0, column=2)
        webEntry.grid(row=1, column=0)
        userEntry.grid(row=1, column=1)
        passEntry.grid(row=1, column=2)
        addEntryBtn.grid(row=1, column=3)

        # widget bind - adding entries
        addEntryBtn.image = self.checkImage
        passEntry.bind('<Return>', lambda x: self.checkEntry(
            webEntry.get(),
            userEntry.get(),
            passEntry.get()))

        # frame - entries
        self.entriesFrame = Frame(self.master)
        self.entriesFrame.grid(row=1, column=0)

        # widget - adding
        toolbarLabel = Button(self.entriesFrame, text='Delete Selection',
            command=self.treeMenuDeleteSelected)
        self.entriesTree = Treeview(self.entriesFrame)
        self.showEntries() # inserts all rows

        # widget pack - adding
        toolbarLabel.grid(row=0, column=0, sticky='w', pady=(20, 5), padx=(5, 5))
        self.entriesTree.grid(row=1, column=0)

        # widget bind - adding
        self.entriesTree.bind("<Double-1>", self.cpyEntry)
        self.entriesTree.bind("<Button-3>", self.popUp)

        # widget config - adding
        self.entriesTree['columns'] = (0, 1, 2)
        self.entriesTree['show'] = 'headings'
        self.entriesTree.column(0, anchor='center')
        self.entriesTree.column(1, anchor='center')
        self.entriesTree.column(2, anchor='center')
        self.entriesTree.heading(0, text='Website')
        self.entriesTree.heading(1, text='Username')
        self.entriesTree.heading(2, text='Password')
        self.entriesTree.tag_configure('even', background='#e3e3e3')


        treeScroll = Scrollbar(self.entriesFrame, orient="vertical", 
            command=self.entriesTree.yview)
        self.entriesTree.configure(yscrollcommand=treeScroll.set)
        treeScroll.grid(row=1, column=1, sticky='NSEW')

        spacer = Label(self.entriesFrame, text='')
        spacer.grid(row=2, column=0)

        legendLabel = Label(self.entriesFrame, text='LEGEND:')
        legendLabel.grid(row=3, column=0, sticky='w')
        f = font.Font(legendLabel, legendLabel.cget("font"))
        f.configure(underline=True)
        legendLabel.configure(font=f)

        cpyPassword = Label(self.entriesFrame,
            text='- Double-click to copy password.')
        cpyPassword.grid(row=4, column=0, sticky='w')
        delRow = Label(self.entriesFrame, text='- Right-click for row options.')
        delRow.grid(row=5, column=0, sticky='w')

    def editEntry(self):
        """Frame for editing an entry."""
        self.TreeFrameEdit = True

        # frame
        self.treeEditFrame = LabelFrame(self.master, text='Edit Entry')
        self.treeEditFrame.grid(row=2, column=0)

        # widget init
        item = self.entriesTree.selection()
        for i in item:
            website = self.entriesTree.item(i, "values")[0]
            username = self.entriesTree.item(i, "values")[1]
        itemInfo = self.rowsDecrypted[int(item[0])]
        curPass = itemInfo[2]

        # widget
        oldLabel = Label(self.treeEditFrame, text='Old Entry')
        newLabel = Label(self.treeEditFrame, text='New Entry')
        webLabel = Label(self.treeEditFrame, text='Website')
        userLabel = Label(self.treeEditFrame, text='Username')
        pwLabel = Label(self.treeEditFrame, text='Password')
        oldWebInfo = Label(self.treeEditFrame, text=website)
        oldUserInfo = Label(self.treeEditFrame, text=username)
        oldPwInfo = Label(self.treeEditFrame, text=curPass)
        newWeb = Entry(self.treeEditFrame, width=30)
        newUser = Entry(self.treeEditFrame, width=30)
        newPw = Entry(self.treeEditFrame, width=30)
        submitBtn = Button(self.treeEditFrame, text='Submit', 
            command=lambda: self.editEntryCheck(
                item,
                newWeb.get(),
                newUser.get(),
                newPw.get()))

        # widget pack
        oldLabel.grid(row=0, column=1, sticky='w', padx=(0, 30))
        newLabel.grid(row=0, column=2, sticky='w')
        webLabel.grid(row=1, column=0, sticky='e', padx=(0, 15))
        userLabel.grid(row=2, column=0, sticky='e', padx=(0, 15))
        pwLabel.grid(row=3, column=0, sticky='e', padx=(0, 15))
        oldWebInfo.grid(row=1, column=1, sticky='w')
        oldUserInfo.grid(row=2, column=1, sticky='w')
        oldPwInfo.grid(row=3, column=1, sticky='w')
        newWeb.grid(row=1, column=2, sticky='w')
        newUser.grid(row=2, column=2, sticky='w')
        newPw.grid(row=3, column=2, sticky='w')
        submitBtn.grid(row=4, column=2, sticky='e')

        # widget bind
        newWeb.insert(0, website)
        newUser.insert(0, username)
        newPw.insert(0, curPass)

    # widget checks and configs
    def editEntryCheck(self, item, nw, nu, np):
        """Get new info for updating an entry."""

        itemInfo = self.entriesInfo[int(item[0])]
        ow = itemInfo[0]
        ou = itemInfo[1]
        op = itemInfo[2]

        ffunc.editEntry(ow, ou, op, nw, nu, np)
        self.switchFrame((self.homeFrame, self.treeEditFrame), ('home',))

    def showEntries(self):
        """Get entries decrypted from database and insert them into tree."""

        rowInfo = ffunc.getEntries()
        self.rowsDecrypted = rowInfo[0]
        self.entriesInfo = rowInfo[1]

        i = 0
        for row in self.rowsDecrypted:
            if i % 2 == 0:
                tag = 'even'
            else:
                tag = 'odd'
            self.entriesTree.insert('' , i, values=(
                row[0],
                row[1],
                '-HIDDEN-'
                ),
                iid=i,
                tags = (tag, i)
            )

            i += 1

    def cpyEntry(self, event):
        """Double click to copy password."""

        item = self.entriesTree.selection()
        for i in item:
            website = self.entriesTree.item(i, "values")[0]
            username = self.entriesTree.item(i, "values")[1]

        itemInfo = self.rowsDecrypted[int(item[0])]
        passwd = itemInfo[2]

        self.master.clipboard_clear()
        self.master.clipboard_append(passwd)

    def popUp(self, event):
        """Enable popup menu if right click is on an entry row."""

        item = self.entriesTree.identify_row(event.y)
        if item:
            self.entriesTree.selection_set(item)

            self.treeMenu()
            self.popUpMenu.post(event.x_root, event.y_root)

    def treeMenu(self):
        """Create popup menu."""

        def editCheck():
            if not self.TreeFrameEdit:
                self.editEntry()
            else:
                self.switchFrame((self.treeEditFrame,), ('editEntry',))

        self.popUpMenu = Menu(self.entriesFrame, tearoff=0)
        self.popUpMenu.add_command(label='Copy Password',
            command=lambda: self.cpyEntry(0))
        self.popUpMenu.add_command(label='Show Password',
            command=self.treeMenuShow)
        self.popUpMenu.add_command(label='Edit Entry',
            command=editCheck)
        self.popUpMenu.add_command(label='Delete Entry',
            command=self.treeMenuDelete)

    def treeMenuShow(self):
        """Show password - from popup menu."""

        item = self.entriesTree.selection()
        for i in item:
            website = self.entriesTree.item(i, "values")[0]
            username = self.entriesTree.item(i, "values")[1]

        itemInfo = self.rowsDecrypted[int(item[0])]
        passwd = itemInfo[2]

        self.entriesTree.item(item, values=(website, username, passwd))

    def treeMenuDelete(self):
        """Delete entry - from popup menu."""

        item = self.entriesTree.selection()
        itemInfo = self.entriesInfo[int(item[0])]
        website = itemInfo[0]
        username = itemInfo[1]
        password = itemInfo[2]

        ffunc.removeEntry(website, username, password)

        if self.TreeFrameEdit:
            self.switchFrame((self.homeFrame, self.treeEditFrame), ('home',))
        else:
            self.switchFrame((self.homeFrame,), ('home',))

    def treeMenuDeleteSelected(self):
        """Create confirmation window for multiple deletions - from popup 
        menu."""

        # window
        confirm = Toplevel()
        x = self.master.winfo_x()
        y = self.master.winfo_y()
        confirm.title('Offline Pass')
        confirm.geometry(f'+{x}+{y}')
        confirm.iconbitmap(self.cwd + '/imgs/favicon.ico')
        confirm.resizable(False, False)

        # widget init
        items = self.entriesTree.selection()
        itemInfo = self.entriesInfo[int(items[0])]

        # widget
        confirmLabel = Label(confirm, text='Are You Sure?')
        confirmYes = Button(confirm, text='Yes',
            command=lambda: self.checkDeleteSelected(
                items,
                self.entriesInfo,
                confirm))
        confirmNo = Button(confirm, text='No',
            command=lambda: confirm.destroy())

        # widget pack
        confirmLabel.grid(row=0, column=0)
        confirmYes.grid(row=1, column=1)
        confirmNo.grid(row=1, column=0)

    def checkDeleteSelected(self, items, oldInfo, window):
        """Delete multiple entries - from popup menu."""

        ffunc.removeMultiEntry(items, oldInfo)

        if self.TreeFrameEdit:
                window.destroy()
                self.switchFrame((self.homeFrame, self.treeEditFrame), ('home',))
        else:
            window.destroy()
            self.switchFrame((self.homeFrame,), ('home',))

    def signUpSubmit(self, password, question, answer, oF, nF):
        """Check if signup fields met."""

        if ffunc.pushSignup(password, question, answer):
            self.switchFrame((oF,), (nF,))
        else:
            if answer == '':
                messagebox.showerror("Error", "Security Answer can't be empty.")
            else:
                messagebox.showerror("Error", "Password requirements not met.")

    def previewPassword(self, entry):
        """For previewing password input."""

        if self.showPassword == False:
            entry.configure(show='')
            self.showPassword = True
        else:
            entry.configure(show='*')
            self.showPassword = False

    def loginCheck(self, password, loginFrame):
        """Check if other frames are active upon successful login."""

        if ffunc.loginCmp(password):
            if self.passwordResetFrame and self.newPasswordFrame:
                self.switchFrame(
                    (loginFrame, self.resetPassFrame, self.newPassFrame),
                    ('home',))
            elif self.passwordResetFrame:
                self.switchFrame((loginFrame, self.resetPassFrame), ('home',))
            else:
                self.switchFrame((loginFrame,), ('home',))
        else:
            messagebox.showerror("Error", "Incorrect password.")

    def secCheck(self, answer):
        """Check if security question matches."""

        if ffunc.secCmp(answer):
            self.switchFrame((self.resetPassFrame,), ('newPassword',))
        else:
            messagebox.showerror("Error", "Answer does not match.")
            return

    def resetSubmit(self, password):
        """Check if password requirements met."""

        if ffunc.pushReset(password):
            self.newPassFrame.destroy()
        else:
            messagebox.showerror("Error", "Password requirements not met.")

    def checkEntry(self, web, user, passwd):
        """Check to make sure new entry has atleast the website field
        populated."""

        if ffunc.pushEntry(web, user, passwd):
            self.switchFrame((self.homeFrame,), ('home',))
        else:
            messagebox.showerror("Error", "Website field can't be empty.")

    def showPasswordReset(self):
        """Check to make sure reset password frame is not already showing."""

        if self.passwordResetFrame == False:
            self.resetPassword()
        else:
            return

    def switchFrame(self, oldFrame, newFrame):
        """Switch between different frames."""

        for frame in oldFrame:
            frame.destroy()
        for frame in newFrame:
            getattr(Frames, frame)(self)
