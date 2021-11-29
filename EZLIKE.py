# EZLIKE
# Save songs to your Spotify library with a hotkey combination.

# Sources:
# https://nitratine.net/blog/post/how-to-make-hotkeys-in-python/
# https://github.com/EuanMorgan/SpotifyDiscoverWeeklyRescuer
# https://github.com/imdadahad/spotify-get-current-playing-track

# Import pynput module
from pynput import keyboard
from datetime import datetime
from win10toast import ToastNotifier
from main import SaveSong

n = ToastNotifier()
s = SaveSong()

# Define key combinations
COMBINATIONS = [
    {keyboard.Key.cmd, keyboard.Key.shift, keyboard.KeyCode(char = 'l')},
    {keyboard.Key.cmd, keyboard.Key.shift, keyboard.KeyCode(char = 'L')}
]

# Track currently pressed keys
current = set()

# Define what happens when combination detected
def execute():

    # Refresh token
    print('Refreshing token...')
    r1, new_token = s.refresh_token()
    print(r1)
    print('New token: {}'.format(new_token))

    # Get current song
    print('Getting current song...')
    r2, song_info = s.get_current_song()
    print(r2)

    # Add current song to library
    print('Adding current song to library...')
    r3, message = s.add_to_library(song_info)
    print(r3)

    print(message)
    
    # Display notification
    n.show_toast('EZLIKE', message, duration = 5, threaded = True,
                 icon_path = 'EZLIKE.ico')

# Define press and release methods
def on_press(key):
    
    # If any key in any combination is being pressed
    if any([key in COMBO for COMBO in COMBINATIONS]):
        
        # Add key to set
        current.add(key)
        
        # If any combination is being pressed
        if any(all(k in current for k in COMBO) for COMBO in COMBINATIONS):
            
            # Do action
            execute()

def on_release(key):
    if any([key in COMBO for COMBO in COMBINATIONS]):
        
        # Remove key from set
        current.remove(key)

# Setup listener for keyboard
with keyboard.Listener(on_press = on_press, on_release = on_release, IS_TRUSTED = True) as listener:
    listener.join()
