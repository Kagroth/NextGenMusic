class Controller
{
	constructor(mp3player, playPauseButtons, addToPlaylistForms)
	{
		this.mp3player = mp3player;
		this.mp3player.controller = this;
		this.playPauseButtons = playPauseButtons;
		this.addToPlaylistForms = addToPlaylistForms;
		this.actualPlaying = null;
		this.that = this;
		console.log("Controller created!");
	}
	
	// przycisk odpalajacy konkretny utwor
	setPlayPlaylistEvent(buttons)
	{
		this.playPlaylistButtons = buttons;
		
		for(let button of this.playPlaylistButtons)
		{
			let playButton = button;
			
			button.addEventListener('click', () => {
				this.mp3player.playPlaylist(playButton.dataset.song_id - 1);				
			}, false);
		}
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
	
	// ustawienie playlisty odtwarzania
	setPlaylist(playlist)
	{
		this.mp3player.setPlaylist(playlist);
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
		let controller = this;
		let formWithPlaylistName;
		let songName;
				
		for(let form of this.removeFromPlaylistForms)
		{
			form.addEventListener("submit", (e) => {
				e.preventDefault();			
				
				formWithPlaylistName = form;
				songName = form.querySelector('.removeFromPlaylistButton').dataset.song_name.split('.')[0];
				
				console.log(form.playlistName.value);
				console.log(songName);
				console.log("Bede usuwal utwor z playlisty!!");
				
			});
		}
		
		// podpiecie obslugi 
		$('.removeFromPlaylistButton').click(function () {
				$('.check').css({
					visibility: 'visible'
				}).animate({
					top: this.clientY,
					left: '50%',
					width: 400,
					opacity: 1
				});
					
				document.querySelector('#removeConfirm').addEventListener('click', () => {
					controller.removeFromPlaylist(formWithPlaylistName, songName);
				}, false);
					
				document.querySelector('#removeReject').addEventListener('click', () => {
					$('.check').css({
						visibility: 'hidden',
						left: '75%',
						opacity: 0
					});
					
					formWithPlaylistName = null;
					songName = null;
				}, false);
					
		});
	}
	
	// wysyla request z usunieciem utworu z playlisty
	removeFromPlaylist(formWithPlaylistName, songName)
	{
		$.ajax({
			beforeSend: function(request)
			{
				request.setRequestHeader("X-CSRFToken", formWithPlaylistName.csrfmiddlewaretoken.value);
			},
			
			url: "/removeFromPlaylist/",
			method: "POST",
			data: {
				playlistName: formWithPlaylistName.playlistName.value,
				songName: songName
			},
			success: function(msg)
			{
				location.href = "/myprofile/" + formWithPlaylistName.playlistName.value + "/";
			},
			error: function(msg)
			{
				alert("Nie udalo sie usunac utworu!");
			}
		});
	}
	
	// wyslanie danych do serwera
	updateListenCount(song)
	{
		let songToUpdate;
		
		if(song !== undefined)
		{			
			songToUpdate = song.getFilename();
		}
		else
		{
			songToUpdate = this.actualPlaying.dataset.song_name.split('.')[0];
		}
		
		console.log("Przed wysłaniem: ");
		console.log(this.csrfToken);
		console.log(songToUpdate);
		
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
				songName: songToUpdate
			},
			success: function(msg)
			{
				console.log(msg.message);
			}
		});
	}
}