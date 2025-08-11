# Problem: https://projecteuler.net/problem=144
from math import sqrt

def reflect_direction(x_value, y_value, vx_value, vy_value):
    normal_x = 8.0 * x_value
    normal_y = 2.0 * y_value

    dot_product = vx_value * normal_x + vy_value * normal_y
    normal_norm_sq = normal_x * normal_x + normal_y * normal_y

    scale = 2.0 * dot_product / normal_norm_sq

    rx_value = vx_value - scale * normal_x
    ry_value = vy_value - scale * normal_y

    return rx_value, ry_value


def next_intersection(x_value, y_value, vx_value, vy_value):
    a_value = 4.0 * vx_value * vx_value + vy_value * vy_value
    b_value = 8.0 * x_value * vx_value + 2.0 * y_value * vy_value
    c_value = 4.0 * x_value * x_value + y_value * y_value - 100.0

    discriminant_value = b_value * b_value - 4.0 * a_value * c_value
    sqrt_discriminant = sqrt(discriminant_value)

    t1_value = (-b_value + sqrt_discriminant) / (2.0 * a_value)
    t2_value = (-b_value - sqrt_discriminant) / (2.0 * a_value)

    t_candidates = [t1_value, t2_value]
    t_next = None

    for t_value in t_candidates:
        if t_value > 1e-10:
            if t_next is None or t_value < t_next:
                t_next = t_value

    next_x = x_value + t_next * vx_value
    next_y = y_value + t_next * vy_value

    return next_x, next_y


def count_reflections():
    previous_x = 0.0
    previous_y = 10.1

    current_x = 1.4
    current_y = -9.6

    hit_count = 0

    while True:
        incoming_vx = current_x - previous_x
        incoming_vy = current_y - previous_y

        reflected_vx, reflected_vy = reflect_direction(
            current_x,
            current_y,
            incoming_vx,
            incoming_vy,
        )

        next_x, next_y = next_intersection(
            current_x,
            current_y,
            reflected_vx,
            reflected_vy,
        )

        previous_x, previous_y = current_x, current_y
        current_x, current_y = next_x, next_y

        hit_count += 1

        if abs(current_x) <= 0.01 and current_y > 0.0:
            break

    return hit_count


def main():
    result_value = count_reflections()
    print(result_value)


if __name__ == "__main__":
    main()
