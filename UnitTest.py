import unittest
import Gui
"""
====================================================================
PROJECT SPRINT 1: USER STORIES & ACCEPTANCE CRITERIA
====================================================================

User Story 1: Choose a board size
- As a player, I want to select a board size from a menu option, 
  so that I can configure the scale and difficulty of the game grid.
  * AC 1.1: Given the application is launched and the main menu is active, 
            when the user clicks on the board size selector, 
            then a list of valid dimensions is displayed. (Status: completed)
  * AC 1.2: Given the board size menu is open, 
            when the user selects a specific grid dimension, 
            then the application updates the game configuration state. (Status: completed)

User Story 2: Choose the board type
- As a player, I want to choose a board layout type (e.g., English, Hexagon, Diamond) 
  so that I can play different geometric variations of the game.
  * AC 2.1: Given configuration options are visible, when the user views the board type menu, 
            then layout options are presented. (Status: completed)
  * AC 2.2: Given multiple board types are available, when the user selects "English", 
            then the classic cross-shaped board template loads. (Status: completed)

User Story 3: Start a new game of the chosen board size and type
- As a player, I want to start a new game session using my selected board size and type 
  so that the pegs are initialized correctly.
  * AC 3.1: Given a board size/type are selected, when the user clicks "New Game", 
            then the board renders with pegs populated and center empty. (Status: completed)
  * AC 3.2: Given an active game is in progress, when the user clicks "New Game", 
            then a confirmation prompt appears before reset. (Status: toDo)

User Story 4: Make a move in a game
- As a player, I want to select a peg and jump it over an adjacent peg into an empty space 
  so that I can capture pegs and progress.
  * AC 4.1: Given an active game, when the user jumps a peg orthogonally into an empty space, 
            then the middle peg is removed and the board updates. (Status: completed)
  * AC 4.2: Given an active game, when the user attempts an invalid move, 
            then the move is rejected and state remains unchanged. (Status: completed)

User Story 5: A game is over
- As a player, I want the system to automatically detect when no more valid moves remain 
  so that the final win/loss state is displayed.
  * AC 5.1: Given a move is made, when no valid jumps remain and >1 peg is left, 
            then a "Game Over" message displays. (Status: toDo)
  * AC 5.2: Given a move is made, when exactly 1 peg remains in the center hole, 
            then a victory message displays. (Status: toDo)
====================================================================
"""

class TestPegSolitaireBoard(unittest.TestCase):
    
    def test_board_dimensions(self):
        """Test that the board is exactly a 7x7 grid."""
        self.assertEqual(len(Gui.board_layout), 7, "Board should have 7 rows")
        for row in Gui.board_layout:
            self.assertEqual(len(row), 7, "Each row should have 7 columns")
            
    def test_initial_center_hole(self):
        """Test that the center position is an empty hole (value 2)."""
        center_val = Gui.board_layout[3][3]
        self.assertEqual(center_val, 2, "Center position should be empty (2)")
        
    def test_corners_are_invalid(self):
        """Test that the corners are properly marked as invalid (value 0)."""
        self.assertEqual(Gui.board_layout[0][0], 0, "Top-left corner should be 0")
        self.assertEqual(Gui.board_layout[0][6], 0, "Top-right corner should be 0")
        self.assertEqual(Gui.board_layout[6][0], 0, "Bottom-left corner should be 0")
        self.assertEqual(Gui.board_layout[6][6], 0, "Bottom-right corner should be 0")
        
    def test_initial_peg_count(self):
        """Test that the standard English board starts with exactly 32 pegs."""
        peg_count = 0
        for row in Gui.board_layout:
            peg_count += row.count(1)
        self.assertEqual(peg_count, 32, "Initial board should contain exactly 32 pegs")

if __name__ == '__main__':
    unittest.main(verbosity=2)
