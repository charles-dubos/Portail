/* Constantes */

const threshold = 100; //this sets the minimum swipe distance, to avoid noise and to filter actual swipes from just moving fingers


/* Variables globales */

let startX;
let startY;
let endX;
let endY;


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
 
    if(startX - endX > threshold){
      linkTo(null, document.getElementById('kbdPageUp'));
    }else if(endX - startX > threshold){
      linkTo(null, document.getElementById('kbdPageDown'));
    };
  })
}
