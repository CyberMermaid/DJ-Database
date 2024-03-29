from flask import Flask, redirect, render_template, flash, url_for
from flask_debugtoolbar import DebugToolbarExtension

from models import db, connect_db, Playlist, Song, PlaylistSong
from forms import NewSongForPlaylistForm, SongForm, PlaylistForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///playlist-app'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

app.config['SECRET_KEY'] = "I'LL NEVER TELL!!"

# Having the Debug Toolbar show redirects explicitly is often useful;
# however, if you want to turn it off, you can uncomment this line:
#
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)


@app.route("/")
def root():
    """Homepage: redirect to /playlists."""

    return redirect("/playlists")


##############################################################################
# Playlist routes


@app.route("/playlists")
def show_all_playlists():
    """Return a list of playlists."""

    playlists = Playlist.query.all()
    return render_template("playlists.html", playlists=playlists)


@app.route("/playlists/<int:playlist_id>")
def show_playlist(playlist_id):
    """Show detail on specific playlist."""
    playlist = Playlist.query.get_or_404(playlist_id)
    form = PlaylistForm(obj=playlist)

    if form.validate_on_submit():
        playlist.name = form.name.data
        playlist.description = form.description.data
        db.session.commit()
        flash(f"Playlist {playlist_id} updated!")
        return redirect(url_for("show_playlist", playlist_id =playlist_id))

    else:
        return render_template("playlists.html", form=form)

@app.route("/playlists/add", methods=["GET", "POST"])
def add_playlist():
    """Handle add-playlist form:

    - if form not filled out or invalid: show form
    - if valid: add playlist to SQLA and redirect to list-of-playlists
    """
    form = PlaylistForm()

    if form.validate_on_submit():
        name = form.name.data
        description = form.description.data
        # Add playlist
        new_playlist = Playlist(name=name,description=description)
        # Add new object to session
        db.session.add(new_playlist)
        # Commit
        db.session.commit()
        flash(f"Added playlist {name}!")
        return redirect(url_for('show_playlist', playlist_id = new_playlist.id))
    else:
        return render_template("playlists.html", form=form)

##############################################################################
# Song routes


@app.route("/songs")
def show_all_songs():
    """Show list of songs."""
    songs = Song.query.all()
    return render_template("songs.html", songs=songs)


@app.route("/songs/<int:song_id>")
def show_song(song_id):
    """return a specific song"""
    # ADD THE NECESSARY CODE HERE FOR THIS ROUTE TO WORK
    song = Song.query.get_or_404(song_id)
    form = SongForm(obj=song)

    if form.validate_on_submit():
        song.title = form.title.data
        song.artist = form.artist.data
        db.session.commit()
        flash(f"Song {song_id} updated!")
        return redirect(url_for("show_song", id =song_id))

    else:
        return render_template("songs.html", form=form)    


@app.route("/songs/add", methods=["GET", "POST"])
def add_song():
    """Handle add-song form:

    - if form not filled out or invalid: show form
    - if valid: add playlist to SQLA and redirect to list-of-songs
    """
    # ADD THE NECESSARY CODE HERE FOR THIS ROUTE TO WORK
    form = SongForm()

    if form.validate_on_submit():
        title = form.title.data
        artist = form.artist.data
        # Add song
        new_song = Song(title=title,artist=artist)
        # Add new object to session
        db.session.add(new_song)
        # Commit
        db.session.commit()
        flash(f"Added song {title}!")
        return redirect(url_for('show_song', song_id = new_song.id))
    else:
        return render_template("new_song.html", form=form)


@app.route("/playlists/<int:playlist_id>/add-song", methods=["GET", "POST"])
def add_song_to_playlist(playlist_id):
    """Add a playlist and redirect to list."""

    # BONUS - ADD THE NECESSARY CODE HERE FOR THIS ROUTE TO WORK

    # THE SOLUTION TO THIS IS IN A HINT IN THE ASSESSMENT INSTRUCTIONS

    playlist = Playlist.query.get_or_404(playlist_id)
    form = NewSongForPlaylistForm()

    # Restrict form to songs not already on this playlist

    curr_on_playlist = ...
    form.song.choices = ...

    if form.validate_on_submit():
    # ADD THE NECESSARY CODE HERE FOR THIS ROUTE TO WORK
        return redirect(f"/playlists/{playlist_id}")

    return render_template("add_song_to_playlist.html",
                             playlist=playlist,
                             form=form)

if __name__ == "__main__":
    app.run()
