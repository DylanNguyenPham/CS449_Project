import unittest
import Gui

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