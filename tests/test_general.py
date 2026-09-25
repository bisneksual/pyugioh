import json
from pytest import fixture

@fixture
def get_query_info():
    with open("data/query_info.json","r") as fp:
        query_info = json.load(fp)
    return query_info



def test_check():
    assert 2+2==4