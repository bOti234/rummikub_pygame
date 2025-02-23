# Rummikub card game made with the pygame library in python!

# Rummikub Rules

Rummikub is a tile-based game for 2 to 4 players, combining elements of rummy and mahjong. The goal is to be the first to play all your tiles by forming valid sets (groups or runs) on the table.

---

## Components
- 106 tiles: 104 numbered tiles (2 sets of tiles numbered 1 to 13 in four colours: black, red, blue, and yellow) and 2 joker tiles.
- 4 tile racks (one for each player). You can only see your tile rack, the rest is not visible to you.

---

## Setup
1. All tiles are shuffled randomly in the deck.
2. Each player draws 14 tiles and they are placed on their rack, keeping them hidden from other players.
3. The remaining tiles form the draw pool.

---

## Objective
Be the first to play all your tiles by forming valid sets (groups or runs) on the table.

---

## Gameplay

### 1. Initial Move
- On your first turn, you must play a set (or sets) with a combined value of at least 30 points. This is called the "initial meld."
- Points are calculated by adding the face values of the tiles in the set(s).
- If you cannot make an initial meld, you must draw a tile from the pool and end your turn.

### 2. Valid Sets
- **Group (Set of the Same Number):** 3 or 4 tiles of the same number in different colours (e.g., red 7, blue 7, black 7).
- **Run (Sequence):** 3 or more consecutive numbers in the same colour (e.g., red 3, red 4, red 5). Since the smallest number is one (1) in every colour and the largest is thirteen (13), the players can "connect" the two ends of the row by placing a same-coloured thirteen and one in this order.

### 3. Using Jokers
- A joker can represent any tile in a set.
- If a joker is on the table, you can replace it with the tile it represents by using the actual tile from your rack. The joker must then be used in the same turn to form a new set.

### 4. Manipulating Sets
- After your initial meld, you can rearrange or add tiles to existing sets on the table to create new valid sets.
- You cannot end your turn with an invalid set on the table. All sets must be valid at the end of your turn.

### 5. Drawing Tiles
- If you cannot (or choose not to) play any tiles, you must draw one tile from the pool and end your turn.

---

## Winning the Game
- The first player to play all their tiles wins the game.
- If the draw pool runs out and no one can play their tiles, the game ends in a draw.

---

## Scoring (Optional)
- After a player wins, the remaining players add up the values of the tiles left on their racks.
- The winner scores the total of all other players' tiles.
- Jokers count as 30 points.

---

## Tips
- Plan ahead to create multiple sets in a single turn.
- Use jokers strategically to maximize your options.
- Keep an eye on your opponents' tiles to anticipate their moves.

---

Enjoy playing Rummikub!
