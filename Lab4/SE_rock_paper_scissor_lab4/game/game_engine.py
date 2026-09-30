import random
import pygame
from game.button import ChoiceButton


class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.choices = ["ROCK", "PAPER", "SCISSORS"]
        btn_w, btn_h = 130, 50
        gap = 20
        total_w = 3 * btn_w + 2 * gap
        start_x = (width - total_w) // 2
        btn_y = height - 85

        self.buttons = [
            ChoiceButton(
                "ROCK",
                pygame.Rect(start_x, btn_y, btn_w, btn_h),
                (160, 50, 50),
                (200, 70, 70)
            ),
            ChoiceButton(
                "PAPER",
                pygame.Rect(
                    start_x + btn_w + gap,
                    btn_y,
                    btn_w,
                    btn_h
                ),
                (40, 100, 170),
                (60, 130, 210)
            ),
            ChoiceButton(
                "SCISSORS",
                pygame.Rect(
                    start_x + 2 * (btn_w + gap),
                    btn_y,
                    btn_w,
                    btn_h
                ),
                (180, 140, 30),
                (220, 180, 50)
            ),
        ]

        self.player_choice = None
        self.cpu_choice = None
        self.result_text = "Make your move!"
        self.result_color = (220, 225, 235)

        self.player_score = 0
        self.cpu_score = 0

        # Task 2: First to X Wins
        self.target_score = 3
        self.game_state = "PLAYING"
        self.match_winner = None

        # Task 3: Track player choices during the current match
        self.player_history = []

        self.round_resolved_time = 0
        self.display_duration = 1800
        self.showing_result = False

        # Task 4: Duration of the icon reveal/shake animation
        self.shake_duration = 350

        self.font_title = pygame.font.SysFont(None, 36)
        self.font_hud = pygame.font.SysFont(None, 26)
        self.font_arena = pygame.font.SysFont(None, 32)

    def determine_winner(self, player, cpu):
        if player == cpu:
            return "TIE"

        # Task 1: Corrected outcome mappings
        rules = {
            ("ROCK", "SCISSORS"): "PLAYER",
            ("SCISSORS", "PAPER"): "PLAYER",
            ("PAPER", "ROCK"): "PLAYER",
            ("SCISSORS", "ROCK"): "CPU",
            ("PAPER", "SCISSORS"): "CPU",
            ("ROCK", "PAPER"): "CPU",
        }

        return rules.get((player, cpu), "TIE")

    def choose_cpu_move(self):
        """
        Task 3: Choose the CPU move based on the player's history.

        If there is no history yet, choose randomly.

        Once there is history:
        - Find the player's most frequently used move.
        - 70% of the time, choose the move that counters it.
        - 30% of the time, choose a random move.
        """

        if not self.player_history:
            return random.choice(self.choices)

        move_counts = {
            choice: self.player_history.count(choice)
            for choice in self.choices
        }

        most_frequent_move = max(
            move_counts,
            key=move_counts.get
        )

        counter_moves = {
            "ROCK": "PAPER",
            "PAPER": "SCISSORS",
            "SCISSORS": "ROCK",
        }

        counter_move = counter_moves[most_frequent_move]

        if random.random() < 0.7:
            return counter_move

        return random.choice(self.choices)

    def play_round(self, choice):
        if self.game_state == "GAME_OVER" or self.showing_result:
            return

        self.player_choice = choice

        # Task 3: Record the player's move
        self.player_history.append(choice)

        self.cpu_choice = self.choose_cpu_move()

        outcome = self.determine_winner(
            self.player_choice,
            self.cpu_choice
        )

        if outcome == "PLAYER":
            self.player_score += 1
            self.result_text = (
                f"You Win! {self.player_choice} beats {self.cpu_choice}."
            )
            self.result_color = (80, 230, 120)

            if self.player_score >= self.target_score:
                self.match_winner = "PLAYER"

        elif outcome == "CPU":
            self.cpu_score += 1
            self.result_text = (
                f"You Lose! {self.cpu_choice} beats {self.player_choice}."
            )
            self.result_color = (240, 80, 80)

            if self.cpu_score >= self.target_score:
                self.match_winner = "CPU"

        else:
            self.result_text = (
                f"It's a Draw! Both picked {self.player_choice}."
            )
            self.result_color = (240, 210, 80)

        self.showing_result = True
        self.round_resolved_time = pygame.time.get_ticks()

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            if self.game_state == "GAME_OVER":
                self.player_score = 0
                self.cpu_score = 0
                self.player_choice = None
                self.cpu_choice = None
                self.result_text = "Make your move!"
                self.result_color = (220, 225, 235)
                self.match_winner = None

                # Task 3: Reset player history for the new match
                self.player_history = []

                self.showing_result = False
                self.game_state = "PLAYING"

            return

        if self.game_state == "GAME_OVER":
            return

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.showing_result:
                return
             
            for btn in self.buttons:
                if btn.contains(event.pos):
                    self.play_round(btn.choice_name)
                    break

    def update(self):
        now = pygame.time.get_ticks()

        if self.showing_result and (
            now - self.round_resolved_time >= self.display_duration
        ):
            self.player_choice = None
            self.cpu_choice = None
            self.showing_result = False

            if self.match_winner == "PLAYER":
                self.game_state = "GAME_OVER"
            elif self.match_winner == "CPU":
                self.game_state = "GAME_OVER"
            else:
                self.result_text = "Make your move!"
                self.result_color = (190, 195, 205)

    # ---------------------------------------------------------
    # Task 4: Procedural geometric icons
    # ---------------------------------------------------------

    def draw_rock_icon(self, screen, center):
        """Draw a simple procedural rock/stone icon."""
        cx, cy = center

        points = [
            (cx - 42, cy + 22),
            (cx - 36, cy - 15),
            (cx - 15, cy - 34),
            (cx + 18, cy - 31),
            (cx + 40, cy - 8),
            (cx + 34, cy + 24),
            (cx + 8, cy + 36),
            (cx - 20, cy + 32),
        ]

        pygame.draw.polygon(
            screen,
            (120, 125, 135),
            points
        )

        pygame.draw.polygon(
            screen,
            (185, 188, 195),
            [
                (cx - 15, cy - 34),
                (cx + 18, cy - 31),
                (cx + 5, cy - 5),
                (cx - 22, cy - 8),
            ]
        )

        pygame.draw.line(
            screen,
            (70, 75, 85),
            (cx - 42, cy + 22),
            (cx - 20, cy + 32),
            3
        )

        pygame.draw.line(
            screen,
            (70, 75, 85),
            (cx - 20, cy + 32),
            (cx + 8, cy + 36),
            3
        )

        pygame.draw.line(
            screen,
            (70, 75, 85),
            (cx + 8, cy + 36),
            (cx + 34, cy + 24),
            3
        )

    def draw_paper_icon(self, screen, center):
        """Draw a procedural sheet-of-paper icon."""
        cx, cy = center

        paper_rect = pygame.Rect(
            cx - 32,
            cy - 42,
            64,
            84
        )

        pygame.draw.rect(
            screen,
            (235, 235, 240),
            paper_rect,
            border_radius=3
        )

        pygame.draw.rect(
            screen,
            (90, 95, 105),
            paper_rect,
            width=3,
            border_radius=3
        )

        # Folded top-right corner
        fold = [
            (cx + 10, cy - 42),
            (cx + 32, cy - 20),
            (cx + 10, cy - 20),
        ]

        pygame.draw.polygon(
            screen,
            (190, 195, 205),
            fold
        )

        pygame.draw.line(
            screen,
            (90, 95, 105),
            (cx + 10, cy - 42),
            (cx + 10, cy - 20),
            3
        )

        pygame.draw.line(
            screen,
            (90, 95, 105),
            (cx + 10, cy - 20),
            (cx + 32, cy - 20),
            3
        )

        # Simple paper lines
        for offset in (-5, 8, 21):
            pygame.draw.line(
                screen,
                (150, 155, 165),
                (cx - 20, cy + offset),
                (cx + 20, cy + offset),
                2
            )

    def draw_scissors_icon(self, screen, center):
        """Draw procedural crossing scissors blades and handles."""
        cx, cy = center

        # Handles
        pygame.draw.circle(
            screen,
            (220, 150, 45),
            (cx - 22, cy + 24),
            13,
            4
        )

        pygame.draw.circle(
            screen,
            (220, 150, 45),
            (cx + 22, cy + 24),
            13,
            4
        )

        # Crossing blades
        pygame.draw.line(
            screen,
            (190, 195, 205),
            (cx - 13, cy + 14),
            (cx + 36, cy - 35),
            9
        )

        pygame.draw.line(
            screen,
            (220, 225, 235),
            (cx + 13, cy + 14),
            (cx - 36, cy - 35),
            9
        )

        # Blade edges
        pygame.draw.line(
            screen,
            (85, 90, 100),
            (cx - 13, cy + 14),
            (cx + 36, cy - 35),
            2
        )

        pygame.draw.line(
            screen,
            (85, 90, 100),
            (cx + 13, cy + 14),
            (cx - 36, cy - 35),
            2
        )

        # Center pivot
        pygame.draw.circle(
            screen,
            (90, 95, 105),
            (cx, cy + 8),
            5
        )

    def draw_choice_icon(self, screen, choice, center):
        """Draw the appropriate icon for a selected move."""
        if choice == "ROCK":
            self.draw_rock_icon(screen, center)
        elif choice == "PAPER":
            self.draw_paper_icon(screen, center)
        elif choice == "SCISSORS":
            self.draw_scissors_icon(screen, center)

    def get_shake_offset(self, elapsed):
        """
        Return a small horizontal/vertical offset during the
        initial reveal animation. The offset decreases to zero.
        """
        if elapsed >= self.shake_duration:
            return 0, 0

        progress = elapsed / self.shake_duration

        # Strong at the beginning, then settles to zero.
        amplitude = int(10 * (1.0 - progress))

        if amplitude <= 0:
            return 0, 0

        # Fast alternating shake.
        direction = -1 if (elapsed // 45) % 2 == 0 else 1

        return direction * amplitude, direction * amplitude // 2

    def render(self, screen):
        screen.fill((24, 28, 36))

        title_surf = self.font_title.render(
            "Rock Paper Scissors",
            True,
            (245, 245, 245)
        )

        screen.blit(
            title_surf,
            (
                self.width // 2 - title_surf.get_width() // 2,
                14
            )
        )

        p_surf = self.font_hud.render(
            f"Player Score: {self.player_score}",
            True,
            (100, 180, 255)
        )

        c_surf = self.font_hud.render(
            f"CPU Score: {self.cpu_score}",
            True,
            (255, 120, 120)
        )

        screen.blit(p_surf, (35, 52))
        screen.blit(
            c_surf,
            (
                self.width - c_surf.get_width() - 35,
                52
            )
        )

        pygame.draw.line(
            screen,
            (45, 52, 66),
            (25, 82),
            (self.width - 25, 82),
            2
        )

        # -----------------------------------------------------
        # Task 2: GAME_OVER screen remains unchanged in behavior
        # -----------------------------------------------------
        if self.game_state == "GAME_OVER":
            winner_text = (
                "You Win the Match!"
                if self.match_winner == "PLAYER"
                else "CPU Wins the Match!"
            )

            winner_surf = self.font_arena.render(
                winner_text,
                True,
                (
                    (80, 230, 120)
                    if self.match_winner == "PLAYER"
                    else (240, 80, 80)
                )
            )

            restart_surf = self.font_arena.render(
                "Press R to Restart",
                True,
                (225, 225, 230)
            )

            screen.blit(
                winner_surf,
                (
                    self.width // 2 - winner_surf.get_width() // 2,
                    125
                )
            )

            screen.blit(
                restart_surf,
                (
                    self.width // 2 - restart_surf.get_width() // 2,
                    175
                )
            )

            return

        # -----------------------------------------------------
        # Task 4: Selection icons and reveal animation
        # -----------------------------------------------------
        if self.player_choice and self.cpu_choice:
            elapsed = pygame.time.get_ticks() - self.round_resolved_time

            player_center = (self.width // 2 - 145, 145)
            cpu_center = (self.width // 2 + 145, 145)

            if elapsed < self.shake_duration:
                offset_x, offset_y = self.get_shake_offset(elapsed)

                player_center = (
                    player_center[0] + offset_x,
                    player_center[1] + offset_y
                )

                cpu_center = (
                    cpu_center[0] - offset_x,
                    cpu_center[1] - offset_y
                )

                # Icons shake during the reveal phase.
                self.draw_choice_icon(
                    screen,
                    self.player_choice,
                    player_center
                )

                self.draw_choice_icon(
                    screen,
                    self.cpu_choice,
                    cpu_center
                )

                # Keep the result hidden until the shake settles.
                reveal_text = self.font_arena.render(
                    "Revealing...",
                    True,
                    (190, 195, 205)
                )

                screen.blit(
                    reveal_text,
                    (
                        self.width // 2
                        - reveal_text.get_width() // 2,
                        235
                    )
                )

            else:
                # Final settled positions.
                self.draw_choice_icon(
                    screen,
                    self.player_choice,
                    player_center
                )

                self.draw_choice_icon(
                    screen,
                    self.cpu_choice,
                    cpu_center
                )

                player_label = self.font_hud.render(
                    self.player_choice,
                    True,
                    (225, 225, 230)
                )

                cpu_label = self.font_hud.render(
                    self.cpu_choice,
                    True,
                    (225, 225, 230)
                )

                screen.blit(
                    player_label,
                    (
                        player_center[0]
                        - player_label.get_width() // 2,
                        195
                    )
                )

                screen.blit(
                    cpu_label,
                    (
                        cpu_center[0]
                        - cpu_label.get_width() // 2,
                        195
                    )
                )

                # Existing round result remains visible after
                # the reveal animation has settled.
                res_surf = self.font_arena.render(
                    self.result_text,
                    True,
                    self.result_color
                )

                screen.blit(
                    res_surf,
                    (
                        self.width // 2
                        - res_surf.get_width() // 2,
                        235
                    )
                )

        else:
            # Normal UI when there are no selections.
            res_surf = self.font_arena.render(
                self.result_text,
                True,
                self.result_color
            )

            screen.blit(
                res_surf,
                (
                    self.width // 2
                    - res_surf.get_width() // 2,
                    205
                )
            )

        # Choice buttons remain active and rendered normally.
        for btn in self.buttons:
            btn.render(screen)