import cv2
import datetime
import glob
import moviepy.editor as mp
import os
import requests
import sqlite3
import youtube_dl
from alpGenerator import alpGenerator
from bs4 import BeautifulSoup
from getWritingSettings import *
from PIL import Image, ImageDraw, ImageFont


class makeLyricsVideo:
    """
    노래 가사 영상을 최대한 간편하게 제작할 수 있도록 도와주는 클래스
    :param Name: 영상 이름
    """

    def __init__(self, name: str) -> None:
        self.videoName = name
        self.makeDir()

    def makeDir(self) -> None:
        """
        영상 제작에 필요한 파일들을 저장하는 디렉토리 생성 메서드
        """
        fileTypes = ["Images", "Lyrics", "Musics", "Videos"]
        try:
            # is exist
            os.chdir("../../Outputs")
            os.mkdir(self.videoName)
            os.chdir(f"./{self.videoName}")
            for fileType in fileTypes:
                os.mkdir(fileType)
        except:
            print("이미 같은 제목의 영상이 있습니다.")
        os.chdir("../../Python/Files")

    def getLyrics(self) -> None:
        """
        영상에 들어갈 가사를 스크래핑 하는 메서드
        """
        fileCreate = open(
            f"../../Outputs/{self.videoName}/Lyrics/lyrics.txt", "w", encoding="cp949"
        )
        basicURL = "https://music.bugs.co.kr/search/integrated?q="
        song = input("노래 제목 - 가수 입력\n> ")
        searchURL = basicURL + song
        searchHtml = requests.get(searchURL).text
        searchSoup = BeautifulSoup(searchHtml, "html.parser")
        lyricsBtnTag = searchSoup.find("a", {"class": "trackInfo"})
        lyricsURL = lyricsBtnTag["href"]
        lyricsHtml = requests.get(lyricsURL).text
        lyricsSoup = BeautifulSoup(lyricsHtml, "html.parser")
        lyricsTag = lyricsSoup.find("xmp")
        lyrics = lyricsTag.text
        lyricsLines = list(lyrics.split("\r\n"))
        enter = lyricsLines.count("")
        for _ in range(enter):
            lyricsLines.remove("")
        fileCreate.write(f"{song}\n#\n")
        for i in range(len(lyricsLines)):
            if i % 2 == 0:
                fileCreate.write(f"{lyricsLines[i]}\n")
            else:
                fileCreate.write(f"{lyricsLines[i]} #\n")
        fileCreate.write("#\n")
        fileCreate.close()

    def makeTitleImg(self) -> None:
        """
        영상에 들어갈 제목 사진을 만드는 메서드
        """
        self.lyricsFile = open(
            f"../../Outputs/{self.videoName}/Lyrics/lyrics.txt", "r", encoding="cp949"
        )
        self.titleLine = self.lyricsFile.readline()
        title, singer = self.titleLine.split("-")
        self.fontsFolder = "../../Settings/Fonts"
        bgImg = Image.open("../../Settings/Images/background/background.jpg")
        draw = ImageDraw.Draw(bgImg)
        selectedFont = ImageFont.truetype(
            os.path.join(self.fontsFolder, ValSet["PreFace - Maker"]["Font"]),
            int(ValSet["PreFace - Maker"]["FontSize"]),
        )
        draw.text(
            (
                int(ValSet["PreFace - Maker"]["PosX"]),
                int(ValSet["PreFace - Maker"]["PosY"]),
            ),
            text=SystemVal["Maker"],
            fill=ValSet["PreFace - Maker"]["Color"],
            font=selectedFont,
        )
        selectedFont = ImageFont.truetype(
            os.path.join(self.fontsFolder, ValSet["TitlePage - Title"]["Font"]),
            int(ValSet["TitlePage - Title"]["FontSize"]),
        )
        draw.text(
            (
                int(ValSet["TitlePage - Title"]["PosX"]),
                int(ValSet["TitlePage - Title"]["PosY"]),
            ),
            text=f"{title}",
            fill=ValSet["TitlePage - Title"]["Color"],
            font=selectedFont,
        )
        selectedFont = ImageFont.truetype(
            os.path.join(self.fontsFolder, ValSet["TitlePage - Singer"]["Font"]),
            int(ValSet["TitlePage - Singer"]["FontSize"]),
        )
        draw.text(
            (
                int(ValSet["TitlePage - Singer"]["PosX"]),
                int(ValSet["TitlePage - Singer"]["PosY"]),
            ),
            text=f"{singer}",
            fill=ValSet["TitlePage - Singer"]["Color"],
            font=selectedFont,
        )
        bgImg.save(f"../../Outputs/{self.videoName}/Images/aa.jpg")
        blankLine = self.lyricsFile.readline()

    def makeImgs(self) -> None:
        """
        영상에 들어갈 가사가 적힌 사진을 만드는 메서드
        """
        curLine1 = self.lyricsFile.readline().split("#")[0]
        curLine2 = self.lyricsFile.readline().split("#")[0]
        nextLine = self.lyricsFile.readline().split("#")[0]
        alps = list(alpGenerator())
        idx = 0
        while curLine1:
            bgImg = Image.open("../../Settings/Images/background/background.jpg")
            draw = ImageDraw.Draw(bgImg)
            selectedFont = ImageFont.truetype(
                os.path.join(
                    self.fontsFolder, ValSet["PreFace - Title & Singer"]["Font"]
                ),
                int(ValSet["PreFace - Title & Singer"]["FontSize"]),
            )
            draw.text(
                (
                    int(ValSet["PreFace - Title & Singer"]["PosX"]),
                    int(ValSet["PreFace - Title & Singer"]["PosY"]),
                ),
                text=f"{self.titleLine}",
                fill=ValSet["PreFace - Title & Singer"]["Color"],
                font=selectedFont,
            )
            selectedFont = ImageFont.truetype(
                os.path.join(self.fontsFolder, ValSet["PreFace - Maker"]["Font"]),
                int(ValSet["PreFace - Maker"]["FontSize"]),
            )
            draw.text(
                (
                    int(ValSet["PreFace - Maker"]["PosX"]),
                    int(ValSet["PreFace - Maker"]["PosY"]),
                ),
                text=SystemVal["Maker"],
                fill=ValSet["PreFace - Maker"]["Color"],
                font=selectedFont,
            )
            selectedFont = ImageFont.truetype(
                os.path.join(
                    self.fontsFolder, ValSet["LyricsPage - CurLyrics1"]["Font"]
                ),
                int(ValSet["LyricsPage - CurLyrics1"]["FontSize"]),
            )
            draw.text(
                (
                    int(ValSet["LyricsPage - CurLyrics1"]["PosX"]),
                    int(ValSet["LyricsPage - CurLyrics1"]["PosY"]),
                ),
                text=f"{curLine1}",
                fill=ValSet["LyricsPage - CurLyrics1"]["Color"],
                font=selectedFont,
            )
            draw.text(
                (
                    int(ValSet["LyricsPage - CurLyrics2"]["PosX"]),
                    int(ValSet["LyricsPage - CurLyrics2"]["PosY"]),
                ),
                text=f"{curLine1}",
                fill=ValSet["LyricsPage - CurLyrics2"]["Color"],
                font=selectedFont,
            )
            draw.text(
                (
                    int(ValSet["LyricsPage - NextLyrics"]["PosX"]),
                    int(ValSet["LyricsPage - NextLyrics"]["PosY"]),
                ),
                text=f"{curLine1}",
                fill=ValSet["LyricsPage - NextLyrics"]["Color"],
                font=selectedFont,
            )
            bgImg.save(f"../../Outputs/{self.videoName}/Images/{alps[idx]}.jpg")
            curLine1 = nextLine
            curLine2 = self.lyricsFile.readline().split("#")[0]
            nextLine = self.lyricsFile.readline().split("#")[0]
            idx += 1
        self.lyricsFile.close()

    def makeFinishImg(self) -> None:
        """
        영상의 마지막 이미지를 만드는 메서드
        """
        bgImg = Image.open("../../Settings/Images/background/background.jpg")
        draw = ImageDraw.Draw(bgImg)
        selectedFont = ImageFont.truetype(
            os.path.join(self.fontsFolder, ValSet["PreFace - Title & Singer"]["Font"]),
            int(ValSet["PreFace - Title & Singer"]["FontSize"]),
        )
        draw.text(
            (
                int(ValSet["PreFace - Title & Singer"]["PosX"]),
                int(ValSet["PreFace - Title & Singer"]["PosY"]),
            ),
            text=f"{self.titleLine}",
            fill=ValSet["PreFace - Title & Singer"]["Color"],
            font=selectedFont,
        )
        selectedFont = ImageFont.truetype(
            os.path.join(self.fontsFolder, ValSet["PreFace - Maker"]["Font"]),
            int(ValSet["PreFace - Maker"]["FontSize"]),
        )
        draw.text(
            (
                int(ValSet["PreFace - Maker"]["PosX"]),
                int(ValSet["PreFace - Maker"]["PosY"]),
            ),
            text=SystemVal["Maker"],
            fill=ValSet["PreFace - Maker"]["Color"],
            font=selectedFont,
        )
        selectedFont = ImageFont.truetype(
            os.path.join(self.fontsFolder, ValSet["LastPage - Thanks For"]["Font"]),
            int(ValSet["LastPage - Thanks For"]["FontSize"]),
        )
        draw.text(
            (
                int(ValSet["LastPage - Thanks For"]["PosX"]),
                int(ValSet["LastPage - Thanks For"]["PosY"]),
            ),
            text=f"Thanks For",
            fill=ValSet["LastPage - Thanks For"]["Color"],
            font=selectedFont,
        )
        draw.text(
            (
                int(ValSet["LastPage - Listening"]["PosX"]),
                int(ValSet["LastPage - Listening"]["PosY"]),
            ),
            text=f"Listening",
            fill=ValSet["LastPage - Listening"]["Color"],
            font=selectedFont,
        )
        bgImg.save(f"../../Outputs/{self.videoName}/Images/zzz.jpg")

    def getChangeTime(self) -> None:
        """
        가사를 넘겨줄 타이밍을 입력받는 메서드
        """
        wait = input("타이밍을 txt 파일에 입력해주세요.")
        getTimeFile = open(
            f"../../Outputs/{self.videoName}/Lyrics/lyrics.txt", "r", encoding="cp949"
        )
        timeList = [0]
        curLine = True
        while curLine != [""]:
            curLine = list(getTimeFile.readline().split("#"))
            if len(curLine) == 2:
                timeList.append(int(curLine[1][0]) * 60 + int(curLine[1][1:3]))
        getTimeFile.close()
        self.frameList = []
        for i in range(len(timeList)):
            if i == 0:
                continue
            self.frameList.append(timeList[i] - timeList[i - 1])

    def makeVideo(self) -> None:
        """
        가사가 적힌 사진을 모아 영상으로 제작하는 메서드
        """
        frameSize = (2560, 1440)
        out = cv2.VideoWriter(
            f"../../Outputs/{self.videoName}/Videos/{self.videoName}-nosound.avi",
            cv2.VideoWriter_fourcc(*"DIVX"),
            1,
            frameSize,
        )
        idx = 0
        for filename in glob.glob(f"../../Outputs/{self.videoName}/Images/*.jpg"):
            for i in range(self.frameList[idx]):
                img = cv2.imread(filename)
                out.write(img)
            idx += 1
        out.release()

    def downloadMusic(self) -> None:
        """
        영상에 필요한 노래를 유튜브 링크로부터 다운로드 받는 메서드
        """
        downloadList = []
        self.youtubeURL = input("유튜브 링크를 입력해주세요 : ")
        downloadList.append(self.youtubeURL)
        output_dir = os.path.join(
            f"../../Outputs/{self.videoName}/Musics/", f"{self.videoName}.mp3"
        )

        ydlOpt = {
            "outtmpl": output_dir,
            "format": "bestaudio/best",
        }

        with youtube_dl.YoutubeDL(ydlOpt) as ydl:
            ydl.download(downloadList)

    def putMusicInVideo(self) -> None:
        """
        영상에 다운로드 받은 음악을 합쳐 완성하는 메서드
        """
        audio = mp.AudioFileClip(
            f"../../Outputs/{self.videoName}/Musics/{self.videoName}.mp3"
        )
        video1 = mp.VideoFileClip(
            f"../../Outputs/{self.videoName}/Videos/{self.videoName}-nosound.avi"
        )
        final = video1.set_audio(audio)
        final.write_videofile(
            f"../../Outputs/{self.videoName}/Videos/{self.videoName}.mp4",
            codec="mpeg4",
            audio_codec="libvorbis",
        )

    def saveDatabase(self) -> None:
        """
        영상 제작에 필요한 데이터들을 DB에 저장하는 메서드
        """
        db = sqlite3.connect("../../Settings/Database/Datas.db")
        cursor = db.cursor()
        cursor.execute(f"SELECT COUNT(*) FROM VideoDatas")
        count = cursor.fetchone()[0]
        insert_query = f"INSERT INTO VideoDatas VALUES('{count+1}','{self.videoName}', '{self.youtubeURL}' ,'{self.frameList}','{datetime.datetime.now()}')"
        cursor.execute(insert_query)
        db.commit()


if __name__ == "__main__":
    name = input("영상 제목을 영어로 입력해주세요 : ")
    video = makeLyricsVideo(name)
    video.getLyrics()
    video.makeTitleImg()
    video.makeImgs()
    video.makeFinishImg()
    video.getChangeTime()
    video.makeVideo()
    video.downloadMusic()
    video.putMusicInVideo()
    video.saveDatabase()
