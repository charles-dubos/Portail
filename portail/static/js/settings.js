/* Fonctions d'onglets */

function selectTab(selected) {
  if ( !selected.classList.contains('active') )
    document.querySelector('#tabBar>.active')
      ?.classList.remove('active');
  selected.classList.toggle('active');
  displayActiveTabContent();  
}

function displayActiveTabContent() {
  document.querySelectorAll('.tabPage').forEach(
    (e) => e.classList.remove('active') );
  if ( activeTabId=document.querySelector('#tabBar>.active')
                  ?.getAttribute('forTab') ) {
    console.log(activeTabId);
    document.getElementById(activeTabId).classList.add('active');
  }
}

/* Fonctions de cookies */
function updateMainPage(element) {
  setCookie( "mainPage", element.options[element.selectedIndex].value);
}

function setMainPage() {
  let cookie = getCookie('mainPage');
  document.querySelectorAll("#mainPage-select > option").forEach(
    (e) =>( e.value == cookie ) ? e.setAttribute('selected','true') : null )
}
