class Controller
{
	constructor(mp3player, playPauseButtons, addToPlaylistForms)
	{
		this.mp3player = mp3player;
		this.playPauseButtons = playPauseButtons;
		this.addToPlaylistForms = addToPlaylistForms;
		this.actualPlaying = null;
		this.that = this;
		console.log("Controller created!");
	}
	
	// formy obslugujace usuwanie z playlist
	setRemoveFromPlaylistForms(forms)
	{
		this.removeFromPlaylistForms = forms;
	}
		
	// ustawienie tokenu csrf
	setCSRFToken(token)
	{
		this.csrfToken = token;
	}

	// ustawienie nazwy uzytkownika
	setUsername(name)
	{
		console.log(name);
		this.username = name;
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
				this.updateListenCount();
				
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
				
				// dodanie utworu do playlisty
				$.ajax({
					beforeSend: function(request){
						request.setRequestHeader("X-CSRFToken", form.csrfmiddlewaretoken.value);
					},
					url: "/addToPlaylist/",
					method: "POST",
					data: {
						playlistName: this.playlistName.value,
						songName: this.querySelector('.addToPlaylistButton').dataset.song_name.split('.')[0]
					},
					success: function(msg){
						console.log(msg.message);
						alert(msg.message);
					}
				});
			};

			console.log(form.playlistName.value);
        }
	}
	
	// podpiecie obslugi usuniecia utworu z Playlisty
	bindRemoveFromPlaylistEvent()
	{
		for(let form of this.removeFromPlaylistForms)
		{
			form.addEventListener("submit", (e) => {
				e.preventDefault();
				let songName = form.querySelector('.removeFromPlaylistButton').dataset.song_name.split('.')[0];
				
				console.log(form.playlistName.value);
				console.log(songName);
				console.log("Bede usuwal utwor z playlisty!!");
				
				$.ajax({
					beforeSend: function(request)
					{
						request.setRequestHeader("X-CSRFToken", form.csrfmiddlewaretoken.value);
					},
					
					url: "/removeFromPlaylist/",
					method: "POST",
					data: {
						playlistName: form.playlistName.value,
						songName: songName
					},
					success: function(msg)
					{
						location.href = "/myprofile/" + form.playlistName.value + "/";
					}
				});
			});
		}
	}
	
	// wyslanie danych do serwera
	updateListenCount()
	{		
		console.log("Przed wysłaniem: ");
		console.log(this.csrfToken);
		console.log(this.actualPlaying.dataset.song_name);
		
		let token = this.csrfToken;
		
		$.ajax({
			beforeSend: function(request)
			{
				console.log(token);
				request.setRequestHeader("X-CSRFToken", token);
			},
			
			url: "/listenCountUpdate/",
			method: "POST", 
			data: {
				songName: this.actualPlaying.dataset.song_name.split('.')[0],
			},
			success: function(msg)
			{
				console.log(msg.message);
			}
		});
	}
}