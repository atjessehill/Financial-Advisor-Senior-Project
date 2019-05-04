from Screener.UserRisk import UserRisk
from Screener.Screen import Screen
import pandas as pd
from Screener.Analyzer import Analyzer
import json
import random

class User:

    def __init__(self, email, fname, lname, risk, knowledge):
        # self.risk = UserRisk.riskScore
        self.firstName = fname
        self.lastname = lname
        self.fullName = fname + " " +lname
        self.risk_number = risk
        self.email = email

        if risk <=5:
            self.risk_profile = "Defensive"
        elif risk > 5:
            self.risk_profile = "Risky"

        if knowledge <= 5:
            self.knowledge = "Beginner"
        elif knowledge > 5:
            self.knowledge = "Advanced"

        self.demo_screen = None
        self.risk_score = None
        self.investing_knowledge = knowledge
        self.age = None
        self.income = None
        self.financialGoals = None
        self.incomeNeeds = None
        self.industry_preference = None # []
        self.screens = {"Risky": None, "Moderate": None, "Defensive": None}

    def setup_profile(self, risk_profile=5, investing_knowledge=0, interests="Tech"):

        self.risk_profile = risk_profile
        self.investing_knowledge = investing_knowledge
        self.industry_preference = interests

    def generate_screen_url(self):

        for key, value in self.screens.items():
            if value == None:
                new_screen = Screen()
                new_screen.get_url(key, self.risk_number, 'Tech')
                self.screens[key] = new_screen

    def generate_screen_url_demo(self):

        r = ["Technology", "Financial", "Consumer+Goods"]
        m = ["Basic+Materials", "Industrial+Goods", "Utilities", "Healthcare"]

        if self.risk_profile == "Risky":
            sector = random.choice(r)
        else:
            sector = random.choice(m)

        new_screen = Screen()
        self.demo_screen = new_screen.get_url_demo(self.risk_profile, "null", sector)

    def run_all_empty_screen(self):
        print("run all empty screen")
        for key, screen in self.screens.items():
            if screen.executed == False:
                screen.run_screen()

    def get_all_screen_results(self):
        for key, screen in self.screens.items():
            print(screen.__str__())

    def user_to_json(self):

        user_profile = {'UserInfo':{'risk_profile': self.risk_profile, "risk_score" : self.risk_score, 'investing_knowledge' : self.investing_knowledge, 'industries:': self.industry_preference, 'age': self.age, 'income':self.income, 'financialGoal':self.financialGoals}}
        screen_dict = {}
        for key, screen in self.screens.items():
            screen_dict[key] = screen.to_dict()

        user_profile.update(screen_dict)
        user_profile = json.dumps(user_profile)
        user_json = json.loads(user_profile)

        return user_json


    def user_to_json_demo(self):

        # user_profile = {'UserInfo':{'risk_profile': self.risk_profile, "risk_score" : self.risk_score,
        # 'investing_knowledge' : self.investing_knowledge, 'industries:': self.industry_preference, 'age': self.age,
        # 'income':self.income, 'financialGoal':self.financialGoals}}

        user_profile = {'risk_profile': self.risk_profile, 'email': self.email, 'knowledge': self.knowledge, 'screen': self.demo_screen}

        user_profile = json.dumps(user_profile)
        user_json = json.loads(user_profile)

        return user_json
