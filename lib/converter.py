from outparser import outparser
from reader import reader
from schema import schema
from survey import survey

survey = survey()
out = outparser('out.csv')
out.write(survey.data)
