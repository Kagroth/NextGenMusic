class Controller
{
	constructor(mp3player, playPauseButtons)
	{
		this.mp3player = mp3player;
		this.playPauseButtons = playPauseButtons;
		this.actualPlaying = null;
		console.log("Controller created!");
	}
	
	bindPlayPauseEvent()
	{
		console.log("Podpinam zdarzenie!");
		for(let button of this.playPauseButtons)
		{
			button.addEventListener('click', () => {
							
				if(this.mp3player.isPlaying())
				{
					this.actualPlaying.querySelector('img').src = "/static/nextgenmusic/css/icons/play.png";
					this.mp3player.pause();
					
					if(this.actualPlaying === button)
					{
						this.actualPlaying = null;
						return;
					}
					
					button.querySelector('img').src = "/static/nextgenmusic/css/icons/stop.png";
					this.mp3player.setSong(new Song("/static/nextgenmusic/music/" + button.dataset.song_name));
				}
				else
				{
					this.mp3player.setSong(new Song("/static/nextgenmusic/music/" + button.dataset.song_name));
					button.querySelector('img').src = "/static/nextgenmusic/css/icons/stop.png";
				}
				
				this.actualPlaying = button;
				this.mp3player.play();
				
			}, false);
		}
	}
}