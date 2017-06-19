"""
Estimate the strength rating of a student defined heuristic by competing
against fixed-depth minimax and alpha-beta search agents in a round-robin
tournament.

This is a FAIR tournament, in the sense that all test_agents are faced with the
exact same random starting positions for a given cpu_agent.  So variation due
to starting positions is eliminated, and more variation can be attributed to
the evaluation functions the test_agents are using.

NOTE: All agents are constructed from the student CustomPlayer implementation,
so any errors present in that class will affect the outcome.

Terminology:
- A "GAME" is a single play of Isolation, from opening moves until someone runs
  out of moves.

- A "FAIR MATCH" is two GAMES. The matches are fair because the board is
  initialized randomly for both players, and the players play each match twice:
  once as the first player and once as the second player.  Randomizing the
  openings and switching the player order corrects for imbalances due to both
  starting position and initiative.

- A "MATCH" is the same thing as a "FAIR MATCH." So when we talk about
  `num_matches` below, there will be 2 * num_matches games played total.
"""

from collections import Counter

from game_agent import (MinimaxPlayer, AlphaBetaPlayer, custom_score,
                        custom_score_2, custom_score_3)
from sample_players import (RandomPlayer, open_move_score,
                            improved_score, center_score)
from tournament_helpers import (format_header, prepare_same_fair_matches,
                                Agent, format_loss_results, format_row_results,
                                format_win_rates, make_dividing_line)


NUM_MATCHES = 5  # number of fair matches for each (cpu_agent, test_agent) pair
TIME_LIMIT = 150  # number of milliseconds before timeout


def play_fair_round(cpu_agent, test_agents, num_matches):
    """
    Pit all test_agents against the same cpu_agent in the SAME fair matches
    (i.e. same starting board configurations for each test_agent).

    This sameness lets you better compare the different evaluation functions
    used by the test_agents, by reducing variability due to different starting
    positions.

    win_counts: IsolationPlayer -> Int, including cpu_agent.player
    loss_reason_counts: String -> Int
    """

    win_counts = Counter()
    loss_reason_counts = Counter()

    for games in prepare_same_fair_matches(cpu_agent, test_agents, num_matches):
        for game in games:
            winner, _, loss_reason = game.play()
            win_counts[winner] += 1
            loss_reason_counts[loss_reason] += 1

    assert sum(win_counts.values()) == 2 * num_matches * len(test_agents)
    return win_counts, loss_reason_counts


def run_fair_tournament(cpu_agents, test_agents, num_matches):
    """
    Run the full tournament, where each cpu_agent in cpu_agents plays a fair round
    against all test_agents. Results are tallied, printed, and returned.

    A single fair round uses the same starting positions for all test_agents.
    Different fair rounds use different starting positions; these are random.
    """

    all_test_agent_wins = Counter()
    all_loss_reasons = Counter()

    print(format_header(test_agents))

    # Play a (row == fair round) of the full tournament
    for idx, cpu_agent in enumerate(cpu_agents):
        print("{!s:^9}{:^13}".format(idx + 1, cpu_agent.name), end="", flush=True)

        win_counts, loss_reasons = play_fair_round(cpu_agent, test_agents, num_matches)

        # Print results
        num_games_each = 2 * num_matches
        print(format_row_results(test_agents, win_counts, num_games_each))

        # Update all_loss_reasons
        all_loss_reasons.update(loss_reasons)

        # Update all_test_agent_wins
        del win_counts[cpu_agent.player]
        all_test_agent_wins.update(win_counts)

    print(make_dividing_line(test_agents))

    total_num_games_per_test_agent = 2 * num_matches * len(cpu_agents)

    assert len(all_test_agent_wins) == len(test_agents)
    assert sum(all_test_agent_wins.values()) <= \
        total_num_games_per_test_agent * len(test_agents)

    print(format_win_rates(test_agents,
        all_test_agent_wins, total_num_games_per_test_agent))
    print(format_loss_results(all_loss_reasons))

    return all_test_agent_wins, all_loss_reasons


def main():
    """Run a tournament between test_agents and cpu_agents."""

    RUN_DESCR = "All improved_score, Board.get_legal_moves unshuffled - tournament_fair"

    # Define two agents to compare -- these agents will play from the same
    # starting position against the same adversaries in the tournament
    test_agents = [
        Agent(AlphaBetaPlayer(score_fn=improved_score), "AB_Improved"),
        Agent(AlphaBetaPlayer(score_fn=improved_score), "AB_Improved"),
        Agent(AlphaBetaPlayer(score_fn=improved_score), "AB_Improved"),
        Agent(AlphaBetaPlayer(score_fn=improved_score), "AB_Improved"),

        #### Using various custom_score functions
        # Agent(AlphaBetaPlayer(score_fn=custom_score), "AB_Custom"),
        # Agent(AlphaBetaPlayer(score_fn=custom_score_2), "AB_Custom_2"),
        # Agent(AlphaBetaPlayer(score_fn=custom_score_3), "AB_Custom_3")
    ]

    # Define a collection of agents to compete against the test agents
    cpu_agents = [
        Agent(RandomPlayer(), "Random"),
        Agent(MinimaxPlayer(score_fn=open_move_score), "MM_Open"),
        Agent(MinimaxPlayer(score_fn=center_score), "MM_Center"),
        Agent(MinimaxPlayer(score_fn=improved_score), "MM_Improved"),
        Agent(AlphaBetaPlayer(score_fn=open_move_score), "AB_Open"),
        Agent(AlphaBetaPlayer(score_fn=center_score), "AB_Center"),
        Agent(AlphaBetaPlayer(score_fn=improved_score), "AB_Improved")
    ]

    print("\n" + RUN_DESCR)
    run_fair_tournament(cpu_agents, test_agents, NUM_MATCHES)


if __name__ == "__main__":
    main()
