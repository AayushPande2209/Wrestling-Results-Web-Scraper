# scraper.py
import requests
from bs4 import BeautifulSoup


HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


def scrape_matches(url: str):
    """
    Scrapes a DubStat tournament/results page and returns match pairs.

    Returns:
    [
        [
            {"name": "...", "team": "...", "result": "W", "score": "...", "round": "..."},
            {"name": "...", "team": "...", "result": "L", "score": "...", "round": "..."}
        ]
    ]
    """
    res = requests.get(url, headers=HEADERS, timeout=30)
    res.raise_for_status()

    soup = BeautifulSoup(res.text, "html.parser")
    matches = []

    # DubStat often uses table rows for results
    rows = soup.select("#results-table table tbody tr")
    
    for row in rows:
        cols = [td.text.strip() for td in row.select("td")]

        date = cols[0]
        event = cols[1]
        round_ = cols[2]
        weight = cols[3]
        wl = cols[4]
        result = cols[5]
        opponent = cols[6]
        opp_school = cols[7]


    if not rows:
        print("No rows found. Page structure may differ.")

    for row in rows:
        cols = row.find_all("td")
        if len(cols) < 4:
            continue

        w1_name = cols[0].get_text(strip=True)
        w2_name = cols[1].get_text(strip=True)
        score = cols[2].get_text(strip=True)
        round_name = cols[3].get_text(strip=True)

        if not w1_name or not w2_name:
            continue

        # Simple winner detection (customize later)
        if score and ("-" in score):
            left, right = score.split("-", 1)
            try:
                left_score = int(left.strip())
                right_score = int(right.strip())
                if left_score > right_score:
                    r1, r2 = "W", "L"
                else:
                    r1, r2 = "L", "W"
            except:
                r1, r2 = "W", "L"
        else:
            r1, r2 = "W", "L"

        matches.append([
            {
                "name": w1_name,
                "team": None,
                "result": r1,
                "score": score,
                "round": round_name
            },
            {
                "name": w2_name,
                "team": None,
                "result": r2,
                "score": score,
                "round": round_name
            }
        ])

    print(f"Scraped {len(matches)} matches")
    return matches
