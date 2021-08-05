try:
    from models import Document
    from lootnika import sout
except:
    from ..models import Document
    from ..lootnika import sout

from logging import Logger


def handler(doc: "Document", vars):
    log: "Logger" = vars['log']
    put_new_doc = vars['put_new_doc']

    doc.fields['reference'] = doc.reference
    doc.fields['import_date'] = doc.create_dtm

    fieldName = 'files'

    files: [dict] = doc.get_field(fieldName)
    if files:
        for file in files:
            newDoc = Document(
                taskId=doc.taskId,
                taskName=doc.taskName,
                reference=f'file_{doc.reference}_{file["id"]}',
                loootId=f'',
                fields=file
            )
            
            newDoc.export = 'post_file'
            put_new_doc(newDoc)

            newDoc.export = 'post_file_info'
            del newDoc.fields['content']
            put_new_doc(newDoc)
            
        del doc.fields['files']
    else:
        log.warning(f'Not found {fieldName} in document {doc.reference}')

    return doc
