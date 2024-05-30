import tkinter as tk
from tkinter import ttk
import random
from tkinter import simpledialog, scrolledtext, messagebox, filedialog

# Function to generate a random FSM
def generate_random_fsm(num_states, num_outputs, num_inputs, initial_connected, complete):
    fsm = {}
    for state in range(num_states):
        fsm[state] = {}
        for inp in range(num_inputs):
            next_state = random.randint(0, num_states - 1)
            output = random.randint(0, num_outputs - 1)
            fsm[state][inp] = (next_state, output)

    if initial_connected:
        visited = set()
        initial_state = 0
        stack = [initial_state]
        while stack:
            current_state = stack.pop()
            if current_state not in visited:
                visited.add(current_state)
                for next_state, _ in fsm[current_state].values():
                    stack.append(next_state)
        if len(visited) < num_states:
            return False, None

    if complete:
        for state in range(num_states):
            for inp in range(num_inputs):
                if inp not in fsm[state]:
                    next_state = random.randint(0, num_states - 1)
                    output = random.randint(0, num_outputs - 1)
                    fsm[state][inp] = (next_state, output)

    return True, fsm

class Frame4(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        label = ttk.Label(self, text="FSMs Generator", font=("Helvetica", 24))
        label.pack(pady=20)
        
        # Creating input fields
        tk.Label(self, text="Enter the number of FSMs to be generated:").pack()
        self.num_fsms_entry = tk.Entry(self)
        self.num_fsms_entry.pack()

        tk.Label(self, text="Enter the number of states:").pack()
        self.num_states_entry = tk.Entry(self)
        self.num_states_entry.pack()

        tk.Label(self, text="Enter the number of inputs:").pack()
        self.num_inputs_entry = tk.Entry(self)
        self.num_inputs_entry.pack()

        tk.Label(self, text="Enter the number of outputs:").pack()
        self.num_outputs_entry = tk.Entry(self)
        self.num_outputs_entry.pack()

        self.initial_connected_var = tk.IntVar()
        tk.Checkbutton(self, text="Initially connected", variable=self.initial_connected_var).pack()

        self.complete_var = tk.IntVar()
        tk.Checkbutton(self, text="Complete", variable=self.complete_var).pack()

        tk.Button(self, text="Generate FSMs", command=self.generate_fsms).pack()

        # Text area for output
        self.output_text = scrolledtext.ScrolledText(self, width=80, height=20)
        self.output_text.pack()

        # Export button
        tk.Button(self, text="Export to File", command=self.export_to_file).pack()

        # Clear button
        tk.Button(self, text="Clear Output", command=self.clear_output).pack()
        
        back_button = ttk.Button(self, text="Back to Main", command=lambda: (self.clear_output(), self.controller.show_main_frame()))
        back_button.pack(pady=10)

    def generate_fsms(self):
        try:
            num_fsms = int(self.num_fsms_entry.get())
            num_states = int(self.num_states_entry.get())
            num_inputs = int(self.num_inputs_entry.get())
            num_outputs = int(self.num_outputs_entry.get())
            initial_connected = self.initial_connected_var.get() == 1
            complete = self.complete_var.get() == 1
        except ValueError:
            messagebox.showerror("Invalid Input", "Please ensure all inputs are integers.")
            return

        self.output_text.delete(1.0, tk.END)

        for fsm_num in range(num_fsms):
            while True:
                success, random_fsm = generate_random_fsm(num_states, num_outputs, num_inputs, initial_connected, complete)
                if success:
                    break
            self.output_text.insert(tk.END, f"{fsm_num} {num_states} {num_states*num_inputs} {num_inputs} {num_outputs} 0\n")
            for state, transitions in random_fsm.items():
                for inp, (next_state, output) in transitions.items():
                    self.output_text.insert(tk.END, f"{state} {next_state} {inp} {output}\n")

    def export_to_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            with open(file_path, 'w') as file:
                file.write(self.output_text.get(1.0, tk.END))
            messagebox.showinfo("Export Successful", "The FSM data has been saved to " + file_path)

    def clear_output(self):
        self.num_fsms_entry.delete(0, tk.END)
        self.num_inputs_entry.delete(0, tk.END)
        self.num_states_entry.delete(0, tk.END)
        self.num_outputs_entry.delete(0, tk.END)
        self.output_text.delete(1.0, tk.END)
