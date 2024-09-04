// ==UserScript==
// @name         Right-Click Image EXIF Viewer
// @namespace    http://tampermonkey.net/
// @version      1.1
// @description  Show EXIF data of any image on right-click in a modal window with copy functionality.
// @author       Yetkin Degirmenci Twitter : yetkinmiller
// @match        *://*/*
// @require      https://cdnjs.cloudflare.com/ajax/libs/exif-js/2.3.0/exif.js
// @grant        none
// ==/UserScript==

(function() {
    'use strict';

    // summon modal window
    function createModal(content) {
        const modal = document.createElement('div');
        modal.style.position = 'fixed';
        modal.style.top = '50%';
        modal.style.left = '50%';
        modal.style.transform = 'translate(-50%, -50%)';
        modal.style.backgroundColor = 'rgba(0, 0, 0, 0.9)';
        modal.style.padding = '20px';
        modal.style.borderRadius = '10px';
        modal.style.color = 'white';
        modal.style.zIndex = '10000';
        modal.style.maxHeight = '80vh';
        modal.style.maxWidth = '80vw';
        modal.style.overflowY = 'auto';
        modal.style.fontFamily = 'monospace';

        const closeButton = document.createElement('button');
        closeButton.textContent = 'Close';
        closeButton.style.marginBottom = '10px';
        closeButton.style.padding = '5px 10px';
        closeButton.style.cursor = 'pointer';
        closeButton.addEventListener('click', function() {
            document.body.removeChild(modal);
        });

        const copyButton = document.createElement('button');
        copyButton.textContent = 'Copy EXIF Data';
        copyButton.style.marginBottom = '10px';
        copyButton.style.marginLeft = '10px';
        copyButton.style.padding = '5px 10px';
        copyButton.style.cursor = 'pointer';
        copyButton.addEventListener('click', function() {
            navigator.clipboard.writeText(content).then(() => {
                alert('EXIF data copied to clipboard!');
            });
        });

        const pre = document.createElement('pre');
        pre.textContent = content;

        modal.appendChild(closeButton);
        modal.appendChild(copyButton);
        modal.appendChild(pre);
        document.body.appendChild(modal);
    }

    // get the data
    function showExifData(img) {
        EXIF.getData(img, function() {
            const allMetaData = EXIF.getAllTags(this);
            const exifString = JSON.stringify(allMetaData, null, 2);

            // If no EXIF data found, display a message
            if (exifString === '{}') {
                createModal('No EXIF data found for this image.');
            } else {
                createModal(exifString);
            }
        });
    }

    // event listener
    document.addEventListener('contextmenu', function(e) {
        if (e.target.tagName === 'IMG') {
            e.preventDefault(); // protect right click at all cost
            showExifData(e.target);
        }
    });

})();
