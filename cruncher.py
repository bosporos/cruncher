from lib import reader
from lib import schema
from lib import survey
from lib import vparser

from lib.func import f_cgl
from lib.func import f_RG
from lib.func import f_gl

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
#    f_cgl.cgl_perform(instance.survey.data, instance.vparser)
    f_RG.RG_perform(instance.survey.data, instance.vparser)
#    f_gl.gl_perform(instance.survey.data, instance.vparser)
    
#    frequencies = instance.vparser.frequencies['Country']
#    taken = set()
#    top = {}
#    for counter in range(20):
#        highest = 0
#        which_highest = ''
#        for country in frequencies:
#            frequency = frequencies[country]
#            if frequency > highest and country not in taken:
#                highest = frequency
#                which_highest = country
#        top[counter] = (which_highest, highest)
#        taken.add(which_highest)
#    for position in top:
#        print "%s & %i \\\\" % (top[position][0], top[position][1])
