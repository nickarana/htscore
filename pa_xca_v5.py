import pandas as pd
import pa_hts_mappings_v4 as htsm

def make_clickable(val):
    return f'<a target="_blank" href="{val}">{val}</a>'

##'<a href="' + df['url'] + '">' + '</a>'

def XCA(csvin,cols_in,cols_out,sortby):

    XCA = pd.read_csv(csvin,usecols=cols_in)
    if 'Competition' in XCA.columns:
        XCA.loc[(XCA['Competition']=='WC/U20'),'Competition']='I'
        XCA.loc[(XCA['Competition']=='HTM'),'Competition']='H'
    XCA['Season']='S' + XCA['Season'].astype(int).astype(str)
    if 'MatchRound' in XCA.columns:
        XCA['Round_Filter']='R' + XCA['MatchRound'].astype(str)
    
    XCA['Match URL'] = 'https://www.hattrick.org/goto.ashx?path=/Club/Matches/Match.aspx?matchID=' + XCA['MatchID'].astype(str)
    XCA['Team URL']='https://www.hattrick.org/goto.ashx?path=/Club/?TeamID=' +  XCA['TeamID'].astype(str)
    if 'Goals' in XCA.columns:
        XCA['Score']=XCA['Goals'].astype(int).astype(str) + '-' + XCA['Opp_Goals'].astype(int).astype(str)

    if 'TacticType' in XCA.columns:
        XCA['Tactic']=XCA['TacticType'].map(htsm.tactic_dict)
        XCA.loc[(XCA['TacticType']==0),'TacticSkill']=''
        
    if 'Match_OT_Pen' in XCA.columns:
        XCA['Len']='Reg'
        XCA.loc[(XCA['Match_OT_Pen']==2),'Len']='OT'
        XCA.loc[(XCA['Match_OT_Pen']==3),'Len']='PK'
     
    XCA=XCA[cols_out].sort_values(by=sortby,ascending=False)
    if 'HTScore' in XCA.columns:
        XCA['HTScore']=XCA['HTScore'].round().astype(int)
    if 'HTSN' in XCA.columns:
        XCA['HTSN']=XCA['HTSN'].round().astype(int)
   
    XCA=XCA.reset_index()
    XCA.index=XCA.index + 1
##    XCA=XCA.drop(['index'],axis=1)
    cols_old = ['MatchRound','Season','Competition','LeagueName','HTScore','TeamName']
    cols_new = ['R','S','Comp','Country','HTS','Team Name']
    for col_old,col_new in zip(cols_old,cols_new):
        if col_old in XCA.columns:
            XCA.rename(columns={col_old:col_new},inplace=True)
##    print(XCA.columns.values,XCA[['TeamName','HTS','HTSN']].head(5))
##    print(XCA.columns.values,XCA[['TeamName','HatStats']].head(5))

##    XCA.rename(columns={'MatchRound':'R','Season':'S','Competition':'Comp','LeagueName':'Country'},inplace=True)
    return(XCA)



##'RatingLeftAtt':'AttL','RatingLeftDef':'DefL','RatingMidAtt':'AttM','RatingMidDef':'DefM','RatingMidfield':'Mid','RatingRightAtt':'AttR','RatingRightDef':'DefR'

def XCA_100(XCA):
    XCA=XCA.head(n=100)
    XCA=XCA.drop(['index','TeamID','Round_Filter'],axis=1)
    XCA = XCA.style.set_table_styles([{"selector": "th", "props": [("text-align", "center")]},
               {"selector": "td", "props": [("text-align", "center")]}]).format({'Match URL': make_clickable,'Team URL': make_clickable},precision=2).to_html(escape=False)
    return(XCA)

def XCA_filter(XCA,xca_filter_value,drop_flag):

    LD=pd.read_csv('LeagueDetails.csv',usecols=['LeagueName']).drop_duplicates()
    country_list = LD['LeagueName'].str.upper().to_list()
    filters = xca_filter_value.split(';')

    for filter_ in filters:
        try:
            XCA=XCA[(XCA['TeamID']==int(filter_))]
        except:
            if filter_.upper() == 'ALL':
                XCA=XCA
            elif str(filter_).upper() in ['L','C','P','H','I']:
                XCA=XCA[(XCA['Comp']==filter_)]
            elif filter_.upper() in country_list:
                XCA=XCA[(XCA['Country'].str.upper()==filter_.upper())]
            elif filter_.upper() in country_list:
                XCA=XCA[(XCA['Country'].str.upper()==filter_.upper())]
            elif len(filter_)==3 and filter_[:1].upper()=='S':
                XCA=XCA[(XCA['S']==filter_.upper())]
            elif len(filter_) in [2,3] and filter_[:1].upper()=='R':
                XCA=XCA[(XCA['Round_Filter']==filter_.upper())]
            elif len(filter_) in [2,3,4] and filter_[:1].upper()=='T':
                XCA=XCA.head(int(filter_[1:]))
##                XCA=XCA[(XCA['Round_Filter']==filter_.upper())]
            elif filter_[:4].upper()=='TAC_':
##                print(filter_[5:].upper())
                XCA=XCA[(XCA['Tactic']==filter_[4:].upper())]
            else:
                XCA=XCA[(XCA['Team Name'].str.contains(filter_,case=False))]
    if drop_flag == 1:
        XCA=XCA.drop(['index','TeamID','Round_Filter'],axis=1)
        XCA = XCA.style.set_table_styles([{"selector": "th", "props": [("text-align", "center")]},
               {"selector": "td", "props": [("text-align", "center")]}]).format({'Match URL': make_clickable,'Team URL': make_clickable},precision=2).to_html(escape=False)
    return(XCA)

def XCAT(XCA,sortby):

    XCA['M']=1
    XCAT_by = ['TeamID','Team Name']
    vars_by = ['Country']
    for var_by in vars_by:
        if var_by in XCA:
            XCAT_by.append(var_by)

##    df.groupby('Company Name').agg(MySum=('Amount', 'sum'), MyCount=('Amount', 'count'))
    XCAT = XCA.groupby(XCAT_by,as_index=False).agg(M=('M','sum'),Max=(sortby,'max'))
    XCAT.rename(columns={'Max':sortby+' max'},inplace=True)
    XCAT = XCAT.sort_values(by=['M',sortby+' max'],ascending=[False,False])
##    HTM = HTM.sort_values(by=['HTSN','Opp_HTSN'],ascending=[False,False])
##    print(XCAT.head(10))    
##    XCA=XCA.head(n=100)
    XCAT['Team URL']='https://www.hattrick.org/goto.ashx?path=/Club/?TeamID=' +  XCAT['TeamID'].astype(str)
    XCAT=XCAT.reset_index()
    XCAT.index=XCAT.index + 1
    XCAT=XCAT.drop(['index','TeamID'],axis=1)    

    XCAT = XCAT.style.set_table_styles([{"selector": "th", "props": [("text-align", "center")]},
               {"selector": "td", "props": [("text-align", "center")]}]).format({'Match URL': make_clickable,'Team URL': make_clickable},precision=2).to_html(escape=False)
    return(XCAT)

##xca_filter_value  ='ooster;s85'
##XCA_filter(XCA(),xca_filter_value)
##XCAT(XCA(htsm.csvXHH,htsm.cols_XHH,htsm.cols_XHH_out,'HatStats'),'HatStats')
##XCAT(XCA_filter(XCA(htsm.csvXHH,htsm.cols_XHH,htsm.cols_XHH_out,'HatStats'),'T500',0),'HatStats')
