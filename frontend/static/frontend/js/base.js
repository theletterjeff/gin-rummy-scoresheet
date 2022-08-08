fillNavbarLinks();

// Base template functions
function fillNavbarLinks() {
  fillNavbarLink('navbar-brand', '');
  if (document.getElementById('login-link')) {
    fillNavbarLink('login-link', '/accounts/login/');
  } else {
    fillNavbarLink('matches-nav-link', '/match/');
    fillNavbarLink('logout-nav-link', '/accounts/logout/');
  };
}

function fillNavbarLink(elemName, urlExtension) {
  let navbarElem = document.getElementById(elemName);
  navbarElem.href = window.location.origin + urlExtension
}