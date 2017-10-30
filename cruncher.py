from reader import reader
from schema import schema
from survey import survey
from vparser import vparser

class cruncher:
    def __init__(self):
        survey = survey()
        vparser = vparser(
            survey.data,
            cannotSplinter={'Country','Gender'},
            splinterPartial={}
        )

if __name__ == '__main__':
    instance = cruncher()
