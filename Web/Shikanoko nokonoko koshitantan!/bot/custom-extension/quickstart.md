# Welcome to your Chrome Extension

## What's in this directory
* `config/`: Webpack configuration for this project.
* `public/`: Popup files.
    * `manifest.json`: Extension [configuration](https://developer.chrome.com/docs/extensions/mv2/manifest/).
* `src/`: Source files for the popup, [background scripts](https://developer.chrome.com/docs/extensions/mv3/service_workers/#manifest), and [content scripts](https://developer.chrome.com/docs/extensions/mv3/content_scripts/).
* `.gitignore`: Lists files to be ignored in your Git repo.
* `package.json`: Contains project configuration, scripts, and dependencies.

## Test the extension
1. `npm run watch`
2. Open [chrome://extensions](chrome://extensions).
3. Enable developer mode (top right of page).
4. Click "Load unpacked extension" (top left page).
5. Select this directory.

## Bundle the extension
To package the source code into static files for the Chrome webstore, execute `npm run build`.

## Documentation
Refer to [the Chrome developer documentation](https://developer.chrome.com/docs/extensions/mv3/getstarted/) to get started.

## VSCode developer tools
Refer to [github.com/gadhagod/vscode-chrome-extension-developer-tools/blob/master/README.md#commands](https://github.com/gadhagod/vscode-chrome-extension-developer-tools/blob/master/README.md#commands).