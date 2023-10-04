import random

# Define the teams (placeholders for the coefficients for now)
teams = [
    "UCL Winner", "UEL Winner", "High Coef Team 1", "High Coef Team 2", "ENG1", "ENG2", "ENG3", "ENG4",
    "ESP1", "ESP2", "ESP3", "ESP4", "GER1", "GER2", "GER3", "GER4", "ITA1", "ITA2", "ITA3", "ITA4",
    "FRA1", "FRA2", "FRA3", "NED1", "NED2", "POR1", "BEL1", "SCO1", "AUT1", "CP1", "CP2", "CP3", "CP4", "CP5",
    "LP1", "LP2"
]

# Mock UEFA coefficients (for simplicity, assigned in order)
coefficients = list(range(36, 0, -1))
teams_with_coefficients = sorted(list(zip(teams, coefficients)), key=lambda x: x[1], reverse=True)

# Create the pots
pot1 = teams_with_coefficients[0:9]
pot2 = teams_with_coefficients[9:18]
pot3 = teams_with_coefficients[18:27]
pot4 = teams_with_coefficients[27:36]

# Simulate fixtures
fixtures = []

for team in teams:
    pots = [pot1, pot2, pot3, pot4]

    # Remove the pot that contains the current team
    for pot in pots:
        if team in [t[0] for t in pot]:
            pots.remove(pot)
            break

    home_matches = 4
    away_matches = 4

    # Draw teams
    for pot in pots:
        draw = random.choice(pot)

        # Ensure not from the same association and not drawn before
        while draw[0][:3] == team[:3] or any(team in fixture and draw[0] in fixture for fixture in fixtures):
            draw = random.choice(pot)

        if home_matches > 0:
            fixtures.append((team, draw[0]))
            home_matches -= 1
        else:
            fixtures.append((draw[0], team))
            away_matches -= 1

# Print fixtures
for fixture in fixtures:
    print(f"{fixture[0]} vs {fixture[1]}")
