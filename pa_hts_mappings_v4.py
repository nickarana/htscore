import pandas as pd

####### v4 changes
#### spec freq dict
#### w-H reduce 50% when 1 Header that is Wing
#### LS conv% change for W-H
#### PC unified dict
####specX_corner head dict, with increased factors
#### added roleID_pos_dict for speeded up code
date_25A = pd.Timestamp(2025,1,7)
date_24C = pd.Timestamp(2024,9,17)
date_24B = pd.Timestamp(2024,5,28)
date_24A = pd.Timestamp(2024, 2, 6)
date_23C = pd.Timestamp(2023, 10, 17)
date_23B = pd.Timestamp(2023, 6, 27)
date_23A = pd.Timestamp(2023, 3, 7)
date_22C = pd.Timestamp(2022, 11, 15)
date_22B = pd.Timestamp(2022, 7, 26)
date_22A = pd.Timestamp(2022, 4, 5)
date_21D = pd.Timestamp(2021, 12, 14)
date_21C = pd.Timestamp(2021, 8, 24)
date_21B = pd.Timestamp(2021, 5, 4)
date_21A = pd.Timestamp(2021, 1, 12)
date_20C = pd.Timestamp(2020, 9, 22)
date_20B = pd.Timestamp(2020, 6, 2)
date_20A = pd.Timestamp(2020, 2, 11)
date_19C = pd.Timestamp(2019, 10, 22)  # first match is fri 25 oct
date_19B = pd.Timestamp(2019, 7, 2)
date_19A = pd.Timestamp(2019, 3, 12)
date_18C = pd.Timestamp(2018, 11, 20)
date_18B = pd.Timestamp(2018, 7, 31)
s1_date_w01_dict = {'18B':date_18B,'18C':date_18C,'19A':date_19A,'19B':date_19B,'19C':date_19C,'20A':date_20A,'20B':date_20B,'20C':date_20C,'21A':date_21A,'21B':date_21B,'21C':date_21C,'21D':date_21D,'22A':date_22A,'22B':date_22B,'22C':date_22C,'23A':date_23A,'23B':date_23B,'23C':date_23C}
s1_sH_dict = {'WC':'WC','18B':69,'18C':70,'19A':71,'19B':72,'19C':73,'20A':74,'20B':75,'20C':76,'21A':77,'21B':78,'21C':79,'21D':80,'22A':81,'22B':82,'22C':83,'23A':84,'23B':85,'23C':86,'24A':87}


def csvW(df,csvout):
    df.to_csv(csvout,mode='w',index=False,header=True)

def csvA(df,csvout):
    df.to_csv(csvout,mode='a',index=False,header=False)


tactic_dict={0:'',1:'PR',2:'CA',3:'AOW',4:'AIM',7:'PC',8:'LS'}

press_dict={0:0,1:0,2:0.00,3:0.23,4:0.68,5:1.14,6:1.41,7:1.74,8:2.08,9:2.52,10:2.86,11:3.25,12:3.44,13:3.59,14:3.74,15:3.89,16:4.04,17:4.19,18:4.34}
pdim_dict={0:0.0000,1:0.0625,2:0.1000,3:0.1250}

ifk_dict={
-27:0.0000,-26:0.0003,-25:0.0004,-24:0.0007,-23:0.0009,-22:0.0013,-21:0.0020,-20:0.0054,-19:0.0094,-18:0.0215,-17:0.0317,-16:0.0465,-15:0.0593,-14:0.0706,
-13:0.0839,-12:0.1012,-11:0.1161,-10:0.1308,-9:0.1468,-8:0.1618,-7:0.1764,-6:0.1928,-5:0.2091,-4:0.2249,-3:0.2427,-2:0.2752,-1:0.3663,0:0.4522,1:0.5250,2:0.5780,3:0.6019,
4:0.6286,5:0.6511,6:0.6794,7:0.7005,8:0.7269,9:0.7526,10:0.7711,11:0.7909,12:0.8113,13:0.8284,14:0.8438,15:0.8570,16:0.8690,17:0.8802,18:0.8870,19:0.9105,20:0.9134,
21:0.9164,22:0.9180,23:0.9196,24:0.9210,25:0.9225,26:0.9240,27:0.9255,28:0.9270,29:0.9285,30:0.9300
}

aim_dict={
    0:0.000,1:0.170,2:0.180,3:0.190,4:0.200,5:0.210,6:0.220,7:0.230,8:0.240,9:0.250,10:0.260,11:0.270,12:0.280,13:0.290,14:0.300,15:0.310,16:0.320,17:0.330,18:0.340,19:0.350,20:0.360,21:0.365,22:0.370,23:0.375,24:0.380,25:0.385,26:0.390,27:0.395,28:0.400,29:0.405,30:0.410,31:0.415,32:0.420,33:0.425,34:0.430,35:0.435,36:0.440,37:0.445,38:0.450,39:0.450,40:0.450
    }

aow_dict={
    0:0.000,1:0.300,2:0.310,3:0.320,4:0.330,5:0.340,6:0.350,7:0.360,8:0.370,9:0.380,10:0.390,11:0.400,12:0.410,13:0.420,14:0.430,15:0.440,16:0.450,17:0.460,18:0.470,19:0.480,20:0.490,21:0.500,22:0.510,23:0.520,24:0.530,25:0.540,26:0.545,27:0.550,28:0.555,29:0.560,30:0.565,31:0.570,32:0.575,33:0.580,34:0.585,35:0.590,36:0.595,37:0.600,38:0.600,39:0.600,40:0.600
    }


ls_pct_dict = {
    0:0.006, 1:0.02, 2:0.0350,3:0.0500,4:0.0650,5:0.0800,6:0.0950,7:0.1100,8:0.1250,9:0.1400,10:0.1500,11:0.1600,12:0.1700,13:0.1800,14:0.1900,15:0.2000,16:0.2075,17:0.2150,18:0.2225,19:0.2300,20:0.2375,21:0.2425,22:0.2475,23:0.2525,24:0.2575,25:0.2625,26:0.2675,27:0.2725,28:0.2775,29:0.2825,30:0.2875,31:0.2925,31:0.2975
    }


ls_dict = {
    0:0.1100,1:0.0387,3:0.0500,4:0.0653,5:0.0876,6:0.1082,7:0.1378,8:0.1617,9:0.1838,10:0.2263,11:0.2566,12:0.2924,13:0.3361,14:0.3777,15:0.4172,16:0.4634,17:0.5570,18:0.5950,19:0.6103,20:0.6293,21:0.6489,22:0.6624,23:0.6724,24:0.6824,25:0.6910,26:0.7000,27:0.7090,28:0.7180,29:0.7270,30:0.7360,31:0.7450,32:0.75
               }

ca_dict ={
    0:0.0000,1:0.0250,2:0.0300,3:0.0350,4:0.0400,5:0.0450,6:0.0500,7:0.0700,8:0.0900,9:0.1089,10:0.1305,11:0.1562,12:0.1902,13:0.2199,14:0.2491,15:0.2870,16:0.3167,17:0.3379,18:0.3518,19:0.3679,20:0.3812,21:0.3906,22:0.4069,23:0.4163,24:0.4260,25:0.4310,26:0.4360,27:0.4410,28:0.4460,29:0.4510,30:0.4560,31:0.4610,32:0.4660,33:0.4710,34:0.4735,35:0.4760,36:0.4785,37:0.4810,38:0.4835,39:0.4860,40:0.4885
 }

ca_def_dict={
2:0.0140,3:0.0323,4:0.0677,5:0.0973
}

corner_anyone_ifk_dict = {
    -40:0.209,-39:0.216,-38:0.224,-37:0.231,-36:0.239,-35:0.246,-34:0.254,-33:0.261,-32:0.269,-31:0.276,-30:0.284,-29:0.291,-28:0.299,-27:0.306,-26:0.314,-25:0.321,-24:0.329,-23:0.336,-22:0.345,-21:0.355,-20:0.365,-19:0.375,-18:0.384,-17:0.391,-16:0.399,-15:0.406,-14:0.415,-13:0.425,-12:0.435,-11:0.445,-10:0.455,-9:0.465,
    -8:0.475,-7:0.485,-6:0.494,-5:0.501,-4:0.509,-3:0.516,-2:0.525,-1:0.535,0:0.545,1:0.555,2:0.563,3:0.568,4:0.573,5:0.578,6:0.583,7:0.588,8:0.593,9:0.598,10:0.603,11:0.608,12:0.613,13:0.618,14:0.623,15:0.628,16:0.633,17:0.638,18:0.643,19:0.648,20:0.653,21:0.658,22:0.663,23:0.668,24:0.673,
     25:0.678,26:0.683,27:0.688,28:0.693,29:0.698,30:0.703
     }

corner_anyone_k_dict= {
    0:1.450,0.25:1.440,0.5:1.430,0.75:1.420,1:1.410,1.25:1.400,1.5:1.390,1.75:1.380,2:1.370,2.25:1.360,2.5:1.350,2.75:1.345,3:1.340,3.25:1.335,3.5:1.330,3.75:1.310,4:1.290,4.25:1.270,4.5:1.250,4.75:1.225,5:1.200,5.25:1.180,5.5:1.160,5.75:1.145,6:1.130,6.25:1.115,6.5:1.100,6.75:1.080,7:1.060,7.25:1.040,7.5:1.020,7.75:1.010,8:1.000,
    8.25:0.990,8.5:0.980,8.75:0.970,9:0.960,9.25:0.950,9.5:0.940,9.75:0.930,10:0.920,10.25:0.915,10.5:0.910,10.75:0.900,11:0.890,11.25:0.885,11.5:0.880,11.75:0.870,12:0.860,12.25:0.855,12.5:0.850,12.75:0.840,13:0.830,13.25:0.825,13.5:0.820,13.75:0.815,14:0.810,14.25:0.805,14.5:0.800,14.75:0.795,15:0.790,15.25:0.785,15.5:0.780,15.75:0.775,16:0.770
}


pnf_pct_dict = {
    '0_0':0,'0_1':0,'0_2':0,'0_3':0,'1_0':0.096,'1_1':0.069,'1_2':0.033,'1_3':0.020,'2_0':0.117,'2_1':0.096,'2_2':0.052,'2_3':0.031,'3_0':0.130,'3_1':0.115,'3_2':0.067,'3_3':0.040
}

isp_ch_dict = {
-46:0.414,-45:0.431,-44:0.448,-43:0.465,-42:0.481,-41:0.498,-40:0.515,-39:0.532,-38:0.548,-37:0.565,-36:0.582,-35:0.599,-34:0.615,-33:0.632,-32:0.649,-31:0.666,-30:0.682,-29:0.699,-28:0.716,-27:0.733,-26:0.749,-25:0.765,-24:0.782,-23:0.798,-22:0.818,-21:0.842,-20:0.865,-19:0.889,-18:0.903,-17:0.906,-16:0.910,-15:0.913,-14:0.923,-13:0.938,-12:0.954,-11:0.969,-10:0.984,-9:0.999,-8:1.013,-7:1.028,-6:1.037,-5:1.042,-4:1.047,-3:1.052,-2:1.057,-1:1.063,0:1.070,1:1.076,2:1.079,3:1.080,4:1.081,5:1.082,6:1.082,7:1.083,8:1.084,9:1.085,10:1.085,11:1.086,12:1.087,13:1.088,14:1.088,15:1.089,16:1.090,17:1.091,18:1.091,19:1.092,20:1.093,21:1.094,22:1.094,23:1.095,24:1.096,25:1.097,26:1.097,27:1.098,28:1.099,29:1.100
}

head_ch_dict={
    -6:0.013,-5:0.034,-4:0.068,-3:0.092,-2:0.147,-1:0.250,0:0.438,1:0.622,2:0.703,3:0.755,4:0.805,5:0.824,6:0.840,7:0.850,8:0.855,9:0.858,10:0.860
}

specX_dict ={
    0:0,1:1,2:1.934,3:2.826,4:3.7,5:4.53,6:5.328,7:6.09,8:6.816,9:7.506,10:8.16
     }
specX_CH_dict ={
    0:0,1:1,2:2.25,3:3.35,4:4.45,5:5.55,6:6.65,7:7.75,8:8.85,9:9.95,10:11.05
    }

spec_freq_dict = {
    'QR':0.0871,'QP':0.0815,'CH':0.0500,'WH':0.0509,'ULP':0.0703,'USA':0.0301,'USO':0.0410,'UM':0.0235,'UOG':0.0425,'CA':0.1000,'WA':0.0800,'TH':0.0954,'ZZ':0.0920
    }

pc_dict= {
0:1.00,1:1.10,2:1.18,3:1.26,4:1.34,5:1.42,6:1.50,7:1.58,8:1.66,9:1.72,10:1.77,11:1.82,12:1.86,13:1.90,14:1.93,15:1.94,16:1.95,17:1.96,18:1.97,19:1.98,20:1.99,21:2.00,22:2.01,23:2.02,24:2.03,25:2.04,26:2.05,27:2.06,28:2.07,29:2.08,30:2.09,31:2.10,32:2.11,33:2.12,34:2.13,35:2.14
}


PK=pd.DataFrame(
[
[1,0.41,0.2,0.18,0.12,0.1,0.09,0.08,0.07,0.06,0.05,0.04,0.03],
[6,0.56,0.36,0.32,0.25,0.22,0.21,0.2,0.19,0.14,0.13,0.12,0.11],
[6.5,0.7,0.52,0.47,0.37,0.34,0.31,0.3,0.29,0.27,0.25,0.22,0.14],
[7,0.71,0.53,0.52,0.43,0.38,0.37,0.41,0.3,0.34,0.31,0.23,0.15],
[7.25,0.74,0.54,0.49,0.53,0.43,0.42,0.38,0.33,0.28,0.26,0.24,0.22],
[7.5,0.77,0.61,0.55,0.52,0.47,0.45,0.43,0.4,0.36,0.33,0.3,0.28],
[8,0.79,0.65,0.58,0.52,0.48,0.45,0.43,0.42,0.4,0.35,0.33,0.31],
[8.5,0.8,0.67,0.6,0.57,0.51,0.48,0.46,0.44,0.39,0.38,0.36,0.28],
[9,0.82,0.73,0.62,0.6,0.53,0.5,0.47,0.46,0.45,0.4,0.37,0.34],
[9.5,0.83,0.7,0.65,0.62,0.55,0.54,0.5,0.48,0.51,0.45,0.42,0.37],
[10.25,0.84,0.76,0.69,0.65,0.62,0.59,0.58,0.56,0.52,0.53,0.46,0.4],
[11.5,0.87,0.8,0.75,0.7,0.67,0.65,0.63,0.6,0.58,0.59,0.53,0.5]
],
columns=['ISP_Att','A','B','C','D','E','F','G','H','I','J','K','L']
)
DFK=pd.DataFrame(
[
[1,0.09,0.04,0.03,0.03,0.01,0.02,0.01,0.01,0.02,0.01,0.01,0.01],
[6,0.18,0.09,0.07,0.05,0.04,0.03,0.03,0.03,0.03,0.04,0.02,0.01],
[6.5,0.25,0.16,0.1,0.1,0.09,0.07,0.08,0.06,0.05,0.04,0.05,0.04],
[7,0.33,0.19,0.17,0.13,0.11,0.1,0.08,0.08,0.07,0.06,0.07,0.04],
[7.25,0.35,0.21,0.16,0.13,0.11,0.13,0.1,0.09,0.08,0.09,0.05,0.06],
[7.5,0.36,0.22,0.18,0.15,0.13,0.13,0.1,0.1,0.1,0.09,0.08,0.05],
[8,0.39,0.24,0.19,0.16,0.14,0.13,0.12,0.12,0.1,0.08,0.07,0.07],
[8.5,0.41,0.24,0.22,0.17,0.16,0.13,0.14,0.1,0.08,0.1,0.08,0.07],
[9,0.42,0.26,0.21,0.19,0.18,0.14,0.14,0.11,0.13,0.12,0.09,0.07],
[9.5,0.45,0.27,0.25,0.19,0.19,0.16,0.13,0.13,0.13,0.11,0.1,0.1],
[10.25,0.5,0.37,0.28,0.24,0.22,0.2,0.19,0.16,0.17,0.15,0.15,0.1],
[11.5,0.53,0.36,0.31,0.27,0.24,0.24,0.19,0.21,0.19,0.17,0.15,0.14]
],
columns=['ISP_Att','A','B','C','D','E','F','G','H','I','J','K','L']
)

PK_DFK=pd.DataFrame(
[
[1,0.28,0.23,0.22,0.21,0.22,0.22,0.22,0.21,0.17,0.21,0.19,0.2],
[6,0.33,0.27,0.26,0.23,0.22,0.24,0.24,0.23,0.2,0.24,0.23,0.22],
[6.5,0.37,0.3,0.28,0.26,0.27,0.25,0.25,0.24,0.25,0.25,0.19,0.24],
[7,0.4,0.33,0.31,0.29,0.28,0.28,0.27,0.25,0.26,0.24,0.24,0.24],
[7.25,0.39,0.32,0.3,0.29,0.28,0.27,0.25,0.27,0.27,0.27,0.26,0.25],
[7.5,0.43,0.34,0.31,0.3,0.29,0.29,0.28,0.27,0.27,0.26,0.26,0.26],
[8,0.42,0.35,0.33,0.31,0.31,0.28,0.28,0.3,0.28,0.27,0.26,0.26],
[8.5,0.43,0.38,0.33,0.33,0.31,0.32,0.29,0.26,0.26,0.27,0.27,0.26],
[9,0.47,0.36,0.34,0.31,0.31,0.3,0.31,0.27,0.29,0.28,0.26,0.27],
[9.5,0.46,0.37,0.34,0.32,0.31,0.3,0.32,0.3,0.29,0.29,0.25,0.27],
[10.25,0.48,0.4,0.36,0.36,0.33,0.34,0.32,0.31,0.3,0.31,0.31,0.28],
[11.5,0.47,0.43,0.38,0.39,0.35,0.36,0.35,0.33,0.32,0.32,0.31,0.31]
],
columns=['ISP_Att','A','B','C','D','E','F','G','H','I','J','K','L']
)

pk_ispatt_dict ={
0.25:0,0.5:0,0.75:0,1:0,1.25:0,1.5:0,1.75:0,2:0,2.25:0,2.5:0,2.75:0,3:0,3.25:0,3.5:0,3.75:0,4:0,4.25:0,4.5:0,4.75:0,5:0,5.25:0,5.5:0,5.75:0,6:1,6.25:1,6.5:2,6.75:2,7:3,7.25:4,7.5:5,7.75:5,8:6,8.25:6,8.5:7,8.75:7,9:8,9.25:8,9.5:9,9.75:9,10:9,10.25:10,10.5:10,10.75:10,11:10,11.25:10,11.5:11,11.75:11,12:11,12.25:11,12.5:11,12.75:11,13:11,13.25:11,13.5:11,13.75:11,14:11,14.25:11,14.5:11,14.75:11,15:11,15.25:11,15.5:11,15.75:11,16:11,16.25:11,16.5:11,16.75:11,17:11,17.25:11,17.5:11,17.75:11,18:11,18.25:11,18.5:11,18.75:11,19:11,19.25:11,19.5:11,19.75:11,20:11,20.25:11,20.5:11,20.75:11,21:11,21.25:11,21.5:11,21.75:11,22:11,22.25:11,22.5:11,22.75:11,23:11,23.25:11,23.5:11,23.75:11,24:11,24.25:11,24.5:11,24.75:11,25:11
}

pk_ispdef_dict = {
0.25:1,0.5:1,0.75:1,1:1,1.25:1,1.5:1,1.75:1,2:1,2.25:1,2.5:1,2.75:1,3:1,3.25:1,3.5:1,3.75:1,4:1,4.25:1,4.5:1,4.75:1,5:1,5.25:1,5.5:1,5.75:1,6:1,6.25:1,6.5:1,6.75:1,7:1,7.25:1,7.5:1,7.75:1,8:2,8.25:2,8.5:3,8.75:3,9:4,9.25:4,9.5:5,9.75:5,10:6,10.25:6,10.5:7,10.75:7,11:8,11.25:8,11.5:9,11.75:9,12:10,12.25:10,12.5:11,12.75:11,13:11,13.25:11,13.5:12,13.75:12,14:12,14.25:12,14.5:12,14.75:12,15:12,15.25:12,15.5:12,15.75:12,16:12,16.25:12,16.5:12,16.75:12,17:12,17.25:12,17.5:12,17.75:12,18:12,18.25:12,18.5:12,18.75:12,19:12,19.25:12,19.5:12,19.75:12,20:12,20.25:12,20.5:12,20.75:12,21:12,21.25:12,21.5:12,21.75:12,22:12,22.25:12,22.5:12,22.75:12,23:12,23.25:12,23.5:12,23.75:12,24:12,24.25:12,24.5:12,24.75:12,25:12
}

seconv_kstars_dict={'QP':0,'QR':1,'TH':2,'ULP':3,'UM':4,'UOG':5,'USO':6,'USA':7,'WA':8,'WH':9,'ZZ':10}

##print(PK.iloc[3][10])
##print(PK.lookup(5,'9'))

SE_CONV = pd.DataFrame(
[
['qp',0.7,0.68,0.66,0.64,0.6196,0.58,0.54,0.5009,0.4865,0.455,0.4459,0.4177,0.4006,0.3845,0.3795,0.3745,0.3695,0.3645,0.3595,0.3545,0.3495,0.3445,0.3395,0.3345],
['qr',0.6,0.59,0.58,0.57,0.55,0.53,0.5085,0.4557,0.4395,0.4189,0.3942,0.3697,0.3667,0.3452,0.3428,0.3273,0.3001,0.2989,0.2909,0.28,0.2692,0.259,0.24,0.23],
['th',0.41,0.4,0.39,0.38,0.37,0.36,0.35,0.3439,0.3327,0.3077,0.297,0.2829,0.2749,0.2699,0.2649,0.2599,0.2549,0.2499,0.2449,0.2399,0.2349,0.2299,0.2249,0.2199],
['ulp',0.7027,0.6304,0.61,0.59,0.57,0.55,0.53,0.5096,0.4889,0.4698,0.4566,0.4472,0.4394,0.42,0.399,0.38,0.3676,0.3361,0.3065,0.3033,0.2917,0.28,0.27,0.26],
['um',0.3609,0.3492,0.3379,0.3237,0.3074,0.2939,0.2798,0.2639,0.2513,0.2357,0.2256,0.216,0.2092,0.2012,0.1962,0.1904,0.1842,0.1781,0.1725,0.1674,0.1611,0.1547,0.148,0.1399],
['uog',0.4028,0.3897,0.3771,0.3613,0.343,0.328,0.3123,0.2945,0.2804,0.263,0.2518,0.241,0.2335,0.2245,0.219,0.2125,0.2055,0.1987,0.1925,0.1868,0.1798,0.1726,0.1652,0.1561],
['uso',0.98,0.96,0.945,0.8804,0.8633,0.8238,0.7854,0.7217,0.7011,0.6535,0.6366,0.6173,0.5869,0.5667,0.552,0.537,0.521,0.5025,0.48,0.4595,0.44,0.42,0.4,0.38],
['usa',0.62,0.6,0.5755,0.5519,0.4934,0.48,0.47,0.4624,0.4509,0.4264,0.4056,0.4006,0.3956,0.3906,0.3856,0.3806,0.3756,0.3706,0.3656,0.3571,0.34,0.33,0.32,0.31],
['wa',0.7652,0.7507,0.7215,0.6879,0.6355,0.6028,0.5734,0.5492,0.501,0.4664,0.4426,0.4145,0.405,0.3782,0.369,0.3596,0.3492,0.34,0.33,0.32,0.3,0.2761,0.2581,0.2167],
['wh',0.9026,0.8865,0.8575,0.8251,0.7756,0.7421,0.7113,0.687,0.6432,0.609,0.5839,0.5599,0.5506,0.525,0.516,0.51,0.5027,0.49,0.48,0.47,0.46,0.4399,0.4158,0.3784],
['zz',0.5859,0.5645,0.4991,0.4767,0.4489,0.4122,0.3863,0.3594,0.3354,0.3038,0.2815,0.2666,0.2499,0.2426,0.2376,0.2221,0.2046,0.1962,0.1893,0.172,0.1746,0.1512,0.1653,0.1325]
],
columns=['K_Stars','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X']
)

SE_LS_CONV = pd.DataFrame(
[
['qp',0.5899,0.5731,0.5562,0.5394,0.5222,0.4888,0.4551,0.4222,0.41,0.3835,0.3758,0.352,0.3376,0.324,0.3198,0.3156,0.3114,0.3072,0.303,0.2988,0.2945,0.2903,0.2861,0.2819],
['qr',0.9386,0.9229,0.9073,0.8916,0.8604,0.8291,0.7954,0.7128,0.6875,0.6553,0.6166,0.5782,0.5736,0.54,0.5362,0.512,0.4694,0.4675,0.455,0.438,0.4212,0.4052,0.3754,0.3598],
['th',0.5668,0.553,0.5392,0.5253,0.5115,0.4977,0.4839,0.4754,0.4599,0.4254,0.4106,0.3911,0.38,0.3731,0.3662,0.3593,0.3524,0.3454,0.3385,0.3316,0.3247,0.3178,0.3109,0.304],
['ulp',0.7211,0.647,0.626,0.6055,0.585,0.5644,0.5439,0.523,0.5017,0.4821,0.4686,0.4589,0.4509,0.431,0.4095,0.39,0.3772,0.345,0.3145,0.3113,0.2993,0.2873,0.2771,0.2668],
['um',0.3526,0.3421,0.3316,0.3209,0.3052,0.2939,0.2819,0.265,0.252,0.2361,0.2254,0.2152,0.2083,0.1999,0.1949,0.1885,0.1815,0.1755,0.1698,0.1643,0.1573,0.1505,0.1437,0.1413],
['uog',0.355,0.3445,0.3339,0.3231,0.3073,0.296,0.2839,0.2668,0.2538,0.2377,0.2269,0.2167,0.2097,0.2013,0.1962,0.1898,0.1827,0.1767,0.171,0.1655,0.1584,0.1515,0.1447,0.1422],
['uso',0.98,0.98,0.98,0.98,0.98,0.98,0.98,0.9008,0.875,0.8156,0.7946,0.7704,0.7325,0.7073,0.689,0.6702,0.6503,0.6271,0.5991,0.5735,0.5492,0.5242,0.4993,0.4743],
['us',0.6316,0.6112,0.5862,0.5622,0.5027,0.489,0.4788,0.471,0.4593,0.4344,0.4132,0.4081,0.403,0.3979,0.3928,0.3877,0.3826,0.3775,0.3724,0.3638,0.3463,0.3362,0.326,0.3158],
['wa',0.7917,0.7766,0.7465,0.7116,0.6575,0.6236,0.5932,0.5681,0.5184,0.4825,0.4579,0.4288,0.419,0.3913,0.3818,0.3721,0.3613,0.3517,0.3414,0.3311,0.3104,0.2856,0.2671,0.2242],
['wh',0.7917,0.7766,0.7465,0.7116,0.6575,0.6236,0.5932,0.5681,0.5184,0.4825,0.4579,0.4288,0.419,0.3913,0.3818,0.3721,0.3613,0.3517,0.3414,0.3311,0.3104,0.2856,0.2671,0.2242],
['zz',0.7602,0.7403,0.7065,0.6728,0.6369,0.6096,0.5653,0.5205,0.4793,0.4336,0.4086,0.3873,0.3587,0.3513,0.3357,0.3138,0.2921,0.2719,0.2667,0.2498,0.2362,0.2265,0.2168,0.2073],
],
columns=['K_Stars','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X']
)

iloc_kstars_dict = {
0:1,0.5:1,1:1,1.5:2,2:3,2.5:4,3:5,3.5:6,4:7,4.5:8,5:9,5.5:10,6:11,6.5:12,7:13,7.5:14,8:15,8.5:16,9:17,9.5:18,10:19,10.5:20,11:21,11.5:22,12:23,12.5:24,13:24,13.5:24,14:24,14.5:24,15:24,15.5:24,16:24,16.5:24,17:24,17.5:24,18:24
    }


roleid_pos_dict = {100:'keeper',101:'defender',102:'defender',103:'defender',104:'defender',105:'defender',106:'midfield',107:'midfield',108:'midfield',109:'midfield',110:'midfield',111:'forward',112:'forward',113:'forward'}

csvXHH='XHH.csv'
csvXCA='xca_new.csv'
csvHTM='MatchArchive16_HTM.csv'
cols_XCA =[
        'MatchID'	,'Competition',	'Season', 'MatchRound',	'LeagueName',
    'TeamID','TeamName','Mid','AttL','AttM','AttR','DefL','DefM','DefR',
        'TacticSkill','HatStats','HatXmid','HatAtt','HatDef'
    ]

cols_XCA_out = [
        'TeamName','Season','MatchRound','Competition','TacticSkill',
     'HatXmid','HatAtt','HatDef',
     'Mid','AttL','AttM','AttR','DefL','DefM','DefR','Match URL','Team URL','TeamID', 'LeagueName','Round_Filter'
     ]

cols_HTM =[
        'MatchID'   ,'Season', 'MatchRound',	'LeagueName','Match_OT_Pen','Goals','Opp_Goals',
    'TeamID','TeamName','Mid','AttL','AttM','AttR','DefL','DefM','DefR',
##    'RatingLeftAtt','RatingLeftDef','RatingMidAtt','RatingMidDef','RatingMidfield','RatingRightAtt','RatingRightDef',
        'TacticType','TacticSkill','HatStats','TacticType','HTScore','HTSN','UserName'
        ]
cols_HTM_out = [
        'TeamName','LeagueName','Season','MatchRound','HTScore','HTSN','HatStats',
##        'RatingLeftAtt','RatingLeftDef','RatingMidAtt','RatingMidDef','RatingMidfield','RatingRightAtt','RatingRightDef',
     'Mid','AttL','AttM','AttR','DefL','DefM','DefR',
        'Score','Len','Tactic','TacticSkill',
        'Match URL','Team URL','TeamID','Round_Filter'
     ]

cols_XHH =[
        'MatchID'	,'Competition',	'Season', 'MatchRound',	'LeagueName',
    'TeamID','TeamName','Mid','AttL','AttM','AttR','DefL','DefM','DefR',
        'TacticType','TacticSkill','HatStats','TacticType'
    ]

cols_XHH_out = [
        'TeamName','Season','MatchRound','Competition','HatStats',
     'Mid','AttL','AttM','AttR','DefL','DefM','DefR','Tactic','TacticSkill','Match URL','Team URL','TeamID', 'LeagueName','Round_Filter'
     ]

hts_def = {
9001:0.3088,9002:0.3212,9003:0.334,9004:0.3474,9005:0.3613,9006:0.3757,9007:0.3907,9008:0.4063,9009:0.4225,9010:0.4394,9011:0.4548,9012:0.4707,9013:0.4872,9014:0.5043,9015:0.5219,9016:0.5402,9017:0.5591,9018:0.5787,9019:0.599,9020:0.62,9021:0.64,9022:0.66,9023:0.68,9024:0.7,9025:0.72,9026:0.74,9027:0.76,9028:0.78,9029:0.8,9030:0.82,9031:0.84,9032:0.86,9033:0.88,9034:0.9,9035:0.92,9036:0.94,9037:0.96,9038:0.98,9039:1,9040:1.02,9041:1.04,9042:1.06,9043:1.08,9044:1.1,9045:1.12,9046:1.14,9047:1.16,9048:1.18,9049:1.2,9050:1.212,9051:1.224,9052:1.236,9053:1.248,9054:1.26,9055:1.272,9056:1.284,9057:1.296,9058:1.308,9059:1.32,9060:1.332,9061:1.344,9062:1.356,9063:1.368,9064:1.38,9065:1.392,9066:1.404,9067:1.416,9068:1.428,9069:1.44,9070:1.452,9071:1.464,9072:1.476,9073:1.488,9074:1.5,9075:1.512,9076:1.524,9077:1.536,9078:1.548,9079:1.56,9080:1.5709,9081:1.5819,9082:1.593,9083:1.6042,9084:1.6154,9085:1.6267,9086:1.6381,9087:1.6496,9088:1.6611,9089:1.6727,9090:1.6827,9091:1.6928,9092:1.703,9093:1.7132,9094:1.7235,9095:1.7338,9096:1.7442,9097:1.7547,9098:1.7652,9099:1.7758,9100:1.7847,9101:1.7936,9102:1.8026,9103:1.8116,9104:1.8207,9105:1.8298,9106:1.8389,9107:1.8481,9108:1.8573,9109:1.8666,9110:1.8759,9111:1.8853,9112:1.8947,9113:1.9042,9114:1.9137,9115:1.9233,9116:1.9329,9117:1.9426,9118:1.9523,9119:1.9621,9120:1.9719,9121:1.9818,9122:1.9917,9123:2.0017,9124:2.0117,9125:2.0167,9126:2.0217,9127:2.0268,9128:2.0319,9129:2.037,9130:2.0421,9131:2.0472,9132:2.0523,9133:2.0574,9134:2.0625,9135:2.0677,9136:2.0729,9137:2.0781,9138:2.0833,9139:2.0885,9140:2.0937,9141:2.0989,9142:2.1041,9143:2.1094,9144:2.1147,9145:2.1168,9146:2.1189,9147:2.121,9148:2.1231,9149:2.1252,9150:2.1273,9151:2.1294,9152:2.1315,9153:2.1336,9154:2.1357,9155:2.1378,9156:2.1399,9157:2.142,9158:2.1441,9159:2.1462,9160:2.1483,2001:0.2736,2002:0.2845,2003:0.2959,2004:0.3077,2005:0.32,2006:0.3328,2007:0.3461,2008:0.3599,2009:0.3743,2010:0.3893,2011:0.4029,2012:0.417,2013:0.4316,2014:0.4467,2015:0.4623,2016:0.4785,2017:0.4952,2018:0.5125,2019:0.5304,2020:0.549,2021:0.5655,2022:0.5825,2023:0.6,2024:0.618,2025:0.6365,2026:0.6556,2027:0.6753,2028:0.6956,2029:0.7165,2030:0.738,2031:0.7565,2032:0.7754,2033:0.7948,2034:0.8147,2035:0.8351,2036:0.856,2037:0.8774,2038:0.8993,2039:0.9218,2040:0.9448,2041:0.9684,2042:0.9926,2043:1.0174,2044:1.0428,2045:1.0689,2046:1.0956,2047:1.123,2048:1.1511,2049:1.1799,2050:1.2094,2051:1.2396,2052:1.2706,2053:1.3024,2054:1.335,2055:1.3684,2056:1.4026,2057:1.4377,2058:1.4736,2059:1.5104,2060:1.5482,2061:1.5869,2062:1.6266,2063:1.6673,2064:1.709,2065:1.7517,2066:1.7955,2067:1.8404,2068:1.8864,2069:1.9336,2070:1.9626,2071:1.992,2072:2.0219,2073:2.0522,2074:2.083,2075:2.1142,2076:2.1459,2077:2.1781,2078:2.2108,2079:2.244,2080:2.2777,2081:2.2891,2082:2.3005,2083:2.312,2084:2.3236,2085:2.3352,2086:2.3469,2087:2.3586,2088:2.3704,2089:2.3823,2090:2.3942,2091:2.4062,2092:2.4182,2093:2.4303,2094:2.4425,2095:2.4547,2096:2.467,2097:2.4793,2098:2.4917,2099:2.5042,2100:2.5167,2101:2.5293,2102:2.5419,2103:2.5546,2104:2.5674,2105:2.5802,2106:2.5931,2107:2.6061,2108:2.6191,2109:2.6322,2110:2.6454,2111:2.6586,2112:2.6719,2113:2.6853,2114:2.6987,2115:2.7122,2116:2.7258,2117:2.7394,2118:2.7531,2119:2.7669,2120:2.7807,2121:2.7946,2122:2.8086,2123:2.8226,2124:2.8367,2125:2.8438,2126:2.8509,2127:2.858,2128:2.8651,2129:2.8723,2130:2.8795,2131:2.8867,2132:2.8939,2133:2.9011,2134:2.9084,2135:2.9157,2136:2.923,2137:2.9303,2138:2.9376,2139:2.9449,2140:2.9523,2141:2.9597,2142:2.9671,2143:2.9745,2144:2.9819,2145:2.9849,2146:2.9879,2147:2.9909,2148:2.9939,2149:2.9969,2150:2.9999,2151:3.0029,2152:3.0059,2153:3.0089,2154:3.0119,2155:3.0149,2156:3.0179,2157:3.0209,2158:3.0239,2159:3.0269,2160:3.0299,8002:0.1909,8003:0.2024,8004:0.2145,8005:0.2274,8006:0.241,8007:0.2555,8008:0.2708,8009:0.2871,8010:0.3043,8011:0.3226,8012:0.342,8013:0.3625,8014:0.3842,8015:0.4072,8016:0.4316,8017:0.4575,8018:0.4849,8019:0.514,8020:0.5448,8021:0.5775,8022:0.6064,8023:0.6367,8024:0.6685,8025:0.702,8026:0.7371,8027:0.7739,8028:0.8126,8029:0.8532,8030:0.8959,8031:0.9317,8032:0.969,8033:1.0078,8034:1.0481,8035:1.09,8036:1.1336,8037:1.1789,8038:1.2261,8039:1.2751,8040:1.3261,8041:1.3593,8042:1.3933,8043:1.4281,8044:1.4638,8045:1.5004,8046:1.5379,8047:1.5764,8048:1.6158,8049:1.6562,8050:1.6976,8051:1.7162,8052:1.7351,8053:1.7542,8054:1.7735,8055:1.793,8056:1.8127,8057:1.8327,8058:1.8528,8059:1.8732,8060:1.8938,8061:1.9147,8062:1.9357,8063:1.957,8064:1.9785,8065:2.0003,8066:2.0223,8067:2.0445,8068:2.067,8069:2.0898,8070:2.1128,8071:2.1339,8072:2.1552,8073:2.1768,8074:2.1985,8075:2.2205,8076:2.2427,8077:2.2652,8078:2.2878,8079:2.3107,8080:2.3338,8081:2.3513,8082:2.3689,8083:2.3867,8084:2.4046,8085:2.4226,8086:2.4408,8087:2.4591,8088:2.4776,8089:2.4961,8090:2.5149,8091:2.5337,8092:2.5527,8093:2.5719,8094:2.5912,8095:2.6106,8096:2.6302,8097:2.6499,8098:2.6698,8099:2.6898,8100:2.7032,8101:2.7168,8102:2.7303,8103:2.744,8104:2.7577,8105:2.7715,8106:2.7854,8107:2.7993,8108:2.8133,8109:2.8274,8110:2.8415,8111:2.8557,8112:2.87,8113:2.8843,8114:2.8987,8115:2.9132,8116:2.9278,8117:2.9424,8118:2.9572,8119:2.9719,8120:2.9868,8121:3.0017,8122:3.0167,8123:3.0318,8124:3.0394,8125:3.047,8126:3.0546,8127:3.0623,8128:3.0699,8129:3.0776,8130:3.0853,8131:3.093,8132:3.1007,8133:3.1085,8134:3.1163,8135:3.124,8136:3.1319,8137:3.1397,8138:3.1475,8139:3.1554,8140:3.1633,8141:3.1712,8142:3.1791,8143:3.1871,8144:3.1903,8145:3.1935,8146:3.1966,8147:3.1998,8148:3.203,8149:3.2062,8150:3.2095,8151:3.2127,8152:3.2159,8153:3.2191,8154:3.2223,8155:3.2255,8156:3.2288,8157:3.232,8158:3.2352,8159:3.2385,8160:3.2417
}

hts_att = {
9001:0.4149,9002:0.4294,9003:0.4444,9004:0.46,9005:0.4761,9006:0.4928,9007:0.51,9008:0.5279,9009:0.5464,9010:0.5655,9011:0.5825,9012:0.6,9013:0.618,9014:0.6365,9015:0.6556,9016:0.6753,9017:0.6956,9018:0.7165,9019:0.738,9020:0.7601,9021:0.7829,9022:0.8025,9023:0.8225,9024:0.8431,9025:0.8621,9026:0.8815,9027:0.9013,9028:0.9216,9029:0.9423,9030:0.9612,9031:0.9804,9032:1,9033:1.02,9034:1.0404,9035:1.056,9036:1.0718,9037:1.0879,9038:1.1042,9039:1.1208,9040:1.1331,9041:1.1456,9042:1.1582,9043:1.1709,9044:1.1838,9045:1.1968,9046:1.21,9047:1.2233,9048:1.2368,9049:1.2504,9050:1.2641,9051:1.278,9052:1.2921,9053:1.3063,9054:1.3207,9055:1.3352,9056:1.3499,9057:1.3647,9058:1.3798,9059:1.3949,9060:1.4103,9061:1.4258,9062:1.4415,9063:1.4573,9064:1.4734,9065:1.4896,9066:1.506,9067:1.5225,9068:1.5393,9069:1.5562,9070:1.5718,9071:1.5875,9072:1.6034,9073:1.6194,9074:1.6356,9075:1.6519,9076:1.6685,9077:1.6851,9078:1.702,9079:1.719,9080:1.7319,9081:1.7449,9082:1.758,9083:1.7712,9084:1.7844,9085:1.7978,9086:1.8113,9087:1.8249,9088:1.8386,9089:1.8524,9090:1.8663,9091:1.8803,9092:1.8944,9093:1.9086,9094:1.9229,9095:1.9373,9096:1.9518,9097:1.9665,9098:1.9812,9099:1.9961,2001:0.5374,2002:0.5562,2003:0.5757,2004:0.5958,2005:0.6167,2006:0.6383,2007:0.6606,2008:0.6837,2009:0.7076,2010:0.7324,2011:0.7544,2012:0.777,2013:0.8003,2014:0.8243,2015:0.849,2016:0.8745,2017:0.9007,2018:0.9277,2019:0.9555,2020:0.9842,2021:1.0137,2022:1.039,2023:1.065,2024:1.0916,2025:1.1189,2026:1.1469,2027:1.1755,2028:1.2049,2029:1.235,2030:1.2659,2031:1.2976,2032:1.33,2033:1.35,2034:1.3702,2035:1.3908,2036:1.4116,2037:1.4328,2038:1.4543,2039:1.4761,2040:1.4945,2041:1.5132,2042:1.5321,2043:1.5513,2044:1.5707,2045:1.5903,2046:1.6102,2047:1.6303,2048:1.6507,2049:1.6713,2050:1.6881,2051:1.7049,2052:1.722,2053:1.7392,2054:1.7566,2055:1.7742,2056:1.7919,2057:1.8098,2058:1.8279,2059:1.8462,2060:1.8647,2061:1.8833,2062:1.9021,2063:1.9211,2064:1.9403,2065:1.9597,2066:1.9793,2067:1.9991,2068:2.0191,2069:2.0393,2070:2.0597,2071:2.0803,2072:2.1011,2073:2.1221,2074:2.1433,2075:2.1647,2076:2.1863,2077:2.2082,2078:2.2303,2079:2.2526,2080:2.2695,2081:2.2865,2082:2.3036,2083:2.3209,2084:2.3383,2085:2.3558,2086:2.3735,2087:2.3913,2088:2.4092,2089:2.4273,2090:2.4455,2091:2.4638,2092:2.4823,2093:2.5009,2094:2.5197,2095:2.5386,2096:2.5576,2097:2.5768,2098:2.5961,2099:2.6156,8001:1,8002:1,8003:1,8004:1,8005:1,8006:1,8007:1,8008:1,8009:1,8010:1,8011:1,8012:1,8013:1,8014:1,8015:1.025,8016:1.05,8017:1.075,8018:1.1,8019:1.125,8020:1.15,8021:1.175,8022:1.2,8023:1.21,8024:1.22,8025:1.23,8026:1.24,8027:1.25,8028:1.26,8029:1.27,8030:1.28,8031:1.29,8032:1.3,8033:1.326,8034:1.3525,8035:1.3728,8036:1.3934,8037:1.4143,8038:1.4355,8039:1.457,8040:1.4731,8041:1.4893,8042:1.5057,8043:1.5222,8044:1.539,8045:1.5559,8046:1.573,8047:1.5903,8048:1.6078,8049:1.6255,8050:1.6434,8051:1.6615,8052:1.6797,8053:1.6982,8054:1.7169,8055:1.7358,8056:1.7549,8057:1.7742,8058:1.7937,8059:1.8134,8060:1.8334,8061:1.8535,8062:1.8739,8063:1.8945,8064:1.9154,8065:1.9364,8066:1.9577,8067:1.9793,8068:2.001,8069:2.0231,8070:2.0433,8071:2.0637,8072:2.0844,8073:2.1052,8074:2.1263,8075:2.1475,8076:2.169,8077:2.1907,8078:2.2126,8079:2.2347,8080:2.2515,8081:2.2684,8082:2.2854,8083:2.3025,8084:2.3198,8085:2.3372,8086:2.3547,8087:2.3724,8088:2.3902,8089:2.4081,8090:2.4262,8091:2.4443,8092:2.4627,8093:2.4812,8094:2.4998,8095:2.5185,8096:2.5374,8097:2.5564,8098:2.5756,8099:2.5949
}

hts_mid = {
9001:0.1056,9002:0.1162,9003:0.1278,9004:0.1406,9005:0.1547,9006:0.1702,9007:0.1872,9008:0.2059,9009:0.2265,9010:0.2492,9011:0.2741,9012:0.3015,9013:0.3316,9014:0.3648,9015:0.4013,9016:0.4414,9017:0.4855,9018:0.5341,9019:0.5875,9020:0.6463,9021:0.7061,9022:0.7662,9023:0.8255,9024:0.8833,9025:0.9434,9026:1,9027:1.057,9028:1.112,9029:1.1642,9030:1.2131,9031:1.258,9032:1.2983,9033:1.3385,9034:1.3787,9035:1.4186,9036:1.4584,9037:1.4977,9038:1.5367,9039:1.5751,9040:1.6145,9041:1.6548,9042:1.6962,9043:1.7386,9044:1.7821,9045:1.8266,9046:1.8723,9047:1.9191,9048:1.9623,9049:2.0064,9050:2.0466,9051:2.0875,9052:2.1293,9053:2.1718,9054:2.2153,9055:2.2596,9056:2.3048,9057:2.3509,9058:2.3979,9059:2.4458,9060:2.4886,9061:2.5322,9062:2.5765,9063:2.6216,9064:2.6675,9065:2.7142,9066:2.7617,9067:2.81,9068:2.8592,9069:2.9092,9070:2.9528,9071:2.9971,9072:3.0421,9073:3.0877,9074:3.134,9075:3.181,9076:3.2288,9077:3.2772,9078:3.3263,9079:3.3762,9080:3.4268,9081:3.4782,9082:3.5304,9083:3.5834,9084:3.6372,9085:3.6918,9086:3.7472,9087:3.8034,9088:3.8605,9089:3.9184,9090:3.9772,9091:4.0369,9092:4.0975,9093:4.159,9094:4.2214,9095:4.2847,9096:4.349,9097:4.4142,9098:4.4804,9099:4.5476,9100:4.6158,9101:4.685,9102:4.7553,9103:4.8266,9104:4.899,9105:4.9725,9106:5.0471,9107:5.1228,9108:5.1996,9109:5.2776,9110:5.3568,2001:0.2025,2002:0.2146,2003:0.2275,2004:0.2411,2005:0.2556,2006:0.2709,2007:0.2872,2008:0.3044,2009:0.3227,2010:0.3421,2011:0.3609,2012:0.3808,2013:0.4017,2014:0.4238,2015:0.4471,2016:0.4717,2017:0.4976,2018:0.525,2019:0.5539,2020:0.5844,2021:0.6165,2022:0.6473,2023:0.6765,2024:0.7035,2025:0.7282,2026:0.75,2027:0.7725,2028:0.7957,2029:0.8195,2030:0.8441,2031:0.8695,2032:0.8955,2033:0.9224,2034:0.9501,2035:0.9786,2036:1.003,2037:1.0231,2038:1.0385,2039:1.0488,2040:1.0593,2041:1.0699,2042:1.0806,2043:1.0914,2044:1.1023,2045:1.1134,2046:1.1245,2047:1.1357,2048:1.1471,2049:1.1586,2050:1.1702,2051:1.1819,2052:1.1937,2053:1.2056,2054:1.2177,2055:1.2299,2056:1.2422,2057:1.2546,2058:1.2671,2059:1.2798,2060:1.2926,2061:1.3055,2062:1.3186,2063:1.3318,2064:1.3451,2065:1.3586,2066:1.3722,2067:1.3859,2068:1.3998,2069:1.4138,2070:1.4279,8001:0.1055,8002:0.1139,8003:0.123,8004:0.1328,8005:0.1434,8006:0.1549,8007:0.1673,8008:0.1807,8009:0.1952,8010:0.2108,8011:0.2277,8012:0.2459,8013:0.2656,8014:0.2869,8015:0.3098,8016:0.3346,8017:0.3614,8018:0.3903,8019:0.4215,8020:0.4552,8021:0.4916,8022:0.5273,8023:0.5615,8024:0.5938,8025:0.6235,8026:0.65,8027:0.6728,8028:0.6929,8029:0.7137,8030:0.7351,8031:0.7572,8032:0.7799,8033:0.8033,8034:0.8274,8035:0.8522,8036:0.8778,8037:0.9041,8038:0.9312,8039:0.9592,8040:0.9808,8041:1.0028,8042:1.0254,8043:1.0485,8044:1.0721,8045:1.0962,8046:1.1208,8047:1.1461,8048:1.1718,8049:1.1982,8050:1.2252,8051:1.2527,8052:1.2809,8053:1.3097,8054:1.3392,8055:1.3693,8056:1.4002,8057:1.4317,8058:1.4639,8059:1.4968,8060:1.5118,8061:1.5269,8062:1.5422,8063:1.5576,8064:1.5732,8065:1.5889,8066:1.6048,8067:1.6208,8068:1.637,8069:1.6534,8070:1.6699,8071:1.6866,8072:1.7035,8073:1.7205,8074:1.7377,8075:1.7551,8076:1.7727,8077:1.7904,8078:1.8083,8079:1.8264,8080:1.8447,8081:1.8631,8082:1.8817,8083:1.9005,8084:1.9195,8085:1.9387,8086:1.9581,8087:1.9777,8088:1.9975,8089:2.0175,8090:2.0377,8091:2.0581,8092:2.0787,8093:2.0995,8094:2.1205,8095:2.1417,8096:2.1631,8097:2.1847,8098:2.2065,8099:2.2286,8100:2.2509,8101:2.2734,8102:2.2961,8103:2.3191,8104:2.3423,8105:2.3657,8106:2.3894,8107:2.4133,8108:2.4374,8109:2.4618,8110:2.4864,3001:0.36,3002:0.38,3003:0.4,3004:0.42,3005:0.44,3006:0.46,3007:0.48,3008:0.5,3009:0.52,3010:0.54,3011:0.56,3012:0.58,3013:0.6,3014:0.62,3015:0.64,3016:0.66,3017:0.68,3018:0.7,3019:0.72,3020:0.74,3021:0.76,3022:0.78,3023:0.8,3024:0.82,3025:0.84,3026:0.86,3027:0.88,3028:0.9,3029:0.92,3030:0.94,3031:0.96,3032:0.98,3033:1,3034:1.02,3035:1.04,3036:1.06,3037:1.0794,3038:1.0935,3039:1.1023,3040:1.1123,3041:1.118,3042:1.1238,3043:1.1296,3044:1.1354,3045:1.1412,3046:1.147,3047:1.1527,3048:1.1586,3049:1.1644,3050:1.1702,3051:1.1819,3052:1.1937,3053:1.2056,3054:1.2177,3055:1.2299,3056:1.2422,3057:1.2546,3058:1.2671,3059:1.2798,3060:1.2926,3061:1.3055,3062:1.3186,3063:1.3318,3064:1.3451,3065:1.3586,3066:1.3722,3067:1.3859,3068:1.3998,3069:1.4138,3070:1.4279
}

hts_ls = {
    8001:0.6433,8002:0.6626,8003:0.6825,8004:0.7029,8005:0.724,8006:0.7458,8007:0.7681,8008:0.7912,8009:0.8149,8010:0.8385,8011:0.8616,8012:0.8847,8013:0.9078,8014:0.9309,8015:0.9539,8016:0.977,8017:1.0001,8018:1.0232,8019:1.0462,8020:1.0693,8021:1.0924,8022:1.1155,8023:1.1386,8024:1.1616,8025:1.1847,8026:1.2078,8027:1.2309,8028:1.254,8029:1.277,8030:1.3001
}