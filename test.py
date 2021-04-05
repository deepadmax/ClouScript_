from clouscript.lexer import Token


def print_tokens(x, indent=0):
    if type(x) is Token:
        if type(x.value) in (list, tuple) or \
          (type(x.value) is Token and x.value.name == 'LIST'):
            print(' '*indent + f'┗━ {x.name}({len(x.value)})')
            
            print_tokens(x.value, indent=indent+1)
            
        else:
            print(' '*indent + f'┗━ {x.name}={repr(x.value)}')
            
    elif type(x) in (list, tuple):
        # print(' '*indent + f'\\_')
        for t in x:
            print_tokens(t, indent=indent+1)
    
    else:
        print(' '*indent + f'<? {type(x).__name__}: {x}>')


text = """
doif (
    /* Three if-statements followed by an else-statement */
    
    CHANNEL.name == "General" (
        3 + (1 * 2)
    )

    USER has not @&1235 (
        statement2
    )

    USER is @4569 (
        statement3
    )
    
    ( 
        statement4// This is the else-statement
    )
)
"""

