/* Constantes */


/* Variables globales */

var selectedChannel = "";

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


// Gestion du switch de dark mode (en local)
const darkMode = {
  state() { return getCookie('darkmode') },
  updateButton() {
    document.getElementById("toggleDarkmode").children[0].classList.remove('fa-moon','fa-sun', 'fa-circle-half-stroke');
    switch (this.state()) {
      case "true":
        document.getElementById("toggleDarkmode").children[0].classList.add('fa-moon');
        break;
      case "false":
        document.getElementById("toggleDarkmode").children[0].classList.add('fa-sun');
        break;
      default:
        document.getElementById("toggleDarkmode").children[0].classList.add('fa-circle-half-stroke');
    }
  },
  switch() {
    switch (this.state()) {
      case "true":
        setCookie( 'darkmode', "false" );
        break;
      case "false":
        setCookie( 'darkmode', "" );
        break;
      default:
        setCookie( 'darkmode', "true" );
    }
    this.updateButton();
    profileMode();
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
window.addEventListener("beforeunload", async function () { await waitAudio('changePage') });


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
