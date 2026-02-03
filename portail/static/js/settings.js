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
