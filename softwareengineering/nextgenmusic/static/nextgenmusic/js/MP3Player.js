
class MP3Player
{
	// audio - obiekt klasy Audio()
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
		this.cursor = 0;
	}
	
	setVolume(volume)
	{
		this.audio.volume = volume;
	}
	
	isPlaying()
	{
		return !this.audio.paused;
	}
	
	play()
	{
		if(!this.isPlaying())
		{
			this.audio.play();
		}
	}
	
	pause()
	{
		if(this.isPlaying())
			this.audio.pause();
	}

	setSongTitle()
	{
		document.querySelector('#now_playing').innerHTML = this.song.getArtist() + " - " + this.song.getTitle();
	}
	
	isPlaylistPlayable()
	{
		if(this.playlist === undefined || 
			this.cursor === undefined ||
			this.playlist.songs === undefined ||
			this.playlist.songs.length === 0)
			return false;
		else
			return true;
	}
	
	// rozpoczyna odtwarzanie playlisty
	playPlaylist(startFrom)
	{
		if(startFrom !== undefined)
			this.cursor = startFrom;
		
		let player = this;
		
		if(!this.isPlaylistPlayable())
			return;
		
		if(this.playlist === undefined || 
			this.cursor === undefined ||
			this.playlist.songs === undefined ||
			this.playlist.songs.length === 0)
			return;
		
		this.setSong(this.playlist.getSong(this.cursor));
		
		this.audio.addEventListener('ended', () => {
			player.playNextSong();
		});
		
		this.setSongTitle();
		this.play();
		this.controller.updateListenCount(this.song);
	}
	
	playNextSong()
	{
		if(!this.isPlaylistPlayable())
			return;
		
		this.getNextIndex('next');		
		this.setSong(this.playlist.getSong(this.cursor));
		this.setSongTitle();
		this.play();
		this.controller.updateListenCount(this.song);
	}
	
	playPrevSong()
	{
		if(!this.isPlaylistPlayable())
			return;
		
		this.getNextIndex('prev');
		this.setSong(this.playlist.getSong(this.cursor));
		this.setSongTitle();
		this.play();
		this.controller.updateListenCount(this.song);
	}
	
	// ustaw kolejny indeks tablicy z piosenkami
	getNextIndex(direction)
	{
		if(direction === "next")
			this.cursor++;
		else
			this.cursor--;
		
		if(this.cursor >= this.playlist.songs.length)
		{
			this.cursor = 0;
			console.log(this.cursor);
			return;
		}
		
		if(this.cursor < 0)
		{
			this.cursor = this.playlist.songs.length - 1;
			console.log(this.cursor);
			return;
		}
		
		console.log(this.cursor);
	}
}