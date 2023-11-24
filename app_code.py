import streamlit as st
import mysql.connector

try:
    # Connect to MySQL
    conn = mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        password='Ilovetvdtol123$',
        database='dbms_project',
        # port=3306
    )

    cursor = conn.cursor()

    # Check if the 'Song' table exists, and create it if not
    cursor.execute("SHOW TABLES LIKE 'Song'")
    table_exists = cursor.fetchone()

    if not table_exists:
        cursor.execute('''
        CREATE TABLE Song (
            SongID INT AUTO_INCREMENT PRIMARY KEY,
            Title VARCHAR(255),
            Duration VARCHAR(255),
            ReleaseYear INT,
            Rating DECIMAL(3, 2),
            Lyrics TEXT,
            PlayCount INT
        );

        CREATE TABLE IF NOT EXISTS User (
            UserID INT AUTO_INCREMENT PRIMARY KEY,
            Username VARCHAR(255),
            Password VARCHAR(255),
            Email VARCHAR(255),
            ProfilePicture VARCHAR(255)
            );
        CREATE TABLE IF NOT EXISTS Artist (
            ArtistID INT AUTO_INCREMENT PRIMARY KEY,
            Name VARCHAR(255),
            Biography TEXT,
            DateOfBirth DATE,
            DateOfDeath DATE,
            Nationality VARCHAR(255)
            );

        CREATE TABLE IF NOT EXISTS Album (
            AlbumID INT AUTO_INCREMENT PRIMARY KEY,
            Title VARCHAR(255),
            ReleaseYear INT,
            Rating DECIMAL(3, 2),
            RecordLabel VARCHAR(255)
            );

        CREATE TABLE IF NOT EXISTS Genre (
            GenreID INT AUTO_INCREMENT PRIMARY KEY,
            Name VARCHAR(255),
            Description TEXT
            );

        CREATE TABLE IF NOT EXISTS Playlist (
            PlaylistID INT AUTO_INCREMENT PRIMARY KEY,
            Name VARCHAR(255),
            Description TEXT,
            CreatedBy INT,
            FOREIGN KEY (CreatedBy) REFERENCES User(UserID)
            );

        CREATE TABLE IF NOT EXISTS File (
            FileID INT AUTO_INCREMENT PRIMARY KEY,
            FileName VARCHAR(255),
            FilePath VARCHAR(255),
            FileSize INT,
            FileFormat VARCHAR(10),
            Bitrate INT,
            SampleRate INT
            );

        CREATE TABLE IF NOT EXISTS Metadata (
            MetadataID INT AUTO_INCREMENT PRIMARY KEY,
            SongID INT,
            AlbumID INT,
            ArtistID INT,
            GenreID INT,
            FileID INT,
            TrackNumber INT,
            Composer VARCHAR(255),
            Conductor VARCHAR(255),
            BPM INT,
            FOREIGN KEY (SongID) REFERENCES Song(SongID),
            FOREIGN KEY (AlbumID) REFERENCES Album(AlbumID),
            FOREIGN KEY (ArtistID) REFERENCES Artist(ArtistID),
            FOREIGN KEY (GenreID) REFERENCES Genre(GenreID),
            FOREIGN KEY (FileID) REFERENCES File(FileID)
            );

        CREATE TABLE IF NOT EXISTS PlaylistTrack (
            PlaylistTrackID INT AUTO_INCREMENT PRIMARY KEY,
            PlaylistID INT,
            TrackID INT,
            Queue INT,
            FOREIGN KEY (PlaylistID) REFERENCES Playlist(PlaylistID),
            FOREIGN KEY (TrackID) REFERENCES Song(SongID)
            );
        ''')

        conn.commit()


    # Streamlit App
    st.title("Music Management System")


    # Function to add a new song
    def add_song(title, duration, release_year, rating, lyrics, play_count):
        query = "INSERT INTO Song (Title, Duration, ReleaseYear, Rating, Lyrics, PlayCount) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (title, duration, release_year, rating, lyrics, play_count)
        cursor.execute(query, values)
        conn.commit()
        st.success("Song added successfully!")


    # Function to display all songs
    def display_songs():
        cursor.execute("SELECT * FROM Song")
        songs = cursor.fetchall()
        st.write("### All Songs")
        for song in songs:
            st.write(
                f"Title: {song[1]}, Duration: {song[2]}, Release Year: {song[3]}, Rating: {song[4]}, Lyrics: {song[5]}, Play Count: {song[6]}")


    # Add a new song
    st.header("Add a New Song")
    new_title = st.text_input("Title:")
    new_duration = st.text_input("Duration:")
    new_release_year = st.number_input("Release Year:", min_value=1900, max_value=2023)
    new_rating = st.number_input("Rating:", min_value=0.0, max_value=5.0, step=0.1)
    new_lyrics = st.text_area("Lyrics:")
    new_play_count = st.number_input("Play Count:", min_value=0)

    if st.button("Add Song"):
        add_song(new_title, new_duration, new_release_year, new_rating, new_lyrics, new_play_count)
        st.success("Song added successfully!")

    # Display all songs
    display_songs()

except mysql.connector.Error as e:
    st.error(f"Error connecting to MySQL: {e}")
finally:
    # Close MySQL connection
    if 'conn' in locals() and conn.is_connected():
        cursor.close()
        conn.close()
