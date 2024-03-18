
// requires a variable intervalTime to exist
// requires the function getRndInteger to exist

let hour = 0;
let minute = 0;
let second = 0;
let count = 0;
let timer;


function updateStopWatch() {
    count += Math.floor(intervalTime / 10);

    if (count >= 100) {
        second++;
        count -= 100;
    }

    if (second == 60) {
        minute++;
        second = 0;
    }
    updateDisplay();
}

function updateDisplay() {
    document.getElementById('min').textContent =minute.toString().padStart(2, '0');
    document.getElementById('sec').textContent =second.toString().padStart(2, '0');
    document.getElementById('count').textContent = Math.min(count + getRndInteger(0, 9), 99).toString().padStart(2, '0');
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
    count = 0;

    updateDisplay();
    document.getElementById('count').textContent = "00";
}