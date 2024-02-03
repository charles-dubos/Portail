/*
 * -- ALL CARDS IN SCREEN --
 * Fonction qui calcule de façon responsive le nombre de cartes pour qu'elles tiennent sur l'écran
 */
let n;
let r;

function loadValues(number, ratio) {
  n=number;
  r=ratio;
  document.getElementsByClassName('content-wrapper')[0].style.top = 
    document.getElementsByClassName("header-menu")[0].offsetHeight+'px';
}

function widthOfCard() {
  let x = document.documentElement.clientWidth;
  let y = document.documentElement.clientHeight;

  // Il faut retirer sur l'axe y l'en-tête et le pied de page...
  Array.from(document.getElementsByClassName("home-menu")).forEach(
    element => {
      y = y - element.offsetHeight
    }
  )

  // Calcul du nombre de lignes et de colonnes optimal
  let computedNumberOfCardByLine = Math.ceil(Math.sqrt(n*x/(y*r)))
  let numberOfLines = Math.ceil(n/computedNumberOfCardByLine)

  // Evaluation que la carte rentre, sinon redimensionnement
  if ((r*x / computedNumberOfCardByLine) > (y / numberOfLines)) {
    computedNumberOfCardByLine = Math.ceil(
      numberOfLines * x / y
    );
  }

  return Math.floor(x/computedNumberOfCardByLine);
}

function updateCardSizes() {
  let a = widthOfCard();
  Array.from(document.getElementsByClassName('card-wrapper')).forEach(
    card => {
      card.style.width = a+'px';
      card.style.height = Math.floor(r*a)+'px';
      card.style.fontSize = Math.floor(a/10)+'px';
    }
  )
}
