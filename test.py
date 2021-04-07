import clouscript


text = """doif (
    /* Three if-statements followed by an else-statement */
    
    CHANNEL.name == "General" (
        3 + (1 * 2)
    )

    USER has not 1235 (
        statement2
    )

    USER is 4569 (
        statement3
    )
    
    ( 
        statement4// This is the else-statement
    )
)"""

elements = clouscript.loads(text)
print(elements)