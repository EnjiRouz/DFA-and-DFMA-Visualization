from dpda import DPDA

# DPDA which which matches zero or more 'a's, followed by the same
# number of 'b's (accepting by final state)
dpda2 = DPDA(
    states={'q1', 'q2', 'q3'},
    input_symbols={'0', '1', 'e'},
    stack_symbols={'#', 'z'},
    transitions={
        'q1': {
            '0': {'z': ('q1', ('z', 'z')), '#': ('q1', ('z', '#'))},  # transition pushes '1' to stack
            '1': {'z': ('q1', '')},
            'e': {'#': ('q2', ('#'))},
        }
    },
    initial_state='q1',
    initial_stack_symbol='#',
    final_states={'q2'}
)



def createdic(lst):
    return {lst[0]: {lst[1]: {lst[2]: (lst[3] , lst[4])}}}


def createTransition(lst):
    mnoj =[]
    kort = []
    end_dic = {}
    for dic in lst:
        for key1, val1 in createdic(dic).items():
            if key1 in end_dic: #сравнили состояния q1,q2 и тд
                for key2, val2 in val1.items():
                    if key2 in end_dic[key1]:
                        for key3, val3 in val2.items():
                            if key3 not in end_dic[key1][key2]:
                                end_dic[key1][key2].update(val2)
                    else:
                         end_dic[key1].update(val1)
            else:
                end_dic.update(createdic(dic))
    return end_dic



def receiver(states, transitions, input_symbols, initial_state, final_states, stack_symbols, initial_stack_symbol):
    return DPDA(states=set(states), input_symbols=set(input_symbols), stack_symbols=set(stack_symbols), transitions=createTransition(transitions), initial_state=initial_state,
                initial_stack_symbol=initial_stack_symbol, final_states=set(final_states))

