import tkinter as tk

root = tk.Tk()

root.rowconfigure(0, weight=1)
root.rowconfigure(1, weight=1)
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)

frame1 = tk.Frame(root, bg='red')
frame1.grid(row=0, column=0, sticky='nsew')

frame2 = tk.Frame(root, bg='blue')
frame2.grid(row=0, column=1, sticky='nsew')

frame3 = tk.Frame(root, bg='green')
frame3.grid(row=1, column=0, columnspan=2, sticky='nsew')

# frame1 içine widget'ları ekleyebilirsiniz
label1 = tk.Label(frame1, text='Frame 1')
label1.pack()

# frame2 içine widget'ları ekleyebilirsiniz
label2 = tk.Label(frame2, text='Frame 2')
label2.pack()

# frame3 içine widget'ları ekleyebilirsiniz
label3 = tk.Label(frame3, text='Frame 3')
label3.pack()

root.mainloop()