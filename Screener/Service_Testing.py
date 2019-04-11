from Screener import User, screen_Builder, Screen, analyzer
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
    out_json = risky_user.user_to_json()

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
    analyzer.exeucute_url(test_screen.screen_url)

build_test_user()