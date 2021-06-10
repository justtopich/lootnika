try:
    from taskstore import Document
except:
    from ..taskstore import Document


# def filter_fields(doc):



def handler(doc:Document, vars):
    print(f'Transform task get {doc.reference}')

    put_new_doc = vars['put_new_doc']

    doc.fields['ref'] = doc.reference
    doc.fields['import_date'] = doc.create_dtm

    for post in doc.get_field('posts')[0]:
        postDoc = Document(doc.taskName, f'{doc.reference}-{post["post_id"]}', '1', post)
        postDoc.fields = post
        postDoc.fields['ref'] = postDoc.reference
        put_new_doc(postDoc)

    # del doc.fields['posts']
    return False
