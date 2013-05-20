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
	set playlist_list to every user playlist

	set return_list to {}

	repeat with pl in playlist_list
		set pl_name to the name of pl
		set pl_song_count to the count of every track in pl

		# if you want to see the special kind playlists remove the following line and
		# the correspondig "end if"
		if special kind of pl is none
			set end of return_list to pl_name & "!MAESTRO!" & pl_song_count
		end if
	end repeat

	set playlist_list_string to my joinList("\n", return_list)
end tell

return playlist_list_string
