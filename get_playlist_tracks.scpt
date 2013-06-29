# joinList by Geert JM Vanderkelen <geert.vanderkelen.org>
# Thanks! ;)
on joinList(delimiter, someList)
	set prevTIDs to AppleScript's text item delimiters
	set AppleScript's text item delimiters to delimiter
	set output to "" & someList
	set AppleScript's text item delimiters to prevTIDs
	return output
end joinList

tell application "iTunes"
	set playlist_tracks to every track in current playlist

	set return_list to {}

	repeat with playlist_track in playlist_tracks
		set track_artist to the artist of playlist_track
		set track_name to the name of the playlist_track
		set album_name to the album of playlist_track

		set end of return_list to track_artist & "!MAESTRO!" & track_name & "!MAESTRO!" & album_name
	end repeat

	set playlist_tracks_string to my joinList("\n", return_list)
end tell

return playlist_tracks_string
