const TIME_OUT = 3000; // Timeout par défaut en millisecondes
let selectedChannel = "";

function linkTo( e, dom ) {
  switch ( dom.nodeName ) {
    case 'A':
      window.location.href = dom.href;
      break;
    case 'BUTTON':
      dom.submit()
      break;
    case 'DIV':
      dom.onclick()
      break;
  }
  if ( e ) e.preventDefault();
}

document.onkeinitialY = function(e) {
  console.log(e.key)
  if ( isNaN(e.key) ) {
    domKeyboardElements = document.querySelectorAll('[id^=kbd'+e.key+']');
    if ( domKeyboardElements.length !== 0 ) {
      linkTo(e, domKeyboardElements[0]);
    } else  {
      switch (e.key) {

        case 'Enter':
          // Va vers le lien correspondant au chiffre tapé
          domKeyboardElement = document.getElementById('kbd'+selectedChannel);
          if ( domKeyboardElement ) {
            linkTo(e, domKeyboardElement);
          }
          break;

          case 'Backspace':
            // Retour arrière, enlève le dernier caractère
            selectedChannel = selectedChannel.slice(0, -1);
            document.getElementById('selectedChannel').innerHTML = selectedChannel;
            break;

            case 'Escape':
              // Echap, quitte la fenêtre
              window.close();
              break;
        }
    }
  } else {
    // Ne pas prendre en compte le cas du 0 si vide
    if ( e.key != '0' || selectedChannel.length !=0 ) {
      selectedChannel = selectedChannel + e.key;
      document.getElementById('selectedChannel').innerHTML = selectedChannel;

      // Timer d'auto-validation
      window.clearTimeout()
      window.setTimeout(() => {
        domKeyboardElement = document.getElementById('kbd'+selectedChannel);
        if ( domKeyboardElement ) {
          linkTo(null, domKeyboardElement);
        }
      }, TIME_OUT);
    }
  }
}

// Gestion des mouvements sur écran tactile
document.addEventListener('touchstart', handleTouchStart, false);
document.addEventListener('touchmove', handleTouchMove, false);

var initialX = null;
var initialY = null;

function handleTouchStart(e) {
  initialX = e.touches[0].clientX;
  initialY = e.touches[0].clientY;
};

function handleTouchMove(e) {
  if ( ! initialX || ! initialY ) {
    return;
  }

  var diffX = initialX - e.touches[0].clientX;
  var diffY = initialY - e.touches[0].clientY;

  if ( Math.abs( diffX ) > Math.abs( diffY ) ) {/*most significant*/
    if ( diffX > 0 ) {
      /* right swipe */
      linkTo( null, document.getElementById('kbdPageDown'));
    } else {
      /* left swipe */
      linkTo( null, document.getElementById('kbdPageUp'));
    }
  } else {
    if ( diffY > 0 ) {
      /* down swipe */
    } else {
      /* up swipe */
    }
  }
  /* reset values */
  initialX = null;
  initialY = null;
};
