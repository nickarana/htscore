import os
from dotenv import load_dotenv
import pandas as pd
import module_universal as univ
from module_universal import csvW,csvA
import datetime
from module_TeamDict import TD
from pychpp import CHPP


def MLXCA(s1,csvin,csvout):
    
    s2 = univ.s1_s2_dict[s1]
    sH = univ.s1_sH_dict[s1]
    csvMRA1 = 'MatchRatings7D_' + s1 + '_archive.csv' # archive for one season, usually this season, but can change
    csvMRA2 = 'MatchRatings7D_' + s2 + '_archive.csv' # archive for one season, usually this season, but can change
    csvMLF = 'MatchList_Full_' + s1 + '.csv' # matchlist for the current season
    csvMLWCN = 'MatchList_WorldCupNew.csv' # matchlist for the current season, WC + U20
    csvMLC = 'MatchList_Cup_' + s1 + '.csv' # matchlist for the current season
    csvMLP = 'MatchList_Promo_' + s1 + '.csv' # matchlist for the current season
    csvMLH = 'MatchList_HTM.csv'

    TD(csvMLF,csvMLC,csvMLWCN)
##    print(TD.TeamID_LeagueName_dict['520558'])

    MA = pd.read_csv(csvout,usecols=['MatchID'])
    MA['MatchID']=MA['MatchID'].astype(int)
    match_list_MA = MA['MatchID'].to_list()
    
    MRA1=pd.read_csv(csvMRA1)
    MRA2=pd.read_csv(csvMRA2)
    MRA1=MRA1[(MRA1['TacticType']==2) & (MRA1['HatStats']>=350)]
    MRA2=MRA2[(MRA2['TacticType']==2) & (MRA2['HatStats']>=350)]
    MRA=pd.concat([MRA1,MRA2])
    MRA['HatXmid']=MRA['RatingRightDef'] + MRA['RatingMidDef'] + MRA['RatingLeftDef'] +  \
    MRA['RatingRightAtt'] + MRA['RatingMidAtt']+ MRA['RatingLeftAtt']
    MRA=MRA[(MRA['HatXmid']>=350)]
    xca_team_list=MRA['TeamID'].astype(int).to_list()
    ##print(len(list(set(xca_team_list))))

    MLWC=pd.read_csv(csvMLWCN,usecols=['HomeTeamID','SeriesID','MatchID','WorldCup'])
    MLWC=MLWC[(MLWC['SeriesID']>8000000)]
    wc_season_dict = MLWC.set_index('MatchID')['WorldCup'].to_dict()
    ##print(len(MLWC))
    mlwc_team_list=MLWC['HomeTeamID'].astype(int).to_list()
    ##print(len(list(set(mlwc_team_list))))

    #### this means it is a WC, not U21
    xca_team_list.extend(mlwc_team_list)
    ##print(len(list(set(xca_team_list))))
    #unique list, not repeating
    xca_team_list=list(set(xca_team_list))
    ##print(len(list(set(xca_team_list))))
    MLHTM = pd.read_csv(csvMLH,usecols=['MatchID'])
    MLHTM['MatchID']=MLHTM['MatchID'].astype(int)
    match_list_MLHTM = MLHTM['MatchID'].to_list()

    now = datetime.datetime.now()
    date_min = now - datetime.timedelta(weeks=1)


    col_MLL=['MatchID','MatchDate','MatchRound','XCATeam','XCATeamID','Comp','Season','LeagueName']
    MLL=pd.DataFrame(data=None,columns=col_MLL)
    for csvML in [csvMLF,csvMLC,csvMLP,csvMLWCN]:
        print(csvML)
        if csvML == csvMLWCN:
            ML=pd.read_csv(csvML,usecols=['MatchID','MatchDate','HomeTeamID','AwayTeamID','MatchRound','WorldCup'],parse_dates=['MatchDate'], date_parser=univ.dateparse1)
        else:              
            ML=pd.read_csv(csvML,usecols=['MatchID','MatchDate','HomeTeamID','AwayTeamID','MatchRound'],parse_dates=['MatchDate'], date_parser=univ.dateparse1)
        ML=ML[(ML['MatchDate']>=date_min)]
        ML['Comp']=''        
        if csvML == csvMLF:
            ML['Comp']='L'
            ML['Season']=sH
        elif csvML == csvMLC:
            ML['Comp']='C'
            ML['Season']=sH
        elif csvML == csvMLP:
            ML['Comp']='P'
            ML['Season']=sH
        elif csvML == csvMLWCN:
            ML['Comp']='I'
            ML['Season']=ML['WorldCup']
        ML.loc[(ML['MatchID'].isin(match_list_MLHTM)),'Comp']='H'
        

        MLH=ML[(ML['HomeTeamID'].astype(int).isin(xca_team_list))].copy()
        MLH['XCATeam']='H'
        MLH['XCATeamID']=MLH['HomeTeamID'].astype(int)
        MLH['LeagueName']=MLH['XCATeamID'].astype(str).map(TD.TeamID_LeagueName_dict)
        MLH=MLH[col_MLL]
        MLA=ML[(ML['AwayTeamID'].astype(int).isin(xca_team_list))].copy()
        MLA['XCATeam']='A'
        MLA['XCATeamID']=MLA['AwayTeamID'].astype(int)
        MLA['LeagueName']=MLA['XCATeamID'].astype(str).map(TD.TeamID_LeagueName_dict)
        MLA=MLA[col_MLL]

        MLL=pd.concat([MLL,MLH,MLA])

    
    print('MLL',len(MLL))
###### remove match already
    MLL= MLL[~(MLL['MatchID'].isin(match_list_MA))]
    print('MLL',len(MLL))
    csvW(MLL,'MatchList_XCA.csv')




def PA_match_process(csvin,csvout,hours_):
    now = datetime.datetime.now()
    date_min = now - datetime.timedelta(hours=hours_)
    date_max= now - datetime.timedelta(hours=3)

    ML0 = pd.read_csv(csvin, parse_dates=['MatchDate'],date_parser=univ.dateparse1)
    ML0['MatchID'] = ML0['MatchID'].astype(int)
    ML = ML0[(ML0['MatchDate']>=date_min) & (ML0['MatchDate']<date_max)].copy()

    match_list_ML= ML['MatchID'].to_list()
    MLZ = ML0[(~ML0['MatchID'].isin(match_list_ML))]
    
    MLH = ML[(ML['XCATeam']=='H')]
    MLA = ML[(ML['XCATeam']=='A')]
    
    match_list_home = MLH['MatchID'].to_list()
    match_list_away = MLA['MatchID'].to_list()
    print(len(match_list_home),len(match_list_away))

    ML['mid_tid']=ML['MatchID'].astype(int).astype(str)+'_'+ML['XCATeamID'].astype(int).astype(str)
    midtid_season_dict = ML.set_index('mid_tid')['Season'].to_dict()
    midtid_round_dict = ML.set_index('mid_tid')['MatchRound'].to_dict()
    midtid_comp_dict = ML.set_index('mid_tid')['Comp'].to_dict()
    midtid_country_dict = ML.set_index('mid_tid')['LeagueName'].to_dict()
    
    
    col_XCA = ['MatchID','TeamID','TeamName','LeagueName','Season','MatchRound','Competition','TacticSkill','HatXmid','HatStats','HatAtt','HatDef','Mid','AttL','AttM','AttR','DefL','DefM','DefR']
    XCA = pd.DataFrame(data=None,columns=col_XCA)
    for matchid in match_list_home:    
        try:
            match = chpp.match(ht_id=matchid,source="htointegrated",events=True)
        except:
            match = chpp.match(ht_id=matchid,events=True)
##        print(matchid)
        if match.home_team_tactic_type == '2':
            rating_right_att = match.home_team_rating_right_att
            rating_left_att = match.home_team_rating_left_att
            rating_mid_att = match.home_team_rating_mid_att
            rating_right_def = match.home_team_rating_right_def
            rating_left_def = match.home_team_rating_left_def
            rating_mid_def = match.home_team_rating_mid_def
            rating_midfield = match.home_team_rating_midfield
            hat_x_mid = rating_right_att + rating_mid_att + rating_left_att + rating_right_def + rating_mid_def + rating_left_def
            hat = rating_midfield * 3 + rating_right_att + rating_mid_att + rating_left_att + rating_right_def + rating_mid_def + rating_left_def

##            print(matchid,hat_x_mid)
            if hat_x_mid >= 400:
##                print(matchid)
                hat_att = rating_right_att + rating_mid_att + rating_left_att
                hat_def = rating_right_def + rating_mid_def + rating_left_def
                match_type = match.type
                team_id = match.home_team_id
                team_name = match.home_team_name
                tac_skill = match.home_team_tactic_skill
                mid_tid = str(int(matchid)) + '_' + str(int(team_id))
                season = midtid_season_dict[mid_tid]
                matchround = midtid_round_dict[mid_tid]
                comp = midtid_comp_dict[mid_tid]
                country = midtid_country_dict[mid_tid]
                XCA.loc[0] = [matchid,team_id,team_name,country,season,matchround,comp, tac_skill, hat_x_mid,hat, hat_att,hat_def,(rating_midfield+3)/4,(rating_left_att+3)/4,(rating_mid_att+3)/4,(rating_right_att+3)/4,(rating_left_def+3)/4,(rating_mid_def+3)/4,(rating_right_def+3)/4]
                print(XCA)
                csvA(XCA,csvout)    

    for matchid in match_list_away:    
        try:
            match = chpp.match(ht_id=matchid,source="htointegrated",events=True)
        except:
            match = chpp.match(ht_id=matchid,events=True)
##        print(matchid)
        if match.away_team_tactic_type == '2':
            rating_right_att = match.away_team_rating_right_att
            rating_left_att = match.away_team_rating_left_att
            rating_mid_att = match.away_team_rating_mid_att
            rating_right_def = match.away_team_rating_right_def
            rating_left_def = match.away_team_rating_left_def
            rating_mid_def = match.away_team_rating_mid_def
            rating_midfield = match.away_team_rating_midfield
            hat_x_mid = rating_right_att + rating_mid_att + rating_left_att + rating_right_def + rating_mid_def + rating_left_def
            hat = rating_midfield * 3 + rating_right_att + rating_mid_att + rating_left_att + rating_right_def + rating_mid_def + rating_left_def

##            print(matchid,hat_x_mid)
            if hat_x_mid >= 400:
##                print(matchid)
                hat_att = rating_right_att + rating_mid_att + rating_left_att
                hat_def = rating_right_def + rating_mid_def + rating_left_def
                match_type = match.type
                team_id = match.away_team_id
                team_name = match.away_team_name
                tac_skill = match.away_team_tactic_skill
                mid_tid = str(int(matchid)) + '_' + str(int(team_id))
                season = midtid_season_dict[mid_tid]
                matchround = midtid_round_dict[mid_tid]
                comp = midtid_comp_dict[mid_tid]
                country = midtid_country_dict[mid_tid]
                XCA.loc[0] = [matchid,team_id,team_name,country,season,matchround,comp, tac_skill, hat_x_mid,hat,hat_att,hat_def,(rating_midfield+3)/4,(rating_left_att+3)/4,(rating_mid_att+3)/4,(rating_right_att+3)/4,(rating_left_def+3)/4,(rating_mid_def+3)/4,(rating_right_def+3)/4]
                print(XCA)
                csvA(XCA,csvout)        
    

    csvW(MLZ,csvin)


load_dotenv()
chpp = CHPP(os.getenv('chpp_consumer_key'),
            os.getenv('chpp_consumer_secret'),
            os.getenv('chpp_access_token_1'),
            os.getenv('chpp_access_token_2')
            )
csvin='MatchList_XCA.csv'
csvout = 'xca_new.csv'
MLXCA('23C',csvin,csvout)
##PA_match_process(csvin,csvout,4)
##        
##








##
##csvMLWCN = 'MatchList_WorldCupNew.csv'
##csvMLWCO = 'MatchList_WorldCup.csv' 
##MLWCN=pd.read_csv(csvMLWCN,usecols=['HomeTeamID','SeriesID','MatchID','WorldCup'])
##MLWCO=pd.read_csv(csvMLWCO,usecols=['HomeTeamID','SeriesID','MatchID','WorldCup'])
##MLWC=pd.concat([MLWCN,MLWCO])
##
##MLWC['MatchID']=MLWC['MatchID'].astype(int)
######MLWC=MLWC[(MLWC['SeriesID']>8000000)]
####wc_season_dict = MLWC.set_index('MatchID')['WorldCup'].to_dict()
####
####MLWC=pd.read_csv(csvMLWCN,usecols=['HomeTeamID','SeriesID','MatchID','WorldCup'])
####MLWC=MLWC[(MLWC['SeriesID']>8000000)]
##wc_season_dict = MLWC.set_index('MatchID')['WorldCup'].to_dict()
##
##
##XCA0 = pd.read_csv('XCA.csv')
##XCA0['MatchID']=XCA0['MatchID'].astype(int)
##mid_hat_dict = XCA0.set_index('MatchID')['HatStats'].to_dict()
##
##XCA=pd.read_csv(csvout)
##XCA['MatchID']=XCA['MatchID'].astype(int)
##XCA['HatStats']=XCA['MatchID'].map(mid_hat_dict)
####XCA['HatStats'] = (XCA['Mid']*4-3) * 3 + \
####    (XCA['DefR']*4-3) + (XCA['DefM']*4-3) + XCA['DefL'] +  \
####    XCA['AttR'] + XCA['AttM']+ XCA['AttL']
##col_XCA = ['MatchID','TeamID','TeamName','LeagueName','Season','MatchRound','Competition','TacticSkill','HatXmid','HatStats','HatAtt','HatDef','Mid','AttL','AttM','AttR','DefL','DefM','DefR']
##XCA=XCA[col_XCA]  
##XCA.loc[(XCA['Competition']=='WC/U20'),'Competition']='I'
##XCA.loc[(XCA['Competition']=='I'),'Season']=XCA['MatchID'].map(wc_season_dict)
##csvW(XCA,csvout)
##
####col_XCA = ['MatchID','TeamID','TeamName','LeagueName','Season','MatchRound','Competition','TacticSkill','HatXmid','HatAtt','HatDef','Mid','AttL','AttM','AttR','DefL','DefM','DefR']
####xca = pd.read_csv('XCA.csv')
####xca = xca[col_XCA]
####csvW(xca,'xca_new.csv')
####PA_match_process(csvin)
####    
####       MRAout_col = ['MatchID', 'Competition', 'Season', 'MatchRound', 'LeagueLevelUnitID',
####                    'LeagueName', 'LeagueLevel', 'Location',
####                   'TeamID', 'TeamName', 'Mid','AttL','AttM','AttR','DefL','DefM','DefR',
####                    'MM','MatchLen', 'TacticSkill', 'HatStats',
####                      'HatXmid','HatAtt','HatDef']
#### 
##
##

