export async function getJsonResponse(endpoint) {
  let json = await fetch(endpoint)
             .then((response) => response.json());
  return json;
}

export async function getJsonResponseArray(endpointArray) {
  let jsonArray = [];
  for (let endpoint of endpointArray) {
    jsonArray.push(await getJsonResponse(endpoint));
  };
  return jsonArray;
}

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
/**
 * Loop over an array of form elements, setting each one as disabled.
 */
export function setFormElemsAsDisabled(elemNames) {
  for (let elemName of elemNames) {
    document.getElementById(elemName).setAttribute('disabled', '');
  }
}
/**
 * Loop over an array of form elements, setting each one as enabled if it is 
 * not already enabled.
 */
export function setFormElemsAsEnabled(elemNames) {
  for (let elemName of elemNames) {
    document.getElementById(elemName).removeAttribute('disabled');
  }
}
/**
 * Set an element as hidden.
 */
export function setElemAsHidden(elemName) {
  document.getElementById(elemName).setAttribute('hidden', '');
}

export function formatDate(dateObj) {
  if ((dateObj instanceof Date) == false) {
    dateObj = new Date(dateObj);
  };
  let monthNum = dateObj.getMonth() + 1;
  let dateNum = dateObj.getDate();
  let yearNum = dateObj.getUTCFullYear() % 100;
  return `${monthNum}/${dateNum}/${yearNum}`;
}

export function formatDateRange(dateObjStart, dateObjEnd) {
  let formattedStart = formatDate(dateObjStart);
  let formattedEnd = formatDate(dateObjEnd);
  return `${formattedStart}-${formattedEnd}`;
}

/**
 * Given a key name ('matches', 'games', 'players'), return the value that
 * is in the next position in the URL (e.g., 'players/some_username' with
 * 'players' passed in as `key` would return 'some_username').
 */
export function getValFromUrl(urlStr, key) {
  let urlArray = urlStr.split('/');
  let val_idx = urlArray.indexOf(key) + 1;
  return urlArray[val_idx];
}

/**
 * Return a Promise of an element loading.
 */
export function waitForElem(elemId) {
  return new Promise((resolve, reject) => {
    if (document.getElementById(elemId)) {
      return resolve(document.getElementById(elemId));
    }
    const observer = new MutationObserver(mutations => {
      if (document.getElementById(elemId)) {
        resolve(document.getElementById(elemId));
        observer.disconnect();
      }
    });
    observer.observe(document.body, {
      childList: true,
      subtree: true
    });
  });
}

/**
 * Get JSON response object of the request player (user).
 */
export async function getRequestPlayerUsername() {
  const requestPlayerEndpoint = window.location.origin + '/api/request-player/';
  const requestPlayerObj = await getJsonResponse(requestPlayerEndpoint);
  return requestPlayerObj.username;
}
/**
 * Format a float value as a percentage.
 */
export function formatAsPct(float) {
  const value = Math.round(float * 100)
  return `${value}%`
}
