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
