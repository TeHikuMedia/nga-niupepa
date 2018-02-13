import context
from tau import *
from hiki_niupepa_kupu import whakarauiri

def test_comma_pounds():
    assert pakaru_moni('£4,565,,3,,4') == 'pāuna moni whā mano, rima rau ono tekau mā rima, me ngā toru herengi me ngā whā pene'


def test_pounds_no_shillings():
    # Tests that the lack of digit in the shillings position doesn't prevent pennies from being recognised as such
    assert pakaru_moni('£4,565,,0,,4') == pakaru_moni('£4,565..0.,4') == 'pāuna moni whā mano, rima rau ono tekau mā rima, me ngā whā pene'


def test_comma_pounds_symbols():
    # Tests that the lack of digit in the shillings position doesn't prevent pennies from being recognised as such
    assert pakaru_moni('4,565 l. 3 s. 4 d.') == 'pāuna moni whā mano, rima rau ono tekau mā rima, me ngā toru herengi me ngā whā pene'


def test_comma_pounds_symbols_no_shillings():
    assert pakaru_moni('4,565 l. 4 d.') == 'pāuna moni whā mano, rima rau ono tekau mā rima, me ngā whā pene'


def test_pounds():
    assert pakaru_moni('£465,,3,,4') == 'pāuna moni whā rau ono tekau mā rima, me ngā toru herengi me ngā whā pene'


def test_pounds_no_shillings():
    # Tests that the lack of digit in the shillings position doesn't prevent pennies from being recognised as such
    assert pakaru_moni('£465,,0,,4') == 'pāuna moni whā rau ono tekau mā rima, me ngā whā pene'


def test_pounds_symbols():
    assert pakaru_moni('465 l. 3 s. 4 d.') == 'pāuna moni whā rau ono tekau mā rima, me ngā toru herengi me ngā whā pene'


def test_pounds_symbols_no_shillings():
    assert pakaru_moni('465 l. 4 d.') == 'pāuna moni whā rau ono tekau mā rima, me ngā whā pene'


def test_rā_kupu_digit_form():
    assert rā_kupu('12/03/24') == 'te tekau mā rua o ngā rā o Māehe i te tau o tō tātou Ariki kotahi mano, iwa rau rua tekau mā whā'


def test_day_month_year():
    assert rā_kupu('13 Hanuere 1843') == rā_kupu('Te 13 o Hanuere, 1843') == rā_kupu('Hanuere 13 1843') == rā_kupu('Hanuere 13, 1843') == 'te tekau mā toru o ngā rā o Hanuere i te tau o tō tātou Ariki kotahi rau waru tekau mā kotahi mano, waru rau whā tekau mā toru'


def test_month_year():
    assert rā_kupu('1843, Hanuere') == rā_kupu('Hanuere, 1843') == 'te marama o Hanuere i te tau o tō tātou Ariki kotahi rau waru tekau mā kotahi mano, waru rau whā tekau mā toru'


def test_day_month():
    assert rā_kupu('13 Hanuere') == rā_kupu('Te 13 o Hanuere') == rā_kupu('Hanuere 13') == 'te tekau mā toru o ngā rā o Hanuere'


def test_tāima_kupu():
    # Test the function works for different lengths and punctuation
    assert tāima_kupu('4:12 a.m') == tāima_kupu('45.04.12 a.m.') == 'tekau mā rua mai i te whā te wā i te ata'


def test_til_format_and_one_oclock():
    # Tests the '22 minutes to 1' format, and that one o'clock shows up as tahi rather than kotahi
    assert tāima_kupu('12. 38') == 'rua tekau mā rua ki te tahi te wā'


def test_am_to_pm():
    # Test the til format for the last am hour converts to pm
    assert tāima_kupu('23.11.45 a.m.') == 'hauwhā ki te tekau mā rua te wā i te ahiahitanga'


def test_comma_pakaru_moni():
    assert pakaru_moni('£3\' 030') == 'pāuna moni toru mano, toru tekau'


def test_comma_hōputu_tau():
    assert hōputu_tau('3’ 030') == 'toru mano, toru tekau'


def test_hautau_rānei_ira():
    assert hautau_rānei_ira('46/01') == '46 mā 01'


def test_pakaru_moni():
    assert pakaru_moni('£345') == 'pāuna moni toru rau whā tekau mā rima'


def test_hōputu_tau():
    assert hōputu_tau('23') == 'rua tekau mā toru'


def test_whakarauiri():
    # Test all the individual components at once, to ensure that calls to functions in whakarauiri are not in the wrong order, and matching parts of strings that should have been matched by a different function first.
    assert whakarauiri('£4,565,,3,,4 £4,565,,0,,4 £4,565..0.,4 4,565 l. 3 s. 4 d. 4,565 l. 4 d. £465,,3,,4 £465,,0,,4 465 l. 3 s. 4 d. 465 l. 4 d. 12/03/24 13 Hanuere 1843 Te 13 o Hanuere, 1843 Hanuere 13 1843 Hanuere 13, 1843 1843, Hanuere Hanuere, 1843 13 Hanuere Te 13 o Hanuere Hanuere 13 4:12 a.m 12. 38 23.11.45 a.m. 45.04.12 a.m. £3\' 030 3’ 030 46/01 £345 23') == 'pāuna moni whā mano rima rau ono tekau mā rima me ngā toru herengi me ngā whā pene pāuna moni whā mano rima rau ono tekau mā rima me ngā whā pene pāuna moni whā mano rima rau ono tekau mā rima me ngā whā pene pāuna moni whā mano rima rau ono tekau mā rima me ngā toru herengi me ngā whā pene pāuna moni whā mano rima rau ono tekau mā rima me ngā whā pene pāuna moni whā rau ono tekau mā rima me ngā toru herengi me ngā whā pene pāuna moni whā rau ono tekau mā rima me ngā whā pene pāuna moni whā rau ono tekau mā rima me ngā toru herengi me ngā whā pene pāuna moni whā rau ono tekau mā rima me ngā whā pene te tekau mā rua o ngā rā o Māehe i te tau o tō tātou Ariki kotahi mano iwa rau rua tekau mā whā te tekau mā toru o ngā rā o Hanuere i te tau o tō tātou Ariki kotahi rau waru tekau mā kotahi mano waru rau whā tekau mā toru te tekau mā toru o ngā rā o Hanuere i te tau o tō tātou Ariki kotahi rau waru tekau mā kotahi mano waru rau whā tekau mā toru te tekau mā toru o ngā rā o Hanuere i te tau o tō tātou Ariki kotahi rau waru tekau mā kotahi mano waru rau whā tekau mā toru te tekau mā toru o ngā rā o Hanuere i te tau o tō tātou Ariki kotahi rau waru tekau mā kotahi mano waru rau whā tekau mā toru te marama o Hanuere i te tau o tō tātou Ariki kotahi rau waru tekau mā kotahi mano waru rau whā tekau mā toru te marama o Hanuere i te tau o tō tātou Ariki kotahi rau waru tekau mā kotahi mano waru rau whā tekau mā toru te tekau mā toru o ngā rā o Hanuere te tekau mā toru o ngā rā o Hanuere te tekau mā toru o ngā rā o Hanuere tekau mā rua mai i te whā te wā i te ata rua tekau mā rua ki te tahi te wā hauwhā ki te tekau mā rua te wā i te ahiahitanga tekau mā rua mai i te whā te wā i te ata pāuna moni toru mano toru tekau toru mano toru tekau whā tekau mā ono mā tahi pāuna moni toru rau whā tekau mā rima rua tekau mā toru'
