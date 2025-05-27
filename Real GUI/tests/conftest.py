import pytest

def pytest_addoption(parser):
    parser.addoption("--fpga", action="store", default="fpga-101.local",  help="fpga host name , i.e. fpga-101.local")
    parser.addoption("--dir", action="store", default='/media/disk/sp',  help="deploy directory")
    parser.addoption("--num", action="store", default=5,  help="number of tests")

@pytest.fixture(scope="module")
def cmdopt(request):
    return request.config.getoption("--fpga")

@pytest.fixture(scope="module")
def diropt(request):
    return request.config.getoption("--dir")


@pytest.fixture(scope="module")
def num_of_tests(request):
    return int(request.config.getoption("--num"))
