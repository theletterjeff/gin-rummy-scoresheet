fillNavbarLinks();

// Base template functions
function fillNavbarLinks() {
  fillNavbarLink('navbar-brand', '');
  if (document.getElementById('login-link')) {
    fillNavbarLink('login-link', '/accounts/login/');
  } else {
    getPlayerUsername().then(function(id) {
      fillNavbarLink('matches-nav-link', '/match/');
      fillNavbarLink('account-nav-link', `/player/${id}`);
      fillNavbarLink('logout-nav-link', '/accounts/logout/');
    });
  };
}

function fillNavbarLink(elemName, urlExtension) {
  let navbarElem = document.getElementById(elemName);
  navbarElem.href = window.location.origin + urlExtension
}

function getPlayerUsername() {
  return fetch(window.location.origin + '/api/logged-in-player/')
    .then((resp) => resp.json())
    .then((data) => data.username)
}