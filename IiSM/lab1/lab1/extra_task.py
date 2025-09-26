import random


def generate_simple_events(probability: float, N: int = 1):
    return [random.random() < probability for _ in range(N)]


class Team:
    def __init__(self, name, rating):
        self.name = name
        self.rating = rating

    def __repr__(self):
        return f'{self.name} (rating: {self.rating})'


def simulate_match(team1, team2):
    total_rating = team1.rating + team2.rating
    win_probability_team1 = team1.rating / total_rating

    return team1 if generate_simple_events(win_probability_team1, 1) else team2


def simulate_round(teams):
    winners = []
    losers = []

    random.shuffle(teams)

    for i in range(0, len(teams), 2):
        team1, team2 = teams[i], teams[i + 1]
        winner = simulate_match(team1, team2)
        loser = team1 if winner == team2 else team2
        winners.append(winner)
        losers.append(loser)

    return winners, losers


def simulate_tournament(teams):
    round_num = 1
    all_losers = []

    while len(teams) > 1:
        print(f'\n---Round {round_num} ---')
        winners, losers = simulate_round(teams)

        print('Pairs of teams:')
        for i in range(len(losers)):
            print(f'{teams[2*i]} vs {teams[2*i + 1]} - Winner: {winners[i]}')

        print('Loser teams:')
        for loser in losers:
            print(loser)

        teams = winners
        all_losers.extend(losers)
        round_num += 1

    print('\n--- Final ---')
    print(f'Tournament Winner: {teams[0]}')
    print('All loser teams:')

    for loser in all_losers:
        print(loser)


def main():
    while True:
        k = int(input('Enter k value: '))
        if k >= 6:
            print('Please enter a valid value! (k <= 6)')
        else:
            break

    num_teams = 2 ** k

    teams = []
    for i in range(num_teams):
        name = f'Team {i + 1}'
        rating = random.randint(0, 100)
        teams.append(Team(name, rating))

    print('List of teams: ')
    for team in teams:
        print(team)

    simulate_tournament(teams)


if __name__ == '__main__':
    main()