class Controller
{
	constructor(mp3player, playPauseButtons, addToPlaylistForms)
	{
		this.mp3player = mp3player;
		this.playPauseButtons = playPauseButtons;
		this.addToPlaylistForms = addToPlaylistForms;
		this.actualPlaying = null;
		console.log("Controller created!");
	}
	
	// podpiecie obslugi odgrywania muzyki z glownego listingu utworow
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
	
	// podpiecie obslugi formularza dodajacego utwor do playlisty
	bindAddToPlaylistEvent()
	{
		console.log("Podpinam zdarzenie formularzy!");
		
		for(let form of this.addToPlaylistForms)
        {
			form.onsubmit = function(e) 
			{
				e.preventDefault();
				console.log(this.playlistName.value);
				console.log(this.csrfmiddlewaretoken.value);
				console.log(this.querySelector('.addToPlaylistButton').dataset.song_name.split('.')[0]);
				
				$.ajax({
					beforeSend: function(request){
						request.setRequestHeader("X-CSRFToken", form.csrfmiddlewaretoken.value);
					},
					url: "/addToPlaylist/",
					method: "POST",
					data: {
						playlistName: this.playlistName.value,
						songName: this.querySelector('.addToPlaylistButton').dataset.song_name.split('.')[0]
					}
				}).done(function(msg){
					console.log(msg);
				});
			};

			console.log(form.playlistName.value);
        }
	}
}