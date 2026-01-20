/* Constantes */


/* Variables globales */


/* Touches clavier */

// Fonctions générales

function linkTo( e, dom ) {
  // En fonction du type, redirige vers le lien, exécute le submit ou le onclick
  switch ( dom.nodeName ) {
    case 'A':
      console.log('Redirection vers ' + dom.href);
      window.location.href = dom.href;
      break;
    case 'BUTTON':
      console.log('Clic bouton');
      dom.submit()
      break;
    case 'DIV':
      console.log('Div clic');
      dom.getElementsByClassName('card-img')[0].onclick()
      break;
  }
  if ( e ) e.preventDefault();
}


// Fonctions d'appui de touche

function keyEnterPress(e) {
  // Va vers le lien correspondant au chiffre tapé
  console.log('Enter pressed');
  domKeyboardElement = document.getElementById('kbd'+selectedChannel);
  if ( domKeyboardElement )  linkTo(e, domKeyboardElement);
  else setChannel("");
}


// Gestion de l'appui
document.onkeydown = function(e) {
  console.log(e.key)
  if ( isNaN(e.key) ) {
    // S'il ne s'agit pas d'un numéro, cherche un id en kbdXXX
    domKeyboardElements = document.querySelectorAll('[id^=kbd'+e.key+']');
    if ( domKeyboardElements.length !== 0 ) {
      linkTo(e, domKeyboardElements[0]);
    } else  {
      // Touches spéciales
      switch (e.key) {

        case 'Enter':
          // Enter, valide la sélection de chaine
          keyEnterPress(e);
          break;

          case 'Backspace':
            // Retour arrière, enlève le dernier caractère
            setChannel(selectedChannel.slice(0, -1));
            break;

          case 'Escape':
            // Echap, quitte la fenêtre
            window.close();
            break;
          
          case 'ArrowLeft':
            selectColLeft();
            break;
          
          case 'ArrowRight':
            selectColRight();
            break;
          
          case 'ArrowUp':
            selectRowUp();
            break;
          
          case 'ArrowDown':
            selectRowDown();
            break;
        }
    }
  } else {
    // Ne pas prendre en compte le cas du 0 initial
    if ( e.key != '0' || selectedChannel.length !=0 ) {
      setChannel( selectedChannel + e.key );

      // Timer d'auto-validation
      timeoutId = window.setTimeout(() => {
        console.log('Timeout ');

        domKeyboardElement = document
          .getElementById('kbd'+selectedChannel);

        if ( domKeyboardElement ) linkTo(null, domKeyboardElement);
        else setChannel( "" );

      }, TIME_OUT);

      e.preventDefault();
    }
  }
}
