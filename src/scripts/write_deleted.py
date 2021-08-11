import os

try:
    from models import Document
    from lootnika import sout
except:
    from ..models import Document
    from ..lootnika import sout

from logging import Logger


def handler(doc: "Document", vars):
    fName = f'outgoing/{doc.taskName}/deleted.txt'

    if os.path.exists(fName):
        mode = 'a'
    else:
        mode = 'w'

    with open(fName, mode=mode) as f:
        f.write(f"{doc.reference},")

    return None
