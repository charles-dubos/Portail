/* Lists sorting */

function sortList () {
  let items = document.getElementById("sortList")
              .getElementsByTagName("li"), current = null;

  // Parcours les éléments
  for (let i of items) {    
    // Identification des poses possibles
    i.ondragstart = () => {
      current = i;
      for (let it of items) {
        if (it != current) { it.classList.add("hint"); }
      }
    };
    
    // Activation de la zone de dépose actuelle
    i.ondragenter = () => {
      for (let j of items) { j.classList.remove("active"); }
      if (i != current) { i.classList.add("active"); }
    };

    // Fin du déplacement
    i.ondragend = () => {
      for (let it of items) {
        it.classList.remove("hint");
        it.classList.remove("active");
        it.classList.remove("current");
    }};
 
    // (B6) DRAG OVER - PREVENT THE DEFAULT "DROP", SO WE CAN DO OUR OWN
    i.ondragover = e => e.preventDefault();
 
    // (B7) ON DROP - DO SOMETHING
    i.ondrop = e => {
      e.preventDefault();
      if (i != current) {
        let currentpos = 0, droppedpos = 0;
        for (let it=0; it<items.length; it++) {
          if (current == items[it]) { currentpos = it; }
          if (i == items[it]) { droppedpos = it; }
        }
        if (currentpos < droppedpos) {
          i.parentNode.insertBefore(current, i.nextSibling);
        } else {
          i.parentNode.insertBefore(current, i);
        }
      }
    };
  }
}
