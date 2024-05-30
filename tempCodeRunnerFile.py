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