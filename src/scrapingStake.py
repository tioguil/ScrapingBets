from bs4 import BeautifulSoup
import re
import csv
from datetime import datetime


def find_mark(outcome_name_string):
    long_mark = re.search(r"[\d.]+ (.+)", outcome_name_string)[1]

    match long_mark:
        case "Pontos":
            return "Pts"
        case "Assistências":
            return "Ast"
        case "Rebotes":
            return "Reb"
        case "Pontos + Assistências":
            return "PA"
        case "Pontos + Rebotes":
            return "PR"
        case "Pontos + Assistências":
            return "PA"
        case "Pontos + Assistências + Rebotes":
            return "PRA"
        case "Assistências + Rebotes":
            return "RA"
        case _:
            return ""


def find_team(player_name):
    csv_file = csv.reader(open('src/data/playersName.csv', "r"), delimiter="\t")

    for row in csv_file:
        if row[0].lower() == player_name.lower():
            return row[1]


def build_line(bet, stake, stake_default):
    house = "Stake"

    overview_bet = bet.find(class_="overview")
    player_name = overview_bet.findAll("span")[2].text
    print("player_name", player_name)

    team = find_team(player_name)
    if not team:
        return None
    print("team", team)

    outcome_name = overview_bet.find(class_="outcome-name")
    outcome_name_string = outcome_name.select('span')[0].text
    print("outcome_name_string", outcome_name_string)

    side = None
    if "over" in outcome_name_string:
        side = "O"
    elif "under" in outcome_name_string:
        side = "U"

    if not side:
        return None
    print("side", side)

    line = re.search(r"[\d.]+", outcome_name_string)[0]
    line = line.replace(".", ",")
    print("line", line)

    mark = find_mark(outcome_name_string)
    print("mark", mark)

    odd = overview_bet.find(class_="odds")
    odd_string = odd.select('span')[0].text
    print(odd_string)

    unity = stake * 1 / stake_default
    unity = str(round(unity, 2)).replace(".", ",")

    csv_line = "{date}\t{name}\t{team}\t{mark}\t{side}\t{line}\t{house}\t{odd}\t{unity}\n".format(
        date=datetime.now().strftime("%d/%m/%y"),
        name=player_name,
        team=team,
        mark=mark,
        side=side,
        line=line,
        house=house,
        odd=odd_string,
        unity=unity
    )
    print(csv_line)
    print("-----------------------------------------")
    return csv_line


def find_stake(bet_line):
    currency = bet_line.find(class_="currency")
    currency_content = currency.find(class_="content")
    formated_stake = currency_content.select('span')[0].text
    stake = float(formated_stake.replace("R$", "").replace(",", "."))

    return stake


def run_scraping_stake(src_page, stake_default):

    with open(src_page, 'r', encoding="utf8") as f:
        webpage = f.read()

    soup = BeautifulSoup(webpage, 'html.parser')

    bet_list = soup.find(class_="betlist-scroll")

    writerFile = open("saida/stakeSaida.csv", 'w', encoding="utf8")

    for bet_line in bet_list:

        tickets = bet_line.find(class_="bet-outcome-list").findAll(class_="ticket")

        if len(tickets) > 1:
            continue

        number_stake = find_stake(bet_line)
        line_string = build_line(tickets[0], number_stake)

        if line_string:
            writerFile.write(line_string)

    writerFile.close()


if __name__ == '__main__':
    run_scraping_stake()
