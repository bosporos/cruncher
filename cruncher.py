from lib import reader
from lib import schema
from lib import survey
from lib import vparser

from lib.func import f_cgl 

class cruncher:
    def __init__(self):
        self.survey = survey.survey()
        self.vparser = vparser.vparser(
            self.survey.data,
            cannotSplinter={'Country'},
            splinterPartial={'Gender': 'm/f/o'}
        )

if __name__ == '__main__':
    instance = cruncher()
    
    f_cgl.cgl_perform(instance.survey.data, instance.vparser)
