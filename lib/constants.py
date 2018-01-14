import re

CRUNCHER_PATHS = {
    'SCHEMA': 'survey_results_schema.csv',
    'PUBLIC': 'survey_results_public.csv'
}

CRUNCHER_FIELDS = {
    'Gender',
    'WantWorkLanguage',
    'Country',
    'Salary'
}

DISTRIBUTE_SPLIT_FIELDS = False

DEBUG = {
    'DEBUG_READ_SCHEMA': False, # Prints all the questions
    'DEBUG_READ_PUBLIC': False, # Breaks execution ????
    'DEBUG_MAKE_VALUES_SCHEMA': False,
    'DEBUG_MAKE_VALUES_FREQUENCIES': False # Dumps all the frequencies of all the data's possible values
}

def numerify(str):
    if isNumeric(str):
        if 'e' in str:
            parts = str.split('e')
            if len(parts) > 2:
                raise Exception("Too many 'e's in this string to numerify: %s" % str)
            power = float(parts[1])
            base = float(parts[0])
            number = base * (10 ** power)
            return number
        else:
            return float(str)
    else:
        raise Exception("I ain't gonna numerify this: %s" % str)

numericality = re.compile("[0-9\.e]+")
def isNumeric(str):
    return numericality.match(str)
