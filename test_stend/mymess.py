from tkinter import *

root = Tk()
root.overrideredirect(1)
root.attributes("-topmost", True)
root.geometry('+320+760')
text = Text(width=115, height=5, background='#445767', foreground='#FFFFFF', font='Any, 15')

text.insert(INSERT, 'Text Lex  ' * 300)
text.configure(state='disabled')
text.pack(side=LEFT)

scroll = Scrollbar(command=text.yview)
scroll.pack(side=LEFT, fill=Y)

text.config(yscrollcommand=scroll.set)

root.mainloop()