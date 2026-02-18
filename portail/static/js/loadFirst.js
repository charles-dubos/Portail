/*
 * -- ALL CARDS IN SCREEN --
 * Fonction qui calcule de façon responsive le nombre de cartes pour qu'elles tiennent sur l'écran
 */

let nbrOfCols; // Nombre de colonnes de cartes
let nbrOfRows; // Nombre de rangées de cartes

let n;
let r;

function loadValues(number, ratio) {
  n=number;
  r=ratio;
  document.getElementById('content-wrapper').style.top = 
    document.getElementsByClassName("header-menu")[0].offsetHeight+'px';
}

function widthOfCard() {
  let x = document.documentElement.clientWidth;
  let y = document.documentElement.clientHeight;

  // Il faut retirer sur l'axe y l'en-tête et le pied de page..
  document.querySelectorAll('.home-menu').forEach(
    element => {
      y = y - element.offsetHeight
    }
  )

  // Calcul du nombre de lignes et de colonnes optimal
  nbrOfCols = Math.ceil(Math.sqrt(n*x/(y*r)))
  nbrOfRows = Math.ceil(n/nbrOfCols)

  // Evaluation que la carte rentre, sinon redimensionnement
  if ((r*x / nbrOfCols) > (y / nbrOfRows)) {
    nbrOfCols = Math.ceil(
      nbrOfRows * x / y
    );
  }

  return Math.floor(x/nbrOfCols);
}

function updateCardSizes() {
  let a = widthOfCard();
  document.querySelectorAll('.card-wrapper').forEach(
    card => {
      card.style.width = a+'px';
      card.style.height = Math.floor(r*a)+'px';
      card.style.fontSize = Math.floor(a/10)+'px';
    }
  )
}
