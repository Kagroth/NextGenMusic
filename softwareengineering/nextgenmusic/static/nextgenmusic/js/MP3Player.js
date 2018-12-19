
class MP3Player
{
	// audio obiekt klasy Audio()
	constructor(audio)
	{
		this.audio = audio;
	}
	
	// song - obiekt klasy Song
	setSong(song)
	{
		this.song = song;
		this.audio.src = this.song.src;
	}
	
	// playlist - obiekt klasy Playlist
	setPlaylist(playlist)
	{
		this.playlist = playlist;
	}
	
	isPlaying()
	{
		return !this.audio.paused;
	}
	
	play()
	{
		if(!this.isPlaying())
			this.audio.play();
	}
	
	pause()
	{
		if(this.isPlaying())
			this.audio.pause();
	}
	
	
}