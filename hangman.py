import pygame
import random
import math
import json
import os

pygame.init()

# ============================================================
# CODEALPHA HANGMAN - ULTIMATE EDITION V3
# ============================================================

WIDTH = 1200
HEIGHT = 750

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("CodeAlpha Hangman - Ultimate Edition")

clock = pygame.time.Clock()
FPS = 60

# ============================================================
# COLORS
# ============================================================

BG = (7, 11, 23)
PANEL = (18, 25, 43)
PANEL_LIGHT = (28, 38, 63)

WHITE = (245, 247, 255)
LIGHT = (170, 183, 210)

CYAN = (55, 220, 255)
BLUE = (70, 120, 255)
PURPLE = (170, 90, 255)

GREEN = (55, 225, 145)
RED = (255, 70, 95)
YELLOW = (255, 205, 70)

# ============================================================
# FONTS
# ============================================================

FONT_TITLE = pygame.font.SysFont("arial", 52, bold=True)
FONT_BIG = pygame.font.SysFont("arial", 40, bold=True)
FONT_WORD = pygame.font.SysFont("arial", 40, bold=True)
FONT_MEDIUM = pygame.font.SysFont("arial", 24, bold=True)
FONT_NORMAL = pygame.font.SysFont("arial", 20)
FONT_SMALL = pygame.font.SysFont("arial", 16)


# ============================================================
# WORD DATABASE
# ============================================================

WORDS = {
    "TECHNOLOGY": [
        "python",
        "computer",
        "programming",
        "developer",
        "software",
        "database",
        "algorithm",
        "internet",
        "technology",
        "keyboard"
    ],

    "SCIENCE": [
        "biology",
        "chemistry",
        "physics",
        "molecule",
        "gravity",
        "planet",
        "electron",
        "evolution",
        "microscope",
        "laboratory"
    ],

    "ANIMALS": [
        "elephant",
        "tiger",
        "giraffe",
        "kangaroo",
        "dolphin",
        "penguin",
        "crocodile",
        "butterfly",
        "cheetah",
        "zebra"
    ],

    "SPORTS": [
        "football",
        "cricket",
        "basketball",
        "tennis",
        "baseball",
        "hockey",
        "badminton",
        "swimming",
        "volleyball",
        "boxing"
    ],

    "MOVIES": [
        "avatar",
        "inception",
        "titanic",
        "gladiator",
        "interstellar",
        "avengers",
        "matrix",
        "batman",
        "spiderman",
        "superman"
    ],

    "GENERAL": [
        "mountain",
        "adventure",
        "chocolate",
        "universe",
        "hospital",
        "airplane",
        "friendship",
        "rainbow",
        "festival",
        "journey"
    ]
}


DIFFICULTIES = {
    "EASY": 8,
    "MEDIUM": 6,
    "HARD": 4
}


# ============================================================
# STATISTICS FILE
# ============================================================

STATS_FILE = "statistics.json"


def load_statistics():

    default = {
        "games": 0,
        "wins": 0,
        "losses": 0,
        "score": 0,
        "best_streak": 0
    }

    if not os.path.exists(STATS_FILE):
        return default

    try:

        with open(STATS_FILE, "r") as file:
            data = json.load(file)

        for key in default:

            if key not in data:
                data[key] = default[key]

        return data

    except:

        return default


def save_statistics(data):

    with open(STATS_FILE, "w") as file:
        json.dump(data, file, indent=4)


# ============================================================
# BUTTON
# ============================================================

class Button:

    def __init__(self, x, y, width, height, text, color=PANEL_LIGHT):

        self.rect = pygame.Rect(
            x,
            y,
            width,
            height
        )

        self.text = text
        self.color = color
        self.hover = False

    def update(self, mouse):

        self.hover = self.rect.collidepoint(mouse)

    def draw(self):

        color = self.color

        if self.hover:

            color = (
                min(color[0] + 18, 255),
                min(color[1] + 18, 255),
                min(color[2] + 18, 255)
            )

        pygame.draw.rect(
            screen,
            color,
            self.rect,
            border_radius=12
        )

        pygame.draw.rect(
            screen,
            (65, 80, 115),
            self.rect,
            2,
            border_radius=12
        )

        text = FONT_MEDIUM.render(
            self.text,
            True,
            WHITE
        )

        text_rect = text.get_rect(
            center=self.rect.center
        )

        screen.blit(text, text_rect)


# ============================================================
# PARTICLE
# ============================================================

class Particle:

    def __init__(self):

        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)

        self.speed = random.uniform(
            0.2,
            0.8
        )

        self.size = random.randint(
            1,
            3
        )

    def update(self):

        self.y -= self.speed

        if self.y < 0:

            self.y = HEIGHT
            self.x = random.randint(
                0,
                WIDTH
            )

    def draw(self):

        pygame.draw.circle(
            screen,
            (35, 75, 115),
            (int(self.x), int(self.y)),
            self.size
        )


# ============================================================
# GAME
# ============================================================

class HangmanGame:

    def __init__(self):

        self.running = True

        self.mode = "MENU"

        self.player_name = ""
        self.name_input = ""

        self.category = "TECHNOLOGY"
        self.difficulty = "MEDIUM"

        self.secret_word = ""
        self.guessed_letters = set()

        self.wrong_guesses = 0
        self.max_wrong = 6

        self.game_over = False
        self.win = False

        self.score = 0
        self.streak = 0

        self.message = ""

        self.stats = load_statistics()

        self.particles = []

        for _ in range(80):
            self.particles.append(
                Particle()
            )

        self.create_buttons()


    # ========================================================
    # BUTTONS
    # ========================================================

    def create_buttons(self):

        self.menu_buttons = [

            Button(
                430, 300, 340, 55,
                "PLAY GAME",
                BLUE
            ),

            Button(
                430, 365, 340, 55,
                "DIFFICULTY",
                PURPLE
            ),

            Button(
                430, 430, 340, 55,
                "CATEGORY",
                PANEL_LIGHT
            ),

            Button(
                430, 495, 340, 55,
                "STATISTICS",
                PANEL_LIGHT
            ),

            Button(
                430, 560, 340, 55,
                "HOW TO PLAY",
                PANEL_LIGHT
            )
        ]

        self.difficulty_buttons = [

            Button(
                190, 280, 240, 70,
                "EASY",
                GREEN
            ),

            Button(
                480, 280, 240, 70,
                "MEDIUM",
                BLUE
            ),

            Button(
                770, 280, 240, 70,
                "HARD",
                RED
            ),

            Button(
                440, 600, 320, 55,
                "BACK",
                PANEL_LIGHT
            )
        ]

        categories = list(WORDS.keys())

        self.category_buttons = []

        for index, category in enumerate(categories):

            row = index // 3
            col = index % 3

            self.category_buttons.append(
                Button(
                    150 + col * 300,
                    230 + row * 95,
                    250,
                    65,
                    category,
                    PANEL_LIGHT
                )
            )

        self.category_buttons.append(
            Button(
                440, 600, 320, 55,
                "BACK",
                PANEL_LIGHT
            )
        )

        self.game_buttons = [

            Button(
                35, 675, 175, 50,
                "NEW GAME",
                BLUE
            ),

            Button(
                225, 675, 175, 50,
                "MAIN MENU",
                PANEL_LIGHT
            )
        ]

        self.stats_back = Button(
            440, 620, 320, 55,
            "BACK",
            PANEL_LIGHT
        )

        self.how_back = Button(
            440, 650, 320, 55,
            "BACK",
            PANEL_LIGHT
        )

        self.name_continue = Button(
            440, 410, 320, 60,
            "CONTINUE",
            BLUE
        )


    # ========================================================
    # BACKGROUND
    # ========================================================

    def background(self):

        screen.fill(BG)

        for particle in self.particles:

            particle.update()
            particle.draw()

        for i in range(7):

            x = 100 + i * 180

            y = 110 + math.sin(
                pygame.time.get_ticks() / 1200 + i
            ) * 25

            pygame.draw.circle(
                screen,
                (14, 24, 44),
                (x, int(y)),
                70
            )


    # ========================================================
    # TITLE
    # ========================================================

    def title(self):

        text = FONT_TITLE.render(
            "CODEALPHA HANGMAN",
            True,
            WHITE
        )

        rect = text.get_rect(
            center=(WIDTH // 2, 85)
        )

        screen.blit(text, rect)

        sub = FONT_SMALL.render(
            "ULTIMATE GRAPHICAL EDITION",
            True,
            CYAN
        )

        rect = sub.get_rect(
            center=(WIDTH // 2, 130)
        )

        screen.blit(sub, rect)


    # ========================================================
    # MENU
    # ========================================================

    def draw_menu(self):

        self.background()
        self.title()

        if self.player_name:

            player = FONT_NORMAL.render(
                f"PLAYER: {self.player_name}",
                True,
                YELLOW
            )

            rect = player.get_rect(
                center=(WIDTH // 2, 190)
            )

            screen.blit(player, rect)

        else:

            text = FONT_NORMAL.render(
                "Start your Hangman adventure",
                True,
                LIGHT
            )

            rect = text.get_rect(
                center=(WIDTH // 2, 190)
            )

            screen.blit(text, rect)

        mouse = pygame.mouse.get_pos()

        for button in self.menu_buttons:

            button.update(mouse)
            button.draw()

        footer = FONT_SMALL.render(
            "Python • Pygame • CodeAlpha Internship Project",
            True,
            LIGHT
        )

        rect = footer.get_rect(
            center=(WIDTH // 2, 710)
        )

        screen.blit(footer, rect)


    # ========================================================
    # NAME SCREEN
    # ========================================================

    def draw_name(self):

        self.background()

        title = FONT_BIG.render(
            "ENTER PLAYER NAME",
            True,
            WHITE
        )

        rect = title.get_rect(
            center=(WIDTH // 2, 150)
        )

        screen.blit(title, rect)

        box = pygame.Rect(
            330, 250, 540, 75
        )

        pygame.draw.rect(
            screen,
            PANEL,
            box,
            border_radius=12
        )

        pygame.draw.rect(
            screen,
            CYAN,
            box,
            2,
            border_radius=12
        )

        text = FONT_BIG.render(
            self.name_input,
            True,
            WHITE
        )

        screen.blit(
            text,
            (355, 268)
        )

        mouse = pygame.mouse.get_pos()

        self.name_continue.update(mouse)
        self.name_continue.draw()

        hint = FONT_SMALL.render(
            "Type your name and press ENTER",
            True,
            LIGHT
        )

        rect = hint.get_rect(
            center=(WIDTH // 2, 510)
        )

        screen.blit(hint, rect)


    # ========================================================
    # DIFFICULTY
    # ========================================================

    def draw_difficulty(self):

        self.background()

        title = FONT_BIG.render(
            "SELECT DIFFICULTY",
            True,
            WHITE
        )

        rect = title.get_rect(
            center=(WIDTH // 2, 150)
        )

        screen.blit(title, rect)

        mouse = pygame.mouse.get_pos()

        for button in self.difficulty_buttons:

            button.update(mouse)
            button.draw()

        current = FONT_NORMAL.render(
            f"CURRENT: {self.difficulty}",
            True,
            YELLOW
        )

        rect = current.get_rect(
            center=(WIDTH // 2, 420)
        )

        screen.blit(current, rect)

        descriptions = [
            "8 LIVES",
            "6 LIVES",
            "4 LIVES"
        ]

        for i, text_value in enumerate(descriptions):

            text = FONT_SMALL.render(
                text_value,
                True,
                LIGHT
            )

            rect = text.get_rect(
                center=(310 + i * 290, 480)
            )

            screen.blit(text, rect)


    # ========================================================
    # CATEGORY
    # ========================================================

    def draw_category(self):

        self.background()

        title = FONT_BIG.render(
            "SELECT CATEGORY",
            True,
            WHITE
        )

        rect = title.get_rect(
            center=(WIDTH // 2, 140)
        )

        screen.blit(title, rect)

        mouse = pygame.mouse.get_pos()

        for button in self.category_buttons:

            button.update(mouse)
            button.draw()

        current = FONT_NORMAL.render(
            f"CURRENT: {self.category}",
            True,
            YELLOW
        )

        rect = current.get_rect(
            center=(WIDTH // 2, 560)
        )

        screen.blit(current, rect)


    # ========================================================
    # START GAME
    # ========================================================

    def start_game(self):

        self.secret_word = random.choice(
            WORDS[self.category]
        ).upper()

        self.guessed_letters = set()

        self.wrong_guesses = 0

        self.max_wrong = DIFFICULTIES[
            self.difficulty
        ]

        self.game_over = False
        self.win = False

        self.message = "GUESS A LETTER"


    # ========================================================
    # GUESS
    # ========================================================

    def guess(self, letter):

        if self.game_over:
            return

        if letter in self.guessed_letters:
            return

        self.guessed_letters.add(letter)

        if letter in self.secret_word:

            self.message = "CORRECT!"

            if all(
                char in self.guessed_letters
                for char in self.secret_word
            ):

                self.win = True
                self.game_over = True

                self.stats["games"] += 1
                self.stats["wins"] += 1

                self.streak += 1

                if self.streak > self.stats["best_streak"]:
                    self.stats["best_streak"] = self.streak

                remaining = (
                    self.max_wrong
                    - self.wrong_guesses
                )

                points = (
                    100
                    + remaining * 25
                    + self.streak * 10
                )

                self.score += points

                self.stats["score"] += points

                save_statistics(self.stats)

                self.message = "YOU WON!"

        else:

            self.wrong_guesses += 1

            self.message = "WRONG LETTER!"

            if self.wrong_guesses >= self.max_wrong:

                self.game_over = True
                self.win = False

                self.stats["games"] += 1
                self.stats["losses"] += 1

                self.streak = 0

                save_statistics(self.stats)

                self.message = "GAME OVER"


    # ========================================================
    # HANGMAN
    # ========================================================

    def draw_hangman(self):

        panel = pygame.Rect(
            30, 115, 480, 500
        )

        pygame.draw.rect(
            screen,
            PANEL,
            panel,
            border_radius=20
        )

        pygame.draw.rect(
            screen,
            (45, 60, 90),
            panel,
            2,
            border_radius=20
        )

        label = FONT_MEDIUM.render(
            "HANGMAN",
            True,
            WHITE
        )

        screen.blit(
            label,
            (60, 140)
        )

        # Gallows

        pygame.draw.line(
            screen,
            LIGHT,
            (115, 550),
            (390, 550),
            8
        )

        pygame.draw.line(
            screen,
            LIGHT,
            (175, 550),
            (175, 190),
            8
        )

        pygame.draw.line(
            screen,
            LIGHT,
            (175, 190),
            (340, 190),
            8
        )

        pygame.draw.line(
            screen,
            LIGHT,
            (340, 190),
            (340, 245),
            8
        )

        wrong = self.wrong_guesses

        if wrong >= 1:

            pygame.draw.circle(
                screen,
                RED,
                (340, 285),
                38,
                5
            )

        if wrong >= 2:

            pygame.draw.line(
                screen,
                RED,
                (340, 323),
                (340, 420),
                7
            )

        if wrong >= 3:

            pygame.draw.line(
                screen,
                RED,
                (340, 345),
                (285, 395),
                7
            )

        if wrong >= 4:

            pygame.draw.line(
                screen,
                RED,
                (340, 345),
                (395, 395),
                7
            )

        if wrong >= 5:

            pygame.draw.line(
                screen,
                RED,
                (340, 420),
                (290, 500),
                7
            )

        if wrong >= 6:

            pygame.draw.line(
                screen,
                RED,
                (340, 420),
                (390, 500),
                7
            )


    # ========================================================
    # WORD PANEL
    # ========================================================

    def draw_word_panel(self):

        panel = pygame.Rect(
            540, 115, 630, 240
        )

        pygame.draw.rect(
            screen,
            PANEL,
            panel,
            border_radius=20
        )

        pygame.draw.rect(
            screen,
            (45, 60, 90),
            panel,
            2,
            border_radius=20
        )

        category = FONT_SMALL.render(
            f"CATEGORY: {self.category}",
            True,
            CYAN
        )

        screen.blit(
            category,
            (570, 140)
        )

        display = ""

        for char in self.secret_word:

            if char in self.guessed_letters:

                display += char + " "

            else:

                display += "_ "

        word = FONT_WORD.render(
            display,
            True,
            WHITE
        )

        rect = word.get_rect(
            center=(855, 215)
        )

        screen.blit(word, rect)

        remaining = (
            self.max_wrong
            - self.wrong_guesses
        )

        lives = FONT_MEDIUM.render(
            f"LIVES: {remaining}/{self.max_wrong}",
            True,
            GREEN if remaining > 2 else RED
        )

        rect = lives.get_rect(
            center=(855, 270)
        )

        screen.blit(lives, rect)

        message = FONT_MEDIUM.render(
            self.message,
            True,
            GREEN if self.win else RED if self.game_over else CYAN
        )

        rect = message.get_rect(
            center=(855, 315)
        )

        screen.blit(message, rect)

        if self.game_over:

            if self.win:

                result_text = "WORD SOLVED!"

            else:

                result_text = (
                    f"WORD: {self.secret_word}"
                )

            result = FONT_SMALL.render(
                result_text,
                True,
                YELLOW
            )

            rect = result.get_rect(
                center=(855, 340)
            )

            screen.blit(result, rect)


    # ========================================================
    # KEYBOARD
    # ========================================================

    def draw_keyboard(self):

        letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

        # Smaller keyboard so it ALWAYS fits.

        key_width = 52
        key_height = 43
        gap = 6

        total_width = (
            9 * key_width
            + 8 * gap
        )

        start_x = (
            WIDTH - total_width
        ) // 2 + 150

        start_y = 390

        mouse = pygame.mouse.get_pos()

        for index, letter in enumerate(letters):

            row = index // 9
            col = index % 9

            x = (
                start_x
                + col * (key_width + gap)
            )

            y = (
                start_y
                + row * (key_height + gap)
            )

            rect = pygame.Rect(
                x,
                y,
                key_width,
                key_height
            )

            hover = rect.collidepoint(
                mouse
            )

            if letter in self.guessed_letters:

                if letter in self.secret_word:
                    color = GREEN
                else:
                    color = RED

            else:

                color = PANEL_LIGHT

                if hover:
                    color = (45, 65, 100)

            pygame.draw.rect(
                screen,
                color,
                rect,
                border_radius=8
            )

            pygame.draw.rect(
                screen,
                (65, 80, 115),
                rect,
                2,
                border_radius=8
            )

            text = FONT_NORMAL.render(
                letter,
                True,
                WHITE
            )

            text_rect = text.get_rect(
                center=rect.center
            )

            screen.blit(
                text,
                text_rect
            )


    # ========================================================
    # GAME SCREEN
    # ========================================================

    def draw_game(self):

        self.background()

        title = FONT_MEDIUM.render(
            "CODEALPHA HANGMAN",
            True,
            WHITE
        )

        screen.blit(
            title,
            (30, 30)
        )

        player = FONT_SMALL.render(
            f"PLAYER: {self.player_name}",
            True,
            YELLOW
        )

        screen.blit(
            player,
            (800, 35)
        )

        score = FONT_SMALL.render(
            f"SCORE: {self.score}",
            True,
            GREEN
        )

        screen.blit(
            score,
            (1010, 35)
        )

        self.draw_hangman()
        self.draw_word_panel()
        self.draw_keyboard()

        mouse = pygame.mouse.get_pos()

        for button in self.game_buttons:

            button.update(mouse)
            button.draw()

        difficulty = FONT_SMALL.render(
            f"DIFFICULTY: {self.difficulty}",
            True,
            LIGHT
        )

        rect = difficulty.get_rect(
            center=(800, 700)
        )

        screen.blit(
            difficulty,
            rect

        )


    # ========================================================
    # STATISTICS
    # ========================================================

    def draw_statistics(self):

        self.background()

        title = FONT_BIG.render(
            "PLAYER STATISTICS",
            True,
            WHITE
        )

        rect = title.get_rect(
            center=(WIDTH // 2, 120)
        )

        screen.blit(title, rect)

        games = self.stats["games"]
        wins = self.stats["wins"]

        if games > 0:

            win_rate = int(
                wins / games * 100
            )

        else:

            win_rate = 0

        rows = [

            ("PLAYER", self.player_name or "Not set"),

            ("GAMES PLAYED", str(games)),

            ("GAMES WON", str(wins)),

            ("GAMES LOST", str(self.stats["losses"])),

            ("WIN RATE", f"{win_rate}%"),

            ("BEST STREAK", str(self.stats["best_streak"])),

            ("TOTAL SCORE", str(self.stats["score"]))
        ]

        y = 210

        for label, value in rows:

            left = FONT_MEDIUM.render(
                label,
                True,
                LIGHT
            )

            right = FONT_MEDIUM.render(
                value,
                True,
                CYAN
            )

            screen.blit(
                left,
                (350, y)
            )

            screen.blit(
                right,
                (700, y)
            )

            y += 50

        mouse = pygame.mouse.get_pos()

        self.stats_back.update(mouse)
        self.stats_back.draw()


    # ========================================================
    # HOW TO PLAY
    # ========================================================

    def draw_how(self):

        self.background()

        title = FONT_BIG.render(
            "HOW TO PLAY",
            True,
            WHITE
        )

        rect = title.get_rect(
            center=(WIDTH // 2, 110)
        )

        screen.blit(title, rect)

        instructions = [

            "1. Enter your player name.",

            "2. Select a difficulty level.",

            "3. Select a word category.",

            "4. Guess letters using the keyboard.",

            "5. Green letters are correct.",

            "6. Red letters are incorrect.",

            "7. Solve the word before your lives reach zero.",

            "8. Correct answers increase your score.",

            "9. Consecutive wins increase your streak.",

            "10. Use ESC to return to the main menu."
        ]

        y = 190

        for line in instructions:

            text = FONT_NORMAL.render(
                line,
                True,
                LIGHT
            )

            screen.blit(
                text,
                (250, y)
            )

            y += 38

        mouse = pygame.mouse.get_pos()

        self.how_back.update(mouse)
        self.how_back.draw()


    # ========================================================
    # DRAW
    # ========================================================

    def draw(self):

        if self.mode == "MENU":
            self.draw_menu()

        elif self.mode == "NAME":
            self.draw_name()

        elif self.mode == "DIFFICULTY":
            self.draw_difficulty()

        elif self.mode == "CATEGORY":
            self.draw_category()

        elif self.mode == "GAME":
            self.draw_game()

        elif self.mode == "STATS":
            self.draw_statistics()

        elif self.mode == "HOW":
            self.draw_how()

        pygame.display.flip()


    # ========================================================
    # MOUSE CLICK
    # ========================================================

    def click(self, position):

        # ---------------- MENU ----------------

        if self.mode == "MENU":

            if self.menu_buttons[0].rect.collidepoint(position):

                if self.player_name:
                    self.start_game()
                    self.mode = "GAME"
                else:
                    self.mode = "NAME"

            elif self.menu_buttons[1].rect.collidepoint(position):

                self.mode = "DIFFICULTY"

            elif self.menu_buttons[2].rect.collidepoint(position):

                self.mode = "CATEGORY"

            elif self.menu_buttons[3].rect.collidepoint(position):

                self.mode = "STATS"

            elif self.menu_buttons[4].rect.collidepoint(position):

                self.mode = "HOW"

        # ---------------- NAME ----------------

        elif self.mode == "NAME":

            if self.name_continue.rect.collidepoint(position):

                if self.name_input.strip():

                    self.player_name = (
                        self.name_input.strip()
                    )

                    self.start_game()

                    self.mode = "GAME"

        # ---------------- DIFFICULTY ----------------

        elif self.mode == "DIFFICULTY":

            for button in self.difficulty_buttons[:3]:

                if button.rect.collidepoint(position):

                    self.difficulty = button.text

                    return

            if self.difficulty_buttons[3].rect.collidepoint(position):

                self.mode = "MENU"

        # ---------------- CATEGORY ----------------

        elif self.mode == "CATEGORY":

            for button in self.category_buttons[:-1]:

                if button.rect.collidepoint(position):

                    self.category = button.text

                    self.start_game()

                    self.mode = "GAME"

                    return

            if self.category_buttons[-1].rect.collidepoint(position):

                self.mode = "MENU"

        # ---------------- GAME ----------------

        elif self.mode == "GAME":

            letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

            key_width = 52
            key_height = 43
            gap = 6

            total_width = (
                9 * key_width
                + 8 * gap
            )

            start_x = (
                WIDTH - total_width
            ) // 2 + 150

            start_y = 390

            for index, letter in enumerate(letters):

                row = index // 9
                col = index % 9

                x = (
                    start_x
                    + col * (key_width + gap)
                )

                y = (
                    start_y
                    + row * (key_height + gap)
                )

                rect = pygame.Rect(
                    x,
                    y,
                    key_width,
                    key_height
                )

                if rect.collidepoint(position):

                    self.guess(letter)

                    return

            if self.game_buttons[0].rect.collidepoint(position):

                self.start_game()

            elif self.game_buttons[1].rect.collidepoint(position):

                self.mode = "MENU"

        # ---------------- STATS ----------------

        elif self.mode == "STATS":

            if self.stats_back.rect.collidepoint(position):

                self.mode = "MENU"

        # ---------------- HOW ----------------

        elif self.mode == "HOW":

            if self.how_back.rect.collidepoint(position):

                self.mode = "MENU"


    # ========================================================
    # KEYBOARD
    # ========================================================

    def key_press(self, event):

        # Name screen

        if self.mode == "NAME":

            if event.key == pygame.K_RETURN:

                if self.name_input.strip():

                    self.player_name = (
                        self.name_input.strip()
                    )

                    self.start_game()

                    self.mode = "GAME"

            elif event.key == pygame.K_BACKSPACE:

                self.name_input = (
                    self.name_input[:-1]
                )

            else:

                if len(self.name_input) < 18:

                    if event.unicode.isprintable():

                        self.name_input += (
                            event.unicode
                        )

            return

        # Game

        if self.mode == "GAME":

            if pygame.K_a <= event.key <= pygame.K_z:

                letter = chr(
                    event.key
                ).upper()

                self.guess(letter)

            elif event.key == pygame.K_ESCAPE:

                self.mode = "MENU"

        else:

            if event.key == pygame.K_ESCAPE:

                self.mode = "MENU"


# ============================================================
# MAIN
# ============================================================

def main():

    game = HangmanGame()

    while game.running:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                game.running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:

                if event.button == 1:

                    game.click(
                        event.pos
                    )

            elif event.type == pygame.KEYDOWN:

                game.key_press(event)

        game.draw()

        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":

    main()