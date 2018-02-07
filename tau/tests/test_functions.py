import context
from tau import *


def test_marama_kupu():
    assert rā_kupu('13 Hanuere 1843') == rā_kupu('Hanuere 13 1843') == rā_kupu('13 Hanuere, 1843') == rā_kupu('Hanuere 13, 1843') == 'te tekau mā toru o ngā rā o Hanuere i te tau o tō tātou Ariki kotahi rau waru tekau mā kotahi mano, waru rau whā tekau mā toru'
