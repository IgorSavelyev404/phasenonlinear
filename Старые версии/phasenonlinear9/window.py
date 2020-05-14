import tkinter as tk
class Win:
    def __init__(self, root):
        """Define window for the app"""
        self.root = root
        self.root.geometry("400x300")
        
        self.button_rename = tk.Button(self.root, text = "New window",
            command= self.new_winF).pack()
 
    def new_winF(self): # new window definition
        newwin = tk.Toplevel(root)
        display = tk.Label(newwin, text="Humm, see a new window !")
        display.pack()    

if __name__ == "__main__":
    root = tk.Tk()
    app = Win(root)
    app.root.title("dots")
    root.mainloop()