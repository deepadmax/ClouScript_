from rich import print

import clouscript


text = """
curse(true, 10)
hearts(-1)
""".strip()

print(f'{text}\n')

elements = clouscript.loads(text)
print(elements.asstring())