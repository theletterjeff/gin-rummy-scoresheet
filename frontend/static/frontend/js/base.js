fillNavbarLinks();

// Base template functions
function fillNavbarLinks() {
  fillNavbarBrandLink();
  if (document.getElementById('login-link')) {
    fillNavbarLoginLink();
    console.log('to do: fill sign up link');
  } else {
    fillNavbarLogoutLink();
    console.log('to do: fill logged in navbar links');
  };
}

function fillNavbarBrandLink() {
  let navbarBrand = document.getElementById("navbar-brand");
  navbarBrand.href = window.location.origin;
}

function fillNavbarLoginLink() {
  let navbarLogin = document.getElementById('login-link');
  navbarLogin.href = window.location.origin + '/login/';
}

function fillNavbarLogoutLink() {
  let navbarLogout = document.getElementById('logout-nav-link');
  navbarLogout.href = window.location.origin + '/accounts/logout/';
}
