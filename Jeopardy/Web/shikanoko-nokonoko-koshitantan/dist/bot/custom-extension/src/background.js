'use strict';

// With background scripts you can communicate with popup
// and contentScript files.
// For more information on background script,
// See https://developer.chrome.com/extensions/background_pages

function save(key, value, origin) {
  return new Promise((resolve, reject) => {
    key = key + "-" + origin;
    console.log("Saving: ", key, value);
    chrome.storage.local.set({ [key]: value }, () => {
      resolve({ message: 'Data saved successfully' })
    })
  })
}
function load(key, origin) {
  return new Promise((resolve, reject) => {
    key = key + "-" + origin;
    console.log("Loading: ", key);
    chrome.storage.local.get([key], data => {
      if (data.hasOwnProperty(key) === false) {
        return reject({ message: 'Data not found' });
      }
      console.log("Data: ", data[key]);
      resolve(data[key]);
    });
  });
}

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  new Promise(async () => {
    const sender_origin = new URL(sender.tab.pendingUrl ?? sender.tab.url).origin;
    console.log("Sender Origin: ", sender_origin);
    console.log("Request: ", request);
    if (request.type === "SAVE") {
      save(request.payload.key, request.payload.value, sender_origin)
        .then(response => sendResponse(response))
        .catch(error => sendResponse({ error }));
    } else if (request.type === "LOAD") {
      load(request.payload.key, sender_origin)
        .then(response => sendResponse(response))
        .catch(error => sendResponse({ error }));
    }
  })
  return true;
});
