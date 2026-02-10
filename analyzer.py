def analyze_password(password):
    """Analyze a password and return feedback"""
    score = 0
    feedback = []

    # Check length
    if len(password) >= 12:
        score += 2
        feedback.append("Good length (12+ characters).")
    elif len(password) >= 8:
        score += 1
        feedback.append("Decent length (8-11 characters).")
    else:
        feedback.append("Too short (less than 8 characters).")

    # Check character variety
    has_upper = False
    has_lower = False
    has_digit = False
    has_symbol = False

    for char in password:
        if char.isupper():
            has_upper = True
        elif char.islower():
            has_lower = True
        elif char.isdigit():
            has_digit = True
        else:
            has_symbol = True

    if has_upper:
        score += 1
        feedback.append("Contains uppercase letters.")
    else:
        feedback.append("Add uppercase letters.")

    if has_lower:
        score += 1
        feedback.append("Contains lowercase letters.")
    else:        
        feedback.append("Add lowercase letters.")
    
    if has_digit:
        score += 1
        feedback.append("Contains digits.")
    else:
        feedback.append("Add digits.")

    if has_symbol:
        score += 1
        feedback.append("Contains symbols.")
    else:
        feedback.append("Add symbols.")

    return score, feedback

# Test 
test_password = {"hello", "Hello123", "Hello123!", "S3cureP@ssw0rd"}

for pwd in test_password:
    score, feedback = analyze_password(pwd)
    print(f"\nPassword: {pwd}")
    print(f"Score: {score}/6")
    print(f"Feedback: {feedback}")
