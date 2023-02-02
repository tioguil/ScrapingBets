import bs4
from bs4 import BeautifulSoup
import re
from src.deparas import deparaMercado, deparaSideBetano
import csv
from datetime import datetime


def findTeam(player_name):
    csv_file = csv.reader(open('data/playersName.csv', "r"), delimiter="\t")

    for row in csv_file:
        if row[0].lower() == player_name.lower():
            return row[1]


def build_line(bet):
    stakeDefault = 450
    house = "Betano"

    simpleBet = bet.find(class_="bet-label__title").text
    if simpleBet != "Simples":
        return ""

    stake = bet.find(class_="total-amounts-item__value").text
    stake = float(stake.replace("R$", "").replace(",", "."))

    odd = bet.find(class_="leg-info").find(class_="bet-odds__value").text
    odd = odd.replace(".", ",").replace(" ", "").replace("\n", "")

    side = bet.find(class_="section-left").find(class_="selection-label").text
    side = re.search(r"\s+(\w+\b)", side)[1]
    side = deparaSideBetano(side)

    if side == '':
        return ""

    line = bet.find(class_="section-left").find(class_="selection-label").text
    line = re.search(r"[\d\.]+$", line)[0]
    line = line.replace(".", ",")

    # market - label
    mercadoLine = bet.find(class_="market-label").text
    mark = re.findall(r"\b[\w\s{1}\,À-ú]+\b", mercadoLine)[0]
    mark = deparaMercado(mark)
    print(mercadoLine)
    if not mark:
        print("Mercado invalido")
        return ""
    print(mark)
    name = re.search(r"(\[).+(\])", mercadoLine)[0]
    name = re.sub(r"[\[\]]", "", name)

    unity = stake * 1 / stakeDefault
    unity = str(round(unity, 2)).replace(".", ",")

    team = findTeam(name) if findTeam(name) else ""

    line = "{date}\t{name}\t{team}\t{mark}\t{side}\t{line}\t{house}\t{odd}\t{unity}\n".format(
        date=datetime.now().strftime("%d/%m/%y"),
        name=name,
        team=team,
        mark=mark,
        side=side,
        line=line,
        house=house,
        odd=odd,
        unity=unity
    )
    print(line)
    print("-----------------------------------------")
    return line


def run_scraping_betano():
    url = 'C:/Users/guil_/Downloads/betanoPage.html'

    with open(url, 'r', encoding="utf8") as f:
        webpage = f.read()

    soup = BeautifulSoup(webpage, 'html.parser')

    bet_list = soup.find(class_="bet-list")

    writerFile = open("../saida/betanoSaida.csv", 'w', encoding="utf8")

    for bet_line in bet_list:

        if type(bet_line) is not bs4.Tag or bet_line.has_attr("class"):
            continue

        line_string = build_line(bet_line)
        if line_string:
            writerFile.write(line_string)

    writerFile.close()

if __name__ == '__main__':
    run_scraping_betano()