from papyri_tools import DocumentType, TokenType, ChunkType, get_tokens_by_type
from pathlib import Path


MYPATH = Path(__file__).parent

TEMPLATE = (MYPATH / Path('scripts/template.html')).read_text()


def build_sentences(ss, opath):
    cons = [f'<h1>{opath[0].upper() + opath[1:]}</h1>']
    last_doc = ''
    for sent, words in ss.items():
        doc_id = sent.split('.')[1]
        if doc_id != last_doc:
            cons.append(f"<h2>{doc_id}</h2>")
            last_doc = doc_id
        cons.append('<p>' + ' '.join(words) + '.</p>')
    (MYPATH / Path(f'docs/{opath}.html')).write_text(TEMPLATE.replace('$body$', '\n'.join(cons)))

if __name__ == '__main__':
    for doc_type in DocumentType._member_map_.values():
        print(doc_type)
        build_sentences(get_tokens_by_type(doc_type, TokenType.text), doc_type._name_)
    # print(' '.join([e.value for e in DocumentType]))



