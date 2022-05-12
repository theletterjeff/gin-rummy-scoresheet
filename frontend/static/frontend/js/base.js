fillNavbarBrandLink();

// Base template functions

function fillNavbarBrandLink() {
  let navbarBrand = document.getElementById("navbar-brand");
  navbarBrand.href = window.location.origin;
}

// Export functions

export function fillTitle(titleString) {
  let title = document.getElementsByTagName('title')[0];
  title.innerHTML = titleString;
}

export function getAPIEndpointRoot() {
    const pageURL = new URL(window.location.href);
    const pageOrigin = pageURL.origin;
    return `${pageOrigin}/api`;
}
