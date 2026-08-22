# Reinforcement Learning Maze Solver


An interactive reinforcement learning project where an agent learns to navigate procedurally generated mazes through trial and error.

The project combines a recursive maze-generation algorithm with a Q-learning agent, allowing the agent to learn which actions produce better outcomes based on rewards and penalties.

## Project Demo

The program visually generates a random maze, trains an agent through repeated episodes, and then visualizes the trained agent navigating the maze.

> The maze is generated algorithmically rather than manually designed, allowing the environment to change between runs.

---

## How It Works

<img width="546" height="546" alt="maze_GIF" src="https://github.com/user-attachments/assets/ec541dd8-a6b2-4962-8b68-f946db51130c" />

The project is built around a reinforcement learning loop:

```text
              ┌─────────────────┐
              │      AGENT      │
              │                 │
              │   Q-Table       │
              └────────┬────────┘
                       │
                  Choose Action
                       │
                       ▼
              ┌─────────────────┐
              │  ENVIRONMENT    │
              │                 │
              │      MAZE       │
              └────────┬────────┘
                       │
                 Reward + State
                       │
                       ▼
              ┌─────────────────┐
              │  UPDATE Q-TABLE │
              └────────┬────────┘
                       │
                       └──────────────► Repeat
```

At each step, the agent:

1. Observes its current state.
2. Selects an action.
3. Moves through the maze.
4. Receives a reward or penalty.
5. Updates its Q-value.
6. Repeats this process over thousands of training episodes.

Over time, the agent learns which actions are more likely to lead toward the goal.

---

## Reinforcement Learning

This project uses **Q-learning**, a model-free reinforcement learning algorithm.

The agent maintains a Q-table where each state contains values representing the expected usefulness of each possible action.

For this project:

```text
0 = Up
1 = Down
2 = Left
3 = Right
```

A simplified representation of the Q-table looks like:

```text
State (1, 1)

Up       → Q-value
Down     → Q-value
Left     → Q-value
Right    → Q-value
```

Initially, the agent has no knowledge of which actions are useful.

Through exploration and repeated interaction with the environment, the Q-values are updated based on the rewards received.

### Reward System

| Event | Reward |
|-------|--------|
| Reach goal | +100 |
| Valid movement | -1 |
| Hit wall | -5 |

The large positive reward for reaching the goal encourages the agent to discover paths that eventually lead to the destination.

---

## Maze Generation

The maze is procedurally generated using **recursive backtracking**, a depth-first-search-based maze generation technique.

The algorithm:

1. Starts at an initial cell.
2. Randomizes the possible directions.
3. Selects an unvisited neighboring cell.
4. Removes the wall between the cells.
5. Recursively continues from the new cell.
6. Backtracks when no unvisited neighboring cells remain.

Because the directions are randomized, the resulting maze changes between generations.

---

## Visualization

The project uses **Pygame** to provide a visual representation of both the maze and the trained agent.

During maze generation, individual passages are carved and rendered on screen.

During the final demonstration:

- Red cells represent maze walls.
- Green represents the reinforcement learning agent.
- Yellow represents the goal.
- Black represents traversable paths.

This makes it possible to visually observe the agent navigating the environment rather than only viewing numerical training results.

---

## Training Process

The agent is initially highly exploratory.

For example:

```text
Early training:

Agent → random movement
       ↓
Hits walls
       ↓
Receives negative rewards
       ↓
Explores different actions
```

As training progresses:

```text
Later training:

Agent → uses learned Q-values
       ↓
Chooses increasingly useful actions
       ↓
Moves toward goal
       ↓
Reaches goal more consistently
```

The agent uses an epsilon-greedy strategy to balance exploration and exploitation.

Early in training, the agent frequently tries random actions.

As training progresses, the exploration rate decreases and the agent increasingly relies on its learned Q-values.

---

## Technologies

### Python

Core programming language used to implement the maze generation, environment, agent, and training system.

### Pygame

Used to create the interactive visualization and render:

- Maze walls
- Maze paths
- Agent position
- Goal position
- Maze generation process
- Agent navigation

### Reinforcement Learning

The project implements Q-learning to allow the agent to learn through trial and error.

### Q-Table

Stores the learned value of taking each possible action from each state.

### Recursive Backtracking

Used to procedurally generate randomized mazes.

---

## Running the Project

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/maze-reinforcement-learning.git
```

### 2. Enter the project directory

```bash
cd maze-reinforcement-learning
```

### 3. Install Pygame

```bash
pip install pygame
```

### 4. Run the program

```bash
python maze_ai.py
```

The program will:

1. Generate a random maze.
2. Visually display the maze generation process.
3. Train the reinforcement learning agent.
4. Run the trained agent through the maze.
5. Visually display the learned path.

---

## Project Architecture

```text
maze-reinforcement-learning/
│
├── maze_ai.py
│
└── README.md
```

The main program contains four major components:

```text
Maze Generator
      │
      ▼
Maze Environment
      │
      ▼
Q-Learning Agent
      │
      ▼
Training Loop
```

### Maze Generator

Creates the procedural environment.

### Maze Environment

Controls the agent's position, available movements, rewards, and goal conditions.

### Agent

Selects actions and updates its Q-values based on experience.

### Training Loop

Runs thousands of interactions between the agent and environment.

---

## Future Improvements

Potential future versions of the project could include:

- Training across thousands of different randomly generated mazes
- Deep Q-Networks (DQN)
- PyTorch-based neural network agent
- Larger and more complex environments
- Real-time training visualization
- Training statistics and reward graphs
- Comparing Q-learning against traditional search algorithms
- Saving and loading trained models
- Adjustable maze difficulty
- Agent path visualization
- Performance benchmarking across maze sizes

---

## What I Learned

This project explores several concepts in computer science and artificial intelligence:

- Reinforcement learning
- Q-learning
- Exploration vs. exploitation
- State and action representations
- Reward-based learning
- Procedural generation
- Recursive algorithms
- Depth-first search
- Object-oriented programming
- Algorithm visualization
- Python development
- Pygame graphics and event handling

---

## Author

**Enjal Parajuli**

Built as an independent AI/algorithm project exploring reinforcement learning and procedural maze generation.
