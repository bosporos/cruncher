from outparser import outparser
from reader import reader
from schema import schema
from survey import survey

def writeTexableOut(data):
    print "\\begin{center}"
    print "\\begin{tabular}{ |c|c|c|c| }"
    for row in data:
        print row['Salary'],' & ',
        print row['Gender'],' & ',
        print row['WantWorkLanguage'].replace('#','\\#'),' & ',
        print row['Country'],' \\\\ '
    print "\\end{tabular}"
    print "\\end{center}"

def writeTexableOutNoSalary(data):
    print "\\begin{center}"
    print "\\begin{tabular}{ |c|c|c| }"
    for row in data:
        print row['Gender'],' & ',
        print row['WantWorkLanguage'].replace('#','\\#'),' & ',
        print row['Country'],' \\\\ '
    print "\\end{tabular}"
    print "\\end{center}"


survey = survey()
out = outparser('out.csv')
out.write(survey.data)
#writeTexableOut(survey.data)
#for n in range(2):
#    print "#"*80
#print ("#" * 30) + "#### NO SALARY! ####" + ("#" * 30)
#for n in range(2):
#    print "#"*80
writeTexableOutNoSalary(survey.data)
