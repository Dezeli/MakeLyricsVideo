import configparser
from time import strftime


class ConfigManager:
    """
    config.ini 파일을 생성하고 쉽게 관리할 수 있게 도와주는 클래스
    """

    def __init__(self) -> None:
        self.config = configparser.ConfigParser()

    def makeDefaultConfigFile(self) -> None:
        """
        config.ini를 생성하는 메서드
        """
        self.config["System"] = {}
        self.config["System"]["Version"] = "0.8"
        self.config["System"]["Update"] = strftime("%Y-%m-%d %H:%M:%S")
        self.config["System"]["Maker"] = "Lyrics WFS"

        defaultWritings = {
            "PreFace - Title & Singer": ["GodoB.ttf", "60", "40", "40", "#5d7530"],
            "PreFace - Maker": ["GodoM.ttf", "60", "2200", "40", "#123152"],
            "TitlePage - Title": ["GodoB.ttf", "150", "170", "400", "Black"],
            "TitlePage - Singer": ["GodoM.ttf", "100", "1300", "800", "#575759"],
            "LyricsPage - CurLyrics1": ["godoMaum.ttf", "180", "200", "370", "Black"],
            "LyricsPage - CurLyrics2": ["godoMaum.ttf", "180", "200", "670", "Black"],
            "LyricsPage - NextLyrics": [
                "godoMaum.ttf",
                "180",
                "200",
                "1130",
                "#575759",
            ],
            "LastPage - Thanks For": ["godoMaum.ttf", "500", "510", "300", "Black"],
            "LastPage - Listening": ["godoMaum.ttf", "500", "670", "650", "Black"],
        }

        for key, val in defaultWritings.items():
            self.config[f"{key}"] = {}
            self.config[f"{key}"]["Font"] = val[0]
            self.config[f"{key}"]["FontSize"] = val[1]
            self.config[f"{key}"]["PosX"] = val[2]
            self.config[f"{key}"]["PosY"] = val[3]
            self.config[f"{key}"]["Color"] = val[4]

        with open("../../Settings/config.ini", "w", encoding="cp949") as configfile:
            self.config.write(configfile)

    def readConfigFile(self) -> None:
        """
        config.ini를 읽어들이는 메서드
        """
        self.config.read("../../Settings/config.ini", encoding="cp949")


if __name__ == "__main__":
    CM = ConfigManager()
    CM.makeDefaultConfigFile()
