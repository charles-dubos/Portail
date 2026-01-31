/* Constantes */
const KBD_TIMEOUT_MS = 2500;
const MOUSE_TIMEOUT_MS = 1500;

/* Variables globales */
var kbdEnterTimer = null;
// var mouseMoveTimer = null;


/* Touches clavier */

// Fonctions générales

async function linkTo( e, dom ) {
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
      await waitAudio('sndEnter');
      document.getElementById('sndPage').muted=true;
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

async function keyEscPress() {
  await waitAudio('sndBye');
  window.close();
}

// Gestion de l'appui
document.onkeydown = function(e) {

  console.log(e.key)
  if ( document.getElementsByClassName('enable-mouse').length != 0 )
      disableMouseOnChilds();

  if ( isNaN(e.key) ) {
    // S'il ne s'agit pas d'un numéro, cherche un id en kbdXXX
    domKeyboardElements = document.querySelectorAll('[id^=kbd'+e.key+']');
    if ( domKeyboardElements.length !== 0 ) {
      linkTo(e, domKeyboardElements[0]);
    } else  {
      // Touches spéciales
      switch (e.key) {

        case 'Enter':
          keyEnterPress(e);
          break;

          case 'Backspace':
            setChannel(selectedChannel.slice(0, -1));
            break;

          case 'Escape':
            keyEscPress();
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
      kbdEnterTimer = window.setTimeout(() => {
        console.log('Timeout ');

        domKeyboardElement = document
          .getElementById('kbd'+selectedChannel);

        if ( domKeyboardElement ) linkTo(null, domKeyboardElement);
        else setChannel( "" );

      }, KBD_TIMEOUT_MS);

      e.preventDefault();
    }
  }
}


/* Désactivation souris */

function enableMouseOnChilds() {
  console.log('Enable mouse')
  document.querySelectorAll('.cards-container').forEach(
    (cardContainer) => cardContainer.classList.add('enable-mouse')
  );
  // if ( mouseMoveTimer ) clearTimeout(mouseMoveTimer);
  // mouseMoveTimer = setTimeout('disableMouseOnChilds()', MOUSE_TIMEOUT_MS);
}

function disableMouseOnChilds() {
  console.log('Disable mouse')
  document.querySelectorAll('.cards-container').forEach(
    (cardContainer) => cardContainer.classList.remove('enable-mouse')
  );
  // mouseMoveTimer = null
}
