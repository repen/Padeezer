import requests, json
from bs4 import BeautifulSoup
from report import ExelPlain
from datetime import datetime
import datetime
import os, re

NAME_FILE = "import.xlsx"
WORK_DIR = os.getcwd()



class ErrorGetContent(Exception):
    pass

class ErrorAttributeElement(Exception):
    pass

class Deezer:
    def __init__(self, message_send = None, report = None):
        self.error = 0
        self.message = None
        self.message_send = message_send
        self.header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; \
                                x64; rv:47.0) Gecko/20100101 Firefox/48.0'}

    def open_urls(self):
        with open( os.path.join( WORK_DIR, "urls.txt" ), encoding="utf8") as f_obj:
            data = [x.replace("\n","") for x in f_obj]
        return data

    def get_content(self, url):
        try:
            r = requests.get(url, headers=self.header)
            if r.status_code == 200:
                return r.text
        except:
            pass

    def main(self):
        _table = '''<table><tbody>{}</tbody></table>'''.strip()
        _iframe = '<iframe scrolling="no" frameborder="0" src="https://www.deezer.com/plugins/player?format=square&amp;autoplay=false&amp;playlist=false&amp;width=300&amp;height=300&amp;color=ff0000&amp;layout=dark&amp;size=medium&amp;type=album&amp;id={}&amp;app_id=1" width="300" height="300"></iframe>'
        _image = '<img src="{}" alt="" class="fr-fic fr-dib">'
        urls = self.open_urls()
        if not urls:
            self.message_send("[Error] No urls")
            raise Exception("[Error] No urls")

        try:
            wb = ExelPlain.load_xlsx(NAME_FILE)
        except FileNotFoundError:
            wb = ExelPlain()
            wb = wb.create_sheet("Music")

        for e2, url in enumerate(urls):
            try:
                html = self.get_content(url)
                if not html:
                    self.message_send("[ERROR] not content")
                    raise ErrorGetContent("[ERROR] not content")
                soup = BeautifulSoup(html, "html.parser")

                scripts = soup.select("script")
                script = list(filter( lambda x: re.search(r"window\.__DZR_APP_STATE__", str(x)) , scripts ) )[0]
                raw = re.findall(r"\=.*?(\{.*?)\<\/script\>", str(script))[0]
                data = json.loads(raw)

                AUTHOR = data["DATA"]["ART_NAME"]
                title = " - ".join( [ AUTHOR, data["DATA"]["ALB_TITLE"] ] )

                image_layer = _image.format( soup.select_one('meta[content][property="og:image"]')["content"] )

                build=[]
                _duration = 0
                for e, track in enumerate(data["SONGS"]["data"], start=1):
                    string1 = '<tr><td style="width:11.911%;">{}</td>'.format( e )
                    string1 += '<td style="width:76.6667%;">{}</td>'.format( track["SNG_TITLE"] )
                    temp = str(datetime.timedelta(seconds=int(track["DURATION"])))
                    _duration += int(track["DURATION"])
                    if "0" == temp[0]:
                        temp = ":".join( temp.split(":")[1:] )

                    string1 += '<td style="width:11.1111%;" width="25">{}</td></tr>'.format(temp)
                    build.append(string1)

                table = _table.format( "".join(build) )

                author = AUTHOR

                released = data["DATA"]["DIGITAL_RELEASE_DATE"].split("-")[0]
                y, m, d  = data["DATA"]["DIGITAL_RELEASE_DATE"].split("-")
                date_released = ".".join([ d, m, y ])

                label = data["DATA"]["LABEL_NAME"]
                quantity_track = e
                total_duration = str(datetime.timedelta(seconds=_duration))
                album_name = data["DATA"]["ALB_TITLE"]
                player = _iframe.format( data["DATA"]["ALB_ID"] )

                sheet_ranges = wb["Music"]
                sheet_ranges.append([title, image_layer, table, author, released, date_released,
                                                label, quantity_track, total_duration, album_name, player])
                self.message_send("processing left count: {}".format(len(urls) - e2))
            except:
                self.message_send("Error {}".format( url ))
        wb.save(NAME_FILE)
        self.message_send("[Successful] saved to {}".format(NAME_FILE))


if __name__ == "__main__":
    start = Deezer()
    start.main()



