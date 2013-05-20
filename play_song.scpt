on run argv
	set song_title to item 1 in argv

	tell application "iTunes" to set playlist_list to the name of every user playlist

	if playlist_list does not contain song_title then
		tell application "iTunes" to play track song_title of current playlist
	else
		tell application "iTunes" to play playlist song_title
	end if

end run