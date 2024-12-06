from collections import defaultdict
from pathlib import Path
import enum


ChunkType = enum.Enum("ChunkType", "type document row")
TokenType = enum.Enum("TokenType", "text lemma")
DocumentType = enum.Enum("DocumentType", 'accounts administration contracts declarations labels letters lists other paraliterary pronouncements receipts reports')

DOCUMENT_MAP = {
    DocumentType.accounts: 'accounts.txt',
    DocumentType.administration: 'administration.txt',
    DocumentType.contracts: 'contracts.txt',
    DocumentType.declarations: 'declarations.txt',
    DocumentType.labels: 'labels.txt',
    DocumentType.letters: 'letters.txt',
    DocumentType.lists: 'lists.txt',
    DocumentType.other: 'other.txt',
    DocumentType.paraliterary: 'paraliterary.txt',
    DocumentType.pronouncements: 'pronouncements.txt',
    DocumentType.receipts: 'receipts.txt',
    DocumentType.reports: 'reports.txt'
}

TOKEN_MAP = {
    TokenType.text: 'text', 
    TokenType.lemma: 'lemma'
}

MYPATH = Path(__file__).parent


def get_tokens_by_type(doc_type, token_type):
    output = {}
    print(type(token_type)) 
    # dict[line_ref] -> dict[token_type] -> list(tokens)
    target = ''
    if type(token_type) == tuple:
        for t in token_type:
            output = defaultdict(lambda : {TOKEN_MAP[t]: [] for t in token_type})
    else:
        target = TOKEN_MAP[token_type]
    with open(MYPATH / Path(DOCUMENT_MAP[doc_type]), 'r', encoding="UTF-8") as f:
        for line in f:
            if not line.strip():
                continue
            if type(token_type) == tuple: 
                for t in token_type:
                    target = TOKEN_MAP[t]
                    try:
                        ref, cons = line.strip().split(' ', maxsplit=1)
                        if ref.endswith(target):
                            output[ref.replace('.' + target, '')][target] = cons.split(' ')
                    except Exception as e:
                        print(line)
                        print(e)
                        exit()
            else:
                try:
                    ref, cons = line.strip().split(' ', maxsplit=1)
                    if ref.endswith(target):
                        output[ref.replace('.' + target, '')] = cons.split(' ')
                except:
                    print(line)
                    exit()
    if type(token_type) == tuple:
        out = {}
        for key, values in output.items():
            out[key] = list(zip(*[list(x) for x in values.values()]))
            print(out[key])
            exit()
        return out
    return output


def group_by_part_id(chunk_type, lines):
    output = defaultdict(list)
    for ref, words in lines.items():
        parts = ref.split('.')
        if chunk_type == ChunkType.type:
            output[parts[0]].extend(words)

        if chunk_type == ChunkType.document:
            output['.'.join(parts[0:2])].extend(words)
        elif chunk_type == ChunkType.row:
            output[ref].extend(words)
    return output

def get_tokens_by_chunk(document_type, token_type, chunk_type):
    rows = get_tokens_by_type(document_type, token_type)
    if chunk_type == ChunkType.row:
        return rows
    return group_by_part_id(chunk_type, rows)


if __name__ == '__main__':
    #print(get_tokens_by_type(DocumentType.accounts, token_type=TokenType.text))
    print(get_tokens_by_chunk(DocumentType.accounts, token_type=TokenType.text, chunk_type=ChunkType.document))
