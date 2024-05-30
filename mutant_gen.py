import random
import time
import copy
from collections import deque

def read_fsm(filename):
    fsm = []
    num_states = num_transitions = num_inputs = num_outputs = void_data = 0
    with open(filename, 'r') as file:
        for i, line in enumerate(file):
            parts = line.strip().split()
            fsm.append(parts)
            if i == 0:
                num_states = int(parts[1])
                num_transitions = int(parts[2])
                num_inputs = int(parts[3])
                num_outputs = int(parts[4])
                void_data = int(parts[5])
    return fsm, num_states, num_transitions, num_inputs, num_outputs, void_data

def write_fsm(filename, fsm):
    with open(filename, 'a') as file:
        for line in fsm:
            file.write(' '.join(line) + '\n')
        file.write('\n')  # Add an empty line after each FSM


def mutate_fsm(fsm, fault_type, num_faults, num_outputs, num_states, num_transitions, num_mutants, extra_st, esf, duration):
    
    
    # Create a set to store unique mutants
    mutants_set = list()

    input_mapping = {chr(i + ord('a')): i for i in range(26)}

    start_time = time.time()
    end_time = start_time + duration

    
    while len(mutants_set) < num_mutants and time.time() < end_time: 

        if fault_type in [0,1]:
            if num_faults > num_transitions:
                num_faults = num_transitions
        else:
            if num_faults > 2*num_transitions:
                num_faults = 2*num_transitions

        num_faults1 = random.randint(1, num_faults)
        

        # Copy the original FSM
        mutant_fsm = copy.deepcopy(fsm)

        # Output OR Transition 
        if fault_type in [0,1]:
            # Randomly choose transitions
            chosen_transitions = random.sample(range(1, num_transitions + 1), num_faults1)
            chosen_transitions.sort()
            for index in chosen_transitions:
                transition = mutant_fsm[index]
                if fault_type == 0:  # Output fault
                    # Mutate the output
                    new_next_output = random.randint(0, num_outputs-1)
                    while new_next_output == int(transition[-1]):
                        new_next_output = random.randint(0, num_outputs-1)
                    transition[-1] = str(new_next_output)  
                elif fault_type == 1:  # Transition fault
                    # Mutate the next state
                    new_next_state = random.randint(1, num_states)
                    while new_next_state == int(transition[1]):
                        new_next_state = random.randint(1, num_states)
                    transition[1] = str(new_next_state)
        
        # Output and Transition
        if fault_type == 2:
            temp_num_faults = num_faults1
            used_trans = []
            while temp_num_faults != 0:
                # Avoid infinite loop
                if len(used_trans) == len(mutant_fsm)-1: break
                # Randomly choosing a transition
                trans_ind = random.randint(1, num_transitions)
                while trans_ind in used_trans:
                    trans_ind = random.randint(1, num_transitions)
                used_trans.append(trans_ind)
                trans = mutant_fsm[trans_ind]
                # Only 1 fault for the fsm
                if temp_num_faults == 1:
                    temp_fault = random.randint(0,1)
                    if temp_fault == 0:  # Output fault
                        # Mutate the output
                        new_next_output = random.randint(0, num_outputs-1)
                        while new_next_output == int(trans[-1]):
                            new_next_output = random.randint(0, num_outputs-1)
                        trans[-1] = str(new_next_output)  
                    elif temp_fault == 1:  # Transition fault
                        # Mutate the next state
                        new_next_state = random.randint(1, num_states)
                        while new_next_state == int(trans[1]):
                            new_next_state = random.randint(1, num_states)
                        trans[1] = str(new_next_state)
                    # Reduce remaining num of faults by the faults done
                    temp_num_faults = temp_num_faults - 1
                
                if temp_num_faults > 1:
                    faults_per_trans = random.randint(1,2)
                    # 1 fault per transition
                    if faults_per_trans == 1:
                        temp_fault = random.randint(0,1)
                        if temp_fault == 0:  # Output fault
                            # Mutate the output
                            new_next_output = random.randint(0, num_outputs-1)
                            while new_next_output == int(trans[-1]):
                                new_next_output = random.randint(0, num_outputs-1)
                            trans[-1] = str(new_next_output)  
                        elif temp_fault == 1:  # Transition fault
                            # Mutate the next state
                            new_next_state = random.randint(1, num_states)
                            while new_next_state == int(trans[1]):
                                new_next_state = random.randint(1, num_states)
                            trans[1] = str(new_next_state)
                    # 2 faults per transition
                    if faults_per_trans == 2: 
                        new_next_output = random.randint(0, num_outputs-1)
                        while new_next_output == int(trans[-1]):
                            new_next_output = random.randint(0, num_outputs-1)
                        trans[-1] = str(new_next_output)
                        new_next_state = random.randint(1, num_states)
                        while new_next_state == int(trans[1]):
                            new_next_state = random.randint(1, num_states)
                        trans[1] = str(new_next_state)
                    # Reduce remaining num of faults by the faults done
                    temp_num_faults = temp_num_faults - faults_per_trans

        
        if fsm[1][2] in [chr(ord('a') + i) for i in range(int(26))]:
            fsm1 = copy.deepcopy(fsm)
            convert_inputs_to_numbers(fsm1, input_mapping)
            mutant_fsm1 = copy.deepcopy(mutant_fsm)
            convert_inputs_to_numbers(mutant_fsm1, input_mapping)
            if not distinguish_machines(fsm1, mutant_fsm1):
                continue
        else:
            if not distinguish_machines(fsm, mutant_fsm):
                continue
        
        
        if esf == 1:
            in_transitions = [] # Transitions into mimicked state
            out_transitions = [] # Transitions from mimicked state
            m = copy.deepcopy(mutant_fsm)
            for t in m:
                if len(t) == 6: continue
                if t[1] == str(extra_st): in_transitions.append(m.index(t))
                if t[0] == str(extra_st): out_transitions.append(t)

            if len(in_transitions) == 0: continue

            # Extra state mutation process
            mutant_fsm[0][1] = str(int(mutant_fsm[0][1])+1)
            new_state = mutant_fsm[0][1]
            mutation = random.choice(in_transitions)
            mutant_fsm[mutation][1] = new_state
            for i in out_transitions:
                i[0] = new_state 
                mutant_fsm.append(i)
            mutant_fsm[0][2] = str(len(mutant_fsm)-1)
        
        
        mutants_set.append(mutant_fsm)
        

            
    return mutants_set

########### FIX ##############################################################################################################
def distinguish_machines(fsm1, fsm2):
    # Extract initial states of both machines
    initial_state1 = int(fsm1[1][0])
    initial_state2 = int(fsm2[1][0])

    # Define function to get next state given current state and input for each machine
    def get_trans(machine, current_state, input1):
        transition = next((t for t in machine if t[0] == current_state and t[2] == input1), None)
        return transition

    # Perform breadth-first search with depth limit n * m
    max_depth = int(fsm1[0][1]) * int(fsm2[0][1])
    queue = deque([(initial_state1, initial_state2, 0)])  # Start with initial states of both machines
    visited = set((initial_state1, initial_state2))  # Keep track of visited states
    while queue:
        state1, state2, depth = queue.popleft()
        if depth > max_depth:
            return False  # Depth limit reached without distinguishing machines
        for input_val in range(int(fsm1[0][3])):  # Loop over possible inputs
            trans1 = get_trans(fsm1[1:], str(state1), str(input_val))
            trans2 = get_trans(fsm2[1:], str(state2), str(input_val))
            
            if trans1 is not None and trans2 is not None:
                next_state1 = int(trans1[1])
                next_state2 = int(trans2[1])
                
                output1 = trans1[3]
                output2 = trans2[3]
                if output1 != output2:
                    return True  # Outputs differ, machines are distinguishable
                next_state_pair = (next_state1, next_state2)
                if next_state_pair not in visited:
                    visited.add(next_state_pair)
                    queue.append((next_state1, next_state2, depth + 1))

    return False  # No distinguishable sequence found within depth limit
#############################################################################################################


def convert_inputs_to_numbers(fsm, input_mapping):
    # Iterate over each transition in the FSM
    for transition in fsm[1:]:
        # Convert input from letter to number
        transition[2] = str(input_mapping.get(transition[2], -1))

    return fsm


def gen_call(input_filename,output_filename, num_mutants,num_faults, fault_type, esf, extra_state, duration):

    #  input_filename = 'original_fsm.txt'
    # output_filename = 'mutated_fsm.txt'
    # num_mutants = 40  # Number of mutants to generate
    # num_faults = 3   # Number of faults 
    # Specify fault type manually (0:output, 1:transition, 2:output&trans)
    # fault_type = 2 
    # esf = 0 # Extra state fault indicator (0:no, 1:yes)
    # extra_state = 3 # State to mimick
    # duration = 60 # Time in seconds
    open(output_filename, 'w').truncate(0)
    
    # Read original FSM and extract additional variables
    original_fsm, num_states, num_transitions, num_inputs, num_outputs, void_data = read_fsm(input_filename)

    if esf == 1 and (1 > extra_state or extra_state > num_states): 
        print("Invalid extra state entered! Program terminating...")
        exit(1)

    

    # Generate mutants
    mutants_set = mutate_fsm(original_fsm, fault_type, num_faults, num_outputs, num_states, num_transitions, num_mutants, extra_state, esf, duration)
    
    for i, m in enumerate(mutants_set, start=1):
        m[0][0] = str(i)
        write_fsm(output_filename, m)

    
    print(f'{len(mutants_set)} mutants saved to {output_filename}')
