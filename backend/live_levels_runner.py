import time
from datetime import datetime

from backend.options_config import TICKER, EXPIRATION_WEIGHTS, MAX_DISTANCE, NUM_LEVELS, REFRESH_SECONDS
from backend.options_common import market_hours_now
from oi_levels import get_oi_levels
from call_put_walls import get_call_put_walls
from gamma_exposure import get_gamma_levels
from max_pain import get_max_pain_levels


def print_model_result(title: str, result: dict):
    print(f"\n{title}")
    print(f"Spot: {result['spot']}")
    print(f"Key Level: {result['key_level']}")
    print("Top Resistances:")
    print(result["top_resistances"].to_string(index=False))
    print("Top Supports:")
    print(result["top_supports"].to_string(index=False))


def run_once():
    print("\n" + "=" * 90)
    print(f"Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    oi = get_oi_levels(TICKER, EXPIRATION_WEIGHTS, MAX_DISTANCE, NUM_LEVELS)
    walls = get_call_put_walls(TICKER, EXPIRATION_WEIGHTS, MAX_DISTANCE, NUM_LEVELS)
    gamma = get_gamma_levels(TICKER, EXPIRATION_WEIGHTS, MAX_DISTANCE, NUM_LEVELS)
    pain = get_max_pain_levels(TICKER, EXPIRATION_WEIGHTS, MAX_DISTANCE, NUM_LEVELS)

    print_model_result("OI LEVELS", oi)
    print_model_result("CALL / PUT WALLS", walls)
    print_model_result("GAMMA LEVELS", gamma)
    print_model_result("MAX PAIN LEVELS", pain)


if __name__ == "__main__":
    while True:
        if market_hours_now():
            try:
                run_once()
            except Exception as e:
                print(f"Error: {e}")
        else:
            print(f"{datetime.now().strftime('%H:%M:%S')} - Market closed or outside run window.")
        time.sleep(REFRESH_SECONDS)
