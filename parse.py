#!/usr/bin/env python3
import os
import argparse
import textwrap
from pathlib import Path
from collections.abc import MutableSequence

"""
Parse TBFSBS (Text-Based Format for Storing Biological Sequences):

The parser reads the file(s) and print the header and the 
sequence length of all sequences in the file(s). Parser also
have the option to write the TBFSBS sequences back into an
output file, with configurable maximum length of the
sequence line.

Header format:

    . begins with the percentage symbol (%)
    . the identifier: string
    . a numeric target value: integer or float or null
    . the description: string (can contain whitespace)

"""

class TBFSBS_Record():
    """Class representing one sequence in TBFSBS format.

    This class represents one sequence in a TBFSBS file.
    The entry has the header with identifier, target value,
    and description, as well the biological sequence.
    The representation of the class objects as a string
    prints the TBFSBS record id, value, description and 
    the sequence length.
    """

    def __init__(self, identifier = None, target_value = None,
                description = None , sequence = None):
        """Initialize class TBFSBS Record.

        This function initialize the TBFSBS record object 
        with the identifier, target value, description,
        and the sequence.

        Parameters
        -------------
        identifier: str
            The identifier of the sequence
        target_value: float
            A numeric target value
        description: str
            A description for the record
        sequence: str
            The biological sequence

        """

        self.identifier = identifier
        self.target_value = target_value
        self.description = description
        self.sequence = sequence

    def __str__(self):
        """Override representation of the class
        objects as a string.

        This function overrides the representation of the
        class objects as string in a format with the Id,
        value, description, and sequence length.
        See the example below:

            ID: Id1
            Value: 2.5
            Description: My description
            Sequence length: 502

        """

        value = self.target_value
        if self.target_value:
            value = round(self.target_value, 1)            

        record_str = "ID: {ID}\n"\
                    "Value: {TARGET_VALUE}\n"\
                    "Description: {DESCRIPTION}\n"\
                    "Sequence length: {SEQ_LENGTH}\n".format(
                        ID = self.identifier,
                        TARGET_VALUE = value,
                        DESCRIPTION = self.description,
                        SEQ_LENGTH = len(self.sequence))

        return record_str

class TBFSBS(MutableSequence):
    """Class representing TBFSBS file sequences.
    
    This class represents all sequences in [a]
    TBFSBS file[s]. The class uses the TBFSBS Record
    class to represent each sequence in the file[s].
    """

    def __init__(self):
        """Initialize class TBFSBS.

        This function initialize the TBFSBS object 
        with a list to store all sequence
        from the file[s].

        """

        super(TBFSBS, self).__init__()
        self._list = list()

    def __len__(self):
        return len(self._list)

    def __getitem__(self, i):
        return self._list[i]

    def __delitem__(self, i):
        del self._list[i]

    def __setitem__(self, i, value):
        self._list[i] = value

    def __str__(self):
        """Override representation of the class
        objects as a string.

        This function overrides the representation of the
        class objects as string with the list of TBFSBS
        records.

        """

        records_str = ""
        for record in self._list:
            records_str += "{RECORD}\n".format(RECORD = record)

        return records_str

    def insert(self, i, value):
        self._list.insert(i, value)

    def append(self, value):
        self._list.append(value)

    def extend(self, value):
        self._list.extend(value)

    def parse(self, input_file):
        """Parse sequences from file.

        This function parses sequences from the file.
        It searches for the line that begins with
        the % character, which represents the header,
        and parses each part of the header structure
        (identifier, target value, and description)
        and sequence.

        Parameters
        -------------
        input_file: str
            The input file name

        """

        with open(input_file) as tbfsbs_file:

            header = ""
            for row in tbfsbs_file:

                if row.startswith("%"):

                    if header:
                        record = TBFSBS_Record(iD,
                                        target_value,
                                        description,
                                        seq)
                        self.append(record)

                    header = row.split()
                    iD = header[1]

                    try:
                        target_value = float(header[2])
                        description = " ".join(header[3:])
                    except:
                        target_value = None
                        description = " ".join(header[2:])

                    seq = ""
                    
                else:
                    seq += row.rstrip()
            else:
                record = TBFSBS_Record(iD,
                                target_value,
                                description,
                                seq)
                self.append(record)

    def write(self, output_file, wrap):
        """Write sequences to a file.

        This function writes all TBFSBS sequences
        parsed from the file[s] back into an
        output file with configurable maximum
        length of the sequence line.
        .

        Parameters
        -------------
        output_file: str
            The output file name
        wrap: int
            Maximum length of the sequence line

        """

        records_str = ""
        for record in self._list:

            value = ""
            if record.target_value:
                value = "{TARGET_VALUE} ".format(
                            TARGET_VALUE = record.target_value)

            records_str += "% {ID} {TARGET_VALUE}"\
                        "{DESCRIPTION}\n{SEQUENCE}\n".format(
                            ID = record.identifier,
                            TARGET_VALUE = value,
                            DESCRIPTION = record.description,
                            SEQUENCE = textwrap.fill(
                                        record.sequence, wrap))
        
        output_file.write(records_str[:-1])
                


def getArguments():
    """Get arguments from terminal

    This function gets arguments from terminal via argparse

    Returns
    -------------
    arguments: Namespace
        Namespace object with all arguments
    """

    parser = argparse.ArgumentParser(
        description="Parse TBFSBS (Text-Based Format for" \
                    " Storing Biological Sequences) file[s].")
    parser.add_argument("input_files", nargs="+", type = str,
                    help = "List of input file names or" \
                    " folder[s] with file[s]")
    parser.add_argument("-o", "--output", nargs = "?",
                    type = argparse.FileType("w"),
                    help = "Output file name.")
    parser.add_argument("-w", "--wrap", nargs = "?",
                    const = float("inf"), type = int,
                    default = float("inf"),
                    help = "Maximum length of the sequence line.")

    return parser.parse_args()


if __name__ == "__main__":
    args = getArguments()

    tbfsbs = TBFSBS()
    input_files = args.input_files

    for input_file in input_files:

        if os.path.isdir(input_file):
            files = list(Path(input_file).rglob("*"))
            input_files.extend(files)
            continue


        print("File: {FILE_NAME}\n".format(
                                FILE_NAME = input_file))

        file = TBFSBS()
        file.parse(input_file)
        print(file)

        tbfsbs.extend(file)

    if args.output:
        tbfsbs.write(args.output, args.wrap)