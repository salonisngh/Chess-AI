
# Negamax Knight: Chess AI Engine

## Overview
Negamax Knight is a lightweight chess engine developed in Python utilizing the Pygame library, designed for both human vs. human and human vs. AI gameplay. The engine employs the alpha-beta pruning optimization of the negamax algorithm, enabling efficient move calculation while maintaining competitive performance at moderate search depths.

## Features
- **Complete Rule Implementation**: Full support for all chess rules including castling, en passant captures, and pawn promotion
- **Interactive GUI**: Responsive interface with piece selection, move highlighting, and visual feedback
- **Multiple Game Modes**: Support for human vs. human and human vs. AI gameplay
- **AI Opponent**: Implementation of Negamax algorithm with alpha-beta pruning for efficient decision-making
- **User-Friendly Features**:
  - Smooth move animations
  - Sound effects for moves, captures, checks, and promotions
  - Undo functionality (Z key)
  - Game reset option (R key)

## Requirements
- Python 3.x
- Pygame library

## Installation
1. Clone the repository:
   ```
   git clone https://github.com/salonisngh/negamax-knight.git
   ```

2. Install the required dependencies:
   ```
   pip install pygame
   ```

3. Run the game:
   ```
   python main.py
   ```

## How to Play
- **Start**: Run the application to begin a new game
- **Move a Piece**: Click on a piece to select it, then click on a highlighted square to move
- **Undo**: Press 'Z' to undo the last move
- **Reset**: Press 'R' to reset the game to its initial state
- **Game Mode**: Select between Human vs. Human or Human vs. AI mode at startup

## Technical Details

### Board Representation
- 8×8 grid rendered with alternating light and dark squares
- Piece images loaded dynamically and resized according to the board size

### AI Implementation
The chess AI uses three core algorithms:
1. **Minimax**: Initial decision-making algorithm that simulates possible future moves
2. **Negamax**: A mathematical simplification of Minimax for two-player zero-sum games
3. **Alpha-Beta Pruning**: Optimization technique that reduces the number of nodes evaluated in the search tree

### Piece Valuation
Standard chess piece weights are used for evaluation:
- Pawn: 1
- Knight: 3
- Bishop: 3
- Rook: 5
- Queen: 9
- King: Infinite (checkmate ends the game)

## Performance
- **Human vs. Human Play**: Smooth and responsive
- **Human vs. AI (Depth=3)**: Responsive with competitive AI decisions
- **Rule Enforcement**: 98% accuracy based on manual verification
- **GUI Responsiveness**: No lag or crashes observed during gameplay

## Future Development
- Advanced evaluation heuristics for deeper strategic analysis
- Opening book integration for stronger early game play
- Multiplayer functionality over a network
- Save/Load game feature
- Enhanced pawn promotion choices
  
##References

-Russell, S., & Norvig, P. (2009). Artificial Intelligence: A Modern Approach (3rd ed.)
-Pygame Documentation: https://www.pygame.org/docs/
-FIDE Laws of Chess: https://handbook.fide.com/chapter/E012023

##License
-This project is licensed under the MIT License - see the LICENSE file for details.

##Acknowledgments

Thanks to the Pygame development team for their excellent library
Special thanks to chess AI researchers whose work inspired this project
