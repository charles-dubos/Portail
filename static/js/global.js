/* Constantes */

const TIME_OUT = 2500; // Timeout par défaut en millisecondes
const SND_ENTER = 'https://universal-soundbank.com/sounds/7571.mp3'; // Son lors de la validation de chaine
const SND_PAGE = 'https://universal-soundbank.com/sounds/9099.mp3'; // Son lors du changement de page
const SND_MOVE = 'https://universal-soundbank.com/sounds/21181.mp3'; // Son lors du déplacement sur la page
const SND_BYE = 'https://universal-soundbank.com/sounds/11576.mp3'; // Avant fermeture fenêtre

/* Variables globales */

var selectedChannel = "";
var timeoutId = null;


/* Fonctions globales */

// makes playing audio return a promise
function waitAudio(mp3url){
  const sound=new Audio(mp3url);
  return new Promise(res=>{
    sound.volume=0.3;
    sound.play();
    sound.onended = res;
  })
}

// makes playing audio not blocking
function playAudio(mp3url){
  const sound=new Audio(mp3url);
  sound.volume=0.1;
  sound.play();
}
