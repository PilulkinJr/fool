import argparse
import itertools
import logging
import random
import sys

from fool.game import Game
from fool.players import COMPUTER_PLAYERS, HumanPlayer, Players

FORMAT = "[%(levelname)7s %(funcName)s] %(message)s"
logging.basicConfig(format=FORMAT, level=logging.WARNING)
log = logging.getLogger(__name__)


def update_ratings(winner, loser, k, draw=False) -> None:
    exp_rating_winner = winner.expected_rating(loser)
    exp_rating_loser = loser.expected_rating(winner)

    score = (1.0, 0.0)
    if draw:
        score = (0.5, 0.5)

    winner.rating += k * (score[0] - exp_rating_winner)
    loser.rating += k * (score[1] - exp_rating_loser)


def set_players(n_players: int = 2, human: bool = False):

    players = Players()

    human_player = None
    if human:
        human_player = HumanPlayer("Игрок")
        players.append(human_player)

    random.shuffle(COMPUTER_PLAYERS)

    for i, PlayerClass in zip(range(n_players), itertools.cycle(COMPUTER_PLAYERS)):
        player = PlayerClass(f"Компьютер {i + 1}")
        player.name += " (" + player.__class__.__name__ + ")"
        players.append(player)

    return players


def main(args=None):

    if args is None:
        args = sys.argv[1:]

    parser = argparse.ArgumentParser("fool")
    subparsers = parser.add_subparsers(dest="subcommand")

    play = subparsers.add_parser("play")
    play.add_argument("-n", "--n_players", type=int, default=1)

    simulate = subparsers.add_parser("simulate")
    simulate.add_argument("-n", "--n_players", type=int, default=2)

    tournament = subparsers.add_parser("tournament")
    tournament.add_argument("-g", "--games", type=int, default=1)

    parsed = parser.parse_args(args)

    if parsed.subcommand == "play":
        players = set_players(parsed.n_players, human=True)
        game = Game(players)
        game.play()

    elif parsed.subcommand == "simulate":
        n_players = parsed.n_players
        players = set_players(n_players, human=False)
        game = Game(players)

        winner, loser, draw = game.play()
        if winner is not None:
            update_ratings(winner, loser, n_players, draw)

    elif parsed.subcommand == "tournament":
        n_games = parsed.games

        participants = set_players(len(COMPUTER_PLAYERS), human=False)
        for player in participants:
            player.name = player.__class__.__name__
        k = len(participants)

        for i in range(n_games):
            random.shuffle(participants)
            print(f"Турнир {i + 1}")
            for j, players in enumerate(itertools.combinations(participants, 2)):
                print(f"Игра {j + 1}")
                game = Game(Players(players))
                winner, loser, draw = game.play()
                if winner is not None:
                    update_ratings(winner, loser, k, draw)
                print()

        score = [(player.name, round(player.rating, 1)) for player in participants]
        score.sort(key=lambda item: item[1], reverse=True)

        print()
        print(score)


if __name__ == "__main__":

    main()
