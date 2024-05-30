import tkinter as tk
from tkinter import ttk
from frame1 import Frame1
from frame2 import Frame2
from frame3 import Frame3
from frame4 import Frame4

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("FSM Tool")
        self.geometry("800x800")
        
        # Create main frame
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(fill="both", expand=True)

        # Create header
        header = ttk.Label(self.main_frame, text="FSM Tools", font=("Helvetica", 32))
        header.pack(pady=20)

        # Create a container frame for buttons to center them
        button_frame = ttk.Frame(self.main_frame)
        button_frame.pack(expand=True)

        # Button width
        button_width = 30

        # Create buttons
        buttons = [
            ("Generate Mutants", self.show_frame1),
            ("FSM Tester and Mutant Killer", self.show_frame2),
            ("FSMs Synchronizing Sequence Finder", self.show_frame3),
            ("FSMs Generator", self.show_frame4)
        ]

        for text, command in buttons:
            button = ttk.Button(button_frame, text=text, command=command, width=button_width)
            button.pack(pady=10)

        # Initialize frames
        self.frames = {}
        for F in (Frame1, Frame2, Frame3, Frame4):
            page_name = F.__name__
            frame = F(parent=self, controller=self)
            self.frames[page_name] = frame

    def show_main_frame(self):
        for frame in self.frames.values():
            frame.pack_forget()
        self.main_frame.pack(fill="both", expand=True)

    def show_frame1(self):
        self.show_frame(Frame1)

    def show_frame2(self):
        self.show_frame(Frame2)

    def show_frame3(self):
        self.show_frame(Frame3)

    def show_frame4(self):
        self.show_frame(Frame4)

    def show_frame(self, frame_class):
        self.main_frame.pack_forget()
        frame = self.frames[frame_class.__name__]
        frame.pack(fill="both", expand=True)

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
