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
