/* Constantes */

const TIME_OUT = 2500; // Timeout par défaut en millisecondes
const LS_MUTED = "portail.dubs_muted"
const LS_MAINPAGE = "portail.dubs_main"


/* Variables globales */

var selectedChannel = "";
var timeoutId = null;

// Gestion du switch de son (en local)
const appMuted = {
  state() { return window.localStorage.getItem(LS_MUTED) },
  updateState() { 
    if ( document.querySelectorAll('audio')[0].muted ) window.localStorage.setItem(LS_MUTED, "true");
    else window.localStorage.removeItem(LS_MUTED);
   },
  updateButton() {
    document.querySelectorAll('audio').forEach(audio => { audio.muted = ( this.state() ) ? true : false });
    document.getElementById("toggleMuted").children[0].classList.remove('fa-volume-high','fa-volume-xmark');
    document.getElementById("toggleMuted").children[0].classList.add( 
      ( this.state() ) ? 'fa-volume-xmark': 'fa-volume-high'
    )
  },
  switch() {
    document.querySelectorAll('audio')[0].muted = ( this.state() ) ? false : true ;
    this.updateState();
    this.updateButton();
  }
}


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

// Son en quittant
window.addEventListener("beforeunload", async function () { await waitAudio('sndPage') });
