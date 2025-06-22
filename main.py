import requests
from typing import Optional, Union
from target import Target

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

class MLP():
    def __init__(self, generation: str, begin_season: int = 1, 
                 begin_episode: int = 1, export_path: str = '.') -> None:
        self.gen = generation
        self.base_url = 'https://static.heartshine.gay'
        self.s = begin_season
        self.e = begin_episode
        self.url_log = []
        self.url = None
        self.export_path = export_path

    def validate_url(self) -> None:
        if self.url is None:
            raise ValueError('The url cannot be None. Use build_url()')


    def log_url(self):
        self.validate_url()
        with open(f'{self.export_path}/log.txt', 'a') as f:
            f.write(self.url + '\n') 

    def build_url(self) -> None:
        self.url = f'{self.base_url}/{self.gen}/'
        self.url += f's{pad_left(self.s, '0', 2)}e{pad_left(self.e, '0', 2)}-480p.mp4'
        self.log_url()

    def download(self) -> Union[str, requests.Response]:
        self.validate_url()

        r = requests.get(self.url)

        if r.url != self.url:
            if self.e == 1:
                print(f'{mlp.s - 1} was the final season. Enjoy!')
                r = 'break'
            else:
                print(f'Episode {self.e - 1} appears to be the last episode of {self.s}.')
                print(f'Looking for the next season: {self.s + 1}')
                r = 'continue'

        return r
        
    

if __name__ == '__main__':

    target = Target('./target')
    target.build(force = True)

    mlp = MLP(generation = 'g4-fim', begin_season = 14, begin_episode = 23, 
              export_path = target.target)

    while True:

        mlp.build_url()

        print("Downloading starts...\n")
        r = mlp.download()
        if r == 'continue':
            mlp.s += 1
            mlp.e = 1
            continue
        if r == 'break':
            break

        print("Writing to file...\n")
        file_name = f'{mlp.s}-{mlp.e}.mp4'

        with open(f'{mlp.export_path}/{file_name}', 'wb') as f:
            for chunk in r.iter_content(chunk_size = 255):
                f.write(chunk)
        print("Download completed..!!")

        mlp.e += 1


