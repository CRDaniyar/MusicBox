from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

tracks = [
    {
        "id": 1,
        "title": "title1",
        "artist": "artist1",
        "genre": "Rap",
        "is_favorite": True,
    },
]

@app.route("/")
def index():
    return render_template("index.html", tracks=tracks)


@app.route("/tracks/<int:track_id>")
def detail(track_id):
    track = None

    for item in tracks:
        if item["id"] == track_id:
            track = item
            break

    if track is None:
        return "Track not found", 404

    return render_template("detail.html", track=track)


@app.route("/tracks/add", methods=["GET", "POST"])
def add_track():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        artist = request.form.get("artist", "").strip()
        genre = request.form.get("genre", "").strip()
        is_favorite = bool(request.form.get("is_favorite"))

        errors = []

        if not title:
            errors.append("Название трека обязательно")

        if not artist:
            errors.append("Исполнитель обязателен")

        if title and artist and any(t["title"].strip().lower() == title.lower() and t["artist"].strip() == artist.lower() for t in tracks):
            errors.append("Такой трек уже добавлен")
            

        if not genre:
            errors.append("Жанр обязателен")

        

        if errors:
            return render_template(
                "add.html",
                errors=errors,
                title=title,
                artist=artist,
                genre=genre,
                is_favorite=is_favorite,
            )

    
        new_track = {
            "id": len(tracks) + 1,
            "title": title,
            "artist": artist,
            "genre": genre,
            "is_favorite": is_favorite,
        }
        
        tracks.append(new_track)
        return redirect(url_for("index"))

    return render_template("add.html")


if __name__ == "__main__":
    app.run(debug=True)
