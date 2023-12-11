from getConfigFile import ConfigManager

"""
config.ini 파일에서 글씨와 관련된 설정 값을 불러오는 파일
"""


CM = ConfigManager()
CM.readConfigFile()
writingCategories = [
    "PreFace - Title & Singer",
    "PreFace - Maker",
    "TitlePage - Title",
    "TitlePage - Singer",
    "LyricsPage - CurLyrics1",
    "LyricsPage - CurLyrics2",
    "LyricsPage - NextLyrics",
    "LastPage - Thanks For",
    "LastPage - Listening",
]

writingitems = ["Font", "FontSize", "PosX", "PosY", "Color"]
ValSet = {}
for category in writingCategories:
    ValSet[category] = {}
    for item in writingitems:
        ValSet[category][item] = CM.config[category][item]

SystemVal = {}
SystemVal["Version"] = CM.config["System"]["Version"]
SystemVal["Update"] = CM.config["System"]["Update"]
SystemVal["Maker"] = CM.config["System"]["Maker"]
