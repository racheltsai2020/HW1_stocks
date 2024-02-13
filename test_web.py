import pytest
from bottle import Bottle, request
from webtest import TestApp

def create_test_app():
    test = Bottle()

    @test.route('/', method='GET')
    def home():
        return 'This is home page'

    @test.route('/result', method='POST')
    def result():
        sym = request.forms.get('sym')
        if sym:
            return sym
        else:
            return 'No Stock Symbol was entered, please go back and enter and Stock Symbol'

    @test.route('/stock/<ticker>', method='GET')
    def stock(ticker):
        if ticker == 'NVDA':
            return 'Stock information for NVDA'
        else:
            return 'The Stock Symbol you entered is not an actual symbol. Please go back and enter another one'

    @test.route('/top', method='GET')
    def pop():
        return 'Top page'

    return test

@pytest.fixture
def app():
    return TestApp(create_test_app())

def test_home(app):
    homePage = app.get('/')
    assert homePage.status_code == 200

def test_resultPage_valid_input(app):
    resultPage = app.post('/result', {'sym': 'NVDA'})
    assert resultPage.body == b'NVDA'

def test_resultPage_error_input(app):
    resultPage = app.post('/result', {'sym': ''})
    assert resultPage.body == b'No Stock Symbol was entered, please go back and enter and Stock Symbol'

def test_stock_valid_ticker(app):
    stockPage = app.get('/stock/NVDA')
    assert stockPage.status_code == 200

def test_stock_error_ticker(app):
    stockPage = app.get('/stock/HINICE')
    assert b'The Stock Symbol you entered is not an actual symbol. Please go back and enter another one' in stockPage.body

def test_top(app):
    topPage = app.get('/top')
    assert topPage.status_code == 200
