fillNavbarBrandLink();

// Functions

export function fillTitle(titleString) {
  let title = document.getElementsByTagName('title')[0];
  title.innerHTML = titleString;
}

function fillNavbarBrandLink() {
  let navbarBrand = document.getElementById("navbar-brand");
  navbarBrand.href = window.location.origin;
}
