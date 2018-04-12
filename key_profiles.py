"""Common key-profiles

A list of common key-profiles used for key finding.

The profiles are presented in their original format
as well as normalized from [0,1] for use in the HMM
- krumhansl_kessler
- aarden_essen
- sapp
- bellman_budge
- temperley
"""

# Original key-profiles
krumhansl_kessler_major_original = [
    6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 
    2.52, 5.19, 2.39, 3.66, 2.29, 2.88
]
krumhansl_kessler_minor_original = [
    6.33, 2.68, 3.52, 5.38, 2.6, 3.53, 
    2.54, 4.75, 3.98, 2.69, 3.34, 3.17
]
aarden_essen_major_original = [
    17.7661, 0.145624, 14.9265, 0.160186, 19.8049, 11.3587, 
    0.291248, 22.062, 0.145624, 8.15494, 0.232998, 4.95122
]
aarden_essen_minor_original = [
    18.2648, 0.737619, 14.0499, 16.8599, 0.702494, 14.4362,
    0.702494, 18.6161, 4.56621, 1.93186, 7.37619, 1.75623
]
sapp_major_original = [
    2, 0, 1, 0, 1, 1, 0, 2, 0, 1, 0, 1
]
sapp_minor_original = [
    2, 0, 1, 1, 0, 1, 0, 2, 1, 0, 0.5, 0.5
]
bellman_budge_major_original = [
    16.8, 0.86, 12.95, 1.41, 13.49, 11.93, 
    1.25, 20.28, 1.8, 8.04, 0.62, 10.57
]
bellman_budge_minor_original = [
    18.16, 0.69, 12.99, 13.34, 1.07, 11.15,
    1.38, 21.07, 7.49, 1.53, 0.92, 10.21
]
temperley_major_original = [
    0.748, 0.06, 0.488, 0.082, 0.67, 0.46, 
    0.096, 0.715, 0.104, 0.366, 0.057, 0.4,
temperley_minor_original = [
    0.712, 0.084, 0.474, 0.618, 0.049, 0.46,
    0.105, 0.747, 0.404, 0.067, 0.133, 0.33
]

# Normalized key-profiles
krumhansl_kessler_major = [
    0.15195022732711172, 0.0533620483369227, 0.08327351040918879, 
    0.05575496530270399, 0.10480976310122037, 0.09787030390045463,
    0.06030150753768843, 0.1241923905240488, 0.05719071548217276,
    0.08758076094759511, 0.05479779851639147, 0.06891600861450106
]
krumhansl_kessler_minor = [
    0.14221523253201526, 0.06021118849696697, 0.07908335205571781,
    0.12087171422152324, 0.05841383958660975, 0.07930802066951245,
    0.05706582790384183, 0.1067175915524601, 0.08941810829027184,
    0.06043585711076162, 0.07503931700741405, 0.07121995057290496
]
aarden_essen_major = [
    0.17766092893562843, 0.001456239417504233, 0.1492649402940239,
    0.0016018593592562562, 0.19804892078043168, 0.11358695456521818,
    0.002912478835008466, 0.2206199117520353, 0.001456239417504233,
    0.08154936738025305, 0.002329979068008373, 0.049512180195127924
]
aarden_essen_minor = [
    0.18264800547944018, 0.007376190221285707, 0.14049900421497014,
    0.16859900505797015, 0.0070249402107482066, 0.14436200433086013,
    0.0070249402107482066, 0.18616100558483017, 0.04566210136986304,
    0.019318600579558018, 0.07376190221285707, 0.017562300526869017
]
sapp_major = [
    0.2222222222222222, 0.0, 0.1111111111111111, 0.0,
    0.1111111111111111, 0.1111111111111111, 0.0, 0.2222222222222222,
    0.0, 0.1111111111111111, 0.0, 0.1111111111111111
]
sapp_minor = [
    0.2222222222222222, 0.0, 0.1111111111111111, 0.1111111111111111,
    0.0, 0.1111111111111111, 0.0, 0.2222222222222222,
    0.1111111111111111, 0.0, 0.05555555555555555, 0.05555555555555555
]
bellman_budge_major = [
    0.168, 0.0086, 0.1295, 0.0141, 0.1349, 0.1193,
    0.0125, 0.2028, 0.018000000000000002, 0.0804, 0.0062, 0.1057
]
bellman_budge_minor = [
    0.1816, 0.0069, 0.12990000000000002, 
    0.1334, 0.010700000000000001, 0.1115, 
    0.0138, 0.2107, 0.07490000000000001, 
    0.015300000000000001, 0.0092, 0.10210000000000001
]
temperley_major = [
    0.17616580310880825, 0.014130946773433817, 0.11493170042392838, 
    0.019312293923692884, 0.15779557230334432, 0.10833725859632594,
    0.02260951483749411, 0.16839378238341965, 0.02449364107395195,
    0.08619877531794629, 0.013424399434762127, 0.09420631182289213
]
temperley_minor = [
    0.1702127659574468, 0.020081281377002155, 0.1133158020559407,
    0.14774085584508725, 0.011714080803251255, 0.10996892182644036,
    0.02510160172125269, 0.1785799665311977, 0.09658140090843893,
    0.016017212526894576, 0.03179536218025341, 0.07889074826679417
]
