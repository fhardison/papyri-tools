# Papyri Tools

This repository is modeled on James's Tauber's [`vocabulary-tools`](https://github.com/jtauber/vocabulary-tools) module for the Greek New Testament, but is for the Greek Papyri taken from the Duke Databank of Digital Papyri. It provides a similar API as well. The main difference is that the papyri are sorted by document type and because the files are large, there is not generic `get_tokens` function. to do that call `get_tokens_by_type` for each `DocumentType`.

See `main.py` in `papyri_tools` or `build_html.py` in to see how it works.

Included in the `docs` folder are html versions of the documents with Alpheios Reading Tools built in.

# Source

data taken from [duke-nlp project repo](https://github.com/alekkeersmaekers/duke-nlp/tree/master) which is under a [CC BY-SA 4.0 License](https://creativecommons.org/licenses/by-sa/4.0/) which got it from [Duke Databank of Digital Papyri](https://github.com/papyri/idp.data) which is under a [CC BY 3.0](https://creativecommons.org/licenses/by/3.0/) license. The duke-nlp repo requests that it be cited as follows, which I'm doing:  

> Keersmaekers, Alek, and Mark Depauw. Forthcoming. “Bringing Together Linguistics and Social History in Automated Text Analysis of Greek Papyri.” Classics@. 

# License

This repo is also under a [CC BY-SA 4.0 License](https://creativecommons.org/licenses/by-sa/4.0/). 
