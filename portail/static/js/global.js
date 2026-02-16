/* Constantes */


/* Variables globales */

var selectedChannel = null;

// Gestion du switch de son (en local)
const appMuted = {
  state() { return getCookie('muted') },
  updateButton() {
    document.querySelectorAll('audio').forEach(audio => { audio.muted = ( this.state() ) ? true : false });
    document.getElementById("toggleMuted").children[0].classList.remove('fa-volume-high','fa-volume-xmark');
    document.getElementById("toggleMuted").children[0].classList.add( 
      ( this.state() ) ? 'fa-volume-xmark': 'fa-volume-high'
    )
  },
  switch() {
    setCookie( 'muted', this.state() === "true" ? "" : "true" );
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
<<<<<<< HEAD
window.addEventListener("beforeunload", async function () { await waitAudio('sndPage') });
=======
window.addEventListener("beforeunload", async function () { await waitAudio('changePage') });
>>>>>>> dev


/* Gestion de cookies */

function setCookie(name, value) {
  document.cookie = name+"="+value;
}

function getCookie(value) {
  let cookieList = document.cookie.split("; ");
  for (let i = 0; i<cookieList.length; i++ ) {
    if ( cookieList[i].startsWith( value+"=" ) ) {
      return (cookieList[i].substring(value.length + 1));
    }
  }
  return ""
}
