from Screener import User, screen_Builder, Screen, Analyzer, report_generator
import json

risk_profiles = ["Risky", "Moderate", "Defensive"]

investing_knowledge = ["low", "medium", "high"]

areas_of_interest = ["Technology", "REITs"]


def build_test_user():

    # builds two tests users, builds and executes screens for each
    # debug in Screen.run_screen is set to True
    safe_user = User.User()
    safe_user.setup_profile("Defensive", 5, "REITs")
    risky_user = User.User()
    risky_user.setup_profile("Risky", 5, "Technology")
    safe_user.generate_screen_url()
    risky_user.generate_screen_url()

    # safe_user.run_all_empty_screen()
    # safe_user.get_all_screen_results()
    risky_user.run_all_empty_screen()

    # risky_user.get_all_screen_results()
    out_json = safe_user.user_to_json()

    # Output the Json
    with open('user_output.txt', 'w') as outfile:
        json.dump(out_json, outfile)

def build_screen_url():

    # builds a url using Screen_Builder.py and screen_builder
    print("Service_Testing.py build_screen")
    test_screen = screen_Builder.screen_Builder("X", "Y", "Defensive")
    test_screen.build_screen()
    print("Screen")
    print(test_screen.screen_url)


def run_screen():
    test_screen = screen_Builder.screen_Builder("X", "Y", "Defensive")
    test_screen.build_screen()
    #Analyzer.execute(test_screen.screen_url)

def analyzer_tests():
    with open('user_output.txt', 'r') as r:
        user_store = json.load(r)

    print(user_store)
    analyzer = Analyzer.Analyzer(user_store)
    screen_output = analyzer.screen_results
    with open('analyzer_output.txt', 'w') as outfile:
        json.dump(screen_output, outfile)

    # building analysis
    analyzer.analysis()

    safe_user = User.User()
    safe_user.setup_profile("Defensive", 5, "REITs")

    print(analyzer.finance_reasons[0].language)
    print(analyzer.img_path)
    generate = report_generator.reportGenerator(safe_user, analyzer.finance_reasons)
    generate.generate_report()

def django_tests():

    fname = "Jesse"
    lname = "Hill"
    fullname = fname + " " + lname
    email = "j_hill14@.pacific.edu"
    risk = 3
    level = 1

    user = User.User(fname, lname, risk, level)

    user.generate_screen_url()
    print(user.user_to_json())

    analyzer = Analyzer.Analyzer(user.user_to_json())
    screen_output = analyzer.screen_results
    print(screen_output)
    analyzer.analysis()
    generate = report_generator.reportGenerator(user, analyzer.finance_reasons)
    generate.generate_report()

def new_tests():

    fname = "Jesse"
    lname = "Hill"
    fullname = fname + " " + lname
    email = "j_hill14@.pacific.edu"
    risk = 3
    level = 1

    user = User.User(email, fname, lname, risk, level)
    user.generate_screen_url_demo()
    print(user.user_to_json_demo())

    analyzer = Analyzer.Analyzer(user.user_to_json_demo(), "Demo")
    analyzer.analysis_demo()
    profile = analyzer.company_profile
    generate = report_generator.reportGenerator(user, analyzer.finance_reasons, profile)
    generate.generate_report()


new_tests()

