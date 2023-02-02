from src.scrapingBet365 import run_scraping_denise
from src.scrapingBetano import run_scraping_betano
from src.scrapingStake import run_scraping_stake
import pandas


def unique_file():
    src_list = [
        'saida/bet365Saida.csv',
        'saida/betanoSaida.csv',
        # 'saida/stakeSaida.csv'
    ]
    final_file_src = 'saida/finalFile.csv'

    writerFile = open(final_file_src, 'w', encoding="utf8")

    for src in src_list:
        with open(src, 'r', encoding="utf8") as f:
            lines = f.read()
            writerFile.write(lines)

    df = pandas.read_csv(final_file_src, names=['data', 'jogador', 'time', 'mercado', 'side', 'linha', 'casa', 'odd', 'unidade'])
    df.sort_values(by=["time"], ascending=True)

    writerFile.close()


if __name__ == '__main__':
    run_scraping_betano()
    run_scraping_denise()
    run_scraping_stake()
    unique_file()
    print("Exit")
