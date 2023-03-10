from bs4 import BeautifulSoup
import re
from src.deparas import deparaMercado, deparaTimes
from datetime import datetime


def getSide(market_line, participant_line):
    if "Marco" in market_line or "Mais" in participant_line or "Over" in participant_line:
        return "Over"
    elif "Menos" in participant_line or "Under" in participant_line:
        return "Under"
    else:
        return re.findall(r"\-\s(\w+)", participant_line)[0]


def getLine(market_line, participant_line):
    if "Marco" in market_line:
        return str((int(re.findall(r"Marcar\s(\d+)", participant_line)[0]) - .5)).replace(".", ",")
    else:
        return re.findall(r"[\d\.]+$", participant_line)[0].replace(".", ",")


def buildLine(bet, stake_default):

    betType = bet.find(class_="myb-OpenBetItem_HeaderText").text

    if betType != "Simples":
        return None

    try:
        participantLine = bet.find(class_="myb-BetParticipant_ParticipantSpan").text
    except:
        return None

    stake = bet.find(class_="myb-OpenBetItem_StakeDesc").text
    odd = bet.find(class_="myb-BetParticipant_HeaderOdds").text.replace(".", ",")
    marketLine = bet.find(class_="myb-BetParticipant_MarketDescription").text
    print(marketLine)

    mercado = re.findall(r"\b[\w\s{1}\,À-ú]+", marketLine)

    if len(mercado) < 2:
        return ""
    mercado = deparaMercado(mercado[1])

    if not mercado:
        return None
    print(mercado)
    print(participantLine)
    name = re.findall(r"[\w\s\'\.\-À-ú\’]+\b", participantLine)[0].replace("’", "")
    time = re.findall(r"[\w\s\'\.\-À-ú\’]+\b", participantLine)[1]
    time = deparaTimes(time)
    side = getSide(marketLine, participantLine)
    prop = getLine(marketLine, participantLine)
    stake = float(stake.replace(".", "").replace("R$", "").replace(",", "."))
    unity = stake * 1 / stake_default
    unity = str(round(unity, 2)).replace(".", ",")

    csv_line = "{date}\t{name}\t{time}\t{mercado}\t{side}\t{linha}\tBet365\t{odd}\t{unidade}\n".format(
        date=datetime.now().strftime("%d/%m/%y"),
        name=name,
        time=time,
        mercado=mercado,
        side=side[:1],
        linha=prop,
        odd=odd,
        unidade=unity
    )
    print(csv_line)
    print("------------------------------------------------------")
    return csv_line


def run_scraping_denise(src_page, stake_default):

    with open(src_page, 'r', encoding="utf8") as f:
        webpage = f.read()

    soup = BeautifulSoup(webpage, 'html.parser')

    bet_list = soup.find(class_="myb-BetItemsContainer_BetItemsContainer")

    writerFile = open("saida/bet365Saida.csv", 'w', encoding="utf8")

    for bet_line in bet_list:
        line = buildLine(bet_line, stake_default)
        if line:
            writerFile.write(line)

    writerFile.close()


if __name__ == '__main__':
    run_scraping_denise()
