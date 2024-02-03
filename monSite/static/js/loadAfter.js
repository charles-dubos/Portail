/*
 * -- ALL CARDS IN SCREEN --
 * Fonction qui calcule de façon responsive le nombre de cartes pour qu'elles tiennent sur l'écran
 */
updateCardSizes();

window.onresize = updateCardSizes


/*
 * -- MODAL BOXES --
 * Affichages de boites modales
 */

// Get the <span> element that closes the modal
var modal = '';

// When the user clicks on the button, open the modal
function enableModal(id) {
  modal = document.getElementById(id);

  // When the user clicks on <span> (x), close the modal
  modal.getElementsByClassName("close")[0].onclick = function() {
    modal.style.display = "none";
  }

  modal.style.display = "block";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}
