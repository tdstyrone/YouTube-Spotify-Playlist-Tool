from youtube_client import YouTubeClient
import subprocess

def mp3_downloader(path, url):
    subprocess.call([
        'youtube-dl',
        '-i',
        '-x',
        '--audio-format',
        'mp3',
        '-o',
        f'{path}/%(title)s.%(ext)s',
        url
    ])
pass


def main():
    yt_client = YouTubeClient()
    print("-----------Welcome to Tyrone's YouTube MP3 Downloader / Spotify Playlist Creator ----------\n")
    print("Select the playlist you want below: ")
    keys = yt_client.get_playlist()
    print("0. Exit")
    print(keys)
    user_choice = int(input("\nYour Choice: "))
    while user_choice != 0:
        try:
            if user_choice == keys[user_choice-1][0]:
                print("----------------DOWNLOADING--------------------")
                print("The songs in the playlist you have chosen are: \n")
                pl_information = yt_client.get_songs(user_choice-1)
                playlist_url = f"https://www.youtube.com/watch?v={keys[user_choice-1][1]}&list" \
                               f"={pl_information['Playlist ID']}"
                user_path = input("\nPlease specify full path to store files: ")  # ~/Music/YouTube_Downloads
                mp3_downloader(user_path, playlist_url)
                user_choice = int(input("\nYour Choice: "))
                # print(pl_information['Songs'])
                song_info = yt_client.get_tracks_artist(pl_information['Songs'])
                # print(song_info)
        except IndexError:
            print("\nNot a Valid Option!!")
            user_choice = int(input("\nYour Choice: "))
    print('\n!!!!THANK YOU FOR USING!!!!')
pass

if __name__ == "__main__":
    main()
