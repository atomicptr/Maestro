on run argv
	set song_title to item 1 in argv

	tell application "iTunes" to set playlist_list to the name of every user playlist
	
	-- probably not the best solution :(
	set song_title to findReplace("`", "'", song_title)

	if playlist_list does not contain song_title then
		tell application "iTunes" to play track song_title of current playlist
	else
		tell application "iTunes" to play playlist song_title
	end if

end run

-- thanks to mathias
-- http://blog.mixable.de/applescript-findreplace-function/
on findReplace(findText, replaceText, sourceText)
   set ASTID to AppleScript's text item delimiters
   set AppleScript's text item delimiters to findText
   set sourceText to text items of sourceText
   set AppleScript's text item delimiters to replaceText
   set sourceText to "" & sourceText
   set AppleScript's text item delimiters to ASTID
   return sourceText
end findReplace