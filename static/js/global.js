/* Constantes */

const TIME_OUT = 2500; // Timeout par défaut en millisecondes


/* Variables globales */

var selectedChannel = "";
var timeoutId = null;


/* Fonctions globales */

// makes playing audio return a promise
function waitAudio(audioId){
  const sound=document.getElementById(audioId);
  return new Promise(res=>{
    sound.volume=sound.getAttribute('data-volume');
    sound.play();
    sound.onended = res;
  })
}

// makes playing audio not blocking
function playAudio(audioId){
  const sound=document.getElementById(audioId);
  sound.volume=sound.getAttribute('data-volume');
  sound.play();
}

window.addEventListener("beforeunload", async function () { await waitAudio('sndPage') });
