
import os
import platform
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from mutant_gen import gen_call


class Frame1(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        # Heading
        heading_label = tk.Label(self, text="Mutant's Generator", font=("Helvetica", 24))
        heading_label.pack(pady=20)

        # upload entry
        upload_frame = tk.Frame(self)
        upload_frame.pack()

        tk.Label(upload_frame, text="Choose FSM file:").pack(side='left', padx=7)
        self.upload_entry = tk.Entry(upload_frame)
        self.upload_entry.pack(side='left')
        upload_button = tk.Button(upload_frame, text="Upload", command=self.upload_fsm)
        upload_button.pack(side='right')





        # Number of Mutants

        mutants_frame = tk.Frame(self)
        mutants_frame.pack()
        tk.Label(mutants_frame, text="Number of Mutants:").pack(side='left', padx=7)
        self.mutants_entry = tk.Entry(mutants_frame)
        self.mutants_entry.pack(side='right')

        # Fault Types
        fault_types_frame = tk.Frame(self)
        fault_types_frame.pack(pady=10)

        fault_types_label = tk.Label(fault_types_frame, text="Fault Types:")
        fault_types_label.pack()

        self.fault_types = ["Output fault", "Transition fault", "Output & transition fault", "Extra state"]
        self.fault_vars = {}
        for idx, fault in enumerate(self.fault_types):
            var = tk.BooleanVar()
            var.set(False)
            self.fault_vars[idx] = var
            checkbox = tk.Checkbutton(fault_types_frame, text=fault, variable=var)
            checkbox.pack(anchor=tk.W)
        
        # State to be mimicked
        states_be_mim_label = tk.Label(self, text="State to be Mimicked:")
        states_be_mim_label.pack()
        self.states_be_mim_entry = tk.Entry(self)
        self.states_be_mim_entry.pack()

        # Max execution time (seconds) per Mutant
        max_excution_time_label = tk.Label(self, text="Max execution time (seconds):")
        max_excution_time_label.pack()
        self.max_excution_time_entry = tk.Entry(self)
        self.max_excution_time_entry.pack()

        # Number of Faults per Mutant
        faults_per_mutant_label = tk.Label(self, text="Number of Faults per Mutant:")
        faults_per_mutant_label.pack()
        self.faults_per_mutant_entry = tk.Entry(self)
        self.faults_per_mutant_entry.pack()

        # Generate Button
        generate_button = tk.Button(self, text="Generate Mutants", command=self.generate_mutants)
        generate_button.pack(pady=20)


        back_button = ttk.Button(self, text="Back to Main", command=lambda: (self.clear_inputs(), self.controller.show_main_frame()))

        back_button.pack(pady=10)

    def upload_fsm(self):
        filename = filedialog.askopenfilename(initialdir="/", title="Select FSM file", filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
        if filename:
            self.upload_entry.delete(0, tk.END)
            self.upload_entry.insert(0, filename)
            
    def clear_inputs(self):
        # Clear FSM entry
        self.upload_entry.delete(0, tk.END)
        # Clear Mutants entry
        self.mutants_entry.delete(0, tk.END)
        self.states_be_mim_entry.delete(0, tk.END)
        self.states_be_mim_entry.delete(0, tk.END)
        # Reset fault checkboxes
        for var in self.fault_vars.values():
            var.set(False)
        # Clear faults per mutant entry
        self.faults_per_mutant_entry.delete(0, tk.END)
        
    def open_file(self, file_path):
        if platform.system() == "Windows":
            os.startfile(file_path)
        elif platform.system() == "Darwin":  # macOS
            os.system(f"open {file_path}")
        else:  # Linux and others
            os.system(f"xdg-open {file_path}")  


    def generate_mutants(self):

        try : 
            fsm_file = self.upload_entry.get()
            num_mutants = int(self.mutants_entry.get())
            selected_faults = [fault for fault, var in self.fault_vars.items() if var.get()]
            num_faults = int(self.faults_per_mutant_entry.get())
            input_filename = self.upload_entry.get()
            esf = 1 if 4 in selected_faults else 0
            extra_state = int(self.states_be_mim_entry.get())
            duration = int(self.max_excution_time_entry.get())
            output_filename = filedialog.asksaveasfilename(defaultextension=".txt", 
                                                           filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
            if output_filename:
                gen_call(input_filename, output_filename, num_mutants, num_faults, selected_faults[0], esf, extra_state, duration)
                self.open_file(output_filename)

        except ValueError:
            tk.messagebox.showerror("Error", "Please enter valid integer values for number of mutants and number of faults per mutants.")
            return



        # testings
        
        print("FSM file:", fsm_file)
        print("Number of Mutants:", num_mutants)
        print("Selected Faults:", selected_faults)
        print("Number of Faults per Mutant:", num_faults)
        

        




    
