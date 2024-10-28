import csv
from ProductionCode.datasource import *

database_accessor = DataSource()

class BirthControl:

    def __init__(self):

        self.data = []
        self.load_data()

    def display_results(self, totaled_answers):
        """
        Iterates through a dictionary to output the dataset answers
        and their percentage values to the user. Returns totaled_answers,
        which is the dictionary of possible answers and their percentages.
        The parameter being passed in is the same as totaled_answers above.
        """
        for response in totaled_answers:
            print(response, ":",totaled_answers[response], "%")
        return totaled_answers


    def load_data(self):
        """
        Opens birthcontroldata.csv and reads it into a list of lists.
        """
        self.data.clear()
        csvfile = open('Data/birthcontroldata.csv')
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in reader:
            self.data.append(row)
        csvfile.close()

    def get_use_of_birth_control_by_demographic(self, demographic):
        """
        Retrieves the user ids of the specified demographic in order to
        total up the use of birth control for those user ids. Then, the results
        are counted and displayed as percentages. 
                Parameters:
                    demographic = the string demographic the user selected and put
                    in either the command line or the url. 
        Returns the dictionary of answers and their percentage results after being displayed. 
        """
        responses = database_accessor.get_use_column_by_demographic(demographic)
        results = self.count_birth_control_use_answers(responses)
        percent_results = self.calc_percentage(results)
        return self.display_results(percent_results)

    def get_birth_control_access_concerns_by_demographic(self, demographic):
        """
        Retrieves the user ids of the specified demographic in order to
        total up the answers for the concern level of access to birth control
        for those user ids. Then, the results are counted and displayed as percentages. 
                Parameters:
                    demographic = the string demographic the user selected and put
                    in either the command line or the url. 
        Returns the dictionary of answers and their percentage results after being displayed. 
        """
        responses = database_accessor.get_access_column_by_demographic(demographic)
        results = self.count_birth_control_access_answers(responses)
        percent_results = self.calc_percentage(results)
        return self.display_results(percent_results)

    def count_birth_control_use_answers(self, use_answers):
        """
        Counts the amount of each possible response to the use question in the dataset
        regarding birth control use for the appropriate list of users based on inputted demographic.
        Then, compiles a dictionary of each possible response and the amount of times that
        response was chosen. 
            Parameters:
                use_answers = the list of answers to the question about birth control use
                from the people in the specified demographic.
        Returns the dictionary totaled_answers which includes the amount of each possible response
        for the question of birth control use.
        """
        never=0
        na=0
        always=0
        half=0
        some=0
        almost=0
        refused=0

        totaled_answers={}
        for item in use_answers:
            if item == ('Never',):
                never=never+1
            elif item== ('Not applicable/Does not have vaginal intercourse/sex',):
                na= na+1
            elif item == ('Every time',):
                always= always+1
            elif item == ('About half the time',):
                half=half+1
            elif item== ('Once in a while',):
                some= some+1
            elif item == ('Almost every time',):
                almost= almost+1
            else:
                refused=refused+1
        totaled_answers["Never"]=never
        totaled_answers["Not applicable/Does not have vaginal intercourse/sex"]=na
        totaled_answers["Every time"]=always
        totaled_answers["About half the time"]=half
        totaled_answers["Once in a while"]=some
        totaled_answers["Almost every time"]=almost
        return totaled_answers

    def count_birth_control_access_answers(self, access_answers):
        """
        Counts the amount of each possible response to the access question in the dataset
        regarding concerns about future access to birth control for the appropriate list 
        of users based on inputted demographic. Then, compiles a dictionary of each possible 
        response and the amount of times that response was chosen. 
            Parameters:
                access_answers = the list of answers to the question about birth control access concerns
                from the people in the specified demographic.
        Returns the dictionary totaled_answers which includes the amount of each possible response
        for the question of birth control access concerns.
        """
        veryConcerned=0
        somewhatConcerned=0
        notVeryConcerned=0
        notAtAllConcerned=0
        notApplicable=0
        dontKnow=0
        refused=0

        totaled_answers={}
        for item in access_answers:
            if item == ('Very concerned',):
                veryConcerned=veryConcerned+1
            elif item== ('Not applicable/don\'t believe in birth control',):
                notApplicable= notApplicable+1
            elif item == ('Somewhat concerned',):
                somewhatConcerned= somewhatConcerned+1
            elif item == ('Not very concerned',):
                notVeryConcerned=notVeryConcerned+1
            elif item== ('Not at all concerned',):
                notAtAllConcerned=notAtAllConcerned+1
            elif item == ('Don\'t know',):
                dontKnow=dontKnow+1
            else:
                refused=refused+1
        totaled_answers["Very concerned"]=veryConcerned
        totaled_answers["Not applicable/don't believe in birth control"]=notApplicable
        totaled_answers["Somewhat concerned"]=somewhatConcerned
        totaled_answers["Not very concerned"]=notVeryConcerned
        totaled_answers["Not at all concerned"]=notAtAllConcerned
        totaled_answers["Don't know"]=dontKnow
        totaled_answers["Refused"]=refused
        return totaled_answers

    def calc_percentage(self, totaled_answers):
        """
        Calculates the percentage of each possible response to the question in the dataset.
            Parameters:
                totaled_answers = the dictionary including each possible response and the
                amount of times that response was chosen by people in the dataset.
        Returns the same dictionary, but formatted based upon percentages instead of total responses.
        """
        total=0
        if totaled_answers == {}:
            print("Dictionary is empty, try again.")
            return {}
        for response in totaled_answers:
            total=total+totaled_answers[response]
        for response in totaled_answers:
            if total!=0:   
                totaled_answers[response]= round((totaled_answers[response]/total)*100)
        return totaled_answers