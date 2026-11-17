from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

tracks = [
    {
        "id": 1,
        "title": "Starboy",
        "artist": "The Weeknd",
        "genre": "R&B / Pop",
        "is_favorite": True,
    },
    {
        "id": 2,
        "title": "Numb",
        "artist": "Linkin Park",
        "genre": "Rock",
        "is_favorite": True,
    },
    {
        "id": 3,
        "title": "Midnight City",
        "artist": "M83",
        "genre": "Electronic",
        "is_favorite": False,
    },
]


def validate_track(title, artist, genre, exclude_id=None):
    errors = []
    if not title:
        errors.append("Название трека обязательно")
    if not artist:
        errors.append("Исполнитель обязателен")
    if not genre:
        errors.append("Жанр обязателен")

    if title and artist and any(
        t["id"] != exclude_id
        and t["title"].strip().lower() == title.lower()
        and t["artist"].strip().lower() == artist.lower()
        for t in tracks
    ):
        errors.append("У этого исполнителя уже добавлен трек с таким названием")

    return errors


@app.route("/")
def index():
    search_query = request.args.get("q", "").strip()
    only_favorites = request.args.get("favorites") == "1"

    filtered_tracks = tracks

    if search_query:
        q_lower = search_query.lower()
        filtered_tracks = [
            t for t in filtered_tracks
            if q_lower in t["title"].lower() or q_lower in t["artist"].lower()
        ]

    if only_favorites:
        filtered_tracks = [t for t in filtered_tracks if t["is_favorite"]]

    return render_template(
        "index.html",
        tracks=filtered_tracks,
        search_query=search_query,
        only_favorites=only_favorites,
    )


@app.route("/tracks/<int:track_id>")
def detail(track_id):
    track = next((t for t in tracks if t["id"] == track_id), None)
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

        errors = validate_track(title, artist, genre)

        if errors:
            return render_template(
                "add.html",
                errors=errors,
                title=title,
                artist=artist,
                genre=genre,
                is_favorite=is_favorite,
            )

        new_id = max([t["id"] for t in tracks], default=0) + 1
        tracks.append({
            "id": new_id,
            "title": title,
            "artist": artist,
            "genre": genre,
            "is_favorite": is_favorite,
        })
        return redirect(url_for("index"))

    return render_template("add.html")


@app.route("/tracks/<int:track_id>/edit", methods=["GET", "POST"])
def edit_track(track_id):
    track = next((t for t in tracks if t["id"] == track_id), None)
    if track is None:
        return "Track not found", 404

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        artist = request.form.get("artist", "").strip()
        genre = request.form.get("genre", "").strip()
        is_favorite = bool(request.form.get("is_favorite"))

        errors = validate_track(title, artist, genre, exclude_id=track_id)

        if errors:
            return render_template(
                "edit.html",
                track=track,
                errors=errors,
                title=title,
                artist=artist,
                genre=genre,
                is_favorite=is_favorite,
            )

        track["title"] = title
        track["artist"] = artist
        track["genre"] = genre
        track["is_favorite"] = is_favorite

        return redirect(url_for("detail", track_id=track["id"]))


    return render_template(
        "edit.html",
        track=track,
        title=track["title"],
        artist=track["artist"],
        genre=track["genre"],
        is_favorite=track["is_favorite"],
    )


@app.route("/tracks/<int:track_id>/delete", methods=["POST"])
def delete_track(track_id):
    track = next((t for t in tracks if t["id"] == track_id), None)
    if track is None:
        return "Track not found", 404

    tracks.remove(track)
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
