import requests
import json
import bisect


def calc_elo_rating(contest_id, problem_status):
    print(f"Calculating rating for contest_id: {contest_id}")

    standings = requests.get(f"https://codeforces.com/api/contest.standings?contestId={contest_id}&showUnofficial=false").json()
    rating_changes = requests.get(f"https://codeforces.com/api/contest.ratingChanges?contestId={contest_id}").json()
    try:
        handle_set = set([standings["result"]["rows"][i]["party"]["members"][0]["handle"] for i in range(len(standings["result"]["rows"]))]) and \
            set([rating_changes["result"][i]["handle"] for i in range(len(rating_changes["result"]))])
        standings["result"]["rows"] = [standings["result"]["rows"][i] for i in range(len(standings["result"]["rows"])) if standings["result"]["rows"][i]["party"]["members"][0]["handle"] in handle_set]
        rating_changes["result"] = [rating_changes["result"][i] for i in range(len(rating_changes["result"])) if rating_changes["result"][i]["handle"] in handle_set]
        assert len(standings["result"]["rows"]) == len(rating_changes["result"]) and len(standings["result"]["rows"]) > 200
        print(f"Number of handle: {len(handle_set)}")
    except Exception as e:
        print(e)

    contest_name = standings["result"]["contest"]["name"]

    print(f"Contest name: {contest_name}")
    # if "Div. 1" in contest_name and "Div. 2" not in contest_name:
    #     print("Pass Div. 1")
    #     return

    if "result" not in standings or "result" not in rating_changes or len(standings["result"]["rows"]) != len(rating_changes["result"]) or len(standings["result"]["rows"]) <= 200:
        print("No result")
        return
    max_rating = 0
    for i in range(len(rating_changes["result"])):
        max_rating = max(max_rating, rating_changes["result"][i]["oldRating"])
    score = 0
    penalty = 0
    print(standings.keys())
    print(standings["result"]["problems"])
    for problem in standings["result"]["problems"]:
        prob = f"{problem['contestId']}{problem['index']}"
        if prob in problem_status.keys():
            for ith, status in enumerate(problem_status[prob]):
                if status == "AC":
                    print(f"AC at {prob} in {ith + 1}th submission, total submissions: {len(problem_status[prob])}")
                    if "points" in problem:
                        score += max(0, problem["points"] - 50 * ith)
                    else:
                        score += 1
                        penalty += ith * 10
                    break
                
    print(f"Score: {score}, Penalty: {penalty}")

    n = len(standings["result"]["rows"])
    print(f"Number of participants: {n}, {len(rating_changes['result'])}")
    rank = n
    for i in range(n):
        if standings["result"]["rows"][i]["points"] < score or (standings["result"]["rows"][i]["points"] == score and standings["result"]["rows"][i]["penalty"] > penalty):
            rank = i
            break
    print(f"Rank: {rank}")

    l, r = 0, max_rating + 100
    while r - l > 1:
        mid = int((l + r) / 2)
        new_seed = 1
        for i in range(n):
            new_seed += 1 / (1 + 10 ** ((mid - rating_changes["result"][i]["oldRating"]) / 400))
        if new_seed < rank:
            r = mid
        else:
            l = mid

    print(f"Rating: {l}")
    return l


with open("sorted_ratings.json", "r") as f:
    sorted_ratings = json.load(f)

def get_percentile(rating):
    idx = bisect.bisect_left(sorted_ratings, float(rating))
    return round(idx / len(sorted_ratings) * 100, 1)


if __name__ == "__main__":
    rating = calc_elo_rating(2024, {"2024A": ["WA", "AC"], "2024B": ["AC", "WA"]})
    percentile = get_percentile(rating)
    print(f"rating: {rating}, percentile: {percentile}")
    calc_elo_rating(2024, {"2024A": ["AC", "AC"], "2024B": ["AC", "WA"]})
    calc_elo_rating(2032, {"2024A": ["AC", "AC"], "2024B": ["AC", "WA"]})
