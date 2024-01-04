
from pychpp import CHPP
##from module_CHPP_NH import CHPP_NH
import os
from dotenv import load_dotenv
import pandas as pd
import numpy as np
from scipy.stats import poisson
import pa_hts_mappings_v4 as htsm
import datetime


#### bring in chpp env variables
load_dotenv()
### establish CHPP connection
##CHPP_NH=CHPP_NH()

chpp = CHPP(os.getenv('chpp_consumer_key'),
            os.getenv('chpp_consumer_secret'),
            os.getenv('chpp_access_token_1'),
            os.getenv('chpp_access_token_2')
            )

##
##chpp = CHPP(CHPP_NH[0],
##            CHPP_NH[1],
##            CHPP_NH[2][0],
##            CHPP_NH[2][1])

###provide matchId


#### still to do
###corner head
## w-h and w-a
#### w-h 1 v0
#### play creatively
##distribution and w/d/l
##actual events

## future
##PC does it impact all the same
##WH adjust for whether there is a wing-head
#### AOW / AIM adjust for volume of cahnces

### establish connections via pychpp
def match_predict(matchid):
    __start = datetime.datetime.now()
    try:
        match = chpp.match(ht_id=matchid,source="htointegrated",events=True)
    except:
        match = chpp.match(ht_id=matchid,events=True)

    try:
        lineup_home = chpp.match_lineup(ht_id=matchid,team_id = match.home_team_id,source="htointegrated")
    except:
        lineup_home = chpp.match_lineup(ht_id=matchid,team_id = match.home_team_id)

    try:
        lineup_away = chpp.match_lineup(ht_id=matchid,team_id = match.away_team_id,source="htointegrated")
    except:
        lineup_away = chpp.match_lineup(ht_id=matchid,team_id = match.away_team_id)


    ###create dictionaries for player specialty, player behaviour
    ps_dict={}
    pb_dict={}
    for i in range(100,114,1):
##        print(i)
        psH='home_' + str(i)
        psA='away_' + str(i)
##        print(htsm.roleid_pos_dict[i])
##        print(i,lineup_home.starting_lineup[htsm.roleid_pos_dict[i]][i].behaviour)
        try:                       
            ps_dict.update({psH:lineup_home.starting_lineup[htsm.roleid_pos_dict[i]][i].player.specialty})
            pb_dict.update({psH:lineup_home.starting_lineup[htsm.roleid_pos_dict[i]][i].behaviour})
        except:
##            print(i,'except')
            ps_dict.update({psH:-1})
            pb_dict.update({psH:-1})
        try:
            ps_dict.update({psA:lineup_away.starting_lineup[htsm.roleid_pos_dict[i]][i].player.specialty})
            pb_dict.update({psA:lineup_away.starting_lineup[htsm.roleid_pos_dict[i]][i].behaviour})
        except:
            ps_dict.update({psA:-1})
            pb_dict.update({psA:-1})

##    print(ps_dict,pb_dict)

##    for i in range(100,114,1):
##        psH='ps_' + str(i)
##        psA='ps_' + str(i)
##        ps_dict.update({psH:0,psA:0})
    ### added in "try" because the speciality on a deleted player is unavailable
    try:
        home_spt_spec = lineup_home.lineup['set pieces'][17].player.specialty
    except:
        home_spt_spec = 0
    home_stars_gk = lineup_home.lineup['keeper'][100].rating_stars
    home_isp_att = match.home_team_rating_ind_set_pieces_att
    home_isp_def = match.home_team_rating_ind_set_pieces_def
    home_rating_midfield = match.home_team_rating_midfield
    home_rating_right_att = match.home_team_rating_right_att
    home_rating_left_att = match.home_team_rating_left_att
    home_rating_mid_att = match.home_team_rating_mid_att
    home_rating_right_def = match.home_team_rating_right_def
    home_rating_left_def = match.home_team_rating_left_def
    home_rating_mid_def = match.home_team_rating_mid_def
    home_tac_type = match.home_team_tactic_type
    home_tac_skill = match.home_team_tactic_skill

    try:
        away_spt_spec = lineup_away.lineup['set pieces'][17].player.specialty
    except:
        away_spt_spec = 0
    away_stars_gk = lineup_away.lineup['keeper'][100].rating_stars
    away_isp_att = match.away_team_rating_ind_set_pieces_att
    away_isp_def = match.away_team_rating_ind_set_pieces_def
    away_rating_midfield = match.away_team_rating_midfield
    away_rating_right_att = match.away_team_rating_right_att
    away_rating_left_att = match.away_team_rating_left_att
    away_rating_mid_att = match.away_team_rating_mid_att
    away_rating_right_def = match.away_team_rating_right_def
    away_rating_left_def = match.away_team_rating_left_def
    away_rating_mid_def = match.away_team_rating_mid_def
    away_tac_type = match.away_team_tactic_type
    away_tac_skill = match.away_team_tactic_skill

    #####count of number of players for triggering SEs
    ##print(vars(lineup_home.starting_lineup['midfield'][109].player),vars(lineup_home.starting_lineup['midfield'][109].player))
    ## notes: O = offensive. D = Defensive .  ht = Head for Tech.  hw = head wing players
    spec_list = ['pnf','cd','pdim','qo','qs','ho','uo','to','ht','qd','hd','hk','ud','um','usa','uog','td','hc','hw','wi','df','hco','hcd']

    ###create dictionary where count starts at 0 for all spec triggering players
    spec_player_dict={}
    for sp in spec_list:
        spH='home_' + sp
        spA='away_' + sp
        spec_player_dict.update({spH:0,spA:0})

    ### increase spec player count by 1 if the player meets the criteria
    ### QS (Quick Stop) needs to look at the players on both teams, and then assigns a partial player depending the logic of how often they stop the event
    for i in [111,112,113]:
        try:
            if pb_dict['home_'+str(i)]>= 0:
                if ps_dict['home_'+str(i)] == 3 and pb_dict['home_'+str(i)]== 0:
                    spec_player_dict['home_pnf']+=1
                if ps_dict['home_'+str(i)] == 1:
                    spec_player_dict['home_to']+=1
                if ps_dict['home_'+str(i)] == 2:
                    spec_player_dict['home_qo']+=1
    ##                print(i,spec_player_dict['home_qo'])
                    if i == 111:
                        try:
                            if ps_dict['away_105'] == 2:
                                spec_player_dict['away_qs']+=1
                        except:
                            pass
                        try:
                            if ps_dict['away_104'] == 2:
                                spec_player_dict['away_qs']+=0.25
                        except:
                            pass
                    if i == 112:
                        try:
                            if ps_dict['away_103'] == 2:
                                spec_player_dict['away_qs']+=1
                        except:
                            pass
                        try:
                            if ps_dict['away_104'] == 2:
                                spec_player_dict['away_qs']+=0.25
                        except:
                            pass
                        try:
                            if ps_dict['away_102'] == 2:
                                spec_player_dict['away_qs']+=0.25
                        except:
                            pass
                    if i == 113:
                        try:
                            if ps_dict['away_101'] == 2:
                                spec_player_dict['away_qs']+=1
                        except:
                            pass
                        try:
                            if ps_dict['away_102'] == 2:
                                spec_player_dict['away_qs']+=0.25
                        except:
                            pass
                if ps_dict['home_'+str(i)] == 4:
                    spec_player_dict['home_uo']+=1
                    spec_player_dict['home_uog']+=1
                if ps_dict['home_'+str(i)] == 5:
                    spec_player_dict['home_ho']+=1
        except:
            pass
        try:
            if pb_dict['away_'+str(i)]>= 0:
                if ps_dict['away_'+str(i)] == 3 and pb_dict['away_'+str(i)]== 0:
                    spec_player_dict['away_pnf']+=1
                if ps_dict['away_'+str(i)] == 1:
                    spec_player_dict['away_to']+=1
                if ps_dict['away_'+str(i)] == 2:
                    spec_player_dict['away_qo']+=1
                    if i == 111:
                        try:
                            if ps_dict['home_105'] == 2:
                                spec_player_dict['home_qs']+=1
                        except:
                            pass
                        try:
                            if ps_dict['home_104'] == 2:
                                spec_player_dict['home_qs']+=0.25
                        except:
                            pass
                    if i == 112:
                        try:
                            if ps_dict['home_103'] == 2:
                                spec_player_dict['home_qs']+=1
                        except:
                            pass
                        try:
                            if ps_dict['home_104'] == 2:
                                spec_player_dict['home_qs']+=0.25
                        except:
                            pass
                        try:
                            if ps_dict['home_102'] == 2:
                                spec_player_dict['home_qs']+=0.25
                        except:
                            pass
    ##                print('qs112')

                    if i == 113:
                        try:
                            if ps_dict['home_101'] == 2:
                                spec_player_dict['home_qs']+=1
                        except:
                            pass
                        try:
                            if ps_dict['home_102'] == 2:
                                spec_player_dict['home_qs']+=0.25
                        except:
                            pass
    ##                print('qs113')
                if ps_dict['away_'+str(i)] == 4:
                    spec_player_dict['away_uo']+=1
                    spec_player_dict['away_uog']+=1
                if ps_dict['away_'+str(i)] == 5:
                    spec_player_dict['away_ho']+=1
        except:
            pass
    ##print('after fw',spec_player_dict['home_qs'],spec_player_dict['away_qs'])
    ##        print('wing' , i , 'behavoiur',pb_dict['home_'+str(i)])
    ##        print('type',i,type(pb_dict['home_'+str(i)]))
    for i in [106,110]:
        try:
            if pb_dict['home_'+str(i)] >=0:
    ##            print(i,spec_player_dict['home_wi'])
                spec_player_dict['home_wi']+=1
    ##            print(i,spec_player_dict['home_wi'])
                if ps_dict['home_'+str(i)] == 2:
    ##                print(i,'before',spec_player_dict['home_qo'])
                    spec_player_dict['home_qo']+=1
    ##                print(i,spec_player_dict['home_qo'])
                    if i == 106:
                        try:
                            if ps_dict['away_105'] == 2:
                                spec_player_dict['away_qs']+=1
                        except:
                            pass
                        try:
                            if ps_dict['away_104'] == 2:
                                spec_player_dict['away_qs']+=0.25
                        except:
                            pass
                    if i == 110:
                        try:
                            if ps_dict['away_101'] == 2:
                                spec_player_dict['away_qs']+=1
                        except:
                            pass
                        try:
                            if ps_dict['away_102'] == 2:
                                spec_player_dict['away_qs']+=0.25
                        except:
                            pass
                if ps_dict['home_'+str(i)] == 1:
                    spec_player_dict['home_to']+=1
                if ps_dict['home_'+str(i)] == 4:
                    spec_player_dict['home_uo']+=1
                    spec_player_dict['home_uog']+=1
                if ps_dict['home_'+str(i)] == 5:
                    spec_player_dict['home_ho']+=1
                    spec_player_dict['home_hw']+=1
        except:
            pass
        try:
    ##        print('away_wi')
            if pb_dict['away_'+str(i)]>= 0:
    ##            print('away_wi')
                spec_player_dict['away_wi']+=1
                if ps_dict['away_'+str(i)] == 2:
                    spec_player_dict['away_qo']+=1
    ##                print('away',i)
                    if i == 106:
                        try:
                            if ps_dict['home_105'] == 2:
                                spec_player_dict['home_qs']+=1
                        except:
                            pass
                        try:
                            if ps_dict['home_104'] == 2:
                                spec_player_dict['home_qs']+=0.25
                        except:
                            pass
                    if i == 110:
                        try:
                            if ps_dict['home_101'] == 2:
                                spec_player_dict['home_qs']+=1
                        except:
                            pass
                        try:
                            if ps_dict['home_102'] == 2:
                                spec_player_dict['home_qs']+=0.25
                        except:
                            pass
                if ps_dict['away_'+str(i)] == 1:
                    spec_player_dict['away_to']+=1
                if ps_dict['away_'+str(i)] == 4:
                    spec_player_dict['away_uo']+=1
                    spec_player_dict['away_uog']+=1
                if ps_dict['away_'+str(i)] == 5:
                    spec_player_dict['away_ho']+=1
                    spec_player_dict['away_hw']+=1
        except:
            pass
    ##print('after wing',spec_player_dict['home_qs'],spec_player_dict['away_qs'])

    for i in [107,108,109]:
        try:
            if pb_dict['home_'+str(i)]>= 0:
                if ps_dict['home_'+str(i)] == 3 and pb_dict['home_'+str(i)]== 2:
                    spec_player_dict['home_pdim']+=1
                if ps_dict['home_'+str(i)] == 2:
    ##                print(i,'before',spec_player_dict['home_qo'])
                    spec_player_dict['home_qo']+=1
    ##                print(i,spec_player_dict['home_qo'])
                    if i == 107:
                        try:
                            if ps_dict['away_104'] == 2:
                                spec_player_dict['away_qs']+=1
                        except:
                            pass
                        try:
                            if ps_dict['away_103'] == 2:
                                spec_player_dict['away_qs']+=0.25
                        except:
                            pass
                        try:
                            if ps_dict['away_105'] == 2:
                                spec_player_dict['away_qs']+=0.25
                        except:
                            pass
                    if i == 108:
                        try:
                            if ps_dict['away_103'] == 2:
                                spec_player_dict['away_qs']+=1
                        except:
                            pass
                        try:
                            if ps_dict['away_104'] == 2:
                                spec_player_dict['away_qs']+=0.25
                        except:
                            pass
                        try:
                            if ps_dict['away_102'] == 2:
                                spec_player_dict['away_qs']+=0.25
                        except:
                            pass
                    if i == 109:
                        try:
                            if ps_dict['away_102'] == 2:
                                spec_player_dict['away_qs']+=1
                        except:
                            pass
                        try:
                            if ps_dict['away_101'] == 2:
                                spec_player_dict['away_qs']+=0.25
                        except:
                            pass
                        try:
                            if ps_dict['away_103'] == 2:
                                spec_player_dict['away_qs']+=0.25
                        except:
                            pass
                if ps_dict['home_'+str(i)] == 1:
                    spec_player_dict['home_to']+=1
                if ps_dict['home_'+str(i)] == 4:
                    spec_player_dict['home_uo']+=1
                    spec_player_dict['home_um']+=1
                if ps_dict['home_'+str(i)] == 5:
                    spec_player_dict['home_ho']+=1
                    spec_player_dict['home_ht']+=1
        except:
            pass
        try:
            if pb_dict['away_'+str(i)]>= 0:
                if ps_dict['away_'+str(i)] == 3 and pb_dict['away_'+str(i)]== 2:
                    spec_player_dict['away_pdim']+=1
                if ps_dict['away_'+str(i)] == 2:
                    spec_player_dict['away_qo']+=1
                    if i == 107:
                        try:
                            if ps_dict['home_104'] == 2:
                                spec_player_dict['home_qs']+=1
##                                print(i,'1')
                        except:
                            pass
                        try:
                            if ps_dict['home_105'] == 2:
                                spec_player_dict['home_qs']+=0.25
                        except:
                            pass
                        try:
                            if ps_dict['home_103'] == 2:
                                spec_player_dict['home_qs']+=0.25
                        except:
                            pass
                    if i == 108:
                        try:
                            if ps_dict['home_103'] == 2:
                                spec_player_dict['home_qs']+=1
                        except:
                            pass
                        try:
                            if ps_dict['home_104'] == 2:
                                spec_player_dict['home_qs']+=0.25
##                                print(i,'0.25')
                        except:
                            pass
                        try:
                            if ps_dict['home_102'] == 2:
                                spec_player_dict['home_qs']+=0.25
                        except:
                            pass
                    if i == 109:
                        try:
                            if ps_dict['home_102'] == 2:
                                spec_player_dict['home_qs']+=1
                        except:
                            pass
                        try:
                            if ps_dict['home_103'] == 2:
                                spec_player_dict['home_qs']+=0.25
                        except:
                            pass
                        try:
                            if ps_dict['home_101'] == 2:
                                spec_player_dict['home_qs']+=0.25
                        except:
                            pass
                if ps_dict['away_'+str(i)] == 1:
                    spec_player_dict['away_to']+=1
                if ps_dict['away_'+str(i)] == 4:
                    spec_player_dict['away_uo']+=1
                    spec_player_dict['away_um']+=1
                if ps_dict['away_'+str(i)] == 5:
                    spec_player_dict['away_ho']+=1
                    spec_player_dict['away_ht']+=1
        except:
            pass
    
    for i in [102,103,104]:
        try:
            if pb_dict['home_'+str(i)]>= 0:
                spec_player_dict['home_df']+=1
##                print(i,spec_player_dict['home_df'])
                spec_player_dict['home_cd']+=1
                if ps_dict['home_'+str(i)] == 1:
                    spec_player_dict['home_td']+=1
                if ps_dict['home_'+str(i)] == 2:
                    spec_player_dict['home_qd']+=1
                if ps_dict['home_'+str(i)] == 4:
                    spec_player_dict['home_ud']+=1
                    spec_player_dict['home_um']+=1
                if ps_dict['home_'+str(i)] == 5:
                    spec_player_dict['home_hd']+=1
                    spec_player_dict['home_ht']+=1
        except:
##            print(i,'pass')
            pass
        try:
            if pb_dict['away_'+str(i)]>= 0:
                spec_player_dict['away_cd']+=1
                spec_player_dict['away_df']+=1
                if ps_dict['away_'+str(i)] == 1:
                    spec_player_dict['away_td']+=1
                if ps_dict['away_'+str(i)] == 2:
                    spec_player_dict['away_qd']+=1
                if ps_dict['away_'+str(i)] == 4:
                    spec_player_dict['away_ud']+=1
                    spec_player_dict['away_um']+=1
                if ps_dict['away_'+str(i)] == 5:
                    spec_player_dict['away_hd']+=1
                    spec_player_dict['away_ht']+=1
        except:
            pass

##    print(pb_dict['home_103'],spec_player_dict['home_df'])
    for i in [101,105]:
        try:
            if pb_dict['home_'+str(i)]>= 0:
                spec_player_dict['home_df']+=1
##                print(i,spec_player_dict['home_df'])
                if ps_dict['home_'+str(i)] == 1:
                    spec_player_dict['home_td']+=1
                if ps_dict['home_'+str(i)] == 2:
                    spec_player_dict['home_qd']+=1
                if ps_dict['home_'+str(i)] == 4:
                    spec_player_dict['home_ud']+=1
                    spec_player_dict['home_um']+=1
                if ps_dict['home_'+str(i)] == 5:
                    spec_player_dict['home_hd']+=1
                    spec_player_dict['home_ht']+=1
        except:
##            print(i,'pass')
            pass
        try:
            if pb_dict['away_'+str(i)]>= 0:
                spec_player_dict['away_df']+=1
                if ps_dict['away_'+str(i)] == 1:
                    spec_player_dict['away_td']+=1
                if ps_dict['away_'+str(i)] == 2:
                    spec_player_dict['away_qd']+=1
                if ps_dict['away_'+str(i)] == 4:
                    spec_player_dict['away_ud']+=1
                    spec_player_dict['away_um']+=1
                if ps_dict['away_'+str(i)] == 5:
                    spec_player_dict['away_hd']+=1
                    spec_player_dict['away_ht']+=1
        except:
            pass
##    print(pb_dict['home_101'],pb_dict['home_105'],spec_player_dict['home_df'])
    ## done here before GK is counted
    spec_player_dict['home_usa'] = spec_player_dict['home_uo'] + spec_player_dict['home_ud']
    spec_player_dict['away_usa'] = spec_player_dict['away_uo'] + spec_player_dict['away_ud']

    for i in [100]:
        try:
            if pb_dict['home_'+str(i)]>= 0:
                if ps_dict['home_'+str(i)] == 4:
                    spec_player_dict['home_ud']+=1
                if ps_dict['home_'+str(i)] == 2:
                    spec_player_dict['home_qd']+=1
                if ps_dict['home_'+str(i)] == 5:
                    spec_player_dict['home_hk']+=1
        except:
            pass
        try:
            if pb_dict['away_'+str(i)]>= 0:
                if ps_dict['away_'+str(i)] == 4:
                    spec_player_dict['away_ud']+=1
                if ps_dict['away_'+str(i)] == 2:
                    spec_player_dict['away_qd']+=1
                if ps_dict['away_'+str(i)] == 5:
                    spec_player_dict['away_hk']+=1
        except:
            pass

    ###players for offense and defendse of Corner-Head.  It is all player on defense, and offense is the same but with neither SP taker nor keeper.
##    print('home_ho','home_hd',spec_player_dict['home_ho'],spec_player_dict['home_hd'])
    spec_player_dict['home_hco']=spec_player_dict['home_ho'] + spec_player_dict['home_hd']
    spec_player_dict['away_hco']=spec_player_dict['away_ho'] + spec_player_dict['away_hd']

    spec_player_dict['home_hcd']=spec_player_dict['home_ho'] + spec_player_dict['home_hd'] + + spec_player_dict['home_hk']
    spec_player_dict['away_hcd']=spec_player_dict['away_ho'] + spec_player_dict['away_hd'] + spec_player_dict['away_hk']
##    print('Head Corner',spec_player_dict['away_ho'],spec_player_dict['away_hd'],spec_player_dict['away_hk'],spec_player_dict['away_hco'],spec_player_dict['away_hcd'])

    ###adjust that the SP taker doesnt count for corner-head event
    for i in [17]:
        try:
            if home_spt_spec == 5:
                spec_player_dict['home_hco']-=1
        except:
            pass
        try:
            if away_spt_spec == 5:
                spec_player_dict['away_hco']-=1
        except:
            pass

    # turn tactic ratings into a dictionary, e.g. such that tactic_dict['home_aow'] will return the tactic skill for the home team for AOW tactic
    # if they do not play the tactic, then it returns 0
    # needed input for the SE section as we need PC rating
    tactic_dict={}
    def ts(tac,tacnum):
        tacH='home_tactic_' + tac
        tacA='away_tactic_' + tac
        tactic_dict.update({tacH:0,tacA:0})
    ##    print(away_tac_type,away_tac_skill)
        if int(home_tac_type) == tacnum:
            tactic_dict.update({tacH:home_tac_skill})
    ##        print(home_tac_skill)
        if int(away_tac_type) == tacnum:
            tactic_dict.update({tacA:away_tac_skill})
    ##        print(away_tac_skill)

    ts('PR',1)
    ts('CA',2)
    ts('AIM',3)
    ts('AOW',4)
    ts('PC',7)
    ts('LS',8)
    ##print(tactic_dict)

    ###needed for Keeper Stars in SE conversion
    iloc_home_KS=htsm.iloc_kstars_dict[float(home_stars_gk)]
    iloc_away_KS=htsm.iloc_kstars_dict[float(away_stars_gk)]


    ###needed for conversion of Corner-Anyone events
    conv_ifk_home = htsm.ifk_dict[max(-27,min(30,home_isp_att - away_isp_def))]
    conv_ifk_away = htsm.ifk_dict[max(-27,min(30,away_isp_att - home_isp_def))]

##corner-HEad has a factor like ISP for IFK, then another factor for the offenseive vs defensive H players
    conv_CH_home = htsm.isp_ch_dict[max(-46,min(29,home_isp_att - away_isp_def))] * htsm.head_ch_dict[max(-6,min(10,spec_player_dict['home_hco'] - spec_player_dict['away_hcd']))]
    conv_CH_away = htsm.isp_ch_dict[max(-46,min(29,away_isp_att - home_isp_def))] * htsm.head_ch_dict[max(-6,min(10,spec_player_dict['away_hco'] - spec_player_dict['home_hcd']))]

##corner anyone is the same as IFK, then has another factor added on for the keeper.  The keeper factor is shifted by some steps if the attacking team plays LS.
    conv_CornerAnyone_home = htsm.corner_anyone_ifk_dict[max(-40,min(30,home_isp_att - away_isp_def))] * htsm.corner_anyone_k_dict[float(away_stars_gk) - (tactic_dict['home_tactic_LS'] / 4)]
    conv_CornerAnyone_away = htsm.corner_anyone_ifk_dict[max(-40,min(30,away_isp_att - home_isp_def))] * htsm.corner_anyone_k_dict[float(home_stars_gk) - (tactic_dict['away_tactic_LS'] / 4)]


    pcN = 1
    if tactic_dict['home_tactic_PC'] > 0 and tactic_dict['away_tactic_PC'] > 0:
        pcN = htsm.pc_dict[int(0.5*tactic_dict['home_tactic_PC'] + 0.5*tactic_dict['away_tactic_PC'])] * 1.40
    elif tactic_dict['home_tactic_PC'] > 0:
        pcN = htsm.pc_dict[tactic_dict['home_tactic_PC']]
    elif tactic_dict['away_tactic_PC'] > 0:
        pcN = htsm.pc_dict[tactic_dict['away_tactic_PC']]
##    print(pcN)

#### when the only Wing-Head target is a winger, then frequency cuts in half
    wh_adjH = 1
    wh_adjA = 1
    if spec_player_dict['home_ho'] == 1 and spec_player_dict['home_hw'] == 1:
        wh_adjH = 0.5
    if spec_player_dict['away_ho'] == 1 and spec_player_dict['away_hw'] == 1:
        wh_adjA = 0.5
    
##    print(htsm.corner_anyone_ifk_dict[max(-40,min(30,home_isp_att - away_isp_def))])
##    print(htsm.corner_anyone_k_dict[float(away_stars_gk) - (tactic_dict['home_tactic_LS'] / 4)])
##    print(htsm.corner_anyone_ifk_dict[max(-40,min(30,away_isp_att - home_isp_def))])
##    print(htsm.corner_anyone_k_dict[float(home_stars_gk) - (tactic_dict['away_tactic_LS'] / 4)])
##    print(away_stars_gk,home_stars_gk)
##    print(conv_CornerAnyone_home,conv_CornerAnyone_away
##    print('conv_ch_away',conv_CH_away)
    ### calculate expected events, goals, conv% for SEs

        ### for SEs, this works using X vs Y, where X is the team with more triggering players and Y has less
        ### first, it uses X to get an adjustment factor.  With X>1, it is not linear (e.g. X = 2 means 1.90 events)
        ###this adjustment factor is different for Corner-Head and all other events
        ### then this is multiplied by the event frequency for X = 1 (e.g. 7.4% for Unpred Long Pass)
        ###then chance distribution is either the X vs Y exponential 3.5, or special cases are corner (by linear possession) and "all other" is 50/50
        ## this is multiplied by the impact of Play Creatively.  pcN- uses same factor for both teams, or if both play PC, uses average * 1.40
        ## conversion rate is based on the opponent Keeper stars, and there are 2 tables: one for LS teams, one for all other teams
        ## the exceptions for conv are corner-anyone (uses IFK) and corner-head (

    quick_stop_dict = {'QP_convH':0 , 'QP_convA':0, 'QR_convH':0, 'QR_convA':0}
    ##quick_stop_dict = {'NH':0,'NA':0,'GH':0,'GA':0}
    tech_head_dict = {'NH':0,'NA':0}
    def se(se_,sef):

        if se_ in ['zz', 'ca']:
            X = 1
        else:
            X= max(spec_player_dict['home_'+se_],spec_player_dict['away_'+se_])
##        print(se_,X)
        if X == 0:
            NH=0
            NA=0
            convH=0
            convA=0
            possH=0
            possA=0
        else:
            if sef == 'CH':
##                print(spec_player_dict['home_hco'], htsm.spec_freq_dict[sef])
                NH_CH = htsm.specX_CH_dict[spec_player_dict['home_hco']] * htsm.spec_freq_dict[sef]
                NA_CH = htsm.specX_CH_dict[spec_player_dict['away_hco']] * htsm.spec_freq_dict[sef]
##                print('NH_CH',NH_CH,spec_player_dict['home_hco'])
            else:
                N = htsm.specX_dict[X] * htsm.spec_freq_dict[sef]
##            if sef=='WA':
##                print(N,X,sef,htsm.specX_dict[X],htsm.spec_freq_dict[sef])

            if se_ == 'ca' or sef == 'CH':
                possH = home_rating_midfield/(home_rating_midfield+away_rating_midfield)
                possA= away_rating_midfield/(home_rating_midfield+away_rating_midfield)
##                print(se_,'poss CH',possA)
            elif se_ in ['zz']:
                possH=0.5
                possA=0.5
            elif pcN == 1 or (tactic_dict['home_tactic_PC'] > 0 and tactic_dict['away_tactic_PC']):
                possH=spec_player_dict['home_'+se_]**3.5/(spec_player_dict['home_'+se_]**3.5+spec_player_dict['away_'+se_]**3.5)
                possA=spec_player_dict['away_'+se_]**3.5/(spec_player_dict['home_'+se_]**3.5+spec_player_dict['away_'+se_]**3.5)
            elif spec_player_dict['home_'+se_]==spec_player_dict['away_'+se_] and tactic_dict['home_tactic_PC'] > 0:
                possH=(spec_player_dict['home_'+se_]+1)/(spec_player_dict['home_'+se_]+spec_player_dict['away_'+se_]+1)
                possA=(spec_player_dict['away_'+se_])/(spec_player_dict['away_'+se_]+spec_player_dict['away_'+se_]+1)
            elif spec_player_dict['home_'+se_]==spec_player_dict['away_'+se_] and tactic_dict['away_tactic_PC'] > 0:
                possH=(spec_player_dict['home_'+se_])/(spec_player_dict['home_'+se_]+spec_player_dict['away_'+se_]+1)
                possA=(spec_player_dict['away_'+se_]+1)/(spec_player_dict['away_'+se_]+spec_player_dict['away_'+se_]+1)
            elif spec_player_dict['home_'+se_]>spec_player_dict['away_'+se_] and tactic_dict['home_tactic_PC'] > 0:
                possH=spec_player_dict['home_'+se_]**4.0/(spec_player_dict['home_'+se_]**4.0+spec_player_dict['away_'+se_]**4.0)
                possA=spec_player_dict['away_'+se_]**4.0/(spec_player_dict['home_'+se_]**4.0+spec_player_dict['away_'+se_]**4.0)
            elif spec_player_dict['away_'+se_]>spec_player_dict['home_'+se_] and tactic_dict['away_tactic_PC'] > 0:
                possH=spec_player_dict['home_'+se_]**4.0/(spec_player_dict['home_'+se_]**4.0+spec_player_dict['away_'+se_]**4.0)
                possA=spec_player_dict['away_'+se_]**4.0/(spec_player_dict['home_'+se_]**4.0+spec_player_dict['away_'+se_]**4.0)
            elif spec_player_dict['home_'+se_]<spec_player_dict['away_'+se_] and tactic_dict['home_tactic_PC'] > 0:
                possH=spec_player_dict['home_'+se_]**2.5/(spec_player_dict['home_'+se_]**2.5+spec_player_dict['away_'+se_]**2.5)
                possA=spec_player_dict['away_'+se_]**2.5/(spec_player_dict['home_'+se_]**2.5+spec_player_dict['away_'+se_]**2.5)
            elif spec_player_dict['away_'+se_]<spec_player_dict['home_'+se_] and tactic_dict['away_tactic_PC'] > 0:
                possH=spec_player_dict['home_'+se_]**2.5/(spec_player_dict['home_'+se_]**2.5+spec_player_dict['away_'+se_]**2.5)
                possA=spec_player_dict['away_'+se_]**2.5/(spec_player_dict['home_'+se_]**2.5+spec_player_dict['away_'+se_]**2.5)
            else:
                possH=0.5
                possA=0.5
#####last scenario shouldn't happen.

            if sef == 'CH':
                NH = NH_CH * possH * pcN
                NA = NA_CH * possA * pcN
##                print(se_,'NH',NH,NH_CH,possH,pcN)
            elif sef == 'WH':
                NH = N * possH * pcN * wh_adjH
                NA = N * possA * pcN * wh_adjA
            else:
                NH = N * possH * pcN
                NA = N * possA * pcN
##                print(se_,'NA',NA)
##            if sef == 'WA':
##                print(se_,NH,N,possH,pcN)
            if se_ == 'ca':
                convH = conv_CornerAnyone_home
                convA = conv_CornerAnyone_away
            elif sef == 'CH':
                convH=conv_CH_home
                convA=conv_CH_away
            elif int(home_tac_type) == 8:
                convH = htsm.SE_LS_CONV.iloc[htsm.seconv_kstars_dict[sef]][iloc_away_KS]
                convA = htsm.SE_LS_CONV.iloc[htsm.seconv_kstars_dict[sef]][iloc_home_KS]
            else:
                convH = htsm.SE_CONV.iloc[htsm.seconv_kstars_dict[sef]][iloc_away_KS]
                convA = htsm.SE_CONV.iloc[htsm.seconv_kstars_dict[sef]][iloc_home_KS]

            # some quick events are stopped by the opponent Q defenders
            if se_ == 'qo':
    ##            quick_stop_dict['NA'] = quick_stop_dict['NA'] + NA  * spec_player_dict['home_qs'] / spec_player_dict['away_qo']
    ##            quick_stop_dict['NH'] = quick_stop_dict['NH'] + NH * spec_player_dict['away_qs'] / spec_player_dict['home_qo']
    ##            quick_stop_dict['GA'] = quick_stop_dict['GA'] + NA * convA * spec_player_dict['home_qs'] / spec_player_dict['away_qo']
    ##            quick_stop_dict['GH'] = quick_stop_dict['GH'] + NH * convH * spec_player_dict['away_qs'] / spec_player_dict['home_qo']
                if sef == 'QP':
                    quick_stop_dict['QP_convH']=convH
                    quick_stop_dict['QP_convA']=convA
                if sef == 'QR':
                    quick_stop_dict['QR_convH']=convH
                    quick_stop_dict['QR_convA']=convA

                try:
                    convH = convH * (1 - spec_player_dict['away_qs'] / spec_player_dict['home_qo'])
                except:
                    pass
                try:
                    convA = convA * (1- spec_player_dict['home_qs'] / spec_player_dict['away_qo'])
                except:
                    pass

            if sef == 'TH':
                if spec_player_dict['home_ht']==0:
                    tech_head_dict['NA']=NA
                    NA=0
                if spec_player_dict['away_ht']==0:
                    tech_head_dict['NH']=NH
                    NH=0

        return(NH,NA,NH*convH,NA*convA,convH,convA)
    ##    return(sef,spec_player_dict['home_'+se_],spec_player_dict['away_'+se_],round(possH,2),round(possA,2),round(NH,2),round(NA,2),round(NH*convH,2),round(NA*convA,2),round(convH,2),round(convA,2))
    ##    return(sef,spec_player_dict['home_'+se_],spec_player_dict['away_'+se_],round(NH,4),round(NA,4),round(NH*convH,4),round(NA*convA,4),round(convH,4),round(convA,4))
    se_QP = se('qo','QP')
    se_QR = se('qo','QR')
    se_UM = se('um','UM')
    se_UOG = se('uog','UOG')
    se_USO = se('uo','USO')
    se_USA = se('usa','USA')
    se_ULP = se('ud','ULP')
    se_CA = se('ca','CA')
    se_WA = se('wi','WA')
    se_WH = se('ho','WH')
    se_ZZ = se('zz','ZZ')
    se_TH = se('to','TH')
    se_CH = se('hco','CH')
    ###for CH, hco is still used for whether to zero out the whole event
    ###otherwise, it uses special formulas


    ##se_CH = se('hc','CH')
    ##print(se_QP[0],se_QP[1],se_QR[0],se_QR[1],quick_stop_dict['QP_convH'],quick_stop_dict['QP_convA'],quick_stop_dict['QR_convH'],quick_stop_dict['QR_convA'])
    ##print(spec_player_dict['home_qo'],spec_player_dict['away_qo'],spec_player_dict['home_qs'],spec_player_dict['away_qs'])
    ##print((se_QP[1] * quick_stop_dict['QP_convA'] + se_QR[1] * quick_stop_dict['QR_convA']))
    ##print((se_QP[0] * quick_stop_dict['QP_convH'] + se_QR[0] * quick_stop_dict['QR_convH']))
    ## quick stop calcs
    try:
##        quick_stop_NH = (se_QP[1] * quick_stop_dict['QP_convA'] + se_QR[1] * quick_stop_dict['QR_convA']) * spec_player_dict['home_qs'] / spec_player_dict['away_qo']
        quick_stop_GH = (se_QP[1] * quick_stop_dict['QP_convA'] + se_QR[1] * quick_stop_dict['QR_convA']) * spec_player_dict['home_qs'] / spec_player_dict['away_qo']
    except:
##        quick_stop_NH = 0
        quick_stop_GH = 0
    try:
##        quick_stop_NA = (se_QP[0] * quick_stop_dict['QP_convH'] + se_QR[0] * quick_stop_dict['QR_convH']) * spec_player_dict['away_qs'] / spec_player_dict['home_qo']
        quick_stop_GA = (se_QP[0] * quick_stop_dict['QP_convH'] + se_QR[0] * quick_stop_dict['QR_convH']) * spec_player_dict['away_qs'] / spec_player_dict['home_qo']
    except:
##        quick_stop_NA=0
        quick_stop_GA=0




    ##print(quick_stop_NH,quick_stop_NA,quick_stop_GH,quick_stop_GA)

    # second one is for checking

    iloc_home_isp_att= htsm.pk_ispatt_dict[(home_isp_att+3)/4]
    iloc_away_isp_att= htsm.pk_ispatt_dict[(away_isp_att+3)/4]
    iloc_home_isp_def=htsm.pk_ispdef_dict[(home_isp_def+3)/4]
    iloc_away_isp_def=htsm.pk_ispdef_dict[(away_isp_def+3)/4]

    ##home_ISP_att = (home_isp_att+3)/4
    conv_pk_home = htsm.PK.iloc[iloc_home_isp_att][iloc_away_isp_def]
    conv_pk_away = htsm.PK.iloc[iloc_away_isp_att][iloc_home_isp_def]

    pnf_pct_home = htsm.pnf_pct_dict[str(int(spec_player_dict['home_pnf'])) + '_' + str(int(spec_player_dict['away_cd']))]
    pnf_pct_away = htsm.pnf_pct_dict[str(int(spec_player_dict['away_pnf'])) + '_' + str(int(spec_player_dict['home_cd']))]

    ##MT = pd.DataFrame(columns=['Item','Chance_Home','Chance_Away','Goal_Home','Goal_Away','Conv_Home','Conv_Away'])
    poss_home=home_rating_midfield**3/(home_rating_midfield**3+away_rating_midfield**3)
    poss_away=1-poss_home
    def conv(att_,def_):
        conv_ = .92*att_**3.5/(att_**3.5+def_**3.5)
        return(conv_)

    def se_poss(home_,away_):
        if home_ + away_ > 0:
            poss_ = home_**3/(home_**3+away_**3)
        else:
            poss_=0
        return(poss_)
    ##print(match.events)
    ##n_=0
    ##for i in range(0,len(match.events)):
    ##    print(match.events[i]['id'])
    ##    if match.events[i]['id']==243:
    ##        n_=n_+1
    ##        print(n_)
    ##print('n_',n_)
    ##    print(match.goals[i]['minute'],match.goals[i]['player_name'])
    ##for goal in match.goals:
    ##    print(goal.minute,player_id,player_name)
    conv_right_home=conv(home_rating_right_att,away_rating_left_def)
    conv_right_away=conv(away_rating_right_att,home_rating_left_def)
    conv_left_home=conv(home_rating_left_att,away_rating_right_def)
    conv_left_away=conv(away_rating_left_att,home_rating_right_def)
    conv_mid_home=conv(home_rating_mid_att,away_rating_mid_def)
    conv_mid_away=conv(away_rating_mid_att,home_rating_mid_def)

    iloc_home_isp_att= htsm.pk_ispatt_dict[(home_isp_att+3)/4]
    iloc_away_isp_att= htsm.pk_ispatt_dict[(away_isp_att+3)/4]
    iloc_home_isp_def=htsm.pk_ispdef_dict[(home_isp_def+3)/4]
    iloc_away_isp_def=htsm.pk_ispdef_dict[(away_isp_def+3)/4]

    ##home_ISP_att = (home_isp_att+3)/4
    conv_pk_home = htsm.PK.iloc[iloc_home_isp_att][iloc_away_isp_def]
    conv_pk_away = htsm.PK.iloc[iloc_away_isp_att][iloc_home_isp_def]

    conv_dfk_home = htsm.DFK.iloc[iloc_home_isp_att][iloc_away_isp_def]
    conv_dfk_away = htsm.DFK.iloc[iloc_away_isp_att][iloc_home_isp_def]

    conv_PNF = .8

    nh_wing_pct = .259 * (1-htsm.aim_dict[min(40,tactic_dict['home_tactic_AIM'])]) + .357 * 0.5 * htsm.aow_dict[min(40,tactic_dict['home_tactic_AOW'])]
    nh_center_pct = .357 * (1-htsm.aow_dict[min(40,tactic_dict['home_tactic_AOW'])]) + .518 * htsm.aim_dict[min(40,tactic_dict['home_tactic_AIM'])]
    na_wing_pct = .259 * (1-htsm.aim_dict[min(40,tactic_dict['away_tactic_AIM'])]) + .357 * 0.5* htsm.aow_dict[min(40,tactic_dict['away_tactic_AOW'])]
    na_center_pct = .357 * (1-htsm.aow_dict[min(40,tactic_dict['away_tactic_AOW'])]) + .518 * htsm.aim_dict[min(40,tactic_dict['away_tactic_AIM'])]


    nc_ifk_pct = .041

    nc_pk_home_pct = .084 * htsm.PK_DFK.iloc[iloc_home_isp_att][iloc_away_isp_def]
    nc_dfk_home_pct = .084 - nc_pk_home_pct

    nc_pk_away_pct = .084 * htsm.PK_DFK.iloc[iloc_away_isp_att][iloc_home_isp_def]
    nc_dfk_away_pct = .084 - nc_pk_away_pct



    ##conv_pk_home = htsm.PK.iloc[iloc_home_isp_att][htsm.pk_ispdef_dict[(away_isp_def+3)/4]]
    ##conv_pk_away = htsm.PK.iloc[htsm.pk_ispatt_dict[(away_isp_att+3)/4]][htsm.pk_ispdef_dict[(home_isp_def+3)/4]]


    ls_pct_home = htsm.ls_pct_dict[min(32,tactic_dict['home_tactic_LS'])]
    ls_pct_away = htsm.ls_pct_dict[min(32,tactic_dict['away_tactic_LS'])]

    conv_ls_home = htsm.ls_dict[min(32,tactic_dict['home_tactic_LS'])]
    conv_ls_away = htsm.ls_dict[min(32,tactic_dict['away_tactic_LS'])]


    ##print(ls_pct_home,ls_pct_away)
    ##### NC = Normal chances
    nc = 10 - htsm.press_dict[min(18,tactic_dict['home_tactic_PR'])] - htsm.press_dict[min(18,tactic_dict['away_tactic_PR'])]
    nc_home= nc * poss_home * (1 - htsm.pdim_dict[spec_player_dict['away_pdim']])
    nc_away= nc * poss_away * (1 - htsm.pdim_dict[spec_player_dict['home_pdim']])
    nh_pdim = nc * poss_home * (htsm.pdim_dict[spec_player_dict['away_pdim']])
    na_pdim = nc * poss_away * (htsm.pdim_dict[spec_player_dict['home_pdim']])
    nc_home_xLS = nc_home * (1- ls_pct_home)
    nc_away_xLS = nc_away * (1- ls_pct_away)
    MT = pd.DataFrame(columns=['Type','Chance Home','Chance Away','Goals Home','Goals Away','Conv% Home','Conv% Away'])
    MTCA = pd.DataFrame(columns=['Type','Chance Home','Chance Away','Goals Home','Goals Away','Conv% Home','Conv% Away'])
    ##MT.loc[1]=['Goals',match.home_team_goals,match.away_team_goals,match.home_team_goals-match.away_team_goals,0]
    ##MT.loc[1]=['Normal',round(nc_home,2),round(nc_away,2),round(nc_home*.3,2),round(nc_away*.3,2),poss_home,poss_away]
    MT.loc[1]=['Left',nc_home_xLS*nh_wing_pct,nc_away_xLS*na_wing_pct,nc_home_xLS*nh_wing_pct*conv_left_home,nc_away_xLS*na_wing_pct*conv_left_away,conv_left_home,conv_left_away]
    MT.loc[2]=['Center',nc_home_xLS*nh_center_pct,nc_away_xLS*na_center_pct,nc_home_xLS*nh_center_pct*conv_mid_home,nc_away_xLS*na_center_pct*conv_mid_away,conv_mid_home,conv_mid_away]
    MT.loc[3]=['Right',nc_home_xLS*nh_wing_pct,nc_away_xLS*na_wing_pct,nc_home_xLS*nh_wing_pct*conv_right_home,nc_away_xLS*na_wing_pct*conv_right_away,conv_right_home,conv_right_away]
    MT.loc[4]=['IFK',nc_home_xLS*nc_ifk_pct,nc_away_xLS*nc_ifk_pct,nc_home_xLS*nc_ifk_pct*conv_ifk_home,nc_away_xLS*nc_ifk_pct*conv_ifk_away,conv_ifk_home,conv_ifk_away]
    MT.loc[5]=['PK',nc_home_xLS*nc_pk_home_pct,nc_away_xLS*nc_pk_away_pct,nc_home_xLS*nc_pk_home_pct*conv_pk_home,nc_away_xLS*nc_pk_away_pct*conv_pk_away,conv_pk_home,conv_pk_away]
    MT.loc[6]=['DFK',nc_home_xLS*nc_dfk_home_pct,nc_away_xLS*nc_dfk_away_pct,nc_home_xLS*nc_dfk_home_pct*conv_dfk_home,nc_away_xLS*nc_dfk_away_pct*conv_dfk_away,conv_dfk_home,conv_dfk_away]
    MT.loc[7]=['LS',nc_home*ls_pct_home,nc_away*ls_pct_away,nc_home*ls_pct_home*conv_ls_home,nc_away*ls_pct_away*conv_ls_away,conv_ls_home,conv_ls_away]
    MT.loc[0]=['Normal',nc_home,nc_away,MT.iloc[0:7,3].sum(),MT.iloc[0:7,4].sum(),MT.iloc[0:7,3].sum()/nc_home_xLS,MT.iloc[0:7,4].sum()/nc_away]
    MT.sort_index(inplace=True)
    ### mt.loc9 will be SEs

    MTSE = pd.DataFrame(columns=['Type','Chance Home','Chance Away','Goals Home','Goals Away','Conv% Home','Conv% Away'])

    MTSE.loc[1]=['Quick Pass',se_QP[0],se_QP[1],se_QP[2],se_QP[3],se_QP[4],se_QP[5]]
    MTSE.loc[2]=['Quick Rush',se_QR[0],se_QR[1],se_QR[2],se_QR[3],se_QR[4],se_QR[5]]
    ## own goal reverses the goals
    MTSE.loc[3]=['Unpred Mistake',se_UM[1],se_UM[0],se_UM[3],se_UM[2],se_UM[5],se_UM[4]]
    MTSE.loc[4]=['Unpred Own Goal',se_UOG[1],se_UOG[0],se_UOG[3],se_UOG[2],se_UOG[5],se_UOG[4]]
    MTSE.loc[5]=['Unpred Score',se_USO[0],se_USO[1],se_USO[2],se_USO[3],se_USO[4],se_USO[5]]
    MTSE.loc[6]=['Unpred Special',se_USA[0],se_USA[1],se_USA[2],se_USA[3],se_USA[4],se_USA[5]]
    MTSE.loc[7]=['Unpred Long Pass',se_ULP[0],se_ULP[1],se_ULP[2],se_ULP[3],se_ULP[4],se_ULP[5]]
    MTSE.loc[8]=['Corner Anyone',se_CA[0],se_CA[1],se_CA[2],se_CA[3],se_CA[4],se_CA[5]]
    MTSE.loc[9]=['Corner Head',se_CH[0],se_CH[1],se_CH[2],se_CH[3],se_CH[4],se_CH[5]]
    MTSE.loc[10]=['Wing Head',se_WH[0],se_WH[1],se_WH[2],se_WH[3],se_WH[4],se_WH[5]]
    MTSE.loc[11]=['Wing Anyone',se_WA[0],se_WA[1],se_WA[2],se_WA[3],se_WA[4],se_WA[5]]
    MTSE.loc[12]=['Tech Head',se_TH[0],se_TH[1],se_TH[2],se_TH[3],se_TH[4],se_TH[5]]
    MTSE.loc[13]=['SE Others',se_ZZ[0],se_ZZ[1],se_ZZ[2],se_ZZ[3],se_ZZ[4],se_ZZ[5]]
    MTSE.loc[0]=['SE',MTSE.iloc[0:13,1].sum(),MTSE.iloc[0:13,2].sum(),MTSE.iloc[0:13,3].sum(),MTSE.iloc[0:13,4].sum(),MTSE.iloc[0:13,3].sum()/MTSE.iloc[0:13,1].sum(),MTSE.iloc[0:13,4].sum()/MTSE.iloc[0:13,2].sum()]
    ##MT.loc[17]=['Corner Head',se_CH[0],se_CH[1],se_CH[2],se_CH[3],se_CH[4],se_CH[5]]

    ##MT.loc[10]=['Quick Pass',se('qo','QP')[0],se('qo','QP')[1],se('qo','QP')[2],se('qo','QP')[3],se('qo','QP')[4],se('qo','QP')[5]]
    ##MT.loc[11]=['Quick Rush',se('qo','QR')[0],se('qo','QR')[1],se('qo','QR')[2],se('qo','QR')[3],se('qo','QR')[4],se('qo','QR')[5]]
    #### own goal reverses the goals
    ##MT.loc[12]=['Unpred Mistake',se('um','UM')[0],se('um','UM')[1],se('um','UM')[3],se('um','UM')[2],se('um','UM')[4],se('um','UM')[5]]
    ##MT.loc[13]=['Unpred Own Goal',se('uog','UOG')[0],se('uog','UOG')[1],se('uog','UOG')[3],se('uog','UOG')[2],se('uog','UOG')[4],se('uog','UOG')[5]]
    ##MT.loc[14]=['Unpred Score',se('uo','USO')[0],se('uo','USO')[1],se('uo','USO')[2],se('uo','USO')[3],se('uo','USO')[4],se('uo','USO')[5]]
    ##MT.loc[15]=['Unpred Special',se('usa','USA')[0],se('usa','USA')[1],se('usa','USA')[2],se('usa','USA')[3],se('usa','USA')[4],se('usa','USA')[5]]
    ##MT.loc[16]=['Unpred Long Pass',se('ud','ULP')[0],se('ud','ULP')[1],se('ud','ULP')[2],se('ud','ULP')[3],se('ud','ULP')[4],se('ud','ULP')[5]]
    ##MT.loc[17]=['Corner Head',se('hc','CH')[0],se('hc','CH')[1],se('hc','CH')[2],se('hc','CH')[3],se('hc','CH')[4],se('hc','CH')[5]]
##    print(spec_player_dict['home_qo'],spec_player_dict['away_qo'],spec_player_dict['home_qs'],spec_player_dict['away_qs'])
##    if quick_stop_NA > 0:
##        conv_qs_home = quick_stop_GA/quick_stop_NA
##    else:
##        conv_qs_home = 0
##    if quick_stop_NH > 0:
##        conv_qs_away = quick_stop_GH/quick_stop_NH
##    else:
##        conv_qs_away = 0

    ##quick_stop_home = spec_player_dict['away_qs'] / spec_player_dict['home_qo']
    ##quick_stop_away = spec_player_dict['home_qs'] / spec_player_dict['away_qo']
    MTSE.loc[14]=['-> Prevented SEs','','','','','','']
    MTSE.loc[15]=['Quick Stop','','',-1*quick_stop_GA,-1*quick_stop_GH,'','']
    MTSE.loc[16]=['Tech No Head',-1*tech_head_dict['NH'],-1*tech_head_dict['NA'],-1*tech_head_dict['NH']*se_TH[4],-1*tech_head_dict['NA']*se_TH[5],se_TH[4],se_TH[5]]


    ca_wing_pct = .259
    ca_center_pct = .357
    ca_dfk_pct = .084
    ca_ifk_pct = .041

    ## missed normal chance
    mnch= MT.iloc[0,1] - MT.iloc[0,3]
    mnca= MT.iloc[0,2] - MT.iloc[0,4]
##    print(MT,'mnch mnca',mnch, mnca)

    ## CA Pct = % of missed normal chance converted to CA
    ## based on CA tactic rating if lose possession and play CA; or based on defender count
    ca_pct_home = 0
    ca_pct_away = 0
    if poss_home < 0.5 and tactic_dict['home_tactic_CA'] > 0:
        ca_pct_home = htsm.ca_dict[tactic_dict['home_tactic_CA']]
    else:
        ca_pct_home = htsm.ca_def_dict[spec_player_dict['home_df']]

    if poss_away < 0.5 and tactic_dict['away_tactic_CA'] > 0:
        ca_pct_away = htsm.ca_dict[tactic_dict['away_tactic_CA']]
    else:
        ca_pct_away = htsm.ca_def_dict[spec_player_dict['away_df']]

    ##CA Chance Home/Away.  Missed Normal chance * ca pct (rate)
    cach = mnca*ca_pct_home
    caca = mnch*ca_pct_away
##    print('mnch,mnca,cach,caca',mnch,mnca,cach,caca,ca_pct_home,ca_pct_away)


    MTCA = pd.DataFrame(columns=['Type','Chance Home','Chance Away','Goals Home','Goals Away','Conv% Home','Conv% Away'])
    MTCA.loc[1]=['CA Left',cach*ca_wing_pct,caca*ca_wing_pct,cach*ca_wing_pct*conv_left_home,caca*ca_wing_pct*conv_left_away,conv_left_home,conv_left_away]
    MTCA.loc[2]=['CA Center',cach*ca_center_pct,caca*ca_center_pct,cach*ca_center_pct*conv_mid_home,caca*ca_center_pct*conv_mid_away,conv_mid_home,conv_mid_away]
    MTCA.loc[3]=['CA Right',cach*ca_wing_pct,caca*ca_wing_pct,cach*ca_wing_pct*conv_right_home,caca*ca_wing_pct*conv_right_away,conv_right_home,conv_right_away]
    MTCA.loc[4]=['CA IFK',cach*ca_ifk_pct,caca*ca_ifk_pct,cach*ca_ifk_pct*conv_ifk_home,caca*ca_ifk_pct*conv_ifk_away,conv_ifk_home,conv_ifk_away]
    MTCA.loc[5]=['CA DFK',cach*ca_dfk_pct,caca*ca_dfk_pct,cach*ca_dfk_pct*conv_dfk_home,caca*ca_dfk_pct*conv_dfk_away,conv_dfk_home,conv_dfk_away]
    MTCA.loc[0]=['CA',MTCA.iloc[0:5,1].sum(),MTCA.iloc[0:5,2].sum(),MTCA.iloc[0:5,3].sum(),MTCA.iloc[0:5,4].sum(),MTCA.iloc[0:5,3].sum()/MTCA.iloc[0:5,1].sum(),MTCA.iloc[0:5,4].sum()/MTCA.iloc[0:5,2].sum()]
    # CAs brought to main table
    MT.loc[8]=MTCA.loc[0]
    MT.loc[9]=MTSE.loc[0]
##    MT[9]=['Normal',nc_home,nc_away,MT.iloc[10:22,3].sum(),MT.iloc[10:22,4].sum(),MT.iloc[10:22,3].sum()/nc_home_xLS,MT.iloc[10:22,4].sum()/nc_away]
    MT.loc[10]=['PNF',pnf_pct_home*(mnch),pnf_pct_away*(mnca),pnf_pct_home*(mnch)*conv_PNF,pnf_pct_away*(mnca)*conv_PNF,conv_PNF,conv_PNF]
    MT.loc[11]=['PDIM',-1 * nh_pdim,-1 * na_pdim, -1 * nh_pdim * MT.iloc[0,5],-1 * na_pdim * MT.iloc[0,6],MT.iloc[0,5],MT.iloc[0,6]]
    MT.sort_index(inplace=True)
    MT.loc[-1] = ['Total',sum(MT.iloc[[0,8,9,10],1]),sum(MT.iloc[[0,8,9,10],2]),sum(MT.iloc[[0,8,9,10],3]),sum(MT.iloc[[0,8,9,10],4]),sum(MT.iloc[[0,8,9,10],3])/sum(MT.iloc[[0,8,9,10],1]),sum(MT.iloc[[0,8,9,10],4])/sum(MT.iloc[[0,8,9,10],2])]
    MT.index=MT.index+1
    MT.sort_index(inplace=True)

##    print(MT)
    xGH = MT.iloc[0,3]
    xGA = MT.iloc[0,4]
##    print('xgh,xga   ',xGH,xGA)
    MTWDL = pd.DataFrame(columns=['W','D','L'])
    MTWDL.loc[0] = [0,poisson.pmf(k=0,mu=xGH)*poisson.pmf(k=0,mu=xGA),poisson.pmf(k=0,mu=xGH)*(1-poisson.pmf(k=0,mu=xGA))]
##    print(MTWDL.round(2))
    for i in range(1,11,1):
        MTWDL.loc[i]=[poisson.pmf(k=i,mu=xGH)*poisson.cdf(k=i-1,mu=xGA),poisson.pmf(k=i,mu=xGH)*poisson.pmf(k=i,mu=xGA),poisson.pmf(k=i,mu=xGH)*(1-poisson.cdf(k=i,mu=xGA))]
    MTWDL.loc[11] = [(1-poisson.cdf(k=10,mu=xGH))*poisson.cdf(k=10,mu=xGA),(1-poisson.cdf(k=10,mu=xGH))*(1-poisson.cdf(k=10,mu=xGA)),0]

    MTWDL =MTWDL.round(3)

##    print('xGH,xGA',xGH,xGA)
##    MTWDL_ = pd.DataFrame(columns=['H','A','W','D','L'])
##    MTWDL_.loc[0] = [poisson.pmf(k=0,mu=xGH),poisson.pmf(k=0,mu=xGA),0,poisson.pmf(k=0,mu=xGH)*poisson.pmf(k=0,mu=xGA),poisson.pmf(k=0,mu=xGH)*(1-poisson.pmf(k=0,mu=xGA))]
####    print(MTWDL.round(2))
##    for i in range(1,11,1):
##        MTWDL_.loc[i]=[poisson.pmf(k=i,mu=xGH),poisson.pmf(k=i,mu=xGA),poisson.pmf(k=i,mu=xGH)*poisson.cdf(k=i-1,mu=xGA),poisson.pmf(k=i,mu=xGH)*poisson.pmf(k=i,mu=xGA),poisson.pmf(k=i,mu=xGH)*(1-poisson.cdf(k=i,mu=xGA))]
##    MTWDL_.loc[11] = [(1-poisson.cdf(k=10,mu=xGH)),(1-poisson.cdf(k=10,mu=xGA)),(1-poisson.cdf(k=10,mu=xGH))*poisson.cdf(k=10,mu=xGA),(1-poisson.cdf(k=10,mu=xGH))*(1-poisson.cdf(k=10,mu=xGA)),0]
##
##    print(MTWDL_.round(3))
    WDL = pd.DataFrame(columns=['Team',match.home_team_name,'Draw',match.away_team_name])
    WDL.loc[0] = ['Goals',match.home_team_goals,np.nan,match.away_team_goals]
    WDL.loc[1] = ['Expected Goals',MT.iloc[0,3].round(2),np.nan,MT.iloc[0,4].round(2)]
    WDL.loc[2] = ['Predicted Win / Draw / Loss',round(sum(MTWDL['W']),2)*100,round(sum(MTWDL['D']),2)*100,round(sum(MTWDL['L']),2)*100]
    WDL.loc[3] = ['HatStats',
        home_rating_right_att + home_rating_mid_att +home_rating_left_att
        + home_rating_right_def + home_rating_mid_def +home_rating_left_def
        + 3 * home_rating_midfield,
    np.nan,
        away_rating_left_att + away_rating_mid_att +away_rating_left_att
        + away_rating_right_def + away_rating_mid_def +away_rating_left_def
        + 3 * away_rating_midfield
                  ]

    ##.replace(np.inf,0)
    ##print(MT.iloc[0,1], MT.iloc[0,3])

    MTCA.sort_index(inplace=True)
    MTSE.sort_index(inplace=True)
    WDL.sort_index(inplace=True)
    MT = MT.set_index('Type').round(2)
    MTCA = MTCA.set_index('Type').round(2)
    MTSE=MTSE.set_index('Type').round(2)
    WDL=WDL.set_index('Team')
##    print(MT,MTSE,WDL)
##    print(MT[['Chance Home','Chance Away','Goals Home','Goals Away']])
##    MT = pd.DataFrame(columns=['Type','Chance Home','Chance Away','Goals Home','Goals Away','Conv% Home','Conv% Away'])

##    print(MT,MTCA,MTSE,MTWDL,WDL)
    MT_ = MT.T.style.set_table_styles([{"selector": "th", "props": [("text-align", "center")]},
           {"selector": "td", "props": [("text-align", "center")]}]).format(precision=2).to_html()
    MTCA_ = MTCA.T.style.set_table_styles([{"selector": "th", "props": [("text-align", "center")]},
           {"selector": "td", "props": [("text-align", "center")]}]).format(precision=2).to_html()

    MTSE_ = MTSE.T.style.set_table_styles([{"selector": "th", "props": [("text-align", "center")]},
           {"selector": "td", "props": [("text-align", "center")]}]).format(precision=2).to_html()
##    print(WDL)
##    WDL['Goals']=WDL['Goals'].astype('Int64')
##    WDL['Expected Goals']=WDL['Expected Goals'].round(2)
##    WDL['Predicted Win / Draw / Loss'] = WDL['Predicted Win / Draw / Loss'].astype('Int64')
##    WDL['HatStats']=WDL['Expected Goals'].astype('Int64')
##    print(WDL)

##    WDL_ = WDL.T.style.set_table_styles([{"selector": "th", "props": [("text-align", "center")]},
##           {"selector": "td", "props": [("text-align", "center")]}]).format({1: '{:.2f}'},precision=0).to_html()
    WDL_ = WDL.T.style.set_table_styles([{"selector": "th", "props": [("text-align", "center")]},
##           {"selector": "td", "props": [("text-align", "center")]}]).format({0:'{:.0f}', 1: '{:.2f}',2:'{:.0f}',3:'{:.0f}'}).to_html()
           {"selector": "td", "props": [("text-align", "center")]}]).format({'Expected Goals': '{:.2f}'},precision=0,na_rep='').to_html()
##    WDL_=WDL_.style.format({1: '{:.2f}'})
##    print(WDL)
    __end = datetime.datetime.now()
##    print('run time',__end - __start)
    return(MT_,MTSE_,WDL_,MTCA_)
    

##    return(MT,MTCA,MTSE,MTWDL,WDL)

    ##goals, hat, hts , win%
    ##diff_buts=match.home_team_goals-match.away_team_goals
    ##print(diff_buts)

    ##id_league = 5662
    ##num_saison=73
    ##league = chpp.league(ht_id=id_league)
    ##print(league.level)



    ##
    ##fixtures = chpp.league_fixtures(ht_id=id_league,season=num_saison)
    ##if num_saison==int(chpp.league_fixtures(ht_id=id_league).season):
    ##    nb_matchs=min(4*int(chpp.league(ht_id=id_league).current_match_round)-4,56)
    ##else:
    ##    nb_matchs=56
    ##liste_matchs=[chpp.match(ht_id=o.ht_id) for o in chpp.league_fixtures(ht_id=id_league,season=num_saison).matches][:nb_matchs]
    ##print(liste_matchs)
    ##
    ##

    ##
    ##MT.loc[1]=['Left',round(nc_home_xLS*nc_wing_pct,2),round(nc_away_xLS*nc_wing_pct,2),round(nc_home_xLS*nc_wing_pct*conv_right_home,2),round(nc_away_xLS*nc_wing_pct*conv_right_away,2),round(conv_right_home,3),round(conv_right_away,3),3)]
    ##MT.loc[2]=['Center',round(nc_home_xLS*nc_center_pct,2),round(nc_away_xLS*nc_center_pct,2),round(nc_home_xLS*nc_center_pct*conv_mid_home,2),round(nc_away_xLS*nc_center_pct*conv_mid_away,2),round(conv_mid_home,3),round(conv_mid_away,3)]
    ##MT.loc[3]=['Right',round(nc_home_xLS*nc_wing_pct,2),round(nc_away_xLS*nc_wing_pct,2),round(nc_home_xLS*nc_wing_pct*conv_left_home,2),round(nc_away_xLS*nc_wing_pct*conv_left_away,2),round(conv_left_home,3),round(conv_left_away,3)]
    ##MT.loc[4]=['IFK',round(nc_home_xLS*nc_ifk_pct,2),round(nc_away_xLS*nc_ifk_pct,2),round(nc_home_xLS*nc_ifk_pct*conv_ifk_home,2),round(nc_away_xLS*nc_ifk_pct*conv_ifk_away,2),round(conv_ifk_home,3),round(conv_ifk_away,3)]
    ##MT.loc[5]=['PK',round(nc_home_xLS*nc_pk_home_pct,2),round(nc_away_xLS*nc_pk_away_pct,2),round(nc_home_xLS*nc_pk_home_pct*conv_pk_home,2),round(nc_away_xLS*nc_pk_away_pct*conv_pk_away,2),round(conv_pk_home,3),round(conv_pk_away,3)]
    ##MT.loc[6]=['DFK',round(nc_home_xLS*nc_dfk_home_pct,2),round(nc_away_xLS*nc_dfk_away_pct,2),round(nc_home_xLS*nc_dfk_home_pct*conv_dfk_home,2),round(nc_away_xLS*nc_dfk_away_pct*conv_dfk_away,2),round(conv_dfk_home,3),round(conv_dfk_away,3)]
    ##MT.loc[7]=['LS',round(nc_home*ls_pct_home,2),round(nc_away*ls_pct_away,2),round(nc_home*ls_pct_home*conv_ls_home,2),round(nc_away*ls_pct_away*conv_ls_away,2),round(conv_ls_home,3),round(conv_ls_away,3)]
    ##MT.loc[0]=['Normal',round(nc_home,2),round(nc_away,2),round(MT.iloc[1:7,3].sum(),2),round(MT.iloc[1:6,4].sum(),2),round(MT.iloc[1:6,3].sum()/nc_home_xLS,3),round(MT.iloc[1:7,4].sum()/nc_away,3)]
    ##MT.sort_index(inplace=True)
    ##MT.loc[8]=['PNF',round(pnf_pct_home*(MT.iloc[0,1] - MT.iloc[0,3]),2),round(pnf_pct_away*(MT.iloc[0,2] - MT.iloc[0,4]),2),round(pnf_pct_home*(MT.iloc[0,1] - MT.iloc[0,3])*conv_PNF,2),round(pnf_pct_away*(MT.iloc[0,2] - MT.iloc[0,4])*conv_PNF,2),conv_PNF,conv_PNF]


##matchid = 718545350
##matchid=715438970
##matchid=718725842
##matchid = 715438966
##matchid=715977580
##matchid=719125248
matchid=724762356
##matchid=31722567
match_predict(matchid)



