
class Song
{
	constructor(src, artist, title, filename)
	{
		this.src = src;
		this.artist = artist;
		this.title = title;
		this.filename = filename;
	}
	
	getSrc()
	{
		return this.src;
	}
	
	getArtist()
	{
		return this.artist;
	}
	
	getTitle()
	{
		return this.title;
	}
	
	getFilename()
	{
		return this.filename.split('.')[0];
	}
}