import bs4 as bs
import datetime
import lxml
import random
import requests
import time

import asyncio
import aiohttp

import gspread

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render

from importexport.async_tasks import get_phpsession_id_async
from importexport.models import Snippet
from importexport.gapi_signals import get_credentials
from importexport.utils import clear_wks_column
from importexport.utils import get_profile_data, get_phpsession_id, UA
from importexport.utils import get_loggedin_username, SNIPPET_ID_ATTR_NAME

# Constants
HEAD = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest",
    "Connection": "keep-alive",
}
session_cookies = {}


@login_required()
def home(request):
    """
        Returns home.html
    """
    return render(request, 'home.html', {})


#@login_required()
#def set_timesleep(request):
#    return JsonResponse({'status': 0}, content_type='application/json', safe=False)


@login_required()
def login_prontopro(request):
    """
        1 -  login with the credentials using python-requests
            - For more security, store in environment variable and call using os.environ['ENV_VAR']
        2 - The app returns a dict with the PHPSESSID
    """
    # start = time.time()
    global session_cookies

    async def asynchronous_login():
        futures = [get_phpsession_id_async(i) for i in range(1, 5)]
        for pid, future in enumerate(asyncio.as_completed(futures)):
            _cookie = await future
            key = get_profile_data(pid + 1).get('key')
            session_cookies[key] = _cookie
            # print('{}: {} {}'.format(key, ">>" * (pid + 1), _cookie))

    ioloop = asyncio.new_event_loop()
    asyncio.set_event_loop(ioloop)
    # print('Asynchronous login:')
    ioloop.run_until_complete(asynchronous_login())
    ioloop.close()
    # print("Asynchronous login: {:.2f} seconds".format(time.time() - start))
    # print(session_cookies)
    return JsonResponse(session_cookies, content_type='application/json', safe=False)


@login_required()
def send_data_to_sheet(request, phpsessid, profile):
    """
        STEP 1 - The method:
            1 - Checks the profile and connect by phpssessid
            2 - With BeautifulSoup we get the keywords
            3 - Send Keywords to gsheet respective
    """
    start = time.time()
    global session_cookies

    if phpsessid is None:
        phpsessid = get_phpsession_id(_pdata)
        session_cookies[_pdata.get('key')] = phpsessid

    cookies = {
        "PHPSESSID": phpsessid,
    }
    _pdata = get_profile_data(profile)

    with requests.session() as session:
        get_s = session.get(
            url=_pdata.get('protected_page'), headers=HEAD, cookies=cookies)
        # print(get_s.status_code, profile, cookies)
        if get_s.status_code == 401:
            phpsessid = get_phpsession_id(_pdata)
            session_cookies[_pdata.get('key')] = phpsessid
            return send_data_to_sheet(request, phpsessid, profile)
        print(get_loggedin_username(get_s.text))

        # parse_html
        soup = bs.BeautifulSoup(get_s.text, 'html.parser')
        tables_keywords = soup.find_all('tr', class_='soft')
        soup_tk = tables_keywords[0].find_next("tr").td.ul.find_all('li')
        topkw_list = [t["data-keyword"] for t in soup_tk]
        # print(topkw_list, len(topkw_list))
        soup_ok = tables_keywords[1].find_next("tr").td.ul.find_all('li')
        other_list = [t["data-keyword"] for t in soup_ok]
        # print(other_list, len(other_list))
        # For name and city
        table_bk = soup.find_all('table', class_='backend-listing')[2]
        name = table_bk.find(id='merchant-name-full').text
        # City
        ortschaft = table_bk.find_all('tr')[3]
        city = ortschaft.find_all('td')[1].text
        # BizClass
        bizclasstext = soup.find_all('h2')[0].text
        bizclass = bizclasstext.split('Servicekategorie "')[1].split('" scheint')[0]
        print("Get Keywords Process took: {:.2f} seconds".format(time.time() - start))

        # auth to GAPI
        gc = gspread.authorize(get_credentials())
        spreadsheet = gc.open(_pdata.get('sheetname'))
        print(profile, spreadsheet)
        wks = spreadsheet.worksheet("Export")
        #clear_wks_column(wks, 'A2:A100', start)
        #clear_wks_column(wks, 'H2:H100', start)
        print("Clear Google Sheets Process took: {:.2f} seconds".format(time.time() - start))

        #import gspread_asyncio
        #async def asynchronous(agcm):
        #    start = time.time()
        #    agc = await agcm.authorize()
        #    ss = await agc.open(_pdata.get('sheetname'))
        #    wks = await ss.worksheet('Export')
        #    tasks = [
        #        ioloop.create_task(clear_wks_column_async(wks, 1, 100, start)),
        #        ioloop.create_task(clear_wks_column_async(wks, 8, 100, start))
        #    ]
        #    await asyncio.wait(tasks)
        #    print("Process took: {:.2f} seconds".format(time.time() - start))

        #ioloop = asyncio.new_event_loop()
        #asyncio.set_event_loop(ioloop)
        #agcm = gspread_asyncio.AsyncioGspreadClientManager(get_credentials)
        #ioloop.run_until_complete(asynchronous(agcm))
        #ioloop.close()

        # to google spreadsheets. 1
        i = 0
        cell_list = wks.range('A2:A150')  # cell_list_topkw
        cell_list.extend(wks.range('H2:H150'))  # cell_other_list
        cell_list.extend(wks.range('Q2:Q2'))  # name
        cell_list.extend(wks.range('S2:S2'))  # city
        cell_list.extend(wks.range('O3:O3'))  # bizclass
        for cell in cell_list:
            # print(cell, cell.row, cell.col)
            if cell.col in (1, 8):
                if cell.col == 1:
                    _list = topkw_list
                if cell.col == 8:
                    _list = other_list

                try:
                    cell.value = _list[i]
                except:
                    cell.value = ''

                if i == 148:
                    i = 0
                else:
                    i += 1

            if cell.col == 17 and cell.row == 2:
                cell.value = name
            if cell.col == 19 and cell.row == 2:
                cell.value = city
            if cell.col == 15 and cell.row == 3:
                cell.value = bizclass
        wks.update_cells(cell_list)

        #wks.update_cell(2, 17, name)
        #wks.update_cell(2, 19, city)
        #wks.update_cell(3, 15, bizclass)
        print("Update Google Sheets Process took: {:.2f} seconds".format(time.time() - start))
        if request.GET.get('with_snippet'):
            return read_snippets(
                request, profile, spreadsheet, cookies,
                from_date=datetime.datetime.now()
            )
    return JsonResponse(cookies, content_type='application/json', safe=False)


@login_required()
def read_snippets(request, profile, spreadsheet=None, cookies=None, from_date=False):
    """
        STEP 2 - The Method:
            1 - Access the sheet by profile credentials
            2 - Get the snippets information, store in database
            3 - Return the information about the save and the quantity of snippets (title + description)

        PS: Here was where I stopped, because the app in the server is open the wrong sheet for lorenzo.
        the commeneted line 173 works to lorenzo, but no to benni, both benni and lorenzo should points
        to the Final_Import worksheet (in current dev)

    """
    if spreadsheet is None:
        gc = gspread.authorize(get_credentials())
        #wks = gc.open("Import <-> Export").worksheet("Import")
        _pdata = get_profile_data(profile)
        spreadsheet = gc.open(_pdata.get('sheetname'))

    wks = spreadsheet.worksheet("Final_Import")
    title, desc, b3 = wks.range('B1:B3')
    # print(profile, 'title=', title.value, '\ndesc=', desc.value)
    snippet = Snippet(
        title=title.value, description=desc.value, keywords=b3.value,
        profile=profile)
    snippet.status = 1
    snippet.save()
    qs = Snippet.objects.exclude(status=Snippet.CANCELLED)
    _date = request.GET.get('from')
    if _date:
        qs = qs.filter(
            date__gte=datetime.datetime.strptime(_date, '%Y-%m-%dT%H:%M:%S.%f%z')
        )
    if from_date:
        qs = qs.filter(date__gte=from_date)
    return JsonResponse(
        {'saved': True, 'total': qs.count(), 'cookies': cookies},
        content_type='application/json', safe=False)


@login_required()
def pop(request):
    """
        STEP 3 - This method check if the snippet exists and return the top by 'pop'
    """
    resp = {}
    qs = Snippet.objects.filter(status=1)
    if qs.exists():
        snippet = qs.order_by('status').first()
        #snippet.status = 1
        # snippet.save()
        resp = {
            'id': snippet.id,
            'profile': snippet.profile,
            'title': snippet.title,
            'keywords': snippet.keywords,
            'description': snippet.description
        }
    return JsonResponse(resp, content_type='application/json', safe=False)


def add_history(profile, title, desc):
    """
        This function is one to add the success data to 'history' worksheet of spreadsheet.
    """
    gc = gspread.authorize(get_credentials())
    _pdata = get_profile_data(profile)
    spreadsheet = gc.open(_pdata.get('sheetname'))
    wks = spreadsheet.worksheet("history")
    #print(title, desc)
    _now = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    try:
        wks.append_row(
            [title, '{}'.format(desc), _now])
    except gspread.exceptions.APIError:
        _desc = 'Profile {} ({})'.format(profile, _pdata.get('username'))
        wks.append_row(
            ['Error', _desc, _now])


@login_required()
def send_snippets(request, profile, id_snippet, phpsessid=None):
    start = time.time()
    _desc = request.GET.get('description')
    _title = request.GET.get('title')
    _phpsessid = request.GET.get('phpsessid')
    cookies = {
        "PHPSESSID": phpsessid or _phpsessid,
    }
    _pdata = get_profile_data(profile)

    result = {}
    with requests.session() as session:
        _home_url = _pdata.get('home_url')
        _protected_page = _pdata.get('protected_page')
        get_s = session.get(
            url=_protected_page, headers=HEAD, cookies=cookies)
        # print(get_s.status_code, profile, cookies)
        if get_s.status_code == 401:
            phpsessid = get_phpsession_id(_pdata)
            global session_cookies
            session_cookies[_pdata.get('key')] = phpsessid
            cookies["PHPSESSID"] = phpsessid
            return send_snippets(request, profile, id_snippet, phpsessid)
        print('send snippet to', get_s, get_loggedin_username(get_s.text))

        # get ID of Snippet from html page
        # xpath:
        # //*[@id="confirm-snippet"]
        _doc = lxml.etree.HTML(get_s.text)
        _id = _doc.xpath('//*[@id="confirm-snippet"]')[0].attrib[SNIPPET_ID_ATTR_NAME]

        _url = _home_url + '/admin/seo/api/writer/snippet/{}/close'.format(_id)
        # print('sending', _url)
        _response = session.post(
            _url, data={
                'title': _title,
                'text': _desc,
            },
            headers={
                "X-Requested-With": "XMLHttpRequest",
                "Referer": _protected_page,
                "User-Agent": UA
            },
            cookies=cookies
        )
        # print(_response, _response.text)
        if _response.status_code == 500:
            result = _response.json()
        snp = Snippet.objects.get(id=id_snippet)
        snp.title = _title
        snp.description = _desc
        if _response.status_code == 200:
            result['msg'] = 'OK'
            add_history(profile, snp.title, snp.description)
            snp.status = 3
            snp.save()
        else:
            result['msg'] = 'ERROR'
            add_history(profile, snp.title, snp.description)
            snp.status = 2
            snp.save()
    # print("Process took: {:.2f} seconds".format(time.time() - start))
    return JsonResponse(result, content_type='application/json', safe=False)


def get_all_snippets(request):
    """
        Just a single method that brings all snippets to fill the datatable
    """
    snippets = Snippet.objects.values(
        'profile', 'title', 'description', 'status').order_by('status')
    snippets_json = {
        "data": list(snippets)
    }
    return JsonResponse(snippets_json, safe=False)


def cancel_all_snippets(request):
    """
        Just a single method that cancel all snippets with status = QUEUED
    """
    snippets = Snippet.objects.filter(status=Snippet.QUEUED).update(
        status=Snippet.CANCELLED)
    return JsonResponse({'count': snippets, 'success': True}, safe=False)
