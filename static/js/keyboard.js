/* Constantes */


/* Variables globales */


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
            document.getElementById('selectedChannelDisplay').innerHTML = "";
          }
          break;

          case 'Backspace':
            // Retour arrière, enlève le dernier caractère
            selectedChannel = selectedChannel.slice(0, -1);
            document.getElementById('selectedChannelDisplay').innerHTML = selectedChannel;
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
      document.getElementById('selectedChannelDisplay').innerHTML = selectedChannel;

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
          document.getElementById('selectedChannelDisplay').innerHTML = "";
        }
      }, TIME_OUT);

      console.log( selectedChannel );
      e.preventDefault();
    }
  }
}
