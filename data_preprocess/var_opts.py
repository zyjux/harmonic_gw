"""
===========================================
Gravity Waves Parameters
===========================================
"""

case20170719 = {
    'caseLat': 14,
    'caseLon': -121,
    'filePrefix': 'TC/201707/GDNBO-SVDNB_npp_',
    'fileSuffix': '_noac_opts.h5',
    'fileList':
    ['d20170719_t0916454_e0918096_b29666_c20220118195134555715',
     'd20170719_t0918108_e0919350_b29666_c20220118195134555715'],
    'fileListStorm':
    ['d20170719_t1056184_e1057426_b29667_c20220118195338307107',
     'd20170719_t1057438_e1059080_b29667_c20220118195338307107',
     'd20170719_t1059092_e1100334_b29667_c20220118195338307107']}

case20171016 = {
    'caseLat': 23,
    'caseLon': -69,
    'filePrefix': 'TC/201710/GDNBO_npp_',
    'fileSuffix': '_nobc_ops.h5',
    'fileList':
    ['d20171016_t0619049_e0624453_b30927_c20220118194618899804',
     'd20171016_t0624466_e0630252_b30927_c20220118194615235230']}

case201807 = {
    'caseLat': 39,
    'caseLon': -66,
    'filePrefix': 'TC/201807/GDNBO-SVDNB_npp_',
    'fileSuffix': '_noac_ops.h5',
    'fileList':
    ['d20180711_t0553263_e0554505_b34729_c20220118200228744535',
     'd20180711_t0554518_e0556159_b34729_c20220118200250204856',
     'd20180711_t0556172_e0557413_b34729_c20220118200250204856']}

case201807j = {
    'caseLat': 39,
    'caseLon': -66,
    'filePrefix': '/TC/201807/GDNBO-SVDNB_j01_',
    'fileSuffix': '_noac_ops.h5',
    'fileList':
    ['j01_d20180711_t0641492_e0643138_b03333_c20220118200127645306',
     'j01_d20180711_t0643150_e0644377_b03333_c20220118200127645306',
     'j01_d20180711_t0644390_e0646035_b03333_c20220118200127645306',
     'j01_d20180711_t0646047_e0647292_b03333_c20220118200206197883']}

case20181010 = {
    'caseLat': 28,
    'caseLon': -86,
    'filePrefix': 'TC/201810/GDNBO-SVDNB_npp_',
    'fileSuffix': '_noac_opts.h5',
    'fileList':
        ['d20181010_t0732173_e0733415_b36021_c20220118200327774728',
         'd20181010_t0733427_e0735069_b36021_c20220118200327774728']}

case20181010je = {
    'caseLat': 28,
    'caseLon': -86,
    'filePrefix': 'TC/201810/GDNBO-SVDNB_j01_',
    'fileSuffix': '_noac_opts.h5',
    'fileList':
    ['j01_d20181010_t0641060_e0642305_b04624_c20220118195630621950',
     'j01_d20181010_t0642317_e0643545_b04624_c20220118195630621950']}

case20181010jw = {
    'caseLat': 28,
    'caseLon': -86,
    'filePrefix': 'TC/201810/GDNBO-SVDNB_j01_',
    'fileSuffix': '_noac_opts.h5',
    'fileList':
    ['j01_d20181010_t0820403_e0822048_b04625_c20220118200333725852',
     'j01_d20181010_t0822061_e0823288_b04625_c20220118200333725852']}

case20200424 = {
    'filePrefix': 'Bore/202004/GDNBO-SVDNB_npp_',
    'fileSuffix': '_noac_ops.h5',
    'fileList':
    ['d20200424_t0835031_e0836273_b43995_c20220317212236725406'],
    'imLocLatStart': 300,
    'imLocLatStop': 768,
    'imLocLonStart': 1800,
    'imLocLonStop': 2400,
    'xRefList': [2104, 2000],
    'yRefList': [456, 550]}

caseOpts = {'subsetSquareSize': 128}
dataOpts001 = {'exRef': '001',
               'subsetSquares': True,
               'subsetSquareSize': 256,
               'subsetSquareOverlap': 200,
               'subsetSquareOversize': None}
