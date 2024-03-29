import pandas as pd
from Screener import test_screen_results, close_px_results, GraphBuilder, data_point_results
import urllib.request
import json
import datetime
import os

debug = False

class ReportGenerator:

    def __init__(self, profile):
        self.profile = profile

        for i in profile.reasons:
            print(i.measure, i.value, i.impact)

class Reasons:

    def __init__(self, measure, value, language):
        self.measure = measure
        self.value = value
        self.language = language

class Profile:

    def __init__(self, ticker, reasons, co):
        self.ticker = ticker
        self.reasons = reasons
        self.finance_reasons = None
        self.co_name = co

    def __str__(self):

        return self.ticker

class Analyzer:

    def __init__(self, user_info):
        # TODO Analyze one screen at a time, so only pass in user profile and one screen. Current setup
        #  will only run the screen that matches the user profile. Ex: UserProfile.Defensive == Screen.Defensive
        testing = False
        self.profile_info = user_info['UserInfo']
        self.objective = self.profile_info['risk_profile']
        risky_screen = user_info['Risky']
        mod_screen = user_info['Moderate']
        def_screen = user_info['Defensive']
        self.screens = [risky_screen, mod_screen, def_screen]
        self.fundamental_values = []
        self.companies = None
        self.company_profile = None

        if debug:
           excelpath = os.path.abspath(os.path.join('frontend/static/Fundamental_Info.xlsx'))

        else:
            excelpath = os.path.abspath(os.path.join('frontend/static/Fundamental_Info.xlsx'))

        self.excel_sheet = pd.read_excel(excelpath, sheet_name="Sheet1")
        self.tags = []
        self.finance_reasons = []
        self.img_path = None


        # Only runs screen that matches user's profile
        if not testing:
            for i in self.screens:
                if self.profile_info['risk_profile'] == i['Objective']:
                    self.screen_results = self.run_screen(i)

        else:
            self.screen_results = test_screen_results.test_3


        #TODO REMOVE
        self.screen_results = test_screen_results.test_3

    def __init__(self, user_info, test):
        # TODO Analyze one screen at a time, so only pass in user profile and one screen. Current setup
        #  will only run the screen that matches the user profile. Ex: UserProfile.Defensive == Screen.Defensive
        print("Demo analyzer")

        self.risk_profile = user_info['risk_profile']
        self.knowledge = user_info['knowledge']
        self.screen = user_info['screen']

        if debug:
           excelpath = "Fundamental_Info.xlsx"

        else:
            excelpath = os.path.abspath(os.path.join('frontend/static/Fundamental_Info.xlsx'))

        self.excel_sheet = pd.read_excel(excelpath, sheet_name="Sheet1")

        self.screen_results = self.run_screen_demo(self.screen)

    def run_screen_demo(self, url):
        print(url)
        contents = urllib.request.urlopen(url)
        decode = contents.read().decode('utf-8')
        json_obj = json.loads(decode)
        return json_obj['data']

    def run_screen(self, screen_info):
        url = screen_info['URL']
        contents = urllib.request.urlopen(url)
        decode = contents.read().decode('utf-8')
        json_obj = json.loads(decode)
        return json_obj['data']

    def defensive_analyzer(self):

        # TODO
        # sort by each criteria, get median company from each and build scoring system of those 3-10 companies
        companies = self.companies

        companies.sort_values(by=['debttoequity'], ascending=True)
        row = int(len(companies.index) / 2)

        company_selection = companies.iloc[row].to_dict()
        ticker = company_selection['ticker']
        company = company_selection['security_name']
        del company_selection['ticker']
        del company_selection['security_name']

        list_reasons = []

        # TODO differentiate between positive, negative, neutral
        for key, value in company_selection.items():
            reason = Reasons(key, value, "positive")
            list_reasons.append(reason)

        self.company_profile = Profile(ticker, list_reasons, company)
        print("Defensive Choice:", self.company_profile.__str__())


    def risky_analyzer(self):

        companies = self.companies

        companies.sort_values(by=['revenuegrowth'], ascending=False)
        row = int(len(companies.index) / 2)

        company_selection = companies.iloc[row].to_dict()
        print(company_selection)
        ticker = company_selection['ticker']
        company = company_selection['security_name']

        del company_selection['ticker']
        del company_selection['security_name']

        list_reasons = []

        # TODO differentiate between positive, negative, neutral
        for key, value in company_selection.items():
            reason = Reasons(key, value, "positive")
            list_reasons.append(reason)

        self.company_profile = Profile(ticker, list_reasons, company)
        print("Risky Choice:", self.company_profile.__str__())


    def graph_price(self):

        identifier = self.company_profile.ticker
        now = datetime.datetime.now()
        end_date = now.date()
        start_date = (now - datetime.timedelta(days=365)).date()

        logic = "https://api-v2.intrinio.com/securities/"+identifier+"/prices?start_date=" + str(start_date) + "&end_date=" + str(end_date) + "&frequency=daily&page_size=365"
        url = logic + "&api_key=OmRhNGVlMTlhZGQ5ZWVmOTdiZTAwOWY3NjNjZGI1OTNi"

        if debug:
            close_prices = pd.DataFrame(close_px_results.test_close_px)
        else:
            contents = urllib.request.urlopen(url)
            decode = contents.read().decode('utf-8')
            dict_obj = json.loads(decode)['stock_prices']
            close_prices = pd.DataFrame(dict_obj)

        close_prices.sort_values(by=['date'], inplace=True, ascending=True)

        self.img_path = GraphBuilder.build_graph(self.company_profile, close_prices)

    def get_standard_fundamentals(self):

        tags = ['name', 'revenuegrowth', 'profitmargin', 'pricetoearnings', 'pricetobook', 'industry_category', 'industry_group', 'basiceps', 'short_description']

        identifier = self.company_profile.ticker
        basic = "https://api.intrinio.com/data_point?identifier=" + identifier + "&item="
        logic = ""
        for i in tags:
            logic = logic + i +','

        logic = logic.strip(',')
        url = basic + logic + "&api_key=OmRhNGVlMTlhZGQ5ZWVmOTdiZTAwOWY3NjNjZGI1OTNi"

        if debug:
            dict_obj = data_point_results.dpr
        else:
            contents = urllib.request.urlopen(url)
            decode = contents.read().decode('utf-8')
            dict_obj = json.loads(decode)['data']

        #todo parse results

        print(dict_obj)
        keyvals = {}

        for item in tags:
            for d in dict_obj:
                if d['item'] == item:
                    keyvals[item] = d['value']

        self.tags = tags
        self.fundamental_values = keyvals
        print(self.tags)

    def report_text(self):

        english_df = self.excel_sheet[self.excel_sheet['Intrinio'].isin(self.tags)]

        list_reasons = []
        #
        # # TODO differentiate between positive, negative, neutral
        # for key, value in company_selection.items():
        #     reason = Reasons(key, value, "positive")
        #     list_reasons.append(reason)

        knowledge = "Basic"

        name = english_df["Name"].tolist()
        english = english_df[knowledge].tolist()
        intrinio = english_df["Intrinio"].tolist()

        list_reasons = []

        for i in range (0, len(intrinio)):
            if intrinio[i] in self.fundamental_values:
                reason = Reasons(name[i], self.fundamental_values[intrinio[i]], english[i])
                list_reasons.append(reason)

        self.finance_reasons = list_reasons

    def analysis(self):

        companies = pd.DataFrame(self.screen_results)
        primary_only = companies['ticker'].str.len() < 5
        self.companies = companies[primary_only]

        if self.objective == "Defensive":
            self.defensive_analyzer()
        elif self.objective == "Risky":
            self.risky_analyzer()

        self.graph_price()
        self.get_standard_fundamentals()
        self.report_text()

    def analysis_demo(self):
        companies = pd.DataFrame(self.screen_results)
        primary_only = companies['ticker'].str.len() < 5
        self.companies = companies[primary_only]

        if self.risk_profile == "Defensive":
            self.defensive_analyzer()
        elif self.risk_profile == "Risky":
            self.risky_analyzer()

        self.graph_price()
        self.get_standard_fundamentals()
        self.report_text()