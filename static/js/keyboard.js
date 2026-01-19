/* Constantes */

const TIME_OUT = 3000; // Timeout par défaut en millisecondes


/* Variables globales */

let selectedChannel = "";
let startX
let startY
let endX
let endY
const threshold = 100; //this sets the minimum swipe distance, to avoid noise and to filter actual swipes from just moving fingers


/* Touches clavier */

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
      dom.onclick()
      break;
  }
  if ( e ) e.preventDefault();
}

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
          // Va vers le lien correspondant au chiffre tapé
          console.log('Enter pressed');
          domKeyboardElement = document.getElementById('kbd'+selectedChannel);
          if ( domKeyboardElement ) {
            console.log('Redirecting to '+ selectedChannel);
            linkTo(e, domKeyboardElement);
          } else {
            selectedChannel = "";
            document.getElementById('selectedChannel').innerHTML = "";
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
    // Ne pas prendre en compte le cas du 0 initial
    if ( e.key != '0' || selectedChannel.length !=0 ) {
      selectedChannel = selectedChannel + e.key;
      document.getElementById('selectedChannel').innerHTML = selectedChannel;

      // Timer d'auto-validation
      window.clearTimeout()
      window.setTimeout(() => {
        console.log('Timeout');
        domKeyboardElement = document.getElementById('kbd'+selectedChannel);
        if ( domKeyboardElement ) {
          console.log('TimeOut redirect to ' + selectedChannel)
          linkTo(null, domKeyboardElement);
        } else {
          selectedChannel = "";
          document.getElementById('selectedChannel').innerHTML = "";
        }
      }, TIME_OUT);

      console.log( selectedChannel );
      e.preventDefault();
    }
  }
}


/* Gestion des mouvements sur écran tactile */

//configs the elements on load
window.onload = function(){
  window.addEventListener('touchstart', function(e){
    //console.log(e);
    startX = e.touches[0].clientX;
    startY = e.touches[0].clientY;
  })
  
  window.addEventListener('touchend', function(e){
    //console.log(event);
    endX = e.changedTouches[0].clientX;
    endY = e.changedTouches[0].clientY;
    let xDist = endX - startX;
    let yDist = endY - startY;
 
    if(startX - endX > threshold){
      linkTo(null, document.getElementById('kbdPageUp'));
    }else if(endX - startX > threshold){
      linkTo(null, document.getElementById('kbdPageDown'));
    };
  })
}
