import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, scrolledtext, messagebox
import random

# Your provided functions integrated into the GUI
def read_fsm(data):
    fsm = []
    lines = data.strip().split('\n')
    fsm_info = lines[0].strip().split()
    fsm_id = int(fsm_info[0])
    num_states = int(fsm_info[1])
    num_transitions = int(fsm_info[2])
    num_inputs = int(fsm_info[3])
    num_outputs = int(fsm_info[4])
    void_data = int(fsm_info[5])

    for line in lines[1:]:
        parts = line.strip().split()
        fsm.append((int(parts[0]), int(parts[1]), parts[2], int(parts[3])))
    return fsm

def extract_input_symbols(fsm):
    input_symbols = set()
    for transition in fsm:
        input_symbols.add(transition[2])
    return list(input_symbols)

def generate_distinguishing_sequence(input_symbols, previous_sequence=None):
    alphabet = input_symbols.copy()
    distinguishing_sequence = []

    if previous_sequence:
        for symbol in previous_sequence:
            if symbol in alphabet:
                alphabet.remove(symbol)

    while len(distinguishing_sequence) < 2:
        random_symbol = random.choice(alphabet)
        distinguishing_sequence.append(random_symbol)

    return distinguishing_sequence

def apply_sequence_to_fsm(fsm, sequence):
    current_state = 1
    outputs = []
    for input_symbol in sequence:
        for transition in fsm:
            if transition[0] == current_state and transition[2] == input_symbol:
                outputs.append(transition[3])
                current_state = transition[1]
                break
    return outputs


##############################

class Frame2(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        label = ttk.Label(self, text="FSM Tester and Mutant Killer", font=("Helvetica", 24))
        label.pack(pady=20)
                # Load Original FSM Button
        self.load_fsm_button = tk.Button(self, text="Load Original FSM", command=self.load_fsm)
        self.load_fsm_button.pack()

        # Load Mutants Button
        self.load_mutants_button = tk.Button(self, text="Load Mutants", command=self.load_mutants)
        self.load_mutants_button.pack()

        # Start Testing Button
        self.start_button = tk.Button(self, text="Start Testing", command=self.start_testing)
        self.start_button.pack()

        # Text Area for Outputs
        self.output_text = scrolledtext.ScrolledText(self, wrap=tk.WORD, width=80, height=20)
        self.output_text.pack(pady=(20, 20))

        # Clear System Button
        self.clear_button = tk.Button(self, text="Clear System", command=self.clear_system)
        self.clear_button.pack()

        # Export Output to File Button
        self.export_button = tk.Button(self, text="Export Output to File", command=self.export_output_to_file)
        self.export_button.pack()

        # FSM and mutants data storage
        self.original_fsm = None
        self.mutants_data = []

        back_button = ttk.Button(self, text="Back to Main", command=lambda: (self.clear_system(), self.controller.show_main_frame()))
        back_button.pack(pady=10)

    def load_fsm(self):
        filename = filedialog.askopenfilename(title="Select FSM File", filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
        if filename:
            with open(filename, 'r') as file:
                data = file.read()
            self.original_fsm = read_fsm(data)
            self.output_text.insert(tk.END, "Loaded original FSM.\n")

    def load_mutants(self):
        filename = filedialog.askopenfilename(title="Select Mutants File", filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
        if filename:
            with open(filename, 'r') as file:
                self.mutants_data = file.read().strip().split('\n\n')
            self.output_text.insert(tk.END, "Loaded mutants data.\n")

    def start_testing(self):
        if not self.original_fsm or not self.mutants_data:
            self.output_text.insert(tk.END, "Error: Please load both FSM and mutants data before testing.\n")
            return

        input_symbols = extract_input_symbols(self.original_fsm)
        previous_sequences = set()
        killed_mutants = set()

        for i, mutant_data in enumerate(self.mutants_data, start=1):
            if not mutant_data:
                continue
            mutant_fsm = read_fsm(mutant_data)
            distinguishing_sequence = generate_distinguishing_sequence(input_symbols, previous_sequences)

            sequence_str = ' '.join(distinguishing_sequence)
            previous_sequences.add(sequence_str)

            original_outputs = apply_sequence_to_fsm(self.original_fsm, distinguishing_sequence)
            mutant_outputs = apply_sequence_to_fsm(mutant_fsm, distinguishing_sequence)

            if original_outputs != mutant_outputs:
                killed_mutants.add(i)
                self.output_text.insert(tk.END, f"Mutant {i} killed by sequence {sequence_str}.\n")
            else:
                self.output_text.insert(tk.END, f"Mutant {i} survived sequence {sequence_str}.\n")

        self.output_text.insert(tk.END, f"All mutants tested. Killed mutants: {killed_mutants}\n")

    def clear_system(self):
        # Clear the output text area
        self.output_text.delete('1.0', tk.END)
        # Reset the stored data
        self.original_fsm = None
        self.mutants_data = []
        # Display a message indicating the system has been cleared
        self.output_text.insert(tk.END, "System cleared. Ready to load new data.\n")

    def export_output_to_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            with open(file_path, 'w') as file:
                file.write(self.output_text.get("1.0", tk.END))
            messagebox.showinfo("Export Successful", "The output has been saved to " + file_path)
