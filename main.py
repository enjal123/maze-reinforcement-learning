import pygame
import random
import time


# ============================================================
# PYGAME SETUP
# ============================================================

pygame.init()

WIDTH = 550
HEIGHT = 550

ROWS = 11
COLS = 11

BOX_SIZE = WIDTH // COLS

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Reinforcement Learning Maze Solver")

clock = pygame.time.Clock()


# ============================================================
# COLORS
# ============================================================

WALL_COLOR = (255, 0, 0)
PATH_COLOR = (0, 0, 0)
AGENT_COLOR = (0, 255, 0)
GOAL_COLOR = (255, 215, 0)


# ============================================================
# MAZE
# ============================================================

maze = [[1 for _ in range(COLS)] for _ in range(ROWS)]


def reset_maze():
    """
    Creates a completely new maze.
    """

    global maze

    maze = [[1 for _ in range(COLS)] for _ in range(ROWS)]

    visited = set()

    maze[1][1] = 0
    visited.add((1, 1))

    generate_maze(1, 1, visited)


def generate_maze(r, c, visited):
    """
    Recursive backtracking maze-generation algorithm.
    """

    directions = ["left", "right", "up", "down"]

    random.shuffle(directions)

    for direction in directions:

        new_r = r
        new_c = c

        if direction == "left":
            new_c -= 2

        elif direction == "right":
            new_c += 2

        elif direction == "up":
            new_r -= 2

        elif direction == "down":
            new_r += 2

        # Make sure the new cell is inside the maze
        if 0 <= new_r < ROWS and 0 <= new_c < COLS:

            # Make sure we haven't visited it
            if (new_r, new_c) not in visited:

                visited.add((new_r, new_c))

                # Find the wall between the cells
                wall_r = (r + new_r) // 2
                wall_c = (c + new_c) // 2

                # Remove the wall
                maze[wall_r][wall_c] = 0

                # Open the new cell
                maze[new_r][new_c] = 0

                # Show maze generation
                draw_maze()

                pygame.time.delay(25)

                generate_maze(new_r, new_c, visited)


# ============================================================
# DRAWING
# ============================================================

def draw_maze(agent_position=None, show_goal=True):
    """
    Draws the maze and optionally the agent and goal.
    """

    screen.fill(PATH_COLOR)

    # Draw walls
    for r in range(ROWS):

        for c in range(COLS):

            if maze[r][c] == 1:

                pygame.draw.rect(
                    screen,
                    WALL_COLOR,
                    (
                        c * BOX_SIZE,
                        r * BOX_SIZE,
                        BOX_SIZE,
                        BOX_SIZE
                    )
                )

    # Draw goal
    if show_goal:

        goal = (ROWS - 2, COLS - 2)

        pygame.draw.circle(
            screen,
            GOAL_COLOR,
            (
                goal[1] * BOX_SIZE + BOX_SIZE // 2,
                goal[0] * BOX_SIZE + BOX_SIZE // 2
            ),
            BOX_SIZE // 3
        )

    # Draw agent
    if agent_position is not None:

        r, c = agent_position

        pygame.draw.circle(
            screen,
            AGENT_COLOR,
            (
                c * BOX_SIZE + BOX_SIZE // 2,
                r * BOX_SIZE + BOX_SIZE // 2
            ),
            BOX_SIZE // 3
        )

    pygame.display.flip()


# ============================================================
# MAZE ENVIRONMENT
# ============================================================

class MazeEnvironment:

    def __init__(self, maze):

        self.maze = maze

        self.start = (1, 1)
        self.goal = (ROWS - 2, COLS - 2)

        self.agent_position = self.start

    def reset(self):

        self.agent_position = self.start

        return self.agent_position

    def step(self, action):

        r, c = self.agent_position

        new_r = r
        new_c = c

        # 0 = up
        # 1 = down
        # 2 = left
        # 3 = right

        if action == 0:
            new_r -= 1

        elif action == 1:
            new_r += 1

        elif action == 2:
            new_c -= 1

        elif action == 3:
            new_c += 1

        # ----------------------------------------------------
        # Hit wall
        # ----------------------------------------------------

        if not (0 <= new_r < ROWS and 0 <= new_c < COLS):

            reward = -5

            return self.agent_position, reward, False

        if self.maze[new_r][new_c] == 1:

            reward = -5

            return self.agent_position, reward, False

        # ----------------------------------------------------
        # Valid movement
        # ----------------------------------------------------

        self.agent_position = (new_r, new_c)

        # ----------------------------------------------------
        # Reached goal
        # ----------------------------------------------------

        if self.agent_position == self.goal:

            reward = 100

            return self.agent_position, reward, True

        # ----------------------------------------------------
        # Normal movement
        # ----------------------------------------------------

        reward = -1

        return self.agent_position, reward, False


# ============================================================
# Q-LEARNING AGENT
# ============================================================

class Agent:

    def __init__(self):

        # Q-table
        #
        # State:
        #     (row, column)
        #
        # Action:
        #     0 = up
        #     1 = down
        #     2 = left
        #     3 = right

        self.q_table = {}

        # Learning rate
        self.learning_rate = 0.1

        # Discount factor
        self.discount_factor = 0.9

        # Exploration probability
        self.epsilon = 1.0

        # Minimum exploration probability
        self.epsilon_min = 0.05

        # How quickly exploration decreases
        self.epsilon_decay = 0.995

    def get_q_values(self, state):

        if state not in self.q_table:

            self.q_table[state] = [0.0, 0.0, 0.0, 0.0]

        return self.q_table[state]

    def choose_action(self, state, training=True):

        q_values = self.get_q_values(state)

        # ----------------------------------------------------
        # Exploration
        # ----------------------------------------------------

        if training and random.random() < self.epsilon:

            return random.randint(0, 3)

        # ----------------------------------------------------
        # Exploitation
        # ----------------------------------------------------

        max_q = max(q_values)

        best_actions = []

        for action in range(4):

            if q_values[action] == max_q:

                best_actions.append(action)

        return random.choice(best_actions)

    def learn(self, state, action, reward, next_state):

        q_values = self.get_q_values(state)

        next_q_values = self.get_q_values(next_state)

        # Best possible future value
        best_future_value = max(next_q_values)

        # Q-learning formula
        target = reward + (
            self.discount_factor * best_future_value
        )

        # Update Q value
        q_values[action] += self.learning_rate * (
            target - q_values[action]
        )

    def decrease_exploration(self):

        if self.epsilon > self.epsilon_min:

            self.epsilon *= self.epsilon_decay


# ============================================================
# TRAINING
# ============================================================

def train_agent(env, agent):

    EPISODES = 5000

    MAX_STEPS = 500

    print()
    print("Starting training...")
    print()

    for episode in range(EPISODES):

        state = env.reset()

        done = False

        total_reward = 0

        for step in range(MAX_STEPS):

            action = agent.choose_action(
                state,
                training=True
            )

            next_state, reward, done = env.step(action)

            agent.learn(
                state,
                action,
                reward,
                next_state
            )

            state = next_state

            total_reward += reward

            if done:
                break

        # Gradually stop exploring
        agent.decrease_exploration()

        # Print progress
        if (episode + 1) % 100 == 0:

            print(
                f"Episode {episode + 1}/{EPISODES} "
                f"| Reward: {total_reward:.0f} "
                f"| Epsilon: {agent.epsilon:.3f}"
            )

    print()
    print("Training complete.")
    print()


# ============================================================
# WATCH TRAINED AGENT
# ============================================================

def watch_agent(env, agent):

    print("Running trained agent...")

    state = env.reset()

    done = False

    steps = 0

    while not done and steps < 500:

        # Keep window responsive
        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                pygame.quit()
                return

        # Choose best learned action
        action = agent.choose_action(
            state,
            training=False
        )

        next_state, reward, done = env.step(action)

        state = next_state

        draw_maze(
            agent_position=state
        )

        pygame.time.delay(100)

        steps += 1

    if done:

        print(
            f"Agent reached the goal in {steps} steps!"
        )

    else:

        print(
            "Agent did not reach the goal."
        )


# ============================================================
# MAIN
# ============================================================

# Generate maze
reset_maze()

# Create environment
env = MazeEnvironment(maze)

# Create agent
agent = Agent()

# Train agent
train_agent(env, agent)

# Watch agent solve maze
watch_agent(env, agent)


# ============================================================
# KEEP WINDOW OPEN
# ============================================================

running = True

while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            running = False

    draw_maze()

    clock.tick(60)


pygame.quit()