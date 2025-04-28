import requests

base_url = 'https://static.heartshine.gay'
generation = 'g4-fim'
s = 1
e = 1


# https://static.heartshine.gay/g4-fim/s11e01-480p.mp4
# /s01e02-480p.mp4'
# https://static.heartshine.gay/g4-fim/s01e01-480p.mp4
# https://static.heartshine.gay/g4-fim/s01e01-480p.mp4
# https://static.heartshine.gay/g4-fim/s01e01-480p.mp4
# https://static.heartshine.gay/g4-fim/s08e01-480p.mp4


def pad_left(x, pad = None, target_length = None):

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



if __name__ == '__main__':

    # Set the range of episodes
    last_season = 1
    s = 1
    e = 1


    url = f'{base_url}/{generation}/s{pad_left(s, '0', 2)}e{pad_left(e, '0', 2)}-1080p.mp4'
    file_name = 'test.mp4'
    # Download the video

    while e < 3 and s == 1:

        r = requests.get(url)

        if r.url != url:

            
            print('Trying next season')
            s += 1
            e = 1
            continue

        file_name = f'{s}-{e}.mp4'
        print("Downloading starts...\n")
        with open(file_name, 'wb') as f:
            for chunk in r.iter_content(chunk_size = 255):
                f.write(chunk)
        print("Download completed..!!")

        e += 1
    # except Exception as e:
    #     print(e)
    # print(r.url)

        # if r.url != url:


