# Problem: https://projecteuler.net/problem=232
from tqdm import tqdm

MAX_T_VALUE = 40
SCORE_LIMIT = 100

p2_win_prob_on_p1_turn = [[0.0 for _ in range(SCORE_LIMIT)] for _ in range(SCORE_LIMIT)]
p2_win_prob_on_p2_turn = [[0.0 for _ in range(SCORE_LIMIT)] for _ in range(SCORE_LIMIT)]

for p1_score in tqdm(range(SCORE_LIMIT - 1, -1, -1)):
    for p2_score in range(SCORE_LIMIT - 1, -1, -1):
        if p1_score + 1 >= SCORE_LIMIT:
            prob_p2_wins_if_p2_fails = 0.0
        else:
            prob_p2_wins_if_p2_fails = p2_win_prob_on_p2_turn[p1_score + 1][p2_score]

        max_p2_win_prob = -1.0
        best_prob_on_p1_turn = 0.0

        for t_attempts in range(1, MAX_T_VALUE + 1):
            success_prob = 1.0 / (1 << t_attempts)
            points_gained = 1 << (t_attempts - 1)
            new_p2_score = p2_score + points_gained

            if new_p2_score >= SCORE_LIMIT:
                prob_p2_wins_if_p2_succeeds = 1.0
            else:
                prob_p2_wins_if_p2_succeeds = p2_win_prob_on_p1_turn[p1_score][new_p2_score]

            current_prob_on_p1_turn = (success_prob * prob_p2_wins_if_p2_succeeds + prob_p2_wins_if_p2_fails) / (1.0 + success_prob)
            current_p2_win_prob = (1.0 - success_prob) * current_prob_on_p1_turn + success_prob * prob_p2_wins_if_p2_succeeds

            if current_p2_win_prob > max_p2_win_prob:
                max_p2_win_prob = current_p2_win_prob
                best_prob_on_p1_turn = current_prob_on_p1_turn

        p2_win_prob_on_p2_turn[p1_score][p2_score] = max_p2_win_prob
        p2_win_prob_on_p1_turn[p1_score][p2_score] = best_prob_on_p1_turn

print(f"{p2_win_prob_on_p1_turn[0][0]:.8f}")