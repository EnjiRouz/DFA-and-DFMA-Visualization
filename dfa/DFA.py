class DFA(object):
    def __init__(self, *, transitions, start_state, final_states):
        if transitions is None:
            raise Exception("transitions argument is None")
        if start_state is None or start_state == "":
            raise Exception("initial state is not specified")
        if final_states is None or len(final_states) == 0:
            raise Exception("end states is not specified")

        self.states = list(transitions.keys())
        self.transitions = transitions
        self.final_states = final_states
        self.start_state = start_state

    def read_input(self, line):
        way = list()
        way.append((self.start_state, line))
        self.__simulation(line, way)
        return way

    # таблица перееходов
    # первый столбец - состояния, первая строка - символы
    def get_table(self):
        table = list()
        all_sybols = list()
        for i in self.transitions:
            for j in self.transitions[i].keys():
                if j not in all_sybols:
                    all_sybols.append(j)

        table.append(["_"] + all_sybols)

        for i in self.states:
            label = ""
            if i in self.final_states:
                label = "-"
            elif i == self.start_state:
                label = "+"
            row = [label + i] + (['0'] * len(all_sybols))

            for j in self.transitions[i].keys():
                row[all_sybols.index(j) + 1] = self.transitions[i][j]
            table.append(row)
        return table

    def __simulation(self, line, way):
        state = self.start_state
        for i in range(len(line)):
            if self.transitions[state].get(line[i]) is not None:
                state = self.transitions[state][line[i]]
                way.append((state, line[i + 1:]))
            else:
                way.append(False)
                return
        way.append(state in self.final_states)

    @staticmethod
    def table_parse(table):
        transitions = dict()
        final_states = list()
        start_state = ""

        for i in table[1:]:
            transition = dict()
            for j in range(1, len(i)):
                if i[j] != '0':
                    transition[table[0][j]] = i[j]
            if i[0][0] == "-":
                final_states.append(i[0][1:])
                transitions[i[0][1:]] = transition
                continue

            if len(transition) == 0:
                raise Exception("there are no transitions from state " + i[0])
            if i[0][0] == "+":
                if start_state != "":
                    raise Exception("incorrect count of starting positions, expected 1")
                start_state = i[0][1:]
                transitions[i[0][1:]] = transition
            else:
                transitions[i[0]] = transition

        return DFA(transitions=transitions, start_state=start_state, final_states=final_states)
