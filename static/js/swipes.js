/* Constantes */

const threshold = 100; //this sets the minimum swipe distance, to avoid noise and to filter actual swipes from just moving fingers
const sortableList = document.querySelector('.sortable-list');


/* Variables globales */

let startX;
let startY;
let endX;
let endY;
let draggingItem = null;


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


/* Lists swipes */

sortableList.addEventListener('dragstart', (e) => {
    draggingItem = e.target;
    e.target.classList.add('dragging');
});

sortableList.addEventListener('dragend', (e) => {
    e.target.classList.remove('dragging');
    document.querySelectorAll('.sortable-item')
        .forEach(item => item.classList.remove('over'));
    draggingItem = null;
});

sortableList.addEventListener('dragover', (e) => {
    e.preventDefault();
    const draggingOverItem = getDragAfterElement(sortableList, e.clientY);
    document.querySelectorAll('.sortable-item').forEach
        (item => item.classList.remove('over'));
    if (draggingOverItem) {
        draggingOverItem.classList.add('over');
        sortableList.insertBefore(draggingItem, draggingOverItem);
    } else {
        sortableList.appendChild(draggingItem); 
    }
});

function getDragAfterElement(container, y) {
    const draggableElements = [...container.querySelectorAll
        ('.sortable-item:not(.dragging)')];
    return draggableElements.reduce((closest, child) => {
        const box = child.getBoundingClientRect();
        const offset = y - box.top - box.height / 2;
        if (offset < 0 && offset > closest.offset) {
            return { offset: offset, element: child };
        } else {
            return closest;
        }
    }, { offset: Number.NEGATIVE_INFINITY }).element;
}
