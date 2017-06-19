"""
Unit tests for various Isolation functionality.
"""

import unittest

from game_agent import AlphaBetaPlayer
from sample_players import (RandomPlayer, open_move_score,
                            improved_score, center_score)
from tournament_helpers import prepare_fair_match, prepare_same_fair_matches, Agent

class FairTournamentTest(unittest.TestCase):
    """Are the tournament_fair functions really generating fair rounds?"""

    def setUp(self):
        self.test_agents = [
            Agent(AlphaBetaPlayer(score_fn=improved_score), "AB_Improved"),
            Agent(AlphaBetaPlayer(score_fn=improved_score), "AB_Improved"),
            Agent(AlphaBetaPlayer(score_fn=improved_score), "AB_Improved"),
            Agent(AlphaBetaPlayer(score_fn=improved_score), "AB_Improved")
        ]

        self.cpu_agent = Agent(RandomPlayer(), "Random")


    def test_prepare_fair_match(self):
        boards, _ = prepare_fair_match("Player1", "Player2")
        board1, board2 = boards

        # The same opening moves were made
        self.assertTrue(board1.get_blank_spaces() == board2.get_blank_spaces())

        # The same players are registered to both games
        self.assertTrue(board1.active_player == board2.inactive_player)
        self.assertTrue(board1.inactive_player == board2.active_player)

        # Player1 has initiative in board1; Player2 has initiative in board2
        self.assertTrue(board1.active_player == "Player1")
        self.assertTrue(board2.active_player == "Player2")


    def test_prepare_same_fair_matches(self):
        num_matches = 5
        game_sequences = []
        for games in prepare_same_fair_matches(
                self.cpu_agent, self.test_agents, num_matches):
            game_sequences.append(games)

        # There should be a sequence of games for each test agent
        self.assertTrue(len(game_sequences) == len(self.test_agents))

        # And each sequence should have 2 * num_matches Boards in it
        self.assertTrue(len(game_sequences[0]) == 2 * num_matches)

        # And for a given position in 0 .. 2 * num_matches,
        # all boards should have the same legal moves
        for game_idx in range(len(game_sequences[0])):
            game1 = game_sequences[0][game_idx]
            for game_seq in game_sequences[1:]:
                game2 = game_seq[game_idx]
                self.assertTrue(game1.get_blank_spaces() == game2.get_blank_spaces())
                self.assertFalse(
                    {game1.active_player, game1.inactive_player} ==
                    {game2.active_player, game2.inactive_player}
                )



if __name__ == '__main__':
    unittest.main()
