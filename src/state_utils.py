import json
import datetime

def update_ranking(winner_id, winner_rating):
    with open('data/state/ranking.json', 'r') as f:
        ranking = json.load(f)
    ranking['ranking'][winner_id] = winner_rating
    with open('data/state/ranking.json', 'w') as f:
        json.dump(ranking, f)

def update_log(winner_id, loser_id):
    with open('data/state/log.txt', 'a') as f:
        f.write(f"{datetime.datetime.now()} {winner_id} {loser_id}\n")
