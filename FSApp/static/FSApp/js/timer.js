
// requires a variable intervalTime to exist
// requires the function getRndInteger to exist

let hour = 0;
let minute = 0;
let second = 0;
let ms = 0;
let timer;


function updateStopWatch() {
    let currentDate = new Date();

    let elapsedTime = currentDate - clientStartTime;
    ms = elapsedTime % 1000;
    let totalSeconds = Math.floor(elapsedTime / 1000);
    second = totalSeconds % 60;
    minute = Math.floor(totalSeconds / 60);

    updateDisplay();
}

function updateDisplay() {
    document.getElementById('min').textContent =minute.toString().padStart(2, '0');
    document.getElementById('sec').textContent =second.toString().padStart(2, '0');
    document.getElementById('count').textContent = ms.toString().slice(0, 2).padStart(2, "0");
}


function startTimer() {
    // Check if the timer is already running
    if (!timer) {
        timer = setInterval(updateStopWatch, intervalTime);
    }
}

function stopTimer() {
    clearInterval(timer);
    timer = null; // Reset timer variable
}

function clearTimer() {
    clearInterval(timer);
    timer = null; // Reset timer variable
    hour = 0;
    minute = 0;
    second = 0;
    ms = 0;

    updateDisplay();
    document.getElementById('count').textContent = "00";
}