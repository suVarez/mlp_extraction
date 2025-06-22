import os
import shutil
from typing import Optional

class Target:
    def __init__(self, path: str) -> None:
        self._path = path
        self.target = '.'

        if os.path.abspath(path):
            self.target = self._clean_path('right')

        else:
            self.target = f'.\\{self._clean_path('both')}'


    def build(self, force: bool = False) -> None:
        if force:
            self.clear()

        print(f'building {self.target}')
        try:
            os.makedirs(self.target)
        except FileExistsError as e:
            print(f'Build stopped as {self.target} already exists')
            print('Try x.clear() first or x.build(force = True)')

    def clear(self) -> None:
        if os.path.exists(self.target):
            print(f'clearing {self.target}')
            shutil.rmtree(self.target)

        else:
            print(f'{self.target} does not exist')


    def _clean_path(self, side: str = '', path: Optional[str] = None) -> str:
        if path is None:
            path = self._path
        if side in ['left', 'both']:
            if path[:2] == '.\\':
                path = path[2:]

            elif path[0] == '\\':
                path = path[1:]

        if side in ['right', 'both']:
            if path[-1] == '\\':
                path = path[:-1]

        return path
    

    def build_subdirectory(self, subdir: str) -> None:
        subdir = self._clean_path(side = 'both', path = subdir)

        if os.path.exists(f'{self.target}\\{subdir}') and os.path.isdir(f'{self.target}\\{subdir}'):
            print(f'{subdir} already exists')

        else:
            os.makedirs(f'{self.target}\\{subdir}')
            print(f'created {subdir}')




        

if __name__ == '__main__':
    m = Target('.\\target')

    m.build(force = True)

    m.build_subdirectory('ertert')