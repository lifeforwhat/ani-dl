# -*- coding: utf-8 -*-
import os
import argparse
from urllib.parse import unquote
try:
    import requests
    from qbittorrent import Client
    from sqlitedict import SqliteDict
    from bs4 import BeautifulSoup
except:
    os.system("pip install requests")
    os.system("pip install sqlitedict")
    os.system("pip install beautifulsoup4")
    os.system("pip install python-qbittorrent")
    import requests
    from sqlitedict import SqliteDict
    from bs4 import BeautifulSoup
    from qbittorrent import Client

def get_filename_from_cd(cd):
    """
    Get filename from content-disposition
    """
    import re
    if not cd:
        return None
    fname = re.findall('filename=(.+)', cd)
    if len(fname) == 0:
        return None
    return fname[0]


def main(args):
    if args.authorize_key == False or args.channel_id == False:
        print("authorize_key or channel_id is needed")
        time.sleep(3)
        return
    qb = Client('http://%s:%s/' %(args.qbit_ip , args.qbit_port), verify=args.qbit_secure)
    url = 'https://discordapp.com/api/v6/channels/%s/messages?limit=%s' % ( args.channel_id, '50')
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
        'authorization': args.authorize_key}
    res = requests.get(url, headers=headers)


    if res.status_code >= 300 :
        print(res)
        print("ERROR ON KEYS (authorize_key or channel_id)")
        return
    j = before_j = res.json()
    page_count = int(args.limit)
    while page_count > 1 :
        page_count += -1
        print("디스코드 페이지를 읽고 있습니다. %s 페이지 남았습니다." % page_count)
        # https://discordapp.com/api/v6/channels/697034062606630962/messages?before=699554317908312124&limit=50
        try:
            final_id = str(before_j[-1]['id'])
        except IndexError:
            print("더이상 찾을 수 있는 디스코드 페이지가 없습니다")
            break
        before_j = requests.get('https://discordapp.com/api/v6/channels/%s/messages?before=%s&limit=%s' % ( args.channel_id, final_id,'50'), headers=headers).json()
        j += before_j

    data = [item for item in j if item['author']['bot'] == True and item['author']['username'] == "data_001"] # data 봇이 뿌려주는 json 데이터만 모은다

    # ani-dl 0.2
    # 현재 탐색한 내용을 DB에 넣어준다
    """with SqliteDict('ani-dl.db') as db :
        for item in data: # sub_url 을 unique 로 쓴다
            item = json.loads(item['embeds'][0]['description'])
            if item['sub_url'] not in db:
                db[item['sub_url']] = item
        db.commit()

    # 다운 완료한 토렌트 정보를 ani-dl_completed.db에 넣어준다
    with SqliteDict('ani-dl.db') as db:
        with SqliteDict('ani-dl_completed.db') as complete_db:
            if args.compare_database == True:
                data = [db[item] for item in db if db[item]['sub_url'] not in complete_db]
            elif args.compare_database == False:
                data = [db[item] for item in db ]
            for item in data:
                if 'sub_url' not in item:
                    print(item)
                if item['sub_url'] not in complete_db:
                    complete_db[item['sub_url']] = True
            complete_db.commit()"""


    white_list = args.filter_title
    if white_list !=  None:
        white_list = [item.strip() for item in white_list.split('|')]
    print("FOUND",len(data))
    for item in data :
        con_js = json.loads(item['embeds'][0]['description'])
        # 온갖 필터링 옵션들
        if white_list != None :#and con_js['onnada']['title'] not in white_list:
            keep = False
            for w in white_list:
                if 'onnada' not in con_js:
                    print(con_js)
                if w.lower() in con_js['onnada']['title'].lower():
                    keep = True
            if keep == False:
                if args.verbose:
                    print("FILTERED BY filter_title , %s\t\t" % args.filter_title ,con_js['onnada'])
                continue

        # ongoing_check
        if args.ongoing_check == True and con_js['myanime']['payload']['status'].lower().count('finished') > 0 :
            continue

        # Year
        if args.specific_year != None and int(con_js['myanime']['payload']['start_year']) < int(args.specific_year): # myanime
            if args.verbose:
                print("FILTERED BY specific_year arugment\t\t",con_js['myanime']['payload'])
            continue

        # 옵션에 맞는 마그넷을 골라주는 과정
        true_mg = ""
        for mg in con_js['magnets']:
            if args.ignore_mass_torrents == True and len(re.findall('\d+ ~ \d+' , mg['title'])) > 0 : # 여러 에피소드 묶여있는 경우
                continue
            if args.resolution in mg['title']:
                true_mg = mg
                break

        # 못 찾았으면 다시 한 바퀴 돌린다
        if true_mg == "":
            for mg in con_js['magnets']:
                if args.ignore_mass_torrents == True and len(re.findall('\d+ ~ \d+', mg['title'])) > 0:  # 여러 에피소드 묶여있는 경우
                    if args.verbose:
                        print("FILTERED BY ignore_mass_torrents argument\t\t", mg['title'])
                    continue
                true_mg = mg
                break

        if true_mg != "" : # 쓸만한 마그넷을 찾았다.
            with SqliteDict('anime_torrent.db') as db:
                if true_mg['magnet'] in db:
                    if args.verbose:
                        print("ALREADY DOWNLOAD (anime_torrent.db)\t\t\t",true_mg['title'])
                    continue # 중복
                else:
                    db.update({true_mg['magnet'] : True})
                    db.commit()
            if true_mg['size'].count('GiB') > 0:
                if float(true_mg['size'].replace('GiB', '').strip()) > float(args.max_volume):
                    if args.verbose:
                        print("FILTERED BY max_volume arugment\t\t", true_mg)
                    continue
                    # Year
            if args.specific_year != None and int(true_mg['date'][:4]) > int(args.specific_year):  # torrent date
                if args.verbose:
                    print("FILTERED BY specific_year arugment\t\t", con_js['myanime']['payload'])
                continue
            print("DOWNLOADING\t\t",true_mg['title'])
            downpath = args.qbit_download_folder
            #qb.download_from_link(true_mg['magnet'] , category = args.qbit_category_name , savepath = downpath)
            res = requests.get(con_js['sub_url'])
            sub_ext = get_filename_from_cd(res.headers.get('content-disposition'))
            sub_ext = unquote(sub_ext).replace('"', '')
            sub_ext = os.path.splitext(sub_ext)[1]
            sub_filename = os.path.splitext(true_mg['title'])[0] + sub_ext
            open(os.path.join(downpath, sub_filename) , 'wb' ).write(res.content)
            # 어차피 nyaa.si 에서만 다운받으니깐.


            magnet = true_mg['magnet'] + "&tr=http%3A%2F%2Fnyaa.tracker.wf%3A7777%2Fannounce&tr=udp%3A%2F%2Fopen.stealth.si%3A80%2Fannounce&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337%2Fannounce&tr=udp%3A%2F%2Ftracker.coppersurfer.tk%3A6969%2Fannounce&tr=udp%3A%2F%2Fexodus.desync.com%3A6969%2Fannounce"
            qb.download_from_link(magnet, category=args.qbit_category_name, savepath=downpath)
            continue



if __name__ == '__main__':
    import time , json , re
    parser = argparse.ArgumentParser(description="애니메이션 Qbittorrent 자동 다운로드, 버전 0.6")
    parser.add_argument("-k","--authorize_key" , type=str,help="인증용 KEY" , default=False)
    parser.add_argument("-c","--channel_id", type=str,help="채널 ID", default=False)
    parser.add_argument("-r", "--resolution" , help="특정 화질 우선 다운로드, 기본값 1080"  , default="1080")
    parser.add_argument("-l", "--limit" , help="탐색값. 숫자가 커질수록 시간이 길어짐. 기본값 2 (페이지 숫자를 말함)"  , default="10")
    parser.add_argument("-q", "--qbit_ip" , help="qbittorrent IP , 기본값 127.0.0.1"  , default="127.0.0.1")
    parser.add_argument("-p", "--qbit_port", help="qbittorrent port, 기본값 8080", default="8080")
    parser.add_argument("-s", "--qbit_secure", help="qbittorrent verify, 기본값 False", default=False)
    parser.add_argument("-d", "--qbit_download_folder", help="qbittorrent download path, 기본값 현재위치", default=os.getcwd())
    parser.add_argument("-ca", "--qbit_category_name", help="qbittorrent category(범주) label name, 기본값 latest_anime", default='latest_anime')
    parser.add_argument("-o", "--ongoing_check", help="현재 방영중인 것만 받기, 기본값 False", default=False)
    parser.add_argument("-y", "--specific_year", help="특정 년도 이상만 받기, 가령 2019면 2019,2020만. 기본값 2020", default="2020")
    parser.add_argument("-f", "--filter_title", help="특정 타이틀만 받기. 구분자 | (쉬프트 + \) , 해당 키워드가 파일 이름또는 디스코드 타이틀에 포함되어 있지 않으면 무시한다.(BETA)", default=None)
    parser.add_argument("-m", "--ignore_mass_torrents", help="여러 에피소드가 묶여있는 토렌트는 무시한다, 기본값 True", default=True)
    parser.add_argument("-max", "--max_volume", help="특정 용량 넘어가는 토렌트 받지 않기, 기본값 3GB", default="3")
    parser.add_argument("-v", "--verbose", help="필터링 된 토렌트 파일 로그 띄우기, 기본값 False", default=False)
    #parser.add_argument("-db", "--compare_database", help="최근에 한 번 검색 또는 다운로드됐던 정보는 무시, 커맨드 창 관리에 용이, 기본값 True", default=True)
    args = parser.parse_args()
    print('authorize_key :',args.authorize_key)
    print('channel_id :',args.channel_id )

    main(args)
