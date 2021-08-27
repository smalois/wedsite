from base64 import b64encode

VOTE_TRANSITION_SECONDS = 30
CROSSFADE_LENGTH_SECONDS = 5
THREAD_POLL_RATE_SECONDS = .5

# Enter the client_id and client_secret values from the spotify developer
# dashboard. (You'll need to register as a spotify developer and create a new
# developer app)
CLIENT_ID=""
CLIENT_SECRET=""
REDIRECT="https://abbyandscott.fun/music/tokenRequest/"
ENCODED_PAIR = CLIENT_ID + ":" + CLIENT_SECRET
ENCODED_PAIR = b64encode(ENCODED_PAIR.encode('ascii')).decode('ascii')

SCOPES = "user-library-read user-read-playback-state user-modify-playback-state" # Space separated list

# Enter the playlist ID for a Spotify playlist to play from
PLAYLIST_ID = ""
# First song is Celebration by Kool & The Gang; whatever song goes here must
# also be in the playlist chosen above.
FIRST_SONG_ID = "1pGCWtHyUUUx2RMjYnaCGw"

ENDPOINT_AUTH="https://accounts.spotify.com/authorize"
ENDPOINT_TOKEN="https://accounts.spotify.com/api/token"

ENDPOINT_PLAYSONG="https://api.spotify.com/v1/me/player/play"
ENDPOINT_STOP="https://api.spotify.com/v1/me/player/pause"
ENDPOINT_ENQUEUE="https://api.spotify.com/v1/me/player/queue"
ENDPOINT_GET_DEVICES="https://api.spotify.com/v1/me/player/devices"
ENDPOINT_GET_PLAYLIST="https://api.spotify.com/v1/playlists/"
ENDPOINT_GET_PLAYBACK_INFO="https://api.spotify.com/v1/me/player"
PLAYSONG_URI = "spotify:track:"
GETPLAYLIST_QUERY="?fields=items(track(id%2Cname%2Cduration_ms%2Cartists(name)))"
GETPLAYLIST_LIMIT="&limit=100"
GETPLAYLIST_INDEX="&offset="

# still need to add artist name to the playlist query
#  artist_name = models.CharField(max_length=200)
