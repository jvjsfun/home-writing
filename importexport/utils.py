import lxml
import time
import requests

from django.conf import settings

SNIPPET_ID_ATTR_NAME = 'data-partner-landing-page-snippet-id'
LANDING_SNIPPET = '/seo/writer/landingPage/snippet/next'
UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 '
'(KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'

PROFILE_DATA = {
    'lorenzo': {
        'key': 'lorenzo',
        'password': 'Lo1402',
        'username': 'lorenzo.writing@gmail.com',
        'client_id': 'prontopro-platform-ch',
        'client_secret': 'GLNYLgrrB7AM9cQjtq5QqRW5',
        'login_url': settings.PRONTOPRO_BASE_URL + 'ch/de/login',
        'root_domain': 'ch',
        'home_url': settings.PRONTOPRO_BASE_URL + 'ch',
        'admin_url': settings.PRONTOPRO_BASE_URL + 'ch/admin',
        'protected_page': settings.PRONTOPRO_BASE_URL + 'ch/admin' + LANDING_SNIPPET,
        'sheetname': 'Snippet Writer Tool CH_Lorenzo'
    },
    'benni': {
        'key': 'benni',
        'password': 'Beera1406',
        'username': 'benni.wolf09@gmail.com',
        'client_id': 'prontopro-platform-at',
        'client_secret': 'KyFWB7qgrSzT9Ffpf5METhqU',
        'login_url': settings.PRONTOPRO_BASE_URL + 'at/login',
        'root_domain': 'at',
        'home_url': settings.PRONTOPRO_BASE_URL + 'at',
        'admin_url': settings.PRONTOPRO_BASE_URL + 'at/admin',
        'protected_page': settings.PRONTOPRO_BASE_URL + 'at/admin' + LANDING_SNIPPET,
        'sheetname': 'Snippet Writer Tool AT_Benjamin'
    },
    'martina': {
        'key': 'martina',
        'password': 'Ma1413',
        'username': 'martina.dresdner@eclipso.at',
        'client_id': 'prontopro-platform-at',
        'client_secret': 'KyFWB7qgrSzT9Ffpf5METhqU',
        'login_url': settings.PRONTOPRO_BASE_URL + 'at/login',
        'root_domain': 'at',
        'home_url': settings.PRONTOPRO_BASE_URL + 'at',
        'admin_url': settings.PRONTOPRO_BASE_URL + 'at/admin',
        'protected_page': settings.PRONTOPRO_BASE_URL + 'at/admin' + LANDING_SNIPPET,
        'sheetname': 'Snippet Writer Tool AT_Martina'
    },
    'linda': {
        'key': 'linda',
        'password': 'Li1415',
        'username': 'linda-welle@web.de',
        'client_id': 'prontopro-platform-ch',
        'client_secret': 'GLNYLgrrB7AM9cQjtq5QqRW5',
        'login_url': settings.PRONTOPRO_BASE_URL + 'ch/de/login',
        'root_domain': 'ch',
        'home_url': settings.PRONTOPRO_BASE_URL + 'ch',
        'admin_url': settings.PRONTOPRO_BASE_URL + 'ch/admin',
        'protected_page': settings.PRONTOPRO_BASE_URL + 'ch/admin' + LANDING_SNIPPET,
        'sheetname': 'Snippet Writer Tool CH_Linda'
    }
}


def clear_wks_column(worksheet, range_value, start=None):
    """
        This method is called for each new loop of snippets generated.
        Cleans the cells that make the calcs
    """
    cell_list = worksheet.range(range_value)
    for cell in cell_list:
        cell.value = ''
    print("Process took: {:.2f} seconds".format(time.time() - start))
    worksheet.update_cells(cell_list)
    print("Process took: {:.2f} seconds".format(time.time() - start))


def get_profile_data(profile_id):
    if profile_id == 1:
        return PROFILE_DATA.get('lorenzo')
    elif profile_id == 2:
        return PROFILE_DATA.get('benni')
    elif profile_id == 3:
        return PROFILE_DATA.get('martina')
    elif profile_id == 4:
        return PROFILE_DATA.get('linda')


def get_phpsession_id(pdata):
    _url = pdata.get('home_url') + '/oauth/token'
    _credentials = {
        'client_id': pdata.get('client_id'),
        'client_secret': pdata.get('client_secret'),
        'username': pdata.get('username'),
        'password': pdata.get('password'),
        'grant_type': 'password'
    }
    _login_url = pdata.get('login_url')
    _headers = {
        'referer': _login_url,
        'user-agent': UA
    }
    _auth = requests.post(_url, data=_credentials, headers=_headers)
    if _auth.status_code == 200:
        _auth_json = _auth.json()
        _token = _auth_json.get('access_token', '')
        _token_type = _auth_json.get('token_type', '')
        _session = requests.post(
            pdata.get('home_url') + '/api/v1/users/self/sessions', data={},
            headers={
                'Authorization': '{} {}'.format(_token_type, _token),
                'Referer': _login_url,
                'User-Agent': UA
            }
        )
        return _session.cookies.get('PHPSESSID')


def get_loggedin_username(html_as_text):
    html = lxml.etree.HTML(html_as_text)
    return html.xpath('/html/body/nav/div[3]/div/div/text()')
