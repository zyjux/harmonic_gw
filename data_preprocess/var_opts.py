"""
===========================================
Gravity Waves Parameters
===========================================
"""

TC20170719 = {
    'caseLat': 14,
    'caseLon': -121,
    'filePrefix': 'TC/201707/GDNBO-SVDNB_npp_',
    'fileSuffix': '_noac_ops.h5',
    'fileList':
    ['d20170719_t0916454_e0918096_b29666_c20220118195134555715',
     'd20170719_t0918108_e0919350_b29666_c20220118195134555715'],
    'fileListStorm':
    ['d20170719_t1056184_e1057426_b29667_c20220118195338307107',
     'd20170719_t1057438_e1059080_b29667_c20220118195338307107',
     'd20170719_t1059092_e1100334_b29667_c20220118195338307107']}

TC20171016 = {
    'caseLat': 23,
    'caseLon': -69,
    'filePrefix': 'TC/201710/GDNBO-SVDNB_npp_',
    'fileSuffix': '_nobc_ops.h5',
    'fileList':
    ['d20171016_t0619049_e0624453_b30927_c20220118194618899804',
     'd20171016_t0624466_e0630252_b30927_c20220118194615235230'],
    'imLocLatStart': 2400,
    'imLocLatStop': 3800,
    'imLocLonStart': 1200,
    'imLocLonStop': 2300,
    'xRefList': [1246],
    'yRefList': [2488]}

TC201807 = {
    'caseLat': 39,
    'caseLon': -66,
    'filePrefix': 'TC/201807/GDNBO-SVDNB_npp_',
    'fileSuffix': '_noac_ops.h5',
    'fileList':
    ['d20180711_t0553263_e0554505_b34729_c20220118200228744535',
     'd20180711_t0554518_e0556159_b34729_c20220118200250204856',
     'd20180711_t0556172_e0557413_b34729_c20220118200250204856']}

TC201807j = {
    'caseLat': 39,
    'caseLon': -66,
    'filePrefix': '/TC/201807/GDNBO-SVDNB_j01_',
    'fileSuffix': '_noac_ops.h5',
    'fileList':
    ['j01_d20180711_t0641492_e0643138_b03333_c20220118200127645306',
     'j01_d20180711_t0643150_e0644377_b03333_c20220118200127645306',
     'j01_d20180711_t0644390_e0646035_b03333_c20220118200127645306',
     'j01_d20180711_t0646047_e0647292_b03333_c20220118200206197883']}

TC20181010 = {
    'caseLat': 28,
    'caseLon': -86,
    'filePrefix': 'TC/201810/GDNBO-SVDNB_npp_',
    'fileSuffix': '_noac_opts.h5',
    'fileList':
        ['d20181010_t0732173_e0733415_b36021_c20220118200327774728',
         'd20181010_t0733427_e0735069_b36021_c20220118200327774728']}

TC20181010je = {
    'caseLat': 28,
    'caseLon': -86,
    'filePrefix': 'TC/201810/GDNBO-SVDNB_j01_',
    'fileSuffix': '_noac_opts.h5',
    'fileList':
    ['j01_d20181010_t0641060_e0642305_b04624_c20220118195630621950',
     'j01_d20181010_t0642317_e0643545_b04624_c20220118195630621950']}

TC20181010jw = {
    'caseLat': 28,
    'caseLon': -86,
    'filePrefix': 'TC/201810/GDNBO-SVDNB_j01_',
    'fileSuffix': '_noac_opts.h5',
    'fileList':
    ['j01_d20181010_t0820403_e0822048_b04625_c20220118200333725852',
     'j01_d20181010_t0822061_e0823288_b04625_c20220118200333725852']}

bore20180114 = {
    'filePrefix': 'Bore/201801/GDNBO-SVDNB_npp_',
    'fileSuffix': '_nobc_ops.h5',
    'fileList':
    [
        # 'd20180114_t0500332_e0501573_b32203_c20220322202437972466',
        'd20180114_t0501586_e0503228_b32203_c20220322202437972466',
        'd20180114_t0503240_e0504482_b32203_c20220322202437972466',
        'd20180114_t0504494_e0506118_b32203_c20220322202437972466'
    ],
    'imLocLatStart': 1350,
    'imLocLatStop': 3100,
    'imLocLonStart': 2650,
    'imLocLonStop': 3600,
    'xRefList': [],
    'yRefList': [],
    'gravityWavesPresent': True
}

bore20180211_01 = {
    'filePrefix': 'Bore/201802/GDNBO-SVDNB_j01_',
    'fileSuffix': '_noac_ops.h5',
    'fileList':
    [
        'd20180211_t0837310_e0838555_b01206_c20220322193857300143',
        'd20180211_t0838568_e0840213_b01206_c20220322193857300143',
        'd20180211_t0840225_e0841471_b01206_c20220322193857300143',
    ],
    'imLocLatStart': 0,
    'imLocLatStop': -1,
    'imLocLonStart': 0,
    'imLocLonStop': -1,
    'xRefList': [],
    'yRefList': [],
    'gravityWavesPresent': False
}

bore20180211_02 = {
    'filePrefix': 'Bore/201802/GDNBO-SVDNB_j01_',
    'fileSuffix': '_noac_ops.h5',
    'fileList':
    [
        'd20180211_t1018311_e1019556_b01207_c20220322193903021563',
        'd20180211_t1019569_e1021214_b01207_c20220322193903021563',
        'd20180211_t1021226_e1022454_b01207_c20220322193903021563',
    ],
    'imLocLatStart': 1250,
    'imLocLatStop': 2300,
    'imLocLonStart': 1200,
    'imLocLonStop': 2000,
    'xRefList': [],
    'yRefList': [],
    'gravityWavesPresent': True
}

bore20180211_03 = {
    'filePrefix': 'Bore/201802/GDNBO-SVDNB_npp_',
    'fileSuffix': '_noac_ops.h5',
    'fileList':
    [
        'd20180211_t0927194_e0928436_b32603_c20220322194738470239',
        'd20180211_t0928449_e0930090_b32603_c20220322194738470239',
        'd20180211_t0930103_e0931327_b32603_c20220322194738470239',
    ],
    'imLocLatStart': 0,
    'imLocLatStop': -1,
    'imLocLonStart': 0,
    'imLocLonStop': -1,
    'xRefList': [],
    'yRefList': [],
    'gravityWavesPresent': False
}

bore20180320_01 = {
    'filePrefix': 'Bore/201803/GDNBO-SVDNB_j01_',
    'fileSuffix': '_nobc_ops.h5',
    'fileList':
    [
        'd20180320_t0349546_e0351192_b01728_c20220323155349103920',
        'd20180320_t0351204_e0352449_b01728_c20220323155349103920',
        'd20180320_t0352461_e0354107_b01728_c20220323155349294253',
    ],
    'imLocLatStart': 0,
    'imLocLatStop': -1,
    'imLocLonStart': 0,
    'imLocLonStop': -1,
    'xRefList': [],
    'yRefList': [],
    'gravityWavesPresent': False
}

bore20180320_02 = {
    'filePrefix': 'Bore/201803/GDNBO-SVDNB_npp_',
    'fileSuffix': '_nobc_ops.h5',
    'fileList':
    [
        'd20180320_t0439419_e0441060_b33125_c20220323155350079415',
        'd20180320_t0441073_e0442314_b33125_c20220323155350079415',
        'd20180320_t0442327_e0443568_b33125_c20220323155350079415',
    ],
    'imLocLatStart': 850,
    'imLocLatStop': 2200,
    'imLocLonStart': 250,
    'imLocLonStop': 2900,
    'xRefList': [],
    'yRefList': [],
    'gravityWavesPresent': True
}

bore20180320_03 = {
    'filePrefix': 'Bore/201803/GDNBO-SVDNB_j01_',
    'fileSuffix': '_nobc_ops.h5',
    'fileList':
    [
        # 'd20180320_t0529290_e0530535_b01729_c20220323155327214546',
        'd20180320_t0530547_e0532193_b01729_c20220323155327214546',
        'd20180320_t0532205_e0533450_b01729_c20220323155327214546',
        'd20180320_t0533463_e0535090_b01729_c20220323155327214546',
    ],
    'imLocLatStart': 1300,
    'imLocLatStop': 2900,
    'imLocLonStart': 1500,
    'imLocLonStop': 4050,
    'xRefList': [],
    'yRefList': [],
    'gravityWavesPresent': True
}

bore20180414_01 = {
    'filePrefix': 'Bore/201804/GDNBO-SVDNB_j01_',
    'fileSuffix': '_nobc_ops.h5',
    'fileList':
    [
        'd20180414_t0731018_e0732263_b02085_c20220322194826923628',
        'd20180414_t0732275_e0733520_b02085_c20220322194826923628',
        'd20180414_t0733533_e0735160_b02085_c20220322194826923628',
    ],
    'imLocLatStart': 400,
    'imLocLatStop': 2300,
    'imLocLonStart': 0,
    'imLocLonStop': 3300,
    'xRefList': [],
    'yRefList': [],
    'gravityWavesPresent': True
}

bore20180414_02 = {
    'filePrefix': 'Bore/201804/GDNBO-SVDNB_npp_',
    'fileSuffix': '_nobc_ops.h5',
    'fileList':
    [
        'd20180414_t0639498_e0641140_b33481_c20220322194827442381',
        'd20180414_t0641152_e0642394_b33481_c20220322194827442381',
        'd20180414_t0642406_e0644048_b33481_c20220322194827442381',
    ],
    'imLocLatStart': 650,
    'imLocLatStop': 1500,
    'imLocLonStart': 1000,
    'imLocLonStop': 2850,
    'xRefList': [],
    'yRefList': [],
    'gravityWavesPresent': True
}

bore20180414_03 = {
    'filePrefix': 'Bore/201804/GDNBO-SVDNB_npp_',
    'fileSuffix': '_nobc_ops.h5',
    'fileList':
    [
        'd20180414_t0820500_e0822142_b33482_c20220322194830950496',
        'd20180414_t0822154_e0823396_b33482_c20220322194830950496',
        'd20180414_t0823408_e0825032_b33482_c20220322194830950496',
    ],
    'imLocLatStart': 1000,
    'imLocLatStop': 1750,
    'imLocLonStart': 2450,
    'imLocLonStop': 3550,
    'xRefList': [],
    'yRefList': [],
    'gravityWavesPresent': True
}

bore20180415_01 = {
    'filePrefix': 'Bore/201804/GDNBO-SVDNB_j01_',
    'fileSuffix': '_nobc_ops.h5',
    'fileList':
    [
        'd20180415_t0417086_e0418332_b02097_c20220323155448395719',
        'd20180415_t0418344_e0419589_b02097_c20220323155448395719',
        'd20180415_t0420002_e0421229_b02097_c20220323155448395719',
    ],
    'imLocLatStart': 0,
    'imLocLatStop': -1,
    'imLocLonStart': 0,
    'imLocLonStop': -1,
    'xRefList': [],
    'yRefList': [],
    'gravityWavesPresent': False
}

bore20180415_02 = {
    'filePrefix': 'Bore/201804/GDNBO-SVDNB_npp_',
    'fileSuffix': '_nobc_ops.h5',
    'fileList':
    [
        'd20180415_t0506567_e0508208_b33494_c20220323155444718507',
        'd20180415_t0508221_e0509445_b33494_c20220323155444718507',
        'd20180415_t0509457_e0511099_b33494_c20220323155444718507',
    ],
    'imLocLatStart': 1200,
    'imLocLatStop': 1700,
    'imLocLonStart': 1500,
    'imLocLonStop': 2550,
    'xRefList': [],
    'yRefList': [],
    'gravityWavesPresent': True
}

bore20180415_03 = {
    'filePrefix': 'Bore/201804/GDNBO-SVDNB_j01_',
    'fileSuffix': '_nobc_ops.h5',
    'fileList':
    [
        'd20180415_t0558087_e0559333_b02098_c20220323155448433901',
        'd20180415_t0559345_e0600572_b02098_c20220323155448433901',
    ],
    'imLocLatStart': 300,
    'imLocLatStop': 800,
    'imLocLonStart': 2800,
    'imLocLonStop': 4000,
    'xRefList': [],
    'yRefList': [],
    'gravityWavesPresent': True
}

bore20180422_01 = {
    'filePrefix': 'Bore/201804/GDNBO-SVDNB_npp_',
    'fileSuffix': '_nobc_ops.h5',
    'fileList':
    [
        'd20180422_t1438359_e1440000_b33599_c20220323163249527483',
        'd20180422_t1440013_e1441254_b33599_c20220323163249527483',
        'd20180422_t1441267_e1442508_b33599_c20220323163249527483',
    ],
    'imLocLatStart': 1000,
    'imLocLatStop': 1450,
    'imLocLonStart': 850,
    'imLocLonStop': 1600,
    'xRefList': [],
    'yRefList': [],
    'gravityWavesPresent': True
}

bore20180422_02 = {
    'filePrefix': 'Bore/201804/GDNBO-SVDNB_j01_',
    'fileSuffix': '_nobc_ops.h5',
    'fileList':
    [
        'd20180422_t1528245_e1529472_b02203_c20220323163315159601',
        'd20180422_t1529485_e1531130_b02203_c20220323163314502898',
        'd20180422_t1531142_e1532388_b02203_c20220323163314502898',
    ],
    'imLocLatStart': 1000,
    'imLocLatStop': 1350,
    'imLocLonStart': 3200,
    'imLocLonStop': 4050,
    'xRefList': [],
    'yRefList': [],
    'gravityWavesPresent': True
}

bore20180513_01 = {
    'filePrefix': 'Bore/201805/GDNBO-SVDNB_npp_',
    'fileSuffix': '_noac_ops.h5',
    'fileList':
    [
        'd20180513_t1626134_e1627376_b33898_c20220323163047573562',
        'd20180513_t1627388_e1629030_b33898_c20220323163047573562',
        'd20180513_t1629042_e1630284_b33898_c20220323163147895032',
    ],
    'imLocLatStart': 600,
    'imLocLatStop': 1450,
    'imLocLonStart': 1050,
    'imLocLonStop': 2550,
    'xRefList': [],
    'yRefList': [],
    'gravityWavesPresent': True
}

bore20180513_02 = {
    'filePrefix': 'Bore/201805/GDNBO-SVDNB_j01_',
    'fileSuffix': '_noac_ops.h5',
    'fileList':
    [
        'd20180513_t1716002_e1717247_b02502_c20220323163117560110',
        'd20180513_t1717260_e1718505_b02502_c20220323163117560110',
        'd20180513_t1718517_e1720162_b02502_c20220323163117560110',
    ],
    'imLocLatStart': 800,
    'imLocLatStop': 1950,
    'imLocLonStart': 1650,
    'imLocLonStop': 3500,
    'xRefList': [],
    'yRefList': [],
    'gravityWavesPresent': True
}

bore20180519_01 = {
    'filePrefix': 'Bore/201805/GDNBO-SVDNB_npp_',
    'fileSuffix': '_noac_ops.h5',
    'fileList':
    [
        'd20180519_t0425165_e0426407_b33976_c20220323162433567303',
        'd20180519_t0426419_e0428061_b33976_c20220323162433567303',
        'd20180519_t0428074_e0429315_b33976_c20220323162433567303',
    ],
    'imLocLatStart': 0,
    'imLocLatStop': -1,
    'imLocLonStart': 0,
    'imLocLonStop': -1,
    'xRefList': [],
    'yRefList': [],
    'gravityWavesPresent': True
}

bore20180519_02 = {
    'filePrefix': 'Bore/201805/GDNBO-SVDNB_j01_',
    'fileSuffix': '_noac_ops.h5',
    'fileList':
    [
        'd20180519_t0515049_e0516276_b02580_c20220323162448588205',
        'd20180519_t0516288_e0517534_b02580_c20220323162448588205',
        'd20180519_t0517546_e0519191_b02580_c20220323162448588205',
    ],
    'imLocLatStart': 0,
    'imLocLatStop': -1,
    'imLocLonStart': 0,
    'imLocLonStop': -1,
    'xRefList': [],
    'yRefList': [],
    'gravityWavesPresent': True
}

bore20180519_03 = {
    'filePrefix': 'Bore/201805/GDNBO-SVDNB_npp_',
    'fileSuffix': '_noac_ops.h5',
    'fileList':
    [
        'd20180519_t0606167_e0607409_b33977_c20220323162448809711',
        'd20180519_t0607421_e0609063_b33977_c20220323162448809711',
        'd20180519_t0609075_e0610317_b33977_c20220323162448809711',
    ],
    'imLocLatStart': 0,
    'imLocLatStop': -1,
    'imLocLonStart': 0,
    'imLocLonStop': -1,
    'xRefList': [],
    'yRefList': [],
    'gravityWavesPresent': True
}

bore20180715 = {
    'filePrefix': 'Bore/201807/GDNBO-SVDNB_npp_',
    'fileSuffix': '_noac_ops.h5',
    'fileList':
    [
        'd20180715_t0313502_e0315143_b34784_c20220323162715347437',
        'd20180715_t0315156_e0316397_b34784_c20220323162715347437',
        'd20180715_t0316410_e0318051_b34784_c20220323162715347437',
    ],
    'imLocLatStart': 0,
    'imLocLatStop': -1,
    'imLocLonStart': 0,
    'imLocLonStop': -1,
    'xRefList': [],
    'yRefList': [],
    'gravityWavesPresent': True
}

bore20180808_01 = {
    'filePrefix': 'Bore/201808/GDNBO-SVDNB_j01_',
    'fileSuffix': '_nobc_ops.h5',
    'fileList':
    [
        'd20180808_t0625303_e0626548_b03730_c20220322201448234397',
        'd20180808_t0626561_e0628206_b03730_c20220322201448234397',
        'd20180808_t0628218_e0629446_b03730_c20220322201503088156',
    ],
    'imLocLatStart': 0,
    'imLocLatStop': -1,
    'imLocLonStart': 0,
    'imLocLonStop': -1,
    'xRefList': [],
    'yRefList': [],
    'gravityWavesPresent': True
}

bore20180808_02 = {
    'filePrefix': 'Bore/201808/GDNBO-SVDNB_npp_',
    'fileSuffix': '_nobc_ops.h5',
    'fileList':
    [
        'd20180808_t0716432_e0718074_b35127_c20220322201508051034',
        'd20180808_t0718086_e0719328_b35127_c20220322201508051034',
        'd20180808_t0719340_e0720582_b35127_c20220322201433922781',
    ],
    'imLocLatStart': 0,
    'imLocLatStop': -1,
    'imLocLonStart': 0,
    'imLocLonStop': -1,
    'xRefList': [],
    'yRefList': [],
    'gravityWavesPresent': True
}

bore20180813_01 = {
    'filePrefix': 'Bore/201808/GDNBO-SVDNB_j01_',
    'fileSuffix': '_nobc_ops.h5',
    'fileList':
    [
        'd20180813_t0623221_e0624448_b03801_c20220322201506597288',
        'd20180813_t0624460_e0626106_b03801_c20220322201506597288',
        'd20180813_t0626118_e0627363_b03801_c20220322201509310652',
    ],
    'imLocLatStart': 0,
    'imLocLatStop': -1,
    'imLocLonStart': 0,
    'imLocLonStop': -1,
    'xRefList': [],
    'yRefList': [],
    'gravityWavesPresent': True
}

bore20180813_02 = {
    'filePrefix': 'Bore/201808/GDNBO-SVDNB_npp_',
    'fileSuffix': '_nobc_ops.h5',
    'fileList':
    [
        'd20180813_t0533343_e0534584_b35197_c20220322201510377833',
        'd20180813_t0534597_e0536238_b35197_c20220322201513821242',
        'd20180813_t0536251_e0537492_b35197_c20220322201513821242',
    ],
    'imLocLatStart': 0,
    'imLocLatStop': -1,
    'imLocLonStart': 0,
    'imLocLonStop': -1,
    'xRefList': [],
    'yRefList': [],
    'gravityWavesPresent': True
}

bore20180813_03 = {
    'filePrefix': 'Bore/201808/GDNBO-SVDNB_npp_',
    'fileSuffix': '_nobc_ops.h5',
    'fileList':
    [
        'd20180813_t0713090_e0714332_b35198_c20220322201514420703',
        'd20180813_t0714345_e0715586_b35198_c20220322201514420703',
        'd20180813_t0715599_e0717240_b35198_c20220322201514420703',
    ],
    'imLocLatStart': 0,
    'imLocLatStop': -1,
    'imLocLonStart': 0,
    'imLocLonStop': -1,
    'xRefList': [],
    'yRefList': [],
    'gravityWavesPresent': True
}

bore20180815_01 = {
    'filePrefix': 'Bore/201808/GDNBO-SVDNB_j01_',
    'fileSuffix': '_nobc_ops.h5',
    'fileList':
    [
        'd20180815_t0555286_e0556531_b03829_c20220323162548806400',
        'd20180815_t0556543_e0558171_b03829_c20220323162617219867',
        'd20180815_t0558183_e0559428_b03829_c20220323162617219867',
    ],
    'imLocLatStart': 0,
    'imLocLatStop': -1,
    'imLocLonStart': 0,
    'imLocLonStop': -1,
    'xRefList': [],
    'yRefList': [],
    'gravityWavesPresent': True
}

bore20180815_02 = {
    'filePrefix': 'Bore/201808/GDNBO-SVDNB_npp_',
    'fileSuffix': '_nobc_ops.h5',
    'fileList':
    [
        'd20180815_t0505408_e0507050_b35225_c20220323162620653803',
        'd20180815_t0507062_e0508304_b35225_c20220323162620653803',
        'd20180815_t0508316_e0509558_b35225_c20220323162620653803',
    ],
    'imLocLatStart': 0,
    'imLocLatStop': -1,
    'imLocLonStart': 0,
    'imLocLonStop': -1,
    'xRefList': [],
    'yRefList': [],
    'gravityWavesPresent': True
}

bore20181010_01 = {
    'filePrefix': 'Bore/201810/GDNBO-SVDNB_j01_',
    'fileSuffix': '_noac_ops.h5',
    'fileList':
    [
        'd20181010_t0817488_e0819133_b04625_c20220322200742737300',
        'd20181010_t0819146_e0820391_b04625_c20220322200742737300',
        'd20181010_t0820403_e0822048_b04625_c20220322200742737300',
    ],
    'imLocLatStart': 0,
    'imLocLatStop': -1,
    'imLocLonStart': 0,
    'imLocLonStop': -1,
    'xRefList': [],
    'yRefList': [],
    'gravityWavesPresent': True
}

bore20181010_02 = {
    'filePrefix': 'Bore/201810/GDNBO-SVDNB_j01_',
    'fileSuffix': '_noac_ops.h5',
    'fileList':
    [
        'd20181010_t0957231_e0958477_b04626_c20220322200729229566',
        'd20181010_t0958489_e1000134_b04626_c20220322200729229566',
        'd20181010_t1000147_e1001392_b04626_c20220322200730153678',
    ],
    'imLocLatStart': 0,
    'imLocLatStop': -1,
    'imLocLonStart': 0,
    'imLocLonStop': -1,
    'xRefList': [],
    'yRefList': [],
    'gravityWavesPresent': True
}

bore20181010_03 = {
    'filePrefix': 'Bore/201810/GDNBO-SVDNB_npp_',
    'fileSuffix': '_noac_ops.h5',
    'fileList':
    [
        'd20181010_t0728029_e0729270_b36021_c20220322200740331225',
        'd20181010_t0729283_e0730507_b36021_c20220322200740331225',
        'd20181010_t0730519_e0732161_b36021_c20220322200740331225',
    ],
    'imLocLatStart': 0,
    'imLocLatStop': -1,
    'imLocLonStart': 0,
    'imLocLonStop': -1,
    'xRefList': [],
    'yRefList': [],
    'gravityWavesPresent': True
}

bore20181010_04 = {
    'filePrefix': 'Bore/201810/GDNBO-SVDNB_npp_',
    'fileSuffix': '_noac_ops.h5',
    'fileList':
    [
        'd20181010_t0909013_e0910255_b36022_c20220322200631005128',
        'd20181010_t0910267_e0911509_b36022_c20220322200631005128',
        'd20181010_t0911521_e0913163_b36022_c20220322200631005128',
    ],
    'imLocLatStart': 0,
    'imLocLatStop': -1,
    'imLocLonStart': 0,
    'imLocLonStop': -1,
    'xRefList': [],
    'yRefList': [],
    'gravityWavesPresent': True
}

bore20181011_01 = {
    'filePrefix': 'Bore/201810/GDNBO-SVDNB_j01_',
    'fileSuffix': '_noac_ops.h5',
    'fileList':
    [
        'd20181011_t0801452_e0803079_b04639_c20220322200555161101',
        'd20181011_t0803092_e0804337_b04639_c20220322200555161101',
        'd20181011_t0804349_e0805595_b04639_c20220322200555161101',
    ],
    'imLocLatStart': 0,
    'imLocLatStop': -1,
    'imLocLonStart': 0,
    'imLocLonStop': -1,
    'xRefList': [],
    'yRefList': [],
    'gravityWavesPresent': True
}

bore20181011_02 = {
    'filePrefix': 'Bore/201810/GDNBO-SVDNB_j01_',
    'fileSuffix': '_noac_ops.h5',
    'fileList':
    [
        'd20181011_t0942453_e0944080_b04640_c20220322200556536683',
        'd20181011_t0944093_e0945338_b04640_c20220322200556536683',
        'd20181011_t0945350_e0946596_b04640_c20220322200556536683',
    ],
    'imLocLatStart': 0,
    'imLocLatStop': -1,
    'imLocLonStart': 0,
    'imLocLonStop': -1,
    'xRefList': [],
    'yRefList': [],
    'gravityWavesPresent': True
}

bore20181203_01 = {
    'filePrefix': 'Bore/201812/GDNBO-SVDNB_j01_',
    'fileSuffix': '_nobc_ops.h5',
    'fileList':
    [
        'd20181203_t0622083_e0623328_b05390_c20220322202459204206',
        'd20181203_t0623340_e0624585_b05390_c20220322202504802836',
        'd20181203_t0624598_e0626225_b05390_c20220322202504802836',
    ],
    'imLocLatStart': 0,
    'imLocLatStop': -1,
    'imLocLonStart': 0,
    'imLocLonStop': -1,
    'xRefList': [],
    'yRefList': [],
    'gravityWavesPresent': True
}

bore20181203_02 = {
    'filePrefix': 'Bore/201812/GDNBO-SVDNB_j01_',
    'fileSuffix': '_nobc_ops.h5',
    'fileList':
    [
        'd20181203_t0801426_e0803071_b05391_c20220322202511630691',
        'd20181203_t0803084_e0804329_b05391_c20220322202511630691',
        'd20181203_t0804341_e0805569_b05391_c20220322202511630691',
    ],
    'imLocLatStart': 0,
    'imLocLatStop': -1,
    'imLocLonStart': 0,
    'imLocLonStop': -1,
    'xRefList': [],
    'yRefList': [],
    'gravityWavesPresent': True
}

bore20181203_03 = {
    'filePrefix': 'Bore/201812/GDNBO-SVDNB_npp_',
    'fileSuffix': '_nobc_ops.h5',
    'fileList':
    [
        'd20181203_t0713213_e0714455_b36787_c20220322202513679031',
        'd20181203_t0714467_e0716109_b36787_c20220322202500916111',
        'd20181203_t0716121_e0717363_b36787_c20220322202500916111',
    ],
    'imLocLatStart': 0,
    'imLocLatStop': -1,
    'imLocLonStart': 0,
    'imLocLonStop': -1,
    'xRefList': [],
    'yRefList': [],
    'gravityWavesPresent': True
}

bore20190531_01 = {
    'filePrefix': 'Bore/201905/GDNBO-SVDNB_j01_',
    'fileSuffix': '_noac_ops.h5',
    'fileList':
    [
        'd20190531_t0535033_e0536260_b07929_c20220321223342720672',
        'd20190531_t0536273_e0537518_b07929_c20220321223342720672',
        'd20190531_t0537530_e0539175_b07929_c20220321223342720672',
    ],
    'imLocLatStart': 0,
    'imLocLatStop': -1,
    'imLocLonStart': 0,
    'imLocLonStop': -1,
    'xRefList': [],
    'yRefList': [],
    'gravityWavesPresent': True
}

bore20190531_02 = {
    'filePrefix': 'Bore/201905/GDNBO-SVDNB_npp_',
    'fileSuffix': '_noac_ops.h5',
    'fileList':
    [
        'd20190531_t0445145_e0446387_b39325_c20220321223400770893',
        'd20190531_t0446399_e0448041_b39325_c20220321223400770893',
        'd20190531_t0448053_e0449295_b39325_c20220321223400770893',
    ],
    'imLocLatStart': 0,
    'imLocLatStop': -1,
    'imLocLonStart': 0,
    'imLocLonStop': -1,
    'xRefList': [],
    'yRefList': [],
    'gravityWavesPresent': True
}

bore20190609_01 = {
    'filePrefix': 'Bore/201906/GDNBO-SVDNB_j01_',
    'fileSuffix': '_noac_ops.h5',
    'fileList':
    [
        'd20190609_t0751595_e0753240_b08058_c20220321234429772053',
        'd20190609_t0753252_e0754497_b08058_c20220321234430925613',
        'd20190609_t0754510_e0756155_b08058_c20220321234430925613',
    ],
    'imLocLatStart': 0,
    'imLocLatStop': -1,
    'imLocLonStart': 0,
    'imLocLonStop': -1,
    'xRefList': [],
    'yRefList': [],
    'gravityWavesPresent': True
}

bore20190609_02 = {
    'filePrefix': 'Bore/201906/GDNBO-SVDNB_j01_',
    'fileSuffix': '_noac_ops.h5',
    'fileList':
    [
        'd20190609_t0931338_e0932583_b08059_c20220321234431570540',
        'd20190609_t0932596_e0934241_b08059_c20220321234431570540',
        'd20190609_t0934253_e0935498_b08059_c20220321234431570540',
    ],
    'imLocLatStart': 0,
    'imLocLatStop': -1,
    'imLocLonStart': 0,
    'imLocLonStop': -1,
    'xRefList': [],
    'yRefList': [],
    'gravityWavesPresent': True
}

bore20190609_03 = {
    'filePrefix': 'Bore/201906/GDNBO-SVDNB_j01_',
    'fileSuffix': '_noac_ops.h5',
    'fileList':
    [
        'd20190609_t1800498_e1802143_b08064_c20220321234615517718',
        'd20190609_t1802156_e1803401_b08064_c20220321234617089194',
        'd20190609_t1803413_e1805041_b08064_c20220321234617089194',
    ],
    'imLocLatStart': 0,
    'imLocLatStop': -1,
    'imLocLonStart': 0,
    'imLocLonStop': -1,
    'xRefList': [],
    'yRefList': [],
    'gravityWavesPresent': True
}

bore20190609_04 = {
    'filePrefix': 'Bore/201906/GDNBO-SVDNB_npp_',
    'fileSuffix': '_noac_ops.h5',
    'fileList':
    [
        'd20190609_t0841470_e0843112_b39455_c20220321234447930655',
        'd20190609_t0843124_e0844366_b39455_c20220321234447930655',
        'd20190609_t0844378_e0846020_b39455_c20220321234441804571',
    ],
    'imLocLatStart': 0,
    'imLocLatStop': -1,
    'imLocLonStart': 0,
    'imLocLonStop': -1,
    'xRefList': [],
    'yRefList': [],
    'gravityWavesPresent': True
}

bore20190609_05 = {
    'filePrefix': 'Bore/201906/GDNBO-SVDNB_npp_',
    'fileSuffix': '_noac_ops.h5',
    'fileList':
    [
        'd20190609_t1850372_e1852014_b39461_c20220321234616335671',
        'd20190609_t1852026_e1853268_b39461_c20220321234616335671',
        'd20190609_t1853280_e1854522_b39461_c20220321234615646428',
    ],
    'imLocLatStart': 0,
    'imLocLatStop': -1,
    'imLocLonStart': 0,
    'imLocLonStop': -1,
    'xRefList': [],
    'yRefList': [],
    'gravityWavesPresent': True
}

bore20190628_01 = {
    'filePrefix': 'Bore/201906/GDNBO-SVDNB_j01_',
    'fileSuffix': '_noac_ops.h5',
    'fileList':
    [
        'd20190628_t1520277_e1521505_b08332_c20220321225901209708',
        'd20190628_t1521517_e1523162_b08332_c20220321225901209708',
        'd20190628_t1523174_e1524420_b08332_c20220321225901209708',
    ],
    'imLocLatStart': 0,
    'imLocLatStop': -1,
    'imLocLonStart': 0,
    'imLocLonStop': -1,
    'xRefList': [],
    'yRefList': [],
    'gravityWavesPresent': True
}

bore20190628_02 = {
    'filePrefix': 'Bore/201906/GDNBO-SVDNB_npp_',
    'fileSuffix': '_noac_ops.h5',
    'fileList':
    [
        'd20190628_t1610148_e1611389_b39729_c20220321225931788359',
        'd20190628_t1611402_e1613043_b39729_c20220321225852177642',
        'd20190628_t1613056_e1614298_b39729_c20220321225852177642',
    ],
    'imLocLatStart': 0,
    'imLocLatStop': -1,
    'imLocLonStart': 0,
    'imLocLonStop': -1,
    'xRefList': [],
    'yRefList': [],
    'gravityWavesPresent': True
}


bore20190701 = {
    'filePrefix': 'Bore/201907/GDNBO-SVDNB_npp_',
    'fileSuffix': '_noac_ops.h5',
    'fileList':
    [
        'd20190701_t0704081_e0709485_b39766_c20220321225900609298',
        'd20190701_t0840521_e0846325_b39767_c20220321225901011102',
        'd20190701_t0846337_e0852141_b39767_c20220321225903018819',
    ],
    'imLocLatStart': 0,
    'imLocLatStop': -1,
    'imLocLonStart': 0,
    'imLocLonStop': -1,
    'xRefList': [],
    'yRefList': [],
    'gravityWavesPresent': True
}

bore20190702_01 = {
    'filePrefix': 'Bore/201907/GDNBO-SVDNB_j01_',
    'fileSuffix': '_noac_ops.h5',
    'fileList':
    [
        'd20190702_t1547113_e1548358_b08389_c20220321225854645453',
        'd20190702_t1548371_e1549598_b08389_c20220321225854645453',
        'd20190702_t1550011_e1551256_b08389_c20220321225854645453',
    ],
    'imLocLatStart': 0,
    'imLocLatStop': -1,
    'imLocLonStart': 0,
    'imLocLonStop': -1,
    'xRefList': [],
    'yRefList': [],
    'gravityWavesPresent': True
}

bore20190702_02 = {
    'filePrefix': 'Bore/201907/GDNBO-SVDNB_npp_',
    'fileSuffix': '_noac_ops.h5',
    'fileList':
    [
        'd20190702_t1457230_e1458472_b39785_c20220321225905660407',
        'd20190702_t1458484_e1500126_b39785_c20220321225905660407',
        'd20190702_t1500138_e1501380_b39785_c20220321225905660407',
    ],
    'imLocLatStart': 0,
    'imLocLatStop': -1,
    'imLocLonStart': 0,
    'imLocLonStop': -1,
    'xRefList': [],
    'yRefList': [],
    'gravityWavesPresent': True
}

bore20190704_01 = {
    'filePrefix': 'Bore/201907/GDNBO-SVDNB_j01_',
    'fileSuffix': '_noac_ops.h5',
    'fileList':
    [
        'd20190704_t1325295_e1326540_b08416_c20220321225854917411',
        'd20190704_t1326552_e1328197_b08416_c20220321225854917411',
        'd20190704_t1328210_e1329437_b08416_c20220321225854917411',
    ],
    'imLocLatStart': 0,
    'imLocLatStop': -1,
    'imLocLonStart': 0,
    'imLocLonStop': -1,
    'xRefList': [],
    'yRefList': [],
    'gravityWavesPresent': True
}

bore20190704_02 = {
    'filePrefix': 'Bore/201907/GDNBO-SVDNB_j01_',
    'fileSuffix': '_noac_ops.h5',
    'fileList':
    [
        'd20190704_t1506296_e1507541_b08417_c20220321225901399421',
        'd20190704_t1507553_e1509181_b08417_c20220321225901399421',
        'd20190704_t1509193_e1510438_b08417_c20220321225901399421',
    ],
    'imLocLatStart': 0,
    'imLocLatStop': -1,
    'imLocLonStart': 0,
    'imLocLonStop': -1,
    'xRefList': [],
    'yRefList': [],
    'gravityWavesPresent': True
}

bore20190706_01 = {
    'filePrefix': 'Bore/201907/GDNBO-SVDNB_j01_',
    'fileSuffix': '_noac_ops.h5',
    'fileList':
    [
        'd20190706_t1250290_e1251535_b08444_c20220321223617035424',
        'd20190706_t1251547_e1253192_b08444_c20220321223617035424',
        'd20190706_t1253205_e1254450_b08444_c20220321223617035424',
    ],
    'imLocLatStart': 0,
    'imLocLatStop': -1,
    'imLocLonStart': 0,
    'imLocLonStop': -1,
    'xRefList': [],
    'yRefList': [],
    'gravityWavesPresent': True
}

bore20190706_02 = {
    'filePrefix': 'Bore/201907/GDNBO-SVDNB_j01_',
    'fileSuffix': '_noac_ops.h5',
    'fileList':
    [
        'd20190706_t1431291_e1432536_b08445_c20220321223627523840',
        'd20190706_t1432548_e1434193_b08445_c20220321223627523840',
        'd20190706_t1434206_e1435451_b08445_c20220321223627523840',
    ],
    'imLocLatStart': 0,
    'imLocLatStop': -1,
    'imLocLonStart': 0,
    'imLocLonStop': -1,
    'xRefList': [],
    'yRefList': [],
    'gravityWavesPresent': True
}

bore20190706_03 = {
    'filePrefix': 'Bore/201907/GDNBO-SVDNB_npp_',
    'fileSuffix': '_noac_ops.h5',
    'fileList':
    [
        'd20190706_t1341422_e1343063_b39841_c20220321223610107866',
        'd20190706_t1343076_e1344317_b39841_c20220321223610107866',
        'd20190706_t1344330_e1345572_b39841_c20220321223610107866',
    ],
    'imLocLatStart': 0,
    'imLocLatStop': -1,
    'imLocLonStart': 0,
    'imLocLonStop': -1,
    'xRefList': [],
    'yRefList': [],
    'gravityWavesPresent': True
}

bore20190730_01 = {
    'filePrefix': 'Bore/201907/GDNBO-SVDNB_j01_',
    'fileSuffix': '_nobc_ops.h5',
    'fileList':
    [
        'd20190730_t0526193_e0527421_b08780_c20220321224132798772',
        'd20190730_t0527433_e0529078_b08780_c20220321224132798772',
        'd20190730_t0529091_e0530336_b08780_c20220321224132798772',
    ],
    'imLocLatStart': 0,
    'imLocLatStop': -1,
    'imLocLonStart': 0,
    'imLocLonStop': -1,
    'xRefList': [],
    'yRefList': [],
    'gravityWavesPresent': True
}

bore20190730_02 = {
    'filePrefix': 'Bore/201907/GDNBO-SVDNB_npp_',
    'fileSuffix': '_nobc_ops.h5',
    'fileList':
    [
        'd20190730_t0436314_e0437556_b40176_c20220321224058925392',
        'd20190730_t0437568_e0439210_b40176_c20220321224058925392',
        'd20190730_t0439222_e0440464_b40176_c20220321224058925392',
    ],
    'imLocLatStart': 0,
    'imLocLatStop': -1,
    'imLocLonStart': 0,
    'imLocLonStop': -1,
    'xRefList': [],
    'yRefList': [],
    'gravityWavesPresent': True
}

bore20190730_03 = {
    'filePrefix': 'Bore/201907/GDNBO-SVDNB_npp_',
    'fileSuffix': '_nobc_ops.h5',
    'fileList':
    [
        'd20190730_t0617316_e0618558_b40177_c20220321224052015208',
        'd20190730_t0618570_e0620212_b40177_c20220321224052015208',
        'd20190730_t0620224_e0621466_b40177_c20220321224052015208',
    ],
    'imLocLatStart': 0,
    'imLocLatStop': -1,
    'imLocLonStart': 0,
    'imLocLonStop': -1,
    'xRefList': [],
    'yRefList': [],
    'gravityWavesPresent': True
}

bore20200320_01 = {
    'filePrefix': 'Bore/202003/GDNBO-SVDNB_j01_',
    'fileSuffix': '_noac_ops.h5',
    'fileList':
    [
        'd20200320_t0841346_e0842591_b12102_c20220317213136071300',
        'd20200320_t0843004_e0844231_b12102_c20220317213136071300',
        'd20200320_t0844243_e0845488_b12102_c20220317213136071300',
    ],
    'imLocLatStart': 0,
    'imLocLatStop': -1,
    'imLocLonStart': 0,
    'imLocLonStop': -1,
    'xRefList': [],
    'yRefList': [],
    'gravityWavesPresent': True
}

bore20200320_02 = {
    'filePrefix': 'Bore/202003/GDNBO-SVDNB_npp_',
    'fileSuffix': '_noac_ops.h5',
    'fileList':
    [
        'd20200320_t0931212_e0932454_b43499_c20220317213137595428',
        'd20200320_t0932466_e0934108_b43499_c20220317213136509036',
        'd20200320_t0934120_e0935362_b43499_c20220317213136509036',
    ],
    'imLocLatStart': 0,
    'imLocLatStop': -1,
    'imLocLonStart': 0,
    'imLocLonStop': -1,
    'xRefList': [],
    'yRefList': [],
    'gravityWavesPresent': True
}

bore20200324 = {
    'filePrefix': 'Bore/202003/GDNBO-SVDNB_npp_',
    'fileSuffix': '_noac_ops.h5',
    'fileList':
    [
        'd20200324_t0815403_e0817045_b43555_c20220317212106220477',
        'd20200324_t0817057_e0818299_b43555_c20220317211403791624',
        'd20200324_t0818311_e0819553_b43555_c20220317211403791624',
    ],
    'imLocLatStart': 0,
    'imLocLatStop': -1,
    'imLocLonStart': 0,
    'imLocLonStop': -1,
    'xRefList': [],
    'yRefList': [],
    'gravityWavesPresent': True
}

bore20200424_01 = {
    'filePrefix': 'Bore/202004/GDNBO-SVDNB_j01_',
    'fileSuffix': '_noac_ops.h5',
    'fileList':
    [
        'd20200424_t0924499_e0926144_b12599_c20220317211613318604',
        'd20200424_t0926156_e0927401_b12599_c20220317211613318604',
        'd20200424_t0927414_e0929059_b12599_c20220317211613318604',
    ],
    'imLocLatStart': 0,
    'imLocLatStop': -1,
    'imLocLonStart': 0,
    'imLocLonStop': -1,
    'xRefList': [],
    'yRefList': [],
    'gravityWavesPresent': True
}

bore20200424_02 = {
    'filePrefix': 'Bore/202004/GDNBO-SVDNB_npp_',
    'fileSuffix': '_noac_ops.h5',
    'fileList':
    [
        'd20200424_t0833377_e0835019_b43995_c20220317212236725406',
        'd20200424_t0835031_e0836273_b43995_c20220317212236725406',
        'd20200424_t0836285_e0837527_b43995_c20220317212236725406',
    ],
    'imLocLatStart': 0,
    'imLocLatStop': -1,
    'imLocLonStart': 0,
    'imLocLonStop': -1,
    'xRefList': [],
    'yRefList': [],
    'gravityWavesPresent': True
}

bore20200616_01 = {
    'filePrefix': 'Bore/202006/GDNBO-SVDNB_j01_',
    'fileSuffix': '_nobc_ops.h5',
    'fileList':
    [
        'd20200616_t1630083_e1631328_b13355_c20220317212330210444',
        'd20200616_t1631341_e1632586_b13355_c20220317212330210444',
        'd20200616_t1632598_e1634226_b13355_c20220317212330210444',
    ],
    'imLocLatStart': 0,
    'imLocLatStop': -1,
    'imLocLonStart': 0,
    'imLocLonStop': -1,
    'xRefList': [],
    'yRefList': [],
    'gravityWavesPresent': True
}

bore20200616_02 = {
    'filePrefix': 'Bore/202006/GDNBO-SVDNB_npp_',
    'fileSuffix': '_nobc_ops.h5',
    'fileList':
    [
        'd20200616_t1538563_e1540205_b44751_c20220317212404280512',
        'd20200616_t1540217_e1541459_b44751_c20220317212404280512',
        'd20200616_t1541471_e1543113_b44751_c20220317212404280512',
    ],
    'imLocLatStart': 0,
    'imLocLatStop': -1,
    'imLocLonStart': 0,
    'imLocLonStop': -1,
    'xRefList': [],
    'yRefList': [],
    'gravityWavesPresent': True
}

bore20200424 = {
    'filePrefix': 'Bore/202004/GDNBO-SVDNB_npp_',
    'fileSuffix': '_noac_ops.h5',
    'fileList':
    ['d20200424_t0835031_e0836273_b43995_c20220317212236725406'],
    'imLocLatStart': 300,
    'imLocLatStop': 768,
    'imLocLonStart': 1800,
    'imLocLonStop': 2400,
    'xRefList': [2104, 2000],
    'yRefList': [456, 550],
    'gravityWavesPresent': True
}

caseOpts = {'subsetSquareSize': 128}
dataOpts001 = {'exRef': '001',
               'subsetSquares': True,
               'subsetSquareSize': 256,
               'subsetSquareOverlap': 200,
               'subsetSquareOversize': None}
