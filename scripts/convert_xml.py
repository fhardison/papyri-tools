# ///script
# dependencies = [ "lxml"]
# ///
from collections import defaultdict
import xml.etree.ElementTree as ET
import os
import sys


def parse_xml_sentences_old(xml_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()
    documents = {}
    sentences_dict = {}
    last_doc = ''
    rows_dict = {}
    doc_id = ''
    for sentence in root.findall('sentence'):
        doc_id = sentence.get('document_id')
        if last_doc != doc_id:
            if last_doc != '':
                documents[last_doc] = sentences_dict
                documents[last_doc] = rows_dict
                if last_doc == '31133':
                    print(len(list(sentences_dict.items())), file=sys.stderr)
                    print(sentences_dict, file=sys.stderr)
                    print(rows_dict, file=sys.stderr)
                # print('new doc', file=sys.stderr)
                sentences_dict = {}
                rows_dict = {}
            last_doc = doc_id
        sentence_id = sentence.get('id')
        sentence_info = {}
        for word in sentence.findall('word'):
            row = word.get('row')
            if not row:
                #print("Row missing", file=sys.stderr)
                continue
            lemma = word.get('lemma', '_')
            normalized = word.get('regularized', '')
            if lemma == '_' or 'gap' in normalized:
                normalized= '[...]'

            word_tuple = (lemma, normalized.replace('|apostrophe|', ''))
            
            if row:
                if row not in sentence_info:
                    sentence_info[row] = []
                    rows_dict[row] = []
                sentence_info[row].append(word_tuple)
                rows_dict[row].append(word_tuple)
        sentences_dict[sentence_id] = sentence_info
    if doc_id != '' and doc_id not in documents:
        documents[doc_id] = rows_dict
        
    return documents



def parse_xml_sentences(xml_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()
    documents = defaultdict(dict)
    last_doc = ''
    doc_id = ''
    for sentence in root.findall('sentence'):
        for word in sentence.findall('word'):
            row = word.get('row')
            docid = word.get('texid')
            if (not row) or (not docid):
                #print("Row missing", file=sys.stderr)
                continue
            lemma = word.get('lemma', '_')
            normalized = word.get('regularized', '')
            if lemma == '_' or 'gap' in normalized:
                normalized= '[...]'
            word_tuple = (lemma, normalized.replace('|apostrophe|', ''))
        
            if row:
                if not row in documents[docid]:
                    documents[docid][row] = []
                documents[docid][row].append(word_tuple)
    return documents

files = [("Papyri_Accounts.xml", 'accounts'),
("Papyri_Administration.xml", 'administration'),
("Papyri_Contracts1.xml", 'contracts'),
("Papyri_Contracts2.xml", 'contracts'),
("Papyri_Contracts3.xml", 'contracts'),
("Papyri_Declarations1.xml", 'declarations'),
("Papyri_Declarations2.xml", 'declarations'),
("Papyri_Labels.xml", 'labels'),
("Papyri_Letters1.xml", 'letters'),
("Papyri_Letters2.xml", 'letters'),
("Papyri_Letters3.xml", 'letters'),
("Papyri_Lists1.xml", 'lists'),
("Papyri_Lists2.xml", 'lists'),
("Papyri_Lists3.xml", 'lists'),
("Papyri_Lists4.xml", 'lists'),
("Papyri_Other.xml", 'other'),
("Papyri_Paraliterary.xml", 'paraliterary'),
("Papyri_Pronouncements.xml", 'pronouncements'),
("Papyri_Receipts1.xml", 'receipts'),
("Papyri_Receipts2.xml", 'receipts'),
("Papyri_Reports.xml", 'reports')]

def clear_files():
    for fdata in files:
        with open(f'../papyri_tools/{fdata[1]}.txt', 'w', encoding="UTF-8") as f:
            f.write('')


def process_files_old(fpath, genre):
    try:
        #if os.path.exists('')
        with open(f'../papyri_tools/{genre}.txt', 'a', encoding="UTF-8") as f:
            # Replace 'your_xml_file.xml' with the actual path to your XML file
            parsed_sentences = parse_xml_sentences(f'../source/{fpath}')
            print(len(parsed_sentences), file=sys.stderr)
            for docid, sentences in parsed_sentences.items():
                for sent_id, rows in sentences.items():
                    for rowid, words in rows.items():
                        forms = []
                        lemmas = []
                        for (lemma, normalized) in words:
                            lemmas.append(lemma)
                            forms.append(normalized)
                        print(f"{genre}.{docid}.{sent_id}.{rowid}.text {' '.join(forms)}", file=f)
                        print(f"{genre}.{docid}.{sent_id}.{rowid}.lemmas {' '.join(lemmas)}", file=f)
    except ET.ParseError as e:
        print(f"Error parsing XML: {e}")
    except FileNotFoundError:
        print("XML file not found.")


def toint(x):
    if '-' in x:
        return int(x.split('-')[-1])
    else:
        return int(x)

def process_files(fpath, genre):
    try:
        #if os.path.exists('')
        with open(f'../papyri_tools/{genre}.txt', 'a', encoding="UTF-8") as f:
            # Replace 'your_xml_file.xml' with the actual path to your XML file
            parsed_sentences = parse_xml_sentences(f'../source/{fpath}')
            print(len(parsed_sentences.items()), file=sys.stderr)
            for docid, rows in parsed_sentences.items():
                for rowid, words in rows.items():
                    forms = []
                    lemmas = []
                    for (lemma, normalized) in words:
                        lemmas.append(lemma)
                        forms.append(normalized)
                    print(f"{genre}.{docid}.{rowid}.text {' '.join(forms)}", file=f)
                    print(f"{genre}.{docid}.{rowid}.lemmas {' '.join(lemmas)}", file=f)
    except ET.ParseError as e:
        print(f"Error parsing XML: {e}")
    except FileNotFoundError:
        print("XML file not found.")

clear_files()

#process_files("Papyri_Letters3.xml", 'letters')
#exit()
for fdata in files:
    print(fdata, file=sys.stderr)
    process_files(fdata[0], fdata[1])
