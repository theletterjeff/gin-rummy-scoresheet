import {getCookie} from './base.js';

let loginForm = document.getElementById("login-form");
loginForm.addEventListener("submit", (e) => submitLoginForm(e));

function getLoginEndpoint() {
  const pageURL = new URL(window.location.href);
  const pageOrigin = pageURL.origin;
  return `${pageOrigin}/api/token/`;
}

async function submitLoginForm(e) {
  e.preventDefault();

  const loginEndpoint = getLoginEndpoint();
  const csrfToken = getCookie("csrftoken");

  let response = await fetch(loginEndpoint, {
    method:"POST",
    headers:{
      "Content-Type": "application/json",
      "X-CSRFToken": csrfToken
    },
    body:JSON.stringify({
      "username": e.target.username.value,
      "password": e.target.password.value,
    })
  });

  if (response.status === 200) {
    let tokenData = await response.json();    
    const homeURL = getHomeURL();

    window.location.href = homeURL;
  } else {
    resetLoginForm();
  };
}

function getHomeURL() {
  const pageURL = new URL(window.location.href);
  return pageURL.origin;
}

/** Reset login form and add an invalid credentials warning */
function resetLoginForm() {
  document.getElementById('login-form').reset();
  
  // Add invalid credentials warning if there isn't already one on the page
  if (document.getElementById('invalid-credentials') == null) {
    addInvalidCredentialsWarning();
  }
}

function addInvalidCredentialsWarning() {
  let invalidCredentialsElem = document.createElement('p');
  let invalidCredentialsText = document.createTextNode('Invalid username and password. Please re-enter.')

  invalidCredentialsElem.appendChild(invalidCredentialsText);
  invalidCredentialsElem.id = 'invalid-credentials';
  invalidCredentialsElem.className = "mt-3 mb-0";

  let loginForm = document.getElementById('login-form');
  loginForm.appendChild(invalidCredentialsElem);
}
