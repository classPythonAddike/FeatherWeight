from tkinter import *
from tkinter.scrolledtext import *
from tkinter import messagebox
from tkinter import filedialog

import webbrowser
import os
import pyperclip
import shelve
import threading

root = Tk()
root.title("New - FeatherWeight")
root.iconbitmap('feather.ico')
currentDir = os.getcwd()
prefs = shelve.open('userPrefs')

try:
    size = prefs['fontSize']
    font = prefs['font']
    he = 15
    filename = prefs['last']
    mode = prefs['mode']
except:
    prefs['fontSize'] = 13
    size = prefs['fontSize']
    prefs['font'] = "Comic Sans MS"
    font = prefs['font']
    he = 15
    prefs['last'] = ""
    filename = prefs['last']
    prefs['mode'] = "light"
    mode = "light"

prefs.close()
fils = (("Python Files", "*.py"), ("HTML Files", "*.html"), ("C++ Files", "*.cpp"), ("Ruby Files", "*.rb"), ("Text Files", "*.txt"))
username = os.environ["USERNAME"]

codext = ScrolledText(root, width = 50, height  = he, font = (font, size), padx = 5, tabs = 25)

def newFile():
    global filename, codext, root

    filename = ""
    codext.delete(1.0, 'end')
    root.title("New - FeatherWeight")

if filename != "":
    try:
        with open(filename) as filtext:
            text = filtext.read()
            codext.insert(1.0, text)
            filtext.close()
            root.title(filename + " - FeatherWeight")
    except:
        newFile()

codext.grid(row = 0, column = 0, columnspan = 50, sticky = 'nswe')

def openFile():
    global root, codext, filename, fils, username

    if filename != "":
        saveFile()
    
    filename = filedialog.askopenfilename(initialdir = r"C:\Users\\" + username + "\Desktop", filetypes = fils)
    if filename != '':
        with open(filename) as g:
            text = g.read()
            g.close()
        codext.delete(1.0, 'end')
        codext.insert(1.0, text)
        root.title(filename + " - FeatherWeight")

def openFileMenu(z):
    openFile()

def saveFile():
    global filename, codext, fils, username
    
    if filename == "":
        fileToSave = filedialog.asksaveasfile(initialdir = r"C:\Users\\" + username + "\Desktop", filetypes = fils, defaultextension = fils)
        if fileToSave == None:
            pass
        else:
            fileToSave.write(codext.get(1.0, 'end'))
            filename = fileToSave.name
            fileToSave.close()
            root.title(filename + " - FeatherWeight")
        
    else:
        file = os.path.splitext(filename)[0]
        os.renames(filename, file + '.txt')
        with open(file + '.txt', 'w') as f:
            text = codext.get(1.0, 'end')
            f.write(text)
            f.close()
        os.renames(file + '.txt', filename)

def saveFileMenu(y):
    saveFile()

def passCommand(com):
    os.system(com)

def runCode():
    global filename, codext, currentDir
    
    saveFile()

    with open(filename) as g:
        text = g.read()
        g.close()
    codext.delete(1.0, 'end')
    codext.insert(1.0, text)
    ext = os.path.splitext(filename)[1]
    root.title(filename + " - FeatherWeight")
    os.chdir(currentDir)
    
    if ext == ".py":
        pathList = os.path.splitext(filename)[0].split("/")
        folder = pathList[:-1]
        directory = ""
        for a in folder:
            directory += a + "\\\\"
        os.chdir(directory)
        x = threading.Thread(target=passCommand, args=("cmd /k \"python \"" + filename + '""',), daemon = True)
        x.start()
        
    elif ext == ".html":
        webbrowser.open(filename)

    elif ext == ".cpp":
        root.ct = Tk()
        root.ct.title("C++ Compiler")
        root.ct.iconbitmap('feather.ico')

        def compilerType(name):
            global filename, root
            cppFile = os.path.splitext(filename)[0]
            pathList = os.path.splitext(filename)[0].split("/")
            folder = pathList[:-1]
            directory = ""
            for a in folder:
                directory += a + "\\\\"
            os.chdir(directory)
            if name == "gcc":
                root.ct.destroy()
                x = threading.Thread(target = passCommand, args = ("cmd /c \"g++ \"" + filename + '" -o "' + cppFile + '.exe""',))
                y = threading.Thread(target = passCommand, args = ('cmd /k "' + cppFile + '.exe"',), daemon = True)
                x.start()
                x.join()
                y.start()
            if name == "bcc":
                root.ct.destroy()
                x = threading.Thread(target = passCommand, args = ("cmd /c \"bcc64 \"" + filename +'""',))
                y = threading.Thread(target = passCommand, args = ('cmd /k "' + cppFile + '.exe"',), daemon = True)
                x.start()
                x.join()
                y.start()
            if name == "tcc":
                root.ct.destroy()
                x = threading.Thread(target = passCommand, args = ("cmd /c \"tcc \"" + filename +'""',))
                y = threading.Thread(target = passCommand, args = ('cmd /k "' + cppFile + '.exe"',), daemon = True)
                x.start()
                x.join()
                y.start()
            
        text = Label(root.ct, text = "FeatherWeight supports the following compilers for C++. Which one are you using?")
        gcc = Button(root.ct, text = "GNU GCC Compiler", padx = 10, pady = 10, command = lambda: compilerType("gcc"))
        bcc = Button(root.ct, text = "Borland C++ Compiler (64-bit)", padx = 10, pady = 10, command = lambda: compilerType("bcc"))
        tcc = Button(root.ct, text = "Turbo C++ Compiler", padx = 10, pady = 10, command = lambda: compilerType("tcc"))
        text.grid(row = 0, column = 0, columnspan = 3)
        gcc.grid(row = 1, column = 0)
        bcc.grid(row = 1, column = 1)
        tcc.grid(row = 1, column = 2)
        root.ct.mainloop()
        
    elif ext == ".rb":
        pathList = os.path.splitext(filename)[0].split("/")
        folder = pathList[:-1]
        directory = ""
        for a in folder:
            directory += a + "\\\\"
        os.chdir(directory)
        x = threading.Thread(target = passCommand, args = ("cmd /k \"ruby \"" + filename + '""',), daemon = True)
        x.start()

    elif ext == ".txt":
        pathList = os.path.splitext(filename)[0].split("/")
        msg = messagebox.showwarning(pathList[-1] + ".txt", "Cannot run a text file!")

def runCodeMenu(x):
    runCode()

def saveCopy():
    global root, codext, filename, fils
    
    fileToCopy = filedialog.asksaveasfile(initialdir = r"C:\Users\\" + username + "\Desktop", filetypes = fils, defaultextension = fils)
    
    if fileToCopy != None:
        fileToCopy.write(codext.get(1.0, 'end'))
        fileToCopy.close()

def saveCopyMenu(w):
    saveCopy()

def helpAbout():
    global filename

    saveFile()
    ext = os.path.splitext(filename)[-1]
    if ext == ".html":
        webbrowser.open("https://www.khanacademy.org/computing/computer-programming/html-css")
    elif ext == ".py":
        webbrowser.open("https://docs.python.org/3/")
    elif ext == ".cpp":
        webbrowser.open('https://devdocs.io/cpp/io/basic_streambuf/gptr')
    elif ext == ".rb":
        webbrowser.open('https://ruby-doc.org/')
    elif ext == ".txt":
        msg = messagebox.showwarning(".txt Files", "Cannot show documentation for a text file!")

def helpAboutMenu(v):
    helpAbout()

def newFileMenu(u):
    newFile()

def zoomIn():
    global codext, size, font
    
    size += 3
    codext['font'] = (font, size)

def zoomInMenu(t):
    zoomIn()

def zoomOut():
    global codext, size, font
    
    size -= 3
    codext['font'] = (font, size)

def zoomOutMenu(s):
    zoomOut()

def copy():
    global codext, filename

    try:
        selection = codext.selection_get()
        pyperclip.copy(selection)
    except:
        pass
    if filename != "":
        saveFile()

def copyMenu(r):
    copy()

def paste():
    global codext
    
    pos = codext.index(INSERT)
    toPaste = pyperclip.paste()
    codext.insert(pos, toPaste)

def pasteMenu(q):
    paste()

def darkMode():
    global codext, mode

    codext['bg'] = "grey"
    codext['fg'] = 'lightblue'
    mode = "dark"
    codext['insertbackground'] = "white"

def darkModeMenu(p):
    darkMode()

def lightMode():
    global codext, mode

    codext['bg'] = "white"
    codext['fg'] = 'black'
    mode = "light"
    codext['insertbackground'] = "black"

def lightModeMenu(o):
    lightMode()

def changeFont():
    global codext, font, currentDir
    os.chdir(currentDir)
    root.changeFont = Tk()
    root.changeFont.title("Change Font")
    root.changeFont.iconbitmap('feather.ico')
    
    def change():
        global font
        font = fnt.get()
        codext['font'] = (font, size)
    
    chng = Button(root.changeFont, text = "Change Font", command = change)
    fnt = Entry(root.changeFont, width = 30)
    fnt.grid(row = 0, column = 0)
    chng.grid(row = 0, column = 1)
    
    root.changeFont.mainloop()

def changeFontMenu(d):
    changeFont()

def closing():
    global root, size, filename, currentDir, font, fontSize, mode
    if (codext.get(1.0, 'end') != "\n"):
        saveFile()
        os.chdir(currentDir)
        prefs = shelve.open("userPrefs")
        prefs['last'] = filename
        prefs['font'] = font
        prefs['fontSize'] = size
        prefs['mode'] = mode
        prefs.close()
    root.destroy()

def completeCode(m):
    global codext
    ind = codext.index(INSERT)
    
    if m.keysym == 'braceleft':
        codext.insert(ind, "}")
        codext.mark_set(INSERT, ind)
    elif m.keysym == 'bracketleft':
        codext.insert(ind, "]")
        codext.mark_set(INSERT, ind)
    elif m.keysym == 'parenleft':
        codext.insert(ind, ")")
        codext.mark_set(INSERT, ind)
    elif m.keysym == 'quotedbl':
        codext.insert(ind, '"')
        codext.mark_set(INSERT, ind)
    elif m.keysym == 'quoteright':
        codext.insert(ind, "'")
        codext.mark_set(INSERT, ind)
    elif m.keysym == 'less':
        codext.insert(ind, ">")
        codext.mark_set(INSERT, ind)

if mode == "dark":
    codext['fg'] = "lightblue"
    codext['bg'] = "grey"
    codext['insertbackground'] = "white"

menubar = Menu(root)

filemenu = Menu(menubar, tearoff = 0)
editmenu = Menu(menubar, tearoff = 0)
runmenu = Menu(menubar, tearoff = 0)
viewmenu = Menu(menubar, tearoff = 0)
helpmenu = Menu(menubar, tearoff = 0)
modemenu = Menu(viewmenu, tearoff = 0)

filemenu.add_command(label = "Save", command = saveFile, accelerator = "Ctrl+S")
root.bind("<Control_L><s>", saveFileMenu)
root.bind("<Control_R><s>", saveFileMenu)
filemenu.add_command(label = "New", command = newFile, accelerator = "Ctrl+N")
root.bind("<Control_L><n>", newFileMenu)
root.bind("<Control_R><n>", newFileMenu)
filemenu.add_command(label = "Save A Copy", command = saveCopy, accelerator = "Alt+S")
root.bind("<Alt_L><s>", saveCopyMenu)
root.bind("<Alt_R><s>", saveCopyMenu)
filemenu.add_command(label = "Open", command = openFile, accelerator = "Ctrl+O")
root.bind("<Control_L><o>", openFileMenu)
root.bind("<Control_R><o>", openFileMenu)

editmenu.add_command(label = "Copy", command = copy, accelerator = "Ctrl+C")
editmenu.add_command(label = "Paste", command = paste, accelerator = "Ctrl+V")

runmenu.add_command(label = "Run", command = runCode, accelerator = "F5")
root.bind("<F5>", runCodeMenu)

viewmenu.add_command(label = "Zoom In", command = zoomIn, accelerator = "Ctrl++")
root.bind("<Control_L><+>", zoomInMenu)
root.bind("<Control_R><+>", zoomInMenu)
viewmenu.add_command(label = "Zoom Out", command = zoomOut, accelerator = "Ctrl+-")
root.bind("<Control_L><minus>", zoomOutMenu)
root.bind("<Control_R><minus>", zoomOutMenu)
viewmenu.add_command(label = "Font", command = changeFont, accelerator = "Ctrl+F")
root.bind("<Control_L><f>", changeFontMenu)
root.bind("<Control_R><f>", changeFontMenu)
modemenu.add_command(label = "Dark Mode", command = darkMode, accelerator = "Alt+D")
root.bind("<Alt_L><d>", darkModeMenu)
root.bind("<Alt_R><d>", darkModeMenu)
modemenu.add_command(label = "Light Mode", command = lightMode, accelerator = "Alt+L")
root.bind("<Alt_L><l>", lightModeMenu)
root.bind("<Alt_R><l>", lightModeMenu)
viewmenu.add_cascade(label = "Mode", menu = modemenu)

helpmenu.add_command(label = "Help", command = helpAbout, accelerator = "Ctrl+H")
root.bind("<Control_L><h>", helpAboutMenu)
root.bind("<Control_R><h>", helpAboutMenu)

root.bind("<Key>", lambda a: completeCode(a))

menubar.add_cascade(label = "File", menu = filemenu)
menubar.add_cascade(label = "Edit", menu = editmenu)
menubar.add_cascade(label = "View", menu = viewmenu)
menubar.add_cascade(label = "Run", menu = runmenu)
menubar.add_cascade(label = "Help", menu = helpmenu)

root.config(menu = menubar)
root.columnconfigure(0, weight = 2)
root.rowconfigure(0, weight = 1)
root.protocol("WM_DELETE_WINDOW", closing)

root.mainloop()
