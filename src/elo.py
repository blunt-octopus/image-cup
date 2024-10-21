import json

def get_ranking(image_id: str):
    with open('data/state/ranking.json', 'r') as f:
        ranking = json.load(f)['ranking']
    return ranking[image_id]

def update_elo(winner_elo: int, loser_elo: int) -> tuple[int, int]:
    with open('config.json', 'r') as f:
        config = json.load(f)
    
    k_factor = config['k_factor']
    
    # Calculate expected scores
    expected_winner = 1 / (1 + 10 ** ((loser_elo - winner_elo) / 400))
    expected_loser = 1 - expected_winner
    
    # Calculate new ratings
    new_winner_elo = round(winner_elo + k_factor * (1 - expected_winner))
    new_loser_elo = round(loser_elo + k_factor * (0 - expected_loser))
    
    return new_winner_elo, new_loser_elo
