"""
Helpers for refactored tournament.py
"""

from collections import namedtuple
import random

from isolation import Board

### Running the Matches ###
Agent = namedtuple("Agent", ["player", "name"])

def get_random_starting_positions(height=7, width=7):
    """
    Get random starting positions for two players on an empty `height` x
    `width` Isolation board.

    Returns: [(row1, col1), (row2, col2)]
    """
    b = Board("", "", width, height)
    moves = []
    for _ in range(2):
        move = random.choice(b.get_legal_moves())
        moves.append(move)
        b.apply_move(move)
    return moves


def prepare_fair_match(player1, player2, opening_moves=None, width=7, height=7):
    """
    A fair match consists of two Boards with the same random starting position
    for each player, one where player1 gets first move and the other where
    player2 gets first move.

    Parameters
    ----------
    player1, player2 : object
        The objects to be registered with the Board as IsolationPlayers

    opening_moves : [(Int, Int), (Int, Int)]
        The two opening moves to be played.
        If None, they will be randomly generated.

    width, height : Int
        The height and width of the Board for gameplay.

    Returns
    -------
    boards : [Board, Board]
        The two games with the same opening moves taken. `player1` went first
        and has initiative in boards[0]; `player2` went first and has initiative
        in boards[1]

    opening_moves : [(Int, Int), (Int, Int)]
        The two opening moves that were played for each Board in boards.
        If caller provided opening_moves, they will remain unchanged.
        If caller didn't provide opening_moves, then these are the random
        opening moves that were generated and played.
    """

    boards = [
        Board(player1, player2, width, height),
        Board(player2, player1, width, height)
    ]

    if not opening_moves:
        b = boards[0]
        opening_moves = get_random_starting_positions(b.height, b.width)

    for move in opening_moves:
        for board in boards:
            board.apply_move(move)
    return boards, opening_moves


def prepare_same_fair_matches(agent, opponents, num_matches):
    """
    Prepare the same fair matches (i.e. same opening moves everywhere)
    between `agent` and each opponent agent in `opponents`.

    Generates len(opponents) lists.
    The ith list generated is a list of 2*num_matches Boards, ready to be
    played between `agent` and opponents[i].
    """

    same_opening_moves = [get_random_starting_positions() for _ in range(num_matches)]
    for opponent in opponents:
        games = []
        for opening_moves in same_opening_moves:
            boards, _ = prepare_fair_match(agent.player, opponent.player, opening_moves)
            games.extend(boards)
        assert len(games) == 2 * num_matches
        yield games


### Output and Text Formatting ###
DESCRIPTION = """
This script evaluates the performance of the custom_score evaluation
function against a baseline agent using alpha-beta search and iterative
deepening (ID) called `AB_Improved`. The three `AB_Custom` agents use
ID and alpha-beta search with the custom_score functions defined in
game_agent.py.
"""

TIMEOUT_TEMPLATE = """
There were {} timeout(s) during the tournament -- make sure
your agent handles search timeout correctly, and consider
increasing the timeout margin for your agent.
"""

FORFEIT_TEMPLATE = """
Your ID search forfeited {} game(s) while there were still legal
moves available to play.
"""

def format_header(test_agents):
    lines = [DESCRIPTION]
    lines.append("{:^74}".format("*************************"))
    lines.append("{:^74}".format("Playing Matches"))
    lines.append("{:^74}".format("*************************"))
    lines.append("\n{:^9}{:^13}".format("Match #", "Opponent") +
        ''.join(['{:^13}'.format(x[1].name) for x in enumerate(test_agents)]))
    lines.append("{:^9}{:^13} ".format("", "") +
        ' '.join(['{:^5}| {:^5}'.format("Won", "Lost") for _ in enumerate(test_agents)]))
    return "\n".join(lines)


def format_row_results(test_agents, win_counts, num_games_each):
    results = []
    for agent in test_agents:
        num_wins = win_counts[agent.player]
        num_losses = num_games_each - num_wins
        results.append("{:^5}| {:^5}".format(num_wins, num_losses))
    return " " + " ".join(results)


def format_loss_results(reasons):
    results = []
    if "timeout" in reasons:
        results.append(TIMEOUT_TEMPLATE.format(reasons["timeout"]))
    if "forfeit" in reasons:
        results.append(FORFEIT_TEMPLATE.format(reasons["forfeit"]))
    return "\n".join(results)


def format_win_rates(test_agents, all_test_agent_wins, total_num_games):
    results_template = "{:^9}{:^13}" + "{:^13}" * len(test_agents)
    win_percentage_template = "{:.1%}"
    data = ["", "Win Rate:"]
    for agent in test_agents:
        num_wins = all_test_agent_wins[agent.player]
        data.append(win_percentage_template.format(num_wins / total_num_games))
    return results_template.format(*data)

def make_dividing_line(test_agents):
    width = 9 + 13 + (13 * len(test_agents))
    return "-" * width
