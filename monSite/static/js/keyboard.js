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

document.onkeydown = function(e) {
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

// Gestion des mouvements Android
document.addEventListener('touchstart', handleTouchStart, false);        
document.addEventListener('touchmove', handleTouchMove, false);

var xDown = null;                                                        
var yDown = null;
                                                                         
function handleTouchStart(evt) {
  const firstTouch = evt.touches[0];                                      
  xDown = firstTouch.clientX;                                      
  yDown = firstTouch.clientY;                                      
};                                                
                                                                         
function handleTouchMove(evt) {
  if ( ! xDown || ! yDown ) {
    return;
  }

  var xUp = evt.touches[0].clientX;                                    
  var yUp = evt.touches[0].clientY;

  var xDiff = xDown - xUp;
  var yDiff = yDown - yUp;
                                                                         
  if ( Math.abs( xDiff ) > Math.abs( yDiff ) ) {/*most significant*/
    if ( xDiff > 0 ) {
      /* right swipe */ 
      linkTo( null, document.getElementById('kbdPageDown'));
    } else {
      /* left swipe */
      linkTo( null, document.getElementById('kbdPageUp'));
    }                       
  } else {
    if ( yDiff > 0 ) {
      /* down swipe */
    } else { 
      /* up swipe */
    }                                                                 
  }
  /* reset values */
  xDown = null;
  yDown = null;                                             
};
