from Screener.Analyzer import Analyzer, Reasons, Profile
from Screener.User import User
from os import path

class reportGenerator:

    def __init__(self, user, reasons, profile):

        self.name = user.firstName
        self.reasons = reasons
        self.ticker = profile.ticker
        self.co_name = profile.co_name

        #TODO function that generates path
        self.img_path = "images/graph.png"
        self.report_path = None
        self.written = None

    def generate_report(self):

        print("Creating report for:", self.name)
        salutation = "Dear "+self.name
        intro = "We found a company called **COMPANY** that we think might be a good investment for you.\n " \
                "There are a few characteristics to look before you decide to buy! "

        intro = "When it comes to investing, time is on your side.  Time gives you the oppurtunity " \
                "to ride out downturns and build up your portfolio; " \
                "However, young adults often forget to save for retirement.  " \
                "The earlier you begin, the more time your savings will have to grow in " \
                "value and the more likely you are to achieve your investing goals.  " \
                "Thats why we have put together a personalized form for you to get started " \
                "regardless of experience level."
        #TODO

        en_reasons = []

        for i in self.reasons:

            if en_reasons:
                first = "We started by looking "

            else:
                first = "First, we looked"

            second =" at "+ self.co_name +'s '+ i.measure + " and we liked their value of " + str(i.value) + "\n"\
            + str(i.language)

            item = first + second

            en_reasons.append(item)

        px_chart = "We also pulled their price movement over the last year which we think you'll find interesting"

        closing = "Always be sure to invest wisely!"

        print(en_reasons)

        basepath = path.dirname(__file__)
        filepath = path.abspath(path.join(basepath,"..","EmailClient", "report_test.txt"))
        file = open(filepath, "w")
        print(filepath)

        file.write(salutation)
        file.write(intro)

        for i in en_reasons:
            file.write(i)

        file.write(px_chart)
        file.write(self.img_path)
        file.write(closing)

        self.written = en_reasons

        self.report_path = filepath