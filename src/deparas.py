def deparaMercado(mercado):
    match mercado:
        case 'Assistências':
            return "Ast"
        case 'Pontos':
            return "Pts"
        case 'Ressaltos':
            return "Reb"
        case 'Rebotes':
            return "Reb"
        case 'Total de Pontos':
            return "Pts"
        case 'Pontos e Ressaltos':
            return "PR"
        case 'Pontos e Assistências':
            return "PA"
        case 'Pontos, Assistências e Ressaltos':
            return "PRA"
        case 'Assistências e Ressaltos':
            return "AR"
        case 'Total de Assistências':
            return "Ast"
        case 'Total de Rebotes':
            return "Reb"
        case 'Total de Pontos, Rebotes e Assistências':
            return "PRA"
        case 'Total de Pontos e Rebotes':
            return "PR"
        case 'Total de Pontos e Assistências':
            return "PA"
        case 'Total de Rebotes e Assistências':
            return "RA"
        case 'Total de Perdas de Bola':
            return "TUR"
        case 'Total Arremessos de três pontos Marcados':
            return "Triplo"
        case _:
            return ""
#

def deparaSideBetano(side):
    match side:
        case 'Mais':
            return "O"
        case 'Menos':
            return "U"
        case _:
            return ""


def deparaTimes(time):
    match time:
        case 'BOS Celtics':
            return "BOS"
        case 'PHI 76ers':
            return "PHI"
        case 'GS Warriors':
            return "GSW"
        case 'LA Lakers':
            return "LAL"
        case 'DET Pistons':
            return "DET"
        case 'ORL Magic':
            return "ORL"
        case 'IND Pacers':
            return "IND"
        case 'WAS Wizards':
            return "WAS"
        case 'MIA Heat':
            return "MIA"
        case 'CLE Cavaliers':
            return "CLE"
        case 'TOR Raptors':
            return "TOR"
        case 'ATL Hawks':
            return "ATL"
        case 'HOU Rockets':
            return "HOU"
        case 'NO Pelicans':
            return "NOP"
        case 'MEM Grizzlies':
            return "MEM"
        case 'NY Knicks':
            return "NYK"
        case 'CHA Hornets':
            return "CHA"
        case 'SA Spurs':
            return "SAS"
        case 'MIN Timberwolves':
            return "MIN"
        case 'OKC Thunder':
            return "OKC"
        case 'UTA Jazz':
            return "UTA"
        case 'DAL Mavericks':
            return "DAL"
        case 'PHX Suns':
            return "PHX"
        case 'POR Trail Blazers':
            return "POR"
        case 'MIL Bucks':
            return "MIL"
        case 'LA Clippers':
            return "LAC"
        case 'CHI Bulls':
            return "CHI"
        case 'DEN Nuggets':
            return "DEN"
        case 'SAC Kings':
            return "SAC"
        case 'BKN Nets':
            return "BKN"
        case _:
            return ""
