fillNavbarLinks();

// Base template functions
function fillNavbarLinks() {
  fillNavbarBrandLink();
  if (document.getElementById('login-link')) {
    fillNavbarLoginLink();
    console.log('to do: fill sign up link');
  } else {
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


// Export functions

export function fillTitle(titleString) {
  let title = document.getElementsByTagName('title')[0];
  title.innerHTML = titleString;
}

/** Get cookie value (used to pass CSRF token to POST requests) */
export function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}
