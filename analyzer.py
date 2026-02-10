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

    return score, feedback

# Test 
test_password = "hello"
score, feedback = analyze_password(test_password)
print(f"Password: {test_password}")
print(f"Score: {score}")
print(f"Feedback: {feedback}")
