# TBFSBS (Text-Based Format for Storing Biological Sequences)

---

Parse TBFSBS (Text-Based Format for Storing Biological Sequences) file[s].

Parser reads the file(s) and print the header and the 
sequence length of all sequences in the file(s). Parser also
have the option to write the TBFSBS sequences back into an
output file, with configurable maximum length of the
sequence line.

Header format:

- begins with the percentage symbol (%)
- the identifier: string
- a numeric target value: integer or float or null
- the description: string (can contain whitespace)

------

## Prerequisites

[Python 3][python]<br>

------

## Usage

```
parse.py [-h] [-o [OUTPUT]] [-w [WRAP]] input_files [input_files ...]
```
Positional arguments:

>**`input_files`**              List of input file names or folder[s] with file[s]

Optional arguments:

>**`-h`, `--help`**           show a help message<br>
>**`-o [OUTPUT]`, `--output [OUTPUT]`**           Output file name<br>
>**`-w [WRAP]`, `--wrap [WRAP]`**           Maximum length of the sequence line<br>

```
python parse.py -output output.txt -wrap 150 MySequences.txt MySequences_2.txt MySequences_Folder/
```

------

[python]: https://www.python.org/
