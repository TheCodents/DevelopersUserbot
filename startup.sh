if [[ -z "$TELETHON_SESSION" && -z "$PYROGRAM_SESSION" ]]
then
	echo "Add PYROGRAM_SESSION or TELETHON_SESSION first!"
elif [[ -z "$TELETHON_SESSION" ]]
then
	python -m _pyrogram
elif [[ -z "$PYROGRAM_SESSION" ]]
then
	python -m _telethon
else
	python -m _pyrogram & python -m _telethon
	exit 1
fi
