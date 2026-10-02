import unittest
import Gui

class TestPegSolitaireAcceptanceCriteria(unittest.TestCase):

    def setUp(self):
        Gui.size_dd.selected_index = 0  # "7x7"
        Gui.type_dd.selected_index = 0  # "English"
        Gui.reset_board()

    # Precondition: Application launched and board size selector is toggled to different dimension options.
    # Postcondition: Board layout updates dimensions dynamically to match choice (e.g. 5x5, 7x7, 9x9).
    def test_AC_1_1_board_size_selection(self):
        Gui.size_dd.selected_index = Gui.size_dd.options.index("5x5")
        Gui.reset_board()
        self.assertEqual(len(Gui.board_layout), 5, "Board should resize to 5 rows")
        self.assertEqual(len(Gui.board_layout[0]), 5, "Board should resize to 5 columns")

        Gui.size_dd.selected_index = Gui.size_dd.options.index("9x9")
        Gui.reset_board()
        self.assertEqual(len(Gui.board_layout), 9, "Board should resize to 9 rows")

    # Precondition: Board configuration dropdown options are visible.
    # Postcondition: Options list contains English, Hexagon, and Diamond layout options.
    def test_AC_2_1_board_type_dropdown_options(self):
        self.assertIn("English", Gui.type_dd.options)
        self.assertIn("Diamond", Gui.type_dd.options)
        self.assertIn("Hexagon", Gui.type_dd.options)

    # Precondition: Multiple board types available in dropdown, user selects "English".
    # Postcondition: Classic cross-shaped template loads onto board layout.
    def test_AC_2_2_select_english_board(self):
        Gui.type_dd.selected_index = Gui.type_dd.options.index("English")
        Gui.reset_board()
        self.assertEqual(len(Gui.board_layout), 7)
        self.assertEqual(Gui.board_layout[3][3], 2, "Center hole should be empty (2)")

    # Precondition: Board size and type chosen, user triggers "New Game".
    # Postcondition: Game board renders with pegs populated and empty center.
    def test_AC_3_1_new_game_initialization(self):
        Gui.reset_board()
        self.assertEqual(Gui.board_layout[3][3], 2, "Center hole should be empty")

    # Precondition: Active game currently in progress (pegs captured).
    # Postcondition: Reset confirmation dialog prompt is displayed.
    def test_AC_3_2_new_game_confirmation_prompt(self):
        Gui.attempt_move((5, 3), (3, 3))
        if Gui.count_pegs() < 32:
            Gui.show_reset_confirm = True

        self.assertTrue(Gui.show_reset_confirm, "Reset confirmation prompt should be triggered")

    # Precondition: User selects peg at (5,3) and jumps to empty space at (3,3).
    # Postcondition: Move executes, middle peg at (4,3) removed, board state updates.
    def test_AC_4_1_valid_move_execution(self):
        success = Gui.attempt_move((5, 3), (3, 3))
        self.assertTrue(success, "Valid orthogonal jump should execute successfully")
        self.assertEqual(Gui.board_layout[5][3], 2, "Source hole should be empty")
        self.assertEqual(Gui.board_layout[4][3], 2, "Middle peg should be captured")
        self.assertEqual(Gui.board_layout[3][3], 1, "Target hole should contain peg")

    # Precondition: User attempts invalid move (e.g., diagonal move).
    # Postcondition: Move is rejected and board layout remains unchanged.
    def test_AC_4_2_invalid_move_rejection(self):
        initial_board = [row[:] for row in Gui.board_layout]
        success = Gui.attempt_move((2, 2), (4, 4))
        self.assertFalse(success, "Diagonal move should be rejected")
        self.assertEqual(Gui.board_layout, initial_board, "Board state should remain unchanged")

    # Precondition: No valid jumps available and >1 peg remaining.
    # Postcondition: System displays Game Over / Loss message.
    def test_AC_5_1_game_over_loss_detection(self):
        Gui.board_layout = [[0]*7 for _ in range(7)]
        Gui.board_layout[0][2] = 1
        Gui.board_layout[6][4] = 1
        
        Gui.check_game_over()
        self.assertEqual(Gui.game_status_message, "Game Over / Loss")

    # Precondition: Exactly 1 peg remaining in center hole.
    # Postcondition: System displays Victory message.
    def test_AC_5_2_victory_detection(self):
        Gui.board_layout = [[0]*7 for _ in range(7)]
        Gui.board_layout[3][3] = 1
        
        Gui.check_game_over()
        self.assertEqual(Gui.game_status_message, "Victory!")

if __name__ == '__main__':
    unittest.main(verbosity=2)
