from shapely.geometry import Polygon, Point
#areaA = Polygon([(31.1882229,121.6069208),(31.1882525,121.6069255),(31.1882821,121.6069297),(31.1883114,121.6069337),(31.1883403,121.6069378),(31.1883686,121.6069423),(31.188396,121.6069472),(31.1884223,121.6069516),(31.1884471,121.6069542),(31.1884699,121.6069538),(31.1884905,121.6069492),(31.1885086,121.6069396),(31.1885243,121.6069254),(31.1885381,121.6069072),(31.1885502,121.6068859),(31.188561,121.6068621),(31.1885708,121.6068368),(31.1885807,121.6068105),(31.1885916,121.6067843),(31.1886045,121.606759),(31.1886206,121.6067353),(31.1886404,121.6067139),(31.1886627,121.6066942),(31.1886859,121.6066753),(31.1887084,121.6066563),(31.1887285,121.6066364),(31.1887449,121.6066148),(31.1887575,121.6065914),(31.1887663,121.606566),(31.1887714,121.6065386),(31.1887729,121.606509),(31.188771,121.6064773),(31.1887663,121.6064436),(31.1887597,121.6064081),(31.1887518,121.6063711),(31.1887435,121.6063329),(31.1887352,121.6062935),(31.1887273,121.6062533),(31.1887194,121.6062123),(31.1887155,121.6061916),(31.1887117,121.6061708),(31.1887078,121.6061499),(31.1887039,121.6061288),(31.1887001,121.6061078),(31.1886962,121.6060866),(31.1886923,121.6060654),(31.1886884,121.6060442),(31.1886844,121.606023),(31.1886805,121.6060018),(31.1886765,121.6059807),(31.1886725,121.6059595),(31.1886684,121.6059384),(31.1886643,121.6059174),(31.1886602,121.6058965),(31.1886561,121.6058756),(31.188652,121.6058548),(31.1886479,121.6058342),(31.1886438,121.6058137),(31.1886358,121.605773),(31.1886283,121.6057329),(31.1886212,121.6056935),(31.1886145,121.605655),(31.1886078,121.6056179),(31.1886007,121.6055828),(31.1885927,121.60555),(31.1885834,121.6055202),(31.1885727,121.6054934),(31.1885605,121.6054696),(31.1885469,121.6054486),(31.1885319,121.6054304),(31.1885155,121.6054149),(31.1884982,121.6054023),(31.1884804,121.6053932),(31.1884627,121.6053884),(31.188438,121.6053905),(31.1884164,121.6054047),(31.1884034,121.60542),(31.1883908,121.6054387),(31.1883783,121.6054601),(31.1883654,121.6054832),(31.1883519,121.6055076),(31.1883379,121.6055329),(31.1883234,121.6055591),(31.1883086,121.605586),(31.1882935,121.6056134),(31.1882783,121.6056413),(31.1882629,121.6056696),(31.1882473,121.6056982),(31.1882316,121.605727),(31.1882157,121.6057559),(31.1881998,121.605785),(31.1881837,121.6058143),(31.1881675,121.6058436),(31.1881513,121.6058729),(31.1881351,121.6059024),(31.1881188,121.6059319),(31.1881025,121.6059614),(31.1880862,121.605991),(31.18807,121.6060206),(31.1880539,121.6060502),(31.1880377,121.6060799),(31.1880217,121.6061096),(31.1880056,121.6061392),(31.1879894,121.6061686),(31.1879732,121.6061979),(31.1879569,121.6062269),(31.1879406,121.6062558),(31.1879244,121.6062846),(31.1879084,121.6063132),(31.1878927,121.6063418),(31.1878773,121.6063702),(31.187862,121.6063983),(31.1878469,121.606426),(31.187832,121.606453),(31.187817,121.6064792),(31.1878022,121.6065046),(31.187788,121.6065294),(31.1877748,121.6065535),(31.1877629,121.6065772),(31.1877528,121.6066005),(31.1877448,121.6066234),(31.1877392,121.6066452),(31.1877362,121.6066751),(31.1877405,121.6067002),(31.1877523,121.6067203),(31.1877697,121.6067373),(31.1877911,121.6067535),(31.1878067,121.6067648),(31.187823,121.6067766),(31.1878395,121.6067889),(31.1878562,121.6068016),(31.1878725,121.6068147),(31.1878885,121.606828),(31.1879045,121.606841),(31.187921,121.6068532),(31.1879386,121.6068639),(31.1879578,121.6068727),(31.187979,121.6068791),(31.188002,121.6068837),(31.1880266,121.6068872),(31.1880525,121.6068904),(31.1880794,121.606894),(31.1881071,121.6068986),(31.1881354,121.606904),(31.1881642,121.6069097),(31.1881934,121.6069155),(31.1882229,121.6069208)])

# areaB = Polygon([(0,1),(1,2),(2,3),(0,1)])

# areaA = Polygon([(121.6069208,31.1882229),(121.6069255,31.1882525),(121.6069297,31.1882821),(121.6069337,31.1883114),(121.6069378,31.1883403),(121.6069423,31.1883686),(121.6069472,31.188396),(121.6069516,31.1884223),(121.6069542,31.1884471),(121.6069538,31.1884699),(121.6069492,31.1884905),(121.6069396,31.1885086),(121.6069254,31.1885243),(121.6069072,31.1885381),(121.6068859,31.1885502),(121.6068621,31.188561),(121.6068368,31.1885708),(121.6068105,31.1885807),(121.6067843,31.1885916),(121.606759,31.1886045),(121.6067353,31.1886206),(121.6067139,31.1886404),(121.6066942,31.1886627),(121.6066753,31.1886859),(121.6066563,31.1887084),(121.6066364,31.1887285),(121.6066148,31.1887449),(121.6065914,31.1887575),(121.606566,31.1887663),(121.6065386,31.1887714),(121.606509,31.1887729),(121.6064773,31.188771),(121.6064436,31.1887663),(121.6064081,31.1887597),(121.6063711,31.1887518),(121.6063329,31.1887435),(121.6062935,31.1887352),(121.6062533,31.1887273),(121.6062123,31.1887194),(121.6061916,31.1887155),(121.6061708,31.1887117),(121.6061499,31.1887078),(121.6061288,31.1887039),(121.6061078,31.1887001),(121.6060866,31.1886962),(121.6060654,31.1886923),(121.6060442,31.1886884),(121.606023,31.1886844),(121.6060018,31.1886805),(121.6059807,31.1886765),(121.6059595,31.1886725),(121.6059384,31.1886684),(121.6059174,31.1886643),(121.6058965,31.1886602),(121.6058756,31.1886561),(121.6058548,31.188652),(121.6058342,31.1886479),(121.6058137,31.1886438),(121.605773,31.1886358),(121.6057329,31.1886283),(121.6056935,31.1886212),(121.605655,31.1886145),(121.6056179,31.1886078),(121.6055828,31.1886007),(121.60555,31.1885927),(121.6055202,31.1885834),(121.6054934,31.1885727),(121.6054696,31.1885605),(121.6054486,31.1885469),(121.6054304,31.1885319),(121.6054149,31.1885155),(121.6054023,31.1884982),(121.6053932,31.1884804),(121.6053884,31.1884627),(121.6053905,31.188438),(121.6054047,31.1884164),(121.60542,31.1884034),(121.6054387,31.1883908),(121.6054601,31.1883783),(121.6054832,31.1883654),(121.6055076,31.1883519),(121.6055329,31.1883379),(121.6055591,31.1883234),(121.605586,31.1883086),(121.6056134,31.1882935),(121.6056413,31.1882783),(121.6056696,31.1882629),(121.6056982,31.1882473),(121.605727,31.1882316),(121.6057559,31.1882157),(121.605785,31.1881998),(121.6058143,31.1881837),(121.6058436,31.1881675),(121.6058729,31.1881513),(121.6059024,31.1881351),(121.6059319,31.1881188),(121.6059614,31.1881025),(121.605991,31.1880862),(121.6060206,31.18807),(121.6060502,31.1880539),(121.6060799,31.1880377),(121.6061096,31.1880217),(121.6061392,31.1880056),(121.6061686,31.1879894),(121.6061979,31.1879732),(121.6062269,31.1879569),(121.6062558,31.1879406),(121.6062846,31.1879244),(121.6063132,31.1879084),(121.6063418,31.1878927),(121.6063702,31.1878773),(121.6063983,31.187862),(121.606426,31.1878469),(121.606453,31.187832),(121.6064792,31.187817),(121.6065046,31.1878022),(121.6065294,31.187788),(121.6065535,31.1877748),(121.6065772,31.1877629),(121.6066005,31.1877528),(121.6066234,31.1877448),(121.6066452,31.1877392),(121.6066751,31.1877362),(121.6067002,31.1877405),(121.6067203,31.1877523),(121.6067373,31.1877697),(121.6067535,31.1877911),(121.6067648,31.1878067),(121.6067766,31.187823),(121.6067889,31.1878395),(121.6068016,31.1878562),(121.6068147,31.1878725),(121.606828,31.1878885),(121.606841,31.1879045),(121.6068532,31.187921),(121.6068639,31.1879386),(121.6068727,31.1879578),(121.6068791,31.187979),(121.6068837,31.188002),(121.6068872,31.1880266),(121.6068904,31.1880525),(121.606894,31.1880794),(121.6068986,31.1881071),(121.606904,31.1881354),(121.6069097,31.1881642),(121.6069155,31.1881934),(121.6069208,31.1882229)])
areaA = Polygon([(121.6053884, 31.1877362), (121.6053884,31.1887729),  (121.6069542, 31.1887729),(121.6069542,31.1877362)])

areaB = Polygon([(121.6053884, 31.1877362), (121.6053884,31.1887729),  (121.6069542, 31.1887729),(121.6069542,31.1877362)])

p = Point(121.60539, 31.18774)
# p = Point(121.641749, 31.034772)
print(p.within(areaA))

# the two parts of dock much match one to one
dock1 = Point((121.6069208,31.1882229))
dock2 = Point(2,2)

dock21 = Point((121.6069378,31.1883403))
dock22 = Point(2,2)

dockPoint =[[dock1, dock2],[dock21, dock22]]


def inWhichArea( lat, lon ):
    p = Point(lat, lon)
    print (p)
    #print (areaA)
    #print(areaA.area)
    print(p.within(areaA))
    if p.within(areaA):
        return 1
    elif p.within(areaB):
        return 2
    else:
        return 0
    pass

inWhichArea(31.18823,121.60691)