SUPPORTS ONLY PYTHON 3

SUPPORTS ONLY Qbittorrent

version 0.6
=========
--specific_year 를 좀 더 포괄적으로 사용 가능.

토렌트 생성년도 또는 방영 시작년도 둘 중 하나라도 만족하면 다운로드.

--verbose 추가 (필터 로그를 다 보여줌)


version 0.5
==========
DB기능 삭제

특정 용량 이상 다운로드 제한 옵션 추가 (--max_volume, 기본값 3GB)

version 0.4
==========
--filter_title 수정.
해당하는 키워드를 '포함'하면 다운로드 진행


version 0.3
===========
Bug Fix

version 0.2
==========
DB added

version 0.1
==========
support qbittorrent ONLY



디스코드 토큰 얻는법
=========================================
![토큰](https://camo.githubusercontent.com/c2b81974c4c3805873fccd916c5cec055bbdb3a7/68747470733a2f2f692e696d6775722e636f6d2f6a68674f554c702e676966)


채널 ID
=========================================
FIX : 697034062606630962



사용법
==========
 ```
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
parser.add_argument("-f", "--filter_title", help="특정 타이틀만 받기. 구분자 | (쉬프트 + \) (BETA)", default=None)
parser.add_argument("-m", "--ignore_mass_torrents", help="여러 에피소드가 묶여있는 토렌트는 무시한다, 기본값 True", default=True)
parser.add_argument("-db", "--making_DB", help="DB에 있는 중복 파일은 무시, 기본값 True", default=True)
```
    
    
위 명령어를 참조하시고



```
python ani-dl.py -k {개인 디스코드 KEY} -c {채널 ID} --qbit_download_folder "F:\애니\애니ONGOING" --qbit_ip 192.168.1.5 --qbit_port 20000
```

이런 식으로 사용하시면 됩니다.





```
특정 애니메이션만 탐색하고 싶을 때
python ani-dl.py -k {개인 디스코드 KEY} -c {채널 ID}  --qbit_download_folder "F:\애니\애니ONGOING" --limit 20 --filter_title "원피스|Hero academia"
```



```
특정 애니메이션만 탐색하고 싶고, 특정 년도 이상만 탐색하고 싶을 때
python ani-dl.py -k {개인 디스코드 KEY} -c {채널 ID}  --qbit_download_folder "F:\애니\애니ONGOING" --limit 20 --filter_title "원피스|Hero academia" --specific_year 2020

다만 이 경우에는 --limit 인자의 값을 크게 주어야만 합니다.
왜냐하면, 이런 search 모드의 경우 많은 데이터베이스를 필요로 하며 탐색 시간 또한 오래걸립니다.
그러나 값을 1000 이상 너무 큰 값을 잡아버리면 에러가 발생할 수 있으므로 적절한 값을 찾아가는 것이 중요합니다.

```



```
올해의 원피스를 다운받고 싶다면,

python ani-dl.py -k {개인 디스코드 KEY} -c {채널 ID}  --qbit_download_folder "F:\애니\애니ONGOING" --limit 100 --filter_title "원피스" --specific_year 2020

이 정도 입력하시면 됩니다.

--limit 값은 조절할 필요가 있습니다.

```
