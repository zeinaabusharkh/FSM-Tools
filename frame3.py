import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from collections import deque
from tkinter import scrolledtext
from tkinter import messagebox

# Functions and classes for FSM management
def map_inputs_to_numbers(fsm):
    input_mapping = {}
    number_mapping = {}
    current_number = 1
    for state, transitions in fsm.transitions.items():
        for i, (endingstate, input_signal, output) in enumerate(transitions):
            if not input_signal.isdigit() and input_signal not in input_mapping:
                input_mapping[input_signal] = str(current_number)
                number_mapping[str(current_number)] = input_signal
                current_number += 1
            if input_signal in input_mapping:
                fsm.transitions[state][i] = (endingstate, input_mapping[input_signal], output)
    return number_mapping

def remap_sequence_to_letters(sequence, number_mapping):
    return ''.join(number_mapping.get(char, char) for char in sequence)

def bfs_synchronizing_sequence(fsm, number_mapping):
    queue = deque([(frozenset(fsm.transitions.keys()), '')])
    visited = set([frozenset(fsm.transitions.keys())])
    inputs = set(number_mapping.values()) | set(str(i) for i in range(1, fsm.inputs + 1))
    while queue:
        current_states, sequence = queue.popleft()
        for input_signal in inputs:
            next_states = set()
            for state in current_states:
                transition_found = False
                for transition in fsm.transitions.get(state, []):
                    end_state, input, _ = transition
                    if input == input_signal or number_mapping.get(input, '') == input_signal:
                        next_states.add(end_state)
                        transition_found = True
                        break
                if not transition_found:
                    next_states.add(state)
            if frozenset(next_states) not in visited:
                visited.add(frozenset(next_states))
                new_sequence = sequence + number_mapping.get(input_signal, input_signal)
                if len(next_states) == 1:
                    return new_sequence
                queue.append((frozenset(next_states), new_sequence))
    return "No synchronizing sequence exists."

class FSM:
    def __init__(self, fsm_id, states, transitions, inputs, outputs, void_data):
        self.fsm_id = fsm_id
        self.states = int(states)
        self.transitions = {str(i): [] for i in range(1, int(states) + 1)}
        self.inputs = int(inputs)
        self.outputs = int(outputs)
        self.void_data = int(void_data)

    def add_transition(self, initialstate, endingstate, input, output):
        self.transitions[str(initialstate)].append((str(endingstate), input, str(output)))

class Frame3(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        label = ttk.Label(self, text="FSMs Synchronizing Sequence Finder", font=("Helvetica", 24))
        label.pack(pady=20)
        self.label = tk.Label(self, text="Upload an FSM file and find its synchronizing sequence.")
        self.label.pack()
        self.upload_button = tk.Button(self, text="Upload File", command=self.upload_file)
        self.upload_button.pack()

        self.result_label = tk.Label(self, text="", wraplength=500)
        self.result_label.pack()

        # Text Area for Outputs
        self.output_text = scrolledtext.ScrolledText(self, wrap=tk.WORD, width=80, height=20)
        self.output_text.pack(pady=(20, 20))

        # Clear System Button
        self.clear_button = tk.Button(self, text="Clear System", command=self.clear_system)
        self.clear_button.pack()

        # Export Output to File Button
        self.export_button = tk.Button(self, text="Export Output to File", command=self.export_output_to_file)
        self.export_button.pack()

        back_button = ttk.Button(self, text="Back to Main", command=lambda: (self.clear_system(), self.controller.show_main_frame()))
        back_button.pack(pady=10)

    def upload_file(self):
        filename = filedialog.askopenfilename(initialdir="/", title="Select file",
                                              filetypes=(("text files", "*.txt"), ("all files", "*.*")))
        if filename:
            try:
                fsms = load_fsms(filename)
                output = []
                for fsm_id, fsm in fsms.items():
                    number_mapping = map_inputs_to_numbers(fsm)
                    sequence = bfs_synchronizing_sequence(fsm, number_mapping)
                    output.append(f"FSM ID: {fsm_id}, Synchronizing Sequence: {sequence if sequence else 'None found'}")
                self.output_text.insert(tk.END, "\n".join(output))
            except Exception as e:
                self.output_text.insert(tk.END, f"Error processing file: {e}")
                
    def export_output_to_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            with open(file_path, 'w') as file:
                file.write(self.output_text.get("1.0", tk.END))
            messagebox.showinfo("Export Successful", "The output has been saved to " + file_path)
    
    def clear_system(self):
        # Clear the output text area
        self.output_text.delete('1.0', tk.END)
       


def load_fsms(filename):
    fsm_list = {}
    with open(filename, "r") as file:
        lines = [line.strip() for line in file]
        fsm = None
        for line in lines:
            if line and line[0].isdigit() and len(line.split()) == 6:  # Checks for the header line
                if fsm:
                    fsm_list[fsm.fsm_id] = fsm
                fsm_id, states, _, inputs, outputs, void_data = line.split()
                fsm = FSM(fsm_id, states, _, inputs, outputs, void_data)
            elif fsm and line:
                initialstate, endingstate, input_signal, output = line.split()
                fsm.add_transition(initialstate, endingstate, input_signal, output)
        if fsm:  # Don't forget the last FSM in the file
            fsm_list[fsm.fsm_id] = fsm
    return fsm_list
        

