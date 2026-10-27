'use strict';

// Content script file will run in the context of web page.
// With content script you can manipulate the web pages using
// Document Object Model (DOM).
// You can also pass information to the parent extension.

// We execute this script by making an entry in manifest.json file
// under `content_scripts` property

// For more information on Content Scripts,
// See https://developer.chrome.com/extensions/content_scripts

// Log `title` of current active web page

function save(data) {
  return new Promise((resolve) => {
    chrome.runtime.sendMessage(
      {
        type: 'SAVE',
        payload: data,
      },
      response => {
        resolve(response);
      }
    );
  })
}

function load(key) {
  return new Promise((resolve, reject) => {
    chrome.runtime.sendMessage(
      {
        type: 'LOAD',
        payload: { key },
      },
      response => {
        if (response.error) {
          return reject(response.error);
        }
        resolve(response);
      }
    );
  })
}

function getInputTemplateFromOuterHTML(outerHTML){
  if (!outerHTML.includes('value=')) {
    outerHTML = outerHTML.replace('>', ' value="">');
  }
  return outerHTML.replace(/name=".*?"/, 'name="{{KEY}}"').replace(/value=".*?"/, 'value="{{VALUE}}"');
}

function input(key, value, outerHTML) {
  key = key.replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;')
  value = value.replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;')
  const template = getInputTemplateFromOuterHTML(outerHTML);
  return template.replace('{{KEY}}', key).replace('{{VALUE}}', value);
}

async function loads() {
  var inputs = document.querySelectorAll('input');
  for (const p of inputs) {
    const key = p.name;
    try {
      var data = await load(key);
      if (data) {
        console.log(input(key, data, p.outerHTML))
        p.outerHTML = input(key, data, p.outerHTML);
      }
    } catch (error) {
      console.log('Error loading data', error);
      continue;
    }
  }
}

async function saves() {
  var inputs = document.querySelectorAll('input');
  for (const input of inputs) {
    input.addEventListener('change', async function (event) {
      const key = event.target.name;
      const value = event.target.value;
      if (!value.includes("shikanoko nokonoko koshitantan")){
        return
      }
      try {
        await save({ key, value });
        console.log('Data saved');
      } catch (error) {
        console.log('Error saving data', error);
      }
    });
  }
}


async function main() {
  console.log('Content script is running');
  await loads();
  await saves();
}

main();
