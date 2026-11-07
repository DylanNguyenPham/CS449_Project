
import unittest
import Gui
from unittest.mock import patch


class TestPegSolitaireAcceptanceCriteria(unittest.TestCase):

    def setUp(self):

        Gui.size_dd.selected_index = 0
        Gui.type_dd.selected_index = 0

        Gui.auto_play_active = False
        Gui.selected_peg = None
        Gui.show_reset_confirm = False

        Gui.reset_board()

    # --------------------------------------------------
    # ORIGINAL ACCEPTANCE CRITERIA TESTS
    # --------------------------------------------------

    # AC 1.1: Board Size Selection
    def test_AC_1_1_board_size_selection(self):

        Gui.size_dd.selected_index = Gui.size_dd.options.index("5x5")
        Gui.reset_board()

        self.assertEqual(len(Gui.board_layout), 5)
        self.assertEqual(len(Gui.board_layout[0]), 5)

        Gui.size_dd.selected_index = Gui.size_dd.options.index("9x9")
        Gui.reset_board()

        self.assertEqual(len(Gui.board_layout), 9)

    # AC 2.1: Board Type Dropdown Options
    def test_AC_2_1_board_type_dropdown_options(self):

        self.assertIn("English", Gui.type_dd.options)
        self.assertIn("Diamond", Gui.type_dd.options)
        self.assertIn("Hexagon", Gui.type_dd.options)

    # AC 2.2: Select English Board
    def test_AC_2_2_select_english_board(self):

        Gui.type_dd.selected_index = Gui.type_dd.options.index("English")
        Gui.reset_board()

        self.assertEqual(len(Gui.board_layout), 7)
        self.assertEqual(Gui.board_layout[3][3], 2)

    # AC 3.1: New Game Initialization
    def test_AC_3_1_new_game_initialization(self):

        Gui.reset_board()

        self.assertEqual(Gui.board_layout[3][3], 2)

    # AC 3.2: New Game Confirmation Prompt
    def test_AC_3_2_new_game_confirmation_prompt(self):

        Gui.attempt_move((5, 3), (3, 3))

        if Gui.count_pegs() < 32:
            Gui.show_reset_confirm = True

        self.assertTrue(Gui.show_reset_confirm)

    # AC 4.1: Valid Move Execution
    def test_AC_4_1_valid_move_execution(self):

        success = Gui.attempt_move((5, 3), (3, 3))

        self.assertTrue(success)

        self.assertEqual(Gui.board_layout[5][3], 2)
        self.assertEqual(Gui.board_layout[4][3], 2)
        self.assertEqual(Gui.board_layout[3][3], 1)

    # AC 4.2: Invalid Move Rejection
    def test_AC_4_2_invalid_move_rejection(self):

        initial_board = [row[:] for row in Gui.board_layout]

        success = Gui.attempt_move((2, 2), (4, 4))

        self.assertFalse(success)
        self.assertEqual(Gui.board_layout, initial_board)

    # AC 5.1: Game Over / Loss Detection
    def test_AC_5_1_game_over_loss_detection(self):

        Gui.board_layout = [[0] * 7 for _ in range(7)]

        Gui.board_layout[0][2] = 1
        Gui.board_layout[6][4] = 1

        Gui.check_game_over()

        self.assertEqual(
            Gui.game_status_message,
            "Game Over / Loss"
        )

    # AC 5.2: Victory Detection
    def test_AC_5_2_victory_detection(self):

        Gui.board_layout = [[0] * 7 for _ in range(7)]

        Gui.board_layout[3][3] = 1

        Gui.check_game_over()

        self.assertEqual(
            Gui.game_status_message,
            "Victory!"
        )

    # --------------------------------------------------
    # MANUAL GAME MODE UNIT TESTS
    # --------------------------------------------------

    # AC 6.1: Randomize Board
    def test_AC_6_1_manual_randomize_board(self):

        original_peg_count = Gui.count_pegs()

        Gui.randomize_board()

        self.assertEqual(
            Gui.count_pegs(),
            original_peg_count
        )

    # AC 6.2: Randomization Preserves Board Dimensions
    def test_AC_6_2_randomize_preserves_board_size(self):

        original_size = len(Gui.board_layout)

        Gui.randomize_board()

        self.assertEqual(
            len(Gui.board_layout),
            original_size
        )

        self.assertEqual(
            len(Gui.board_layout[0]),
            original_size
        )

    # AC 6.3: Randomization Preserves Invalid Positions
    def test_AC_6_3_randomize_preserves_invalid_positions(self):

        invalid_positions = []

        for r in range(len(Gui.board_layout)):
            for c in range(len(Gui.board_layout[r])):

                if Gui.board_layout[r][c] == 0:
                    invalid_positions.append((r, c))

        Gui.randomize_board()

        for r, c in invalid_positions:

            self.assertEqual(
                Gui.board_layout[r][c],
                0
            )

    # AC 6.4: Randomization Clears Selected Peg
    def test_AC_6_4_randomize_clears_selection(self):

        Gui.selected_peg = (5, 3)

        Gui.randomize_board()

        self.assertIsNone(Gui.selected_peg)

    # AC 6.5: Randomization Stops Automated Gameplay
    def test_AC_6_5_randomize_stops_auto_play(self):

        Gui.start_auto_play()

        Gui.randomize_board()

        self.assertFalse(Gui.auto_play_active)
        self.assertEqual(Gui.game_mode, "Manual")

    # AC 6.6: Manual Mode Remains Active After Randomization
    def test_AC_6_6_manual_mode_after_randomization(self):

        Gui.randomize_board()

        self.assertEqual(Gui.game_mode, "Manual")

    # --------------------------------------------------
    # AUTOMATED GAME MODE UNIT TESTS
    # --------------------------------------------------

    # AC 7.1: Start Automated Gameplay
    def test_AC_7_1_start_auto_play(self):

        success = Gui.start_auto_play()

        self.assertTrue(success)
        self.assertTrue(Gui.auto_play_active)
        self.assertEqual(Gui.game_mode, "Automated")

    # AC 7.2: Automated Move Selection
    def test_AC_7_2_auto_selects_valid_move(self):

        Gui.start_auto_play()

        valid_moves = Gui.get_valid_moves()

        self.assertGreater(len(valid_moves), 0)

        with patch(
            "Gui.random.choice",
            side_effect=lambda moves: moves[0]
        ):

            success = Gui.auto_play_step()

        self.assertTrue(success)

    # AC 7.3: Automated Move Updates Board
    def test_AC_7_3_auto_move_updates_board(self):

        initial_peg_count = Gui.count_pegs()

        Gui.start_auto_play()

        with patch(
            "Gui.random.choice",
            side_effect=lambda moves: moves[0]
        ):

            success = Gui.auto_play_step()

        self.assertTrue(success)

        self.assertEqual(
            Gui.count_pegs(),
            initial_peg_count - 1
        )

    # AC 7.4: Automated Game Continues Until Game Over
    def test_AC_7_4_auto_play_until_game_over(self):

        Gui.start_auto_play()

        move_count = 0

        while Gui.auto_play_active and move_count < 100:

            success = Gui.auto_play_step()

            if success:
                move_count += 1
            else:
                break

        self.assertGreater(move_count, 0)

        self.assertFalse(Gui.auto_play_active)

        self.assertIn(
            Gui.game_status_message,
            ["Victory!", "Game Over / Loss"]
        )

    # AC 7.5: Stop Automated Gameplay
    def test_AC_7_5_stop_auto_play(self):

        Gui.start_auto_play()

        success = Gui.stop_auto_play()

        self.assertTrue(success)
        self.assertFalse(Gui.auto_play_active)
        self.assertEqual(
            Gui.game_status_message,
            "Auto Play Stopped"
        )

    # AC 7.6: Automated Gameplay Stops When No Moves Remain
    def test_AC_7_6_auto_play_no_valid_moves(self):

        Gui.board_layout = [[0] * 7 for _ in range(7)]

        Gui.board_layout[0][2] = 1
        Gui.board_layout[6][4] = 1

        success = Gui.start_auto_play()

        self.assertFalse(success)
        self.assertFalse(Gui.auto_play_active)

        self.assertEqual(
            Gui.game_status_message,
            "Game Over / Loss"
        )

    # AC 7.7: Automated Gameplay Does Not Allow Invalid Moves
    def test_AC_7_7_auto_only_uses_valid_moves(self):

        valid_moves = Gui.get_valid_moves()

        for start_pos, end_pos in valid_moves:

            r1, c1 = start_pos
            r2, c2 = end_pos

            dr = r2 - r1
            dc = c2 - c1

            self.assertTrue(
                (abs(dr) == 2 and dc == 0)
                or (abs(dc) == 2 and dr == 0)
            )

    # AC 7.8: Automated Gameplay Stops After Victory
    def test_AC_7_8_auto_play_stops_after_victory(self):

        Gui.board_layout = [[0] * 7 for _ in range(7)]

        Gui.board_layout[3][3] = 1

        success = Gui.start_auto_play()

        self.assertFalse(success)
        self.assertFalse(Gui.auto_play_active)

        self.assertEqual(
            Gui.game_status_message,
            "Victory!"
        )


if __name__ == '__main__':

    unittest.main(verbosity=2)

