on run argv
	set itunes_item to item 1 in argv

	tell application "iTunes" to set playlist_list to the name of every user playlist

	if playlist_list does not contain itunes_item then
		tell application "iTunes" to play (first track of current playlist whose database ID is itunes_item)
	else
		tell application "iTunes" to play playlist itunes_item
	end if

end run