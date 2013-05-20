on run argv
	tell application "iTunes"
		set the_track to the track (item 1 of argv)
		set the_path to item 2 of argv
		set file_name to item 3 of argv
	
		my exportArtwork_(the_track, the_path, file_name)
	end tell
end run

# script by doug
to exportArtwork_(theTrack, exportFolder, artworkName)
	tell application "iTunes"
		try
			tell theTrack to set {artworkData, imageFormat} to {(raw data of artwork 1), (format of artwork 1) as text}
		on error
			# probably no artwork
			return false
		end try
	end tell
	
	set ext to ".png"
	set fileType to "PNG"
	if imageFormat contains "JPEG" then
		set ext to ".jpg"
		set fileType to "JPEG"
	end if
	
	set pathToNewFile to (exportFolder & artworkName & ext) as text
	
	# if file with same name exists in same location then delete it
	# optional
	try
		do shell script "rm " & quoted form of POSIX path of pathToNewFile
	end try
	
	try
		set fileRef to (open for access pathToNewFile with write permission)
		set eof fileRef to 0
		write artworkData to fileRef starting at 0
		close access fileRef
	on error m
		try
			close access fileRef
		end try
		return false
	end try
	
	try
		tell application "System Events" to set file type of (pathToNewFile as alias) to fileType
	on error m
		# may not be critical
		log ("ERROR: " & m)
	end try
	
	return true
	
end exportArtwork_