import { getRequestPlayerUsername } from './utils.js';

fillNavbarLinks();

// Base template functions
function fillNavbarLinks() {
  fillNavbarLink('navbar-brand', '');
  if (document.getElementById('login-link')) {
    fillNavbarLink('login-link', '/accounts/login/');
    fillNavbarLink('signup-link', '/accounts/signup/');
  } else {
    getRequestPlayerUsername().then(function(username) {
      fillNavbarLink('matches-nav-link', `/players/${username}/matches/`);
      fillNavbarLink('account-nav-link', `/players/${username}/`);
      fillNavbarLink('logout-nav-link', '/accounts/logout/');
    });
  };
}

function fillNavbarLink(elemName, urlExtension) {
  let navbarElem = document.getElementById(elemName);
  navbarElem.href = window.location.origin + urlExtension
}
