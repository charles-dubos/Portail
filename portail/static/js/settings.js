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
  setCookie( "mainPage", element.id.substring(5));
  loadPagesCookies();
}

// function setMainPage() {
//   let cookie = getCookie('mainPage');
//   document.querySelectorAll("#mainPage-select > option").forEach(
//     (e) =>( e.value == cookie ) ? e.setAttribute('selected','true') : null )
// }

function loadPagesCookies() {
  let mainPageId = getCookie('mainPage');
  document.querySelectorAll('input[type="checkbox"]').forEach(chkBox => chkBox.disabled = false);
  document.getElementById("home-"+mainPageId).checked = true;
  delMaskPage(mainPageId);
  document.getElementById("mask-"+mainPageId).disabled = true;
  loadMaskPages();
}

function getMaskPages() {
  let maskPages = getCookie('maskPages');
  if (!maskPages) maskPages = [];
  else maskPages = JSON.parse(maskPages);
  return maskPages;
}

function switchMask(chkBox) {
  if ( chkBox.name == getCookie('mainPage') ) return;
  ( chkBox.checked ? addMaskPage : delMaskPage )(chkBox.name);
  loadMaskPages();
}

function addMaskPage(id) {
  maskPages = getMaskPages();
  maskPages.push(String(id))
  console.log(maskPages)
  setCookie('maskPages', JSON.stringify(
    maskPages )
  );
}

function delMaskPage(id) {
  maskPages = getMaskPages();
  setCookie('maskPages', JSON.stringify( 
    maskPages.filter(function (pageId) {
      return pageId !== id;
      })
    )
  );
}

function loadMaskPages() {
  maskPages = getMaskPages()
  console.log(maskPages);
  document.querySelectorAll(
      'input[type="checkbox"][id^="mask-"]'
    ).forEach(
      chkBox => chkBox.checked = ( maskPages.includes(chkBox.name) ) ? true : false
  );
}

