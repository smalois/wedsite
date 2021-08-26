# Wedding website

The source code for a personal wedding event website that I built. It's main functionality allows each guest to scan a code to log into the website, vote on what song plays next, and participate in a scavenger hunt.

## Disclaimer

I wouldn't recommend depending on this out-of-the-box to work the same way for you but, for what it's worth, it worked perfectly fine for our wedding.

Be aware that this is more of a toy project that is designed around a 1-time event. User accounts are easily accessible by anybody because passwords are encoded directly in the individual guest URLs. Don't use the guest application for anything that requires a secure and unique long-term user account.

## Guests

* "Guests" are Django users with additional data for music voted status and scavenger hunt progress
* Guests are logged in automatically by visiting their unique url.
* To initialize the database with guests, run the Django admin command "update_guestlist <csv_guestlist>".
  * This grabs columns named "First name" and "Last name". Guest passwords are just truncated hashes of the concatenated names.
  * When the guest is successfully created, that guest's unique URL is printed to stdout.
 
## Music
 
* The Spotify API is used to play music on a device. 
* There's one master Spotify user that actually plays the music. Users can vote to influence the next song thath plays from the master account.
  * Voting is enabled when the song starts and stops 30 seconds (configurable) before the end of the song.
  * 30 seconds before the end of the song, the next song is enqueued (this allows crossfade to be set on the Spotify player device)
* At the moment, just the default device will be used (even though there's some code to suggest otherwise)
* To access the player, log in to the django admin account and go to the root URL. From there, you'll be able to log into the Spotify API.
* There are rudimentary controls for starting the music and doing some other management tasks.

## Scavenger Hunt

* Designed so that guests can scan a QR code to expose the next clue.
* A series of URLs can be provided to function as a set of clues.
* Progress on each clue is tracked when the guest visits each URL.
* Progress is tracked in a bitmap that is actually just a 16 byte string of 1s and 0s.
