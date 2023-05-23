# import the os module, which will be used for file handling
import os
# import the itertools module, which will be used for generating combinations of teams
import itertools

# main_menu function displays the main menu and returns the user's choice
def main_menu():
    print("\nWelcome to the Team Manager!")
    print("1. Add teams and players")
    print("2. Start tournament")
    print("3. View leaderboard")
    print("4. Exit")

    choice = input("Enter your choice (1-4): ")
    return int(choice)


# function for adding teams and players
def add_teams_and_players(teams):
    while True:
        team_name = input("Enter the team name (type 'done' to finish): ")
        if team_name.lower() == "done":
            break
        
        # create a new team if it does not exist
        if team_name not in teams:
            teams[team_name] = {"players": [], "score": 0}
            
        # adding players to the team
        while True:
            player_name = input(f"Enter a player name for team '{team_name}' (type 'done' to finish): ")
            if player_name.lower() == "done":
                break
            teams[team_name]["players"].append(player_name)
            
    # save the teams to the file
    save_teams_to_file(teams)

# function for loading teams from a file
def load_teams_from_file():
    teams = {}
    if os.path.exists("teams.txt"):
        with open("teams.txt", "r") as f:
            for line in f:
                team_name, players, score = line.strip().split(":")
                teams[team_name] = {"players": players.split(","), "score": int(score)}
    return teams

# function for saving teams to a file
def save_teams_to_file(teams):
    with open("teams.txt", "w") as f:
        for team_name, team_info in teams.items():
            f.write(f"{team_name}:{','.join(team_info['players'])}:{team_info['score']}\n")

# function for viewing the leaderboard
def view_leaderboard(teams):
    sorted_teams = sorted(teams.items(), key=lambda x: x[1]["score"], reverse=True)

    print("\nLeaderboard:")
    for i, (team_name, team_info) in enumerate(sorted_teams, start=1):
        print(f"{i}. {team_name} - Score: {team_info['score']}")

# function for starting the tournament
def start_tournament(teams):
    # generate all possible matches
    matches = list(itertools.combinations(teams.keys(), 2))

    for match in matches:
       play_match(teams, match)

    # save the results to the file
    save_teams_to_file(teams)

    # Check for tiebreaker round
    sorted_teams = sorted(teams.items(), key=lambda x: x[1]["score"], reverse=True)
    max_score = sorted_teams[0][1]["score"]
    tiebreaker_teams = [team for team in sorted_teams if team[1]["score"] == max_score]

    if len(tiebreaker_teams) > 1:
        print("\nTiebreaker round:")
        tiebreaker_matches = list(itertools.combinations([team[0] for team in tiebreaker_teams], 2))

        for match in tiebreaker_matches:
            play_match(teams, match)

        save_teams_to_file(teams)

    view_leaderboard(teams)

# function for playing a match
def play_match(teams, match):
    print(f"\nMatch: {match[0]} vs {match[1]}")
    result = input("Enter the winner ('draw' for a draw): ")

    if result == match[0]:
        teams[match[0]]["score"] += 3
    elif result == match[1]:
        teams[match[1]]["score"] += 3
    elif result.lower() == "draw":
        teams[match[0]]["score"] += 1
        teams[match[1]]["score"] += 1
    else:        print("Invalid input. Please try again.")

# main execution of the program
if __name__ == "__main__":
    teams = load_teams_from_file()

    while True:
        choice = main_menu()

        if choice == 1:
            add_teams_and_players(teams)
        elif choice == 2:
            if len(teams) < 2:
                print("There must be at least 2 teams to start a tournament.")
            else:
                start_tournament(teams)
        elif choice == 3:
            view_leaderboard(teams)
        elif choice == 4:
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")
