on run argv
	set song_title to item 1 in argv

	try
		tell application "iTunes" to play track song_title of current playlist
	on error error_message
		tell application "iTunes" to play playlist song_title
	end try
end run