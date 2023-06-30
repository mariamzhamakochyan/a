function openTerminal() {
    var terminalWindow = document.getElementById('terminal-window');
    terminalWindow.style.display = 'block';
}

function closeTerminal() {
    var terminalWindow = document.getElementById('terminal-window');
    terminalWindow.style.display = 'none';
}

// Existing JavaScript code

function executeCommand() {
    const commandInput = document.getElementById('terminal-command');
    const command = commandInput.value.trim();
    commandInput.value = '';

    if (command !== '') {
        const outputDiv = document.getElementById('terminal-output');
        outputDiv.innerHTML += `<p class="command-prompt">studentname@Picsart-Academy ~ $ ${command}</p>`;

        fetch('/execute', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `command=${encodeURIComponent(command)}`,
        })
        .then(response => response.json())
        .then(data => {
            outputDiv.innerHTML += `<p class="command-output">${data.output}</p>`;
            outputDiv.scrollTop = outputDiv.scrollHeight;
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }
}

function handleKeyPress(event) {
    if (event.key === 'Enter') {
        executeCommand();
    }
}

function sendCommand(command) {
    fetch('/execute', {
      method: 'POST',
      body: new URLSearchParams({
        command: command
      })
    })
      .then(response => response.json())
      .then(data => {
        const terminalOutput = document.getElementById('terminal-output');
        terminalOutput.innerHTML += `<div>${data.output}</div>`;
      });
  }
  



var terminalWindow = document.getElementById('terminal-window');
var terminalHeader = document.querySelector('.terminal-header');

// Variables to store the initial position of the mouse and the terminal window
var initialMouseX = 0;
var initialMouseY = 0;
var initialTerminalX = 0;
var initialTerminalY = 0;

// Function to handle the start of dragging
function startDragging(e) {
    initialMouseX = e.clientX;
    initialMouseY = e.clientY;
    initialTerminalX = terminalWindow.offsetLeft;
    initialTerminalY = terminalWindow.offsetTop;

    // Add event listeners for dragging
    document.addEventListener('mousemove', dragTerminal);
    document.addEventListener('mouseup', stopDragging);
}

// Function to handle dragging
function dragTerminal(e) {
    var deltaX = e.clientX - initialMouseX;
    var deltaY = e.clientY - initialMouseY;
    var newTerminalX = initialTerminalX + deltaX;
    var newTerminalY = initialTerminalY + deltaY;

    // Update the position of the terminal window
    terminalWindow.style.left = newTerminalX + 'px';
    terminalWindow.style.top = newTerminalY + 'px';
}

// Function to handle the end of dragging
function stopDragging() {
    // Remove event listeners for dragging
    document.removeEventListener('mousemove', dragTerminal);
    document.removeEventListener('mouseup', stopDragging);
}

// Add event listener to the terminal header for initiating dragging
terminalHeader.addEventListener('mousedown', startDragging);

// Function to toggle full-screen mode
function toggleFullscreen() {
    var terminalWindow = document.getElementById('terminal-window');

    if (!document.fullscreenElement && !document.mozFullScreenElement && !document.webkitFullscreenElement && !document.msFullscreenElement) {
        if (document.documentElement.requestFullscreen) {
            terminalWindow.requestFullscreen();
        } else if (document.documentElement.mozRequestFullScreen) {
            terminalWindow.mozRequestFullScreen();
        } else if (document.documentElement.webkitRequestFullscreen) {
            terminalWindow.webkitRequestFullscreen(Element.ALLOW_KEYBOARD_INPUT);
        } else if (document.documentElement.msRequestFullscreen) {
            terminalWindow.msRequestFullscreen();
        }
    } else {
        if (document.exitFullscreen) {
            document.exitFullscreen();
        } else if (document.mozCancelFullScreen) {
            document.mozCancelFullScreen();
        } else if (document.webkitExitFullscreen) {
            document.webkitExitFullscreen();
        } else if (document.msExitFullscreen) {
            document.msExitFullscreen();
        }
    }
}
// ... your existing code ...

function openFolder(folderName) {
    var folderWindow = document.getElementById('folder-window');
    folderWindow.style.display = 'block';

    var folderTitle = document.querySelector('.folder-title');
    folderTitle.textContent = folderName;

    // Call a function to fetch and display the content of the folder
    fetchFolderContent(folderName);
}

function closeFolder() {
    var folderWindow = document.getElementById('folder-window');
    folderWindow.style.display = 'none';
}



function getFolderContent(folderName) {
    // Simulate fetching folder content from a fake database based on the folder name
    if (folderName === 'home') {
        return [
            { name: 'file1.txt', type: 'file' },
            { name: 'file2.txt', type: 'file' },
            { name: 'folder1', type: 'folder' }
        ];
    } else if (folderName === 'folder1') {
        return [
            { name: 'file3.txt', type: 'file' },
            { name: 'file4.txt', type: 'file' },
            { name: 'folder2', type: 'folder' }
        ];
    }
    return [];
}