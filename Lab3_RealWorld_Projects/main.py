# main.py
import access_control

# --- REQUIRED INPUTS ---
STUDENT_ID = "TUPM-25-0590"       # Replace with your actual ID
FAVORITE_ARTIST = "Arthur Nery"  # Replace with your favorite artist (UPPERCASE)

# --- SETUP VARIABLES ---
SEED_NUM = int(STUDENT_ID[-1])
CONTROL_NUM = max(1, SEED_NUM)
threshold = CONTROL_NUM * 5

# --- EXERCISE 1 EXECUTION ---
print("=== EXERCISE 1: SECURE ACCESS SYSTEM ===")
access_level = access_control.compute_access_level(CONTROL_NUM, FAVORITE_ARTIST)

# This will trigger the decorator and the validation
decision = access_control.validate_access(access_level, threshold)

# --- ASSESSMENT DATA OUTPUT ---
print("\n[Assessment Data for Manual]")
print(f"CONTROL_NUM Used: {CONTROL_NUM}")
print(f"FAVORITE_ARTIST Length: {len(FAVORITE_ARTIST)}")
print(f"Computed Access Level: {access_level}")
print(f"Threshold Applied: {threshold}")
print(f"Final Authorization Decision: {decision}")
print("========================================\n")

import media_engine

# ==========================================
# === EXERCISE 2: RECURSIVE SIGNAL SHUTDOWN ===
# ==========================================
print("\n=== EXERCISE 2: RECURSIVE SIGNAL SHUTDOWN ===")

# Decorator for Exercise 2
def auth_logger(func):
    def wrapper(power, calls=0):
        if calls == 0: 
            print("Authorization Started")
        
        result = func(power, calls)
        
        if power == 0: 
            print("Authorization Completed")
        return result
    return wrapper

# Recursive Function
@auth_logger
def signal_shutdown(power, calls=0):
    if power == 0:
        return calls
    print(f"Current signal strength: {power}")
    return signal_shutdown(power - 1, calls + 1)

# Execute Exercise 2
initial_power = CONTROL_NUM + len(FAVORITE_ARTIST)
total_calls = signal_shutdown(initial_power)

print("\n[Assessment Data for Ex 2]")
print(f"CONTROL_NUM Used: {CONTROL_NUM}")
print(f"Initial Signal Strength: {initial_power}")
print(f"Base Case Condition: power == 0")
print(f"Total Recursive Calls: {total_calls}")


# ==========================================
# === EXERCISE 3: STREAMING MEDIA ANALYTICS ===
# ==========================================
print("\n=== EXERCISE 3: STREAMING MEDIA ANALYTICS ===")

stream_limit = CONTROL_NUM + len(FAVORITE_ARTIST)
total_plays = 0
records_processed = 0
play_history = []

# Loop through the generator
for plays in media_engine.play_count_stream(stream_limit):
    play_history.append(plays)
    total_plays += plays
    records_processed += 1

print("\n[Assessment Data for Ex 3]")
print(f"CONTROL_NUM Used: {CONTROL_NUM}")
print(f"FAVORITE_ARTIST Used: {FAVORITE_ARTIST}")
print(f"Computed Stream Limit: {stream_limit}")
print(f"Generated Play Counts: {play_history}")
print(f"Total Plays (Sum): {total_plays}")
print(f"Number of Records Processed: {records_processed}")
print("========================================\n")
