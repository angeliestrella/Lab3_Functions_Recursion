# access_control.py

# Decorator for logging
def audit_log(func):
    def wrapper(level, threshold):
        print("Authorization Started")
        result = func(level, threshold)
        print("Authorization Completed")
        return result
    return wrapper

def compute_access_level(control_num, artist):
    return (control_num * 3) + len(artist)

# Apply the decorator to the validation function
@audit_log
def validate_access(level, threshold):
    if level >= threshold:
        return "ACCESS GRANTED"
    else:
        return "ACCESS DENIED"
