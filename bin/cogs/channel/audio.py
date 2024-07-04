import yt_dlp


ytdl_info = {
    # "format": "m4a/bestaudio/best",
    "format": "bestaudio",
    # ℹ️ See help(yt_dlp.postprocessor) for a list of available Postprocessors and their arguments
    "postprocessors": [
        {  # Extract audio using ffmpeg
            "key": "FFmpegExtractAudio",
            # "preferredcodec": "m4a",
        }
    ],
}


def ytdl_audio(url="https://youtu.be/dQw4w9WgXcQ?si=5XbMEbJQpmsH2kpY", type="url"):
    try:
        if type == "text":
            url = f"ytsearch:{url}"

        # print("url", url, "type", type)

        info = {"url": "", "title": ""}

        with yt_dlp.YoutubeDL(ytdl_info) as ytdl:
            song_info = ytdl.extract_info(url, download=False)

            check_for = "entries" if song_info.get("_type") == "playlist" else "formats"

            for each in song_info[check_for]:
                if each.get("fps") is None and each.get("format_note") == "medium":
                    info["url"] = each["url"]
                    info["title"] = song_info["title"]
                    return info

    except Exception as e:
        print(f"Error in code {e}")


# v = extract_audio("back in black", "text")
# fps : null
# "format_note": "medium"
