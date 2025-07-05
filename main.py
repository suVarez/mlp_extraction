import requests
from typing import Optional, Union
from target import Target
from time import sleep
from playwright.sync_api import sync_playwright
from lxml import etree as et

def pad_left(x: Union[str, int], pad: str, target_length: int):

    if target_length is None:
        print('Must supply a target length.')
        return
    
    if pad is None:
        print('Must supply a value to pad with.')
        return

    if target_length < len(str(x)):
        print('Desired length must be larger than the length of the input.')
        return

    x = str(x)

    res = ''.join([pad for i in range(0, target_length - len(x))]) + x

    return res

def get_rendered_html(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)
        page.wait_for_load_state('networkidle')  # Wait for network to be idle
        html = page.content()
        browser.close()
        return html





class MLP():


    def __init__(self, generation: str, begin_season: int = 1, 
                 begin_episode: int = 1, export_path: str = '.', 
                 url: Optional[str] = None) -> None:
        self.gen = generation
        self.base_url = 'https://static.heartshine.gay'
        self.details_url = f'https://{generation}.heartshine.gay'
        self.s = begin_season
        self.e = begin_episode
        self.url_log = []
        self.url = url
        self.export_path = export_path
        self.html = None

    def validate_url(self) -> None:
        if self.url is None:
            raise ValueError('The url cannot be None. Use build_url()')


    def log_url(self):
        self.validate_url()
        with open(f'{self.export_path}/log.txt', 'a') as f:
            f.write(self.url + '\n')  # type: ignore


    def build_url(self) -> None:
        self.url = f'{self.base_url}/{self.gen}/'
        self.url += f's{pad_left(self.s, "0", 2)}e{pad_left(self.e, "0", 2)}-1080p.mp4'
        self.log_url()

    def download(self) -> Union[str, requests.Response]:
        self.validate_url()

        r = requests.get(self.url) # type: ignore

        if r.url != self.url:
            if self.e == 1:
                print(f'{mlp.s - 1} was the final season. Enjoy!')
                r = 'break'
            else:
                print(f'Episode {self.e - 1} appears to be the last episode of {self.s}.')
                print(f'Looking for the next season: {self.s + 1}')
                r = 'continue'

        return r
        

def get_rendered_html(url: str) -> Optional[str]:
    html = None
    with sync_playwright() as p:
        browser = p.chromium.launch( headless = True)
        page = browser.new_page()
        page.goto(url)
        page.wait_for_load_state('networkidle')  # Wait for network to be idle
        html = page.content()
        browser.close()

    return html



if __name__ == '__main__':

    target = Target('./target')
    target.build()

    # loop through all seasons of a generation to get the season and episode 
    # names
    parser = et.HTMLParser()
    season_names = []
    episode_names = {}
    max_season = None
    s = 1
    generation = 'g4-fim'
    gen_prefix = 'fim'
    while max_season is None or s <= max_season:

        url = f'https://{gen_prefix}.heartshine.gay/?s={s}&e=1&res=480&lo=0'


        rendered_html = get_rendered_html(url)

        root = et.fromstring(rendered_html, parser)

        if max_season is None:
            seasons = root.find('.//select[@id="seasList"]')
            season_names = [child.text for child in seasons.getchildren()]
            episode_names = {s:[] for s in season_names}
            max_season = len(season_names)

        episodes = root.find('.//select[@id="epList"]')

        for child in episodes.getchildren():

            episode_names[season_names[s-1]].append(child.text)
        print(episode_names)
        s += 1        



    mlp = MLP(generation = generation, begin_season = 1, begin_episode = 1, 
              export_path = target.target)


    s = 1
    e = 1
    current_season = season_names[s-1]
    current_episodes = episode_names[current_season]
    while s < max_season and e < len(current_episodes):
        sleep(5)
        if e == 1:
            target.build_subdirectory(current_season)

        target_file = f'{current_season}/{current_episodes[e-1]}.mp4'

        mlp.e = e
        mlp.s = s
        mlp.build_url()

        print("Downloading starts...\n")
        r = mlp.download()
        if r == 'continue':
            s += 1
            e = 1
            continue
        elif r == 'break':
            break

        print("Writing to file...\n")

        with open(f'{mlp.export_path}/{target_file}', 'wb') as f:
            for chunk in r.iter_content(chunk_size = 255):
                f.write(chunk)
        print("Download completed..!!")

        e += 1


