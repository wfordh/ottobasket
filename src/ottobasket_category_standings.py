import requests
from bs4 import BeautifulSoup
import pandas as pd


def main():
    league_id = 26
    league_url = f"https://ottoneu.fangraphs.com/basketball/{league_id}/standings"

    r = requests.get(league_url)
    soup = BeautifulSoup(r.content, "html.parser")

    category_standings = soup.find_all("div", {"class": "table-container"})[1].find(
        "table"
    )
    headers = [
        th.text.strip() for th in category_standings.find("thead").find_all("th")
    ]
    rows = category_standings.find("tbody").find_all("tr")
    data = [[td.text.strip() for td in row.find_all("td")] for row in rows]
    categories_df = pd.DataFrame(data, columns=headers)
    for col in categories_df.columns:
        try:
            categories_df[col] = pd.to_numeric(categories_df[col])
        except ValueError:
            # already an object column
            pass
    print(categories_df.dtypes)

    categories_df["PTS_rk"] = categories_df.PTS.rank()
    categories_df["REB_rk"] = categories_df.REB.rank()
    categories_df["AST_rk"] = categories_df.AST.rank()
    categories_df["STL_rk"] = categories_df.STL.rank()
    categories_df["BLK_rk"] = categories_df.BLK.rank()
    categories_df["FG%_rk"] = categories_df["FG%"].rank()
    categories_df["FTM_rk"] = categories_df.FTM.rank()
    categories_df["3PT%_rk"] = categories_df["3PT%"].rank()
    categories_df["TOV_rk"] = categories_df.TOV.rank(ascending=False)

    keep_cols = [
        col for col in categories_df if col in ["Team", "G", "Min"] or "_rk" in col
    ]
    rank_cols = [col for col in categories_df if "_rk" in col]
    categories_df["Total"] = categories_df[rank_cols].sum(axis=1)
    sorted_cats_df = categories_df.sort_values(by=["Total"], axis=0, ascending=False)
    print(sorted_cats_df)
    sorted_cats_df.to_csv("./sorted_cats_standings.csv", index=False)


if __name__ == "__main__":
    main()
