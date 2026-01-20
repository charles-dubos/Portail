/* Constantes */


/* Variables globales */


/* Selection de carte */

function unselectCard() {
  document.querySelectorAll('.selected').forEach(element => {
    element.classList.remove('selected')
  });
}

function selectCard() {
  if ( document.getElementById('kbd'+selectedChannel) )
    document.getElementById('kbd'+selectedChannel).classList.add(
      'selected'
    );
}

function updateSelectedChannel() {
  unselectCard();
  if ( timeoutId ) {
    window.clearTimeout(timeoutId);
    timeoutId = null
  };
  document.getElementById('selectedChannelDisplay').innerHTML = selectedChannel;
  selectCard();
}

function setChannel(newChannel) {
  selectedChannel=newChannel;
  updateSelectedChannel();
}

// Fonctions de sélection par déplacement
function changeCard(move) {
  let arrayOfChannelId = Array.from(document.getElementsByClassName('card')).map(
    (e) => e.getAttribute('id').substring(3)
  );
  
  let newIndex=arrayOfChannelId.indexOf(selectedChannel);
  if ( newIndex === -1 ) {
    // S'il n'y a pas de canal sélectionné, sélection du premier
    newIndex=0
  } else {
    newIndex = newIndex + ( ( (newIndex+move)>=0 && (newIndex+move)< arrayOfChannelId.length ) ? move : 0 )
  }
  setChannel( arrayOfChannelId[newIndex] );
}

function selectColLeft() { changeCard(-1) }

function selectColRight() { changeCard(1) }

function selectRowUp() { changeCard(-nbrOfCols) }

function selectRowDown(){ changeCard(nbrOfCols) }
