if [[ -z "$TELETHON_SESSION" && -z "$PYROGRAM_SESSION" ]]
then
	python -m _pyrogram && python -m _telethon
elif [[ -z "$TELETHON_SESSION" ]]
then
	python -m _telethon
elif [[ -z "$PYROGRAM_SESSION" ]]
then
	python -m _pyrogram
else
	echo "Add PYROGRAM_SESSION or TELETHON_SESSION first!"
	exit 1
fi
