import pytest
from loguru import logger
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
URL='https://cp.osgrm.ru/'
URL_INFO=('https://cp.osgrm.ru/#/info')
URL_DOCUMENTS=('https://cp.osgrm.ru/#/documents')
E_MAIL='testuser+qa-2@osgrm.ru'
PASSWORD='Test123-'
CASES=[
    #('Имя документа', '[data-placeholder="Имя документа"]',), #В разделе "Документы" отсутствует колонка "Имя документа"
    ('Barcode', '[data-placeholder="Штрих-код документа"]', 'R029256105', '[class="mat-cell cdk-cell mat-tooltip-trigger cdk-column-uf_barcode mat-column-uf_barcode cell-uf_barcode matCell ng-star-inserted"]'),
    ('Document type', '[data-placeholder="Тип документа"]', 'договор', '[class="mat-cell cdk-cell mat-tooltip-trigger cdk-column-uf_doc_type mat-column-uf_doc_type cell-uf_doc_type matCell ng-star-inserted"]'),
    ('Contractor', '[data-placeholder="Контрагент"]', 'ИП Лущик К.А.', '[class="mat-cell cdk-cell mat-tooltip-trigger cdk-column-uf_contractor mat-column-uf_contractor cell-uf_contractor matCell ng-star-inserted"]'),
    ('INN', '[data-placeholder="INN"]', '5687913638', '[class="mat-cell cdk-cell mat-tooltip-trigger cdk-column-uf_inn mat-column-uf_inn cell-uf_inn matCell ng-star-inserted"]'),
    ('KPP', '[data-placeholder="КПП"]', '771801001', '[class="mat-cell cdk-cell mat-tooltip-trigger cdk-column-uf_KPP mat-column-uf_KPP cell-uf_KPP matCell ng-star-inserted"]'),
    ('Date of document', '[class="mat-start-date mat-date-range-input-inner ng-untouched ng-pristine ng-valid"]', '20.09.2019', '[class="mat-cell cdk-cell mat-tooltip-trigger cdk-column-uf_docdate mat-column-uf_docdate cell-uf_docdate matCell ng-star-inserted"]')
]
@pytest.mark.parametrize('case_name, input, search_value, obtained_field', CASES)
def test_e2e(case_name, input, search_value, obtained_field, browser):
    """"
    Test case e2e view document
    """
    logger.info(f'CASE : {case_name}')
    browser.get(url=URL)    
    email_input=WebDriverWait(browser, timeout=20, poll_frequency=2).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[id="loginform-username-input"]')))
    email_input.send_keys(E_MAIL)
    password_input=WebDriverWait(browser, timeout=20, poll_frequency=2).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[id="loginform-password-input"]')))
    password_input.click()
    password_input.send_keys(PASSWORD)
    browser.find_element(by=By.CSS_SELECTOR, value='[id="loginform-enter-button"]').click()
    WebDriverWait(browser, timeout=20, poll_frequency=2).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[id="home-main-menu"]')))
    obtained_url_info=browser.current_url
    assert obtained_url_info==URL_INFO, 'Неверный URL главной страницы'
    WebDriverWait(browser, timeout=20, poll_frequency=2).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[id="documents-and-scans-menu"]'))).click()
    WebDriverWait(browser, timeout=20, poll_frequency=2).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[id="search-dialog-button-search"]')))
    obtained_url_info=browser.current_url
    assert obtained_url_info==URL_DOCUMENTS, 'Неверный URL раздела "Документы"'
    doc_id_input=WebDriverWait(browser, timeout=20, poll_frequency=2).until(EC.element_to_be_clickable((By.CSS_SELECTOR, input)))
    doc_id_input.click()
    doc_id_input.send_keys(search_value)
    browser.find_element(by=By.CSS_SELECTOR, value='[id="search-dialog-button-search"]').click()
    obtained_value=WebDriverWait(browser, timeout=20, poll_frequency=2).until(EC.visibility_of_element_located((By.CSS_SELECTOR, obtained_field)))
    assert obtained_value.text==search_value, 'Неверный результат поиска'
    actions=ActionChains(browser)
    actions.double_click(obtained_value).perform()
    doc_view=WebDriverWait(browser, timeout=20, poll_frequency=2).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[id="canvasImage"]')))
    assert doc_view.is_displayed(), "Документ не отображается"