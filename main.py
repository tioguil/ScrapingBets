from src.scrapingBet365 import run_scraping_denise
from src.scrapingBetano import run_scraping_betano
from src.scrapingStake import run_scraping_stake
import pandas


def merging_files():
    src_list_output = [
        'saida/bet365Saida.csv',
        'saida/betanoSaida.csv',
        # 'saida/stakeSaida.csv'
    ]
    final_file_src = 'saida/finalFile.csv'

    writerFile = open(final_file_src, 'w', encoding="utf8")

    for src in src_list_output:
        with open(src, 'r', encoding="utf8") as f:
            lines = f.read()
            writerFile.write(lines)

    writerFile.close()
    df = pandas.read_csv(final_file_src,
                         names=['data', 'jogador', 'time', 'mercado', 'side', 'linha', 'casa', 'odd', 'unidade'],
                         sep='\t')
    df.sort_values(by=["time"], ascending=True).to_csv("saida/finalFileOrd.csv", encoding='utf-8', sep='\t',
                                                       index=False)


if __name__ == '__main__':
    stake = 400
    run_scraping_betano('C:/Users/guil_/Downloads/betanoPage.html', stake)
    run_scraping_denise('C:/Users/guil_/Downloads/bet365Page.html', stake)
    # run_scraping_stake('C:/Users/guil_/Downloads/stake.html', stake)
    merging_files()
    print("Exit")
