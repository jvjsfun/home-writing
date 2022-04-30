import asyncio
import aiohttp
import time

from importexport.utils import get_profile_data, UA


async def get_phpsession_id_async(pid):
    # print('Fetch async process {} started'.format(pid))
    start = time.time()
    _pdata = get_profile_data(pid)
    key = _pdata.get('key')
    _url = _pdata.get('home_url') + '/oauth/token'
    _credentials = {
        'client_id': _pdata.get('client_id'),
        'client_secret': _pdata.get('client_secret'),
        'username': _pdata.get('username'),
        'password': _pdata.get('password'),
        'grant_type': 'password'
    }
    _login_url = _pdata.get('login_url')
    _headers = {
        'referer': _login_url,
        'user-agent': UA
    }
    async with aiohttp.ClientSession(headers=_headers) as session:
        async with session.post(_url, data=_credentials) as auth:
            if auth.status != 200:
                return

            _auth_json = await auth.json()
            _token = _auth_json.get('access_token', '')
            _token_type = _auth_json.get('token_type', '')
            _headers2 = {
                'Authorization': '{} {}'.format(_token_type, _token),
                'Referer': _login_url,
                'User-Agent': UA
            }
            _url2 = _pdata.get('home_url') + '/api/v1/users/self/sessions'
            async with aiohttp.ClientSession(headers=_headers2) as session2:
                async with session2.post(_url2, data={}) as resp:
                    cookies = session2.cookie_jar.filter_cookies(_pdata.get('home_url'))
                    for k, v in cookies.items():
                        if k == 'PHPSESSID':
                            _cookie = v.value
                            break
                    # session_cookies[key] = _cookie
                    # print('Process {}: {}, took: {:.2f} seconds'.format(
                    #    pid, _cookie, time.time() - start))
                resp.close()
        auth.close()
    #session.close()
    return _cookie
