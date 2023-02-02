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


def buildLine(bet):
    stakeDefault = 450

    betType = bet.find(class_="myb-SettledBetItemHeader_Text").text

    if betType.find("Simples") == -1:
        return None

    try:
        participantLine = bet.find(class_="myb-BetParticipant_ParticipantSpan").text
    except:
        return None

    stake = bet.find(class_="myd-StakeDisplay_StakeWrapper").text
    odd = bet.find(class_="myb-BetParticipant_HeaderOdds").text.replace(".", ",")
    marketLine = bet.find(class_="myb-BetParticipant_MarketDescription").text
    result_str = bet.find(class_="myb-SettledBetItem_BetStateContainer").text
    print(marketLine)

    print(result_str)

    result = "W"
    if "Perdida" in result_str:
        result = "L"

    print(result)

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
    stake = float(stake.replace("R$", "").replace(",", "."))
    unity = stake * 1 / stakeDefault
    unity = str(round(unity, 2)).replace(".", ",")

    csv_line = "{date}\t{name}\t{time}\t{mercado}\t{side}\t{linha}\tBet365\t{odd}\t{unidade}\t{result}\n".format(
        date=datetime.now().strftime("%d/%m/%y"),
        name=name,
        time=time,
        mercado=mercado,
        side=side[:1],
        linha=prop,
        odd=odd,
        unidade=unity,
        result=result
    )
    print(csv_line)
    print("------------------------------------------------------")
    return csv_line


def run_scraping_denise():
    src = 'C:/Users/guil_/Downloads/bet365Page.html'

    with open(src, 'r', encoding="utf8") as f:
        webpage = f.read()

    soup = BeautifulSoup(webpage, 'html.parser')

    bet_list = soup.find(class_="myb-BetItemsContainer_BetItemsContainer")

    writerFile = open("../saida/bet365SaidaResult.csv", 'w', encoding="utf8")

    for bet_line in bet_list:
        line = buildLine(bet_line)
        if line:
            writerFile.write(line)

    writerFile.close()


if __name__ == '__main__':
    run_scraping_denise()
