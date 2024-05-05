import io
import json
import requests
import pandas as pd

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

@data_loader
def load_data_from_api(*args, **kwargs):
    """
    Template for loading data from API
    """
    # url = 'http://maps.googleapis.com/maps/api/elevation/json?locations=42.974049,-81.205203|42.974298,-81.195755&sensor=false'
    # response = requests.get(url)
    # print(response.text)
    
    # data = json.loads(response.text)
    # print(data)
    # df = pd.json_normalize(data)
    spartan_token = "v4=eyJhbGciOiJkaXIiLCJlbmMiOiJBMTI4R0NNIiwia2lkIjoidXJuOjM0MzpzMzpzdDpwcm9kdWN0aW9uOmNlayIsInppcCI6IkRFRiJ9..0V4_FdtGGpXIYEB6.H2YUre63Fkl1AzifSMAdJYsNR9Y8tRuPT1Epi4mwsDyjkqupj1Sh1wtB0U29daTkk-bmXipGl47aLUSqqji3nu2B7L2QggOocYaHpQzLnmU7rUkN-_FwxxmzbdISR1wANufaKK5wi5eH6xOUJvTld5XhclC06jELf2PmGxoivamp3HG5Bt7tI-KXDnd2b_kHzdigW7XNrG9XlUkRAeyrgmUNfmLb2_IeLPmoW4XMDLZCGt4ZTycI0BENbVF8SndqabIfJ2pQnBuye3Vx0oUX817MEZSf0uY3SfN9MPZYvijKWugCJy5fbi5MvAbm7tcG5PN4jImzizFYkOwsGwzKeh51GBPvUo-kJofSuJsRb-3fLKP5JGPw69CiO-QSibXX114uEtt277Ql50aoARg7sSbws1_4KO9Buv2gFHW9DpjCjV1lmKzdZ1WYPmJ5gqRNkDLmm7p1SO1MVKcWDALQOs-oKNJ1E_X1tsnXommq4op6gQP8ktKjzddB3wYTzz5mwa9l7fpYxN1Jrz7ovhmDLEi2b3LTeo9rI6asTCE08n8Sp0m9v2GWa8-Z0ipmsv7AJlBA8bGeU1SRmzn5nbPRgfbiHadFHGHEMGwe0IE1ccJiqe8RmMUDSrWHCBBeWw2dHHwbT3vq9fqv2u9beIitsrq-flLefojRsMayzqLUZUaCyq7SUkznuLMbNTu7GIZZ5jhqeNZ19lOws2Zqdow6gue37ZXod-Uz91p78wbdHrQV3rUYfE4XYZlwGDPz2jUGol5GLgOT2Th9DPAHa6KM7-c-inqDCh0P6aaKTHuMAHBR0egRyp3CgvMO8nATQ2FnkszF_MIp9LcKs9_2s1oR-tqaMcec6A.o9YhJmXXfS1lfGGdPvd9EA"

    xuid = 2533274848622227

    headers = {"x-343-authorization-spartan": spartan_token,
               "Accept": "application/json"
    }

    response = requests.get('https://halostats.svc.halowaypoint.com/hi/players/xuid({})/matches'.format(xuid), headers=headers)
    print(response)
    #r3 = response.json()

    data = json.loads(response.text)
    #print(data)
    df = pd.json_normalize(data["Results"])

    #print(r3)


    return df


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
