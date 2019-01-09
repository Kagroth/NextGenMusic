
class Playlist
{
	constructor(songs)
	{
		// tablica piosenek
		this.songs = songs;
	}
	
	getSong(index)
	{
		return this.songs[index];		
	}
}