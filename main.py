import os
import sys
import re
import json
import base64
from urllib.request import urlretrieve

#Drag and Drop 처리
try:
    droppedFile = sys.argv[1]
    print(droppedFile)
except IndexError:
    droppedFile = 'example.json'
    print("No file dropped")

path, ext = os.path.splitext(droppedFile)
ext = ext.lower()

#Json 열기
file = open(droppedFile, 'rt', encoding='UTF-8')
jsonString = json.load(file)


#json 일경우
if ext == '.json' or ext == '.bplist':
    # 폴더 생성 함수
    def createFolder(dir):
        try:
            if not os.path.exists(dir):
                os.makedirs(dir)
        except:
            print('폴더 생성 실패 ->' + dir)


    #플레이리스트의 곡 개수
    songLen = len(jsonString.get('songs'))

    #플레이 리스트 제목 폴더 생성
    createFolder("./"+jsonString.get('playlistTitle'))

    #커버 저장
    try:
        imgdata = base64.b64decode(jsonString.get('image').split(',')[1])
        filename = jsonString.get('playlistTitle')+'_cover.png'
        with open(filename, 'wb') as f:
            f.write(imgdata)
        print("\n커버이미지 저장완료 \t->"+filename+"\n")
    except:
        print("\n커버 이미지 없음")

    #맵 파싱 및 다운로드
    cnt=0
    for i in jsonString.get('songs'):
        cnt += 1
        print(str(songLen)+"곡 중 "+str(cnt)+"번째 다운로드 중... "+i.get('songName'))
        try:
            filename = re.sub('[\/:*?"<>|]', '', i.get('songName')) + '.zip'
            urlretrieve("https://cdn.beatsaver.com/"+i.get('hash').lower()+".zip", "./" + jsonString.get('playlistTitle') + "/" + filename)
        except:
            print("https://cdn.beatsaver.com/"+i.get('hash').lower()+".zip")
            print("다운로드 중 에러 발생")
    print("\n곡 모음집 다운로드 완료\n")
else:
    print("\n올바른 파일을 드래그 해주세요 \n.bplist 및 .json파일만 지원합니다.\n")

os.system("pause")
