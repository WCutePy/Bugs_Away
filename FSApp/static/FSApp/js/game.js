
let gameId;
let updateInterval;
let serverStartTime;
let clientStartTime;
let serverTimeOffset;

let intervalTime = 25;

let a = 0;

let audioAllowed = true;

const bgMusic = [
    new Audio("../../../static/FSApp/audio/bg-1.mp3"),
    new Audio("../../../static/FSApp/audio/bg-2.mp3"),
    new Audio("../../../static/FSApp/audio/bg-3.mp3"),
]

for(let i = 0; i < bgMusic.length; i++){
    bgMusic[i].loop = true;
    bgMusic[i].volume = 0.2;
}


function getRndInteger(min, max) {
    return Math.floor(Math.random() * (max - min) ) + min;
}


function timeSinceStart(){
    return new Date() - clientStartTime;
}


function clickedStartGame(event){
    document.getElementById('start-game-buttons').classList.add("hidden");
    document.getElementById('timer-wrapper').classList.remove("invisible");
    document.getElementById("difficulty").textContent = this.textContent;    
    document.getElementById("difficulty").classList.remove("hidden");
    document.getElementById("end-of-game").classList.add("hidden");

    document.getElementById('frame').querySelectorAll('img').forEach(function(imgElement) {
        imgElement.parentNode.removeChild(imgElement);
    });
    document.getElementById("frame").onclick = clickedFrame;

    clearTimer();
    let bg = bgMusic[parseInt(this.getAttribute("data-value"))]
    bg.currentTime = 0;
    bg.play();

    $.ajax({
        url: `start_game?difficultyLevel=${this.getAttribute("data-value")}`,
        method: "GET",
        dataType: "json",
        success: function (data) {
            serverStartTime = new Date(data["startTime"]);

            clientStartTime = new Date();

            gameId = data["gameId"];
            requestGameState();
            updateInterval = setInterval(requestGameState, intervalTime);
            // requestAnimationFrame(requestGameState);
        },
        error: function (error) {
            console.error("Error in AJAX request start game:", error);
        }
    })
}


function requestGameState() {
    // a++
    // const index = a;
    // on success calls updateGameState
    // console.log(`Requesting ${index}`);
    $.ajax({
        url: `get_game_state?gameId=${gameId}`,
        method: "GET",
        dataType: "json",
        success: function(data) {
            // console.log(`Starting update ${index}`);
            updateGameState(data);
            // console.log(`Finished update ${index}`);
            // requestAnimationFrame(requestGameState);
        },
        error: function (error) {
            // console.log(`Errored on update ${index}`);
            console.error("Error in AJAX request update game state:", error);
        }
    })
    updateStopWatch();
}


function updateGameState(data) {
    const container = document.getElementById("frame");

    const targets = data["targets"];

    const existingTargets = Array.from(container.getElementsByClassName("game-target")); // change into get children if slow
    let removals = 0;

    existingTargets.forEach(existingTarget => {
        const targetId = existingTarget.id;
        const matchingData = targets.find(
            dataTarget => "target" + dataTarget[2] == targetId);

        if (!matchingData) {
            existingTarget.remove();
            removals += 1;
        } else {
            existingTarget.style.left = "" + matchingData[0] + "%";
            existingTarget.style.top = "" + matchingData[1] + "%";
        }
    });

    targets.forEach(newTargetData => {
        const existingTarget = existingTargets.find(
            target => target.id == "target" + newTargetData[2]);

        if (!existingTarget) {
            const newTarget = createTarget("target" + newTargetData[2], newTargetData[0], newTargetData[1], newTargetData[4]);
            container.appendChild(newTarget);
        } 
    });

    if (document.getElementById("hp-display").innerHTML != data["hp"]){
        document.getElementById("hp-display").innerHTML = data["hp"];
        removals -= parseInt(data["hp"]);
        if (audioAllowed){
            new Audio("../../../static/FSApp/audio/damage-1.mp3").play();
        }
    }
    document.getElementById("kill-display").innerHTML = data["kills"];

    if ((removals > 0) && audioAllowed === true){
        if (removals === 1){
            new Audio("../../../static/FSApp/audio/hit-1.mp3").play();
        } else if (removals === 2){
            new Audio("../../../static/FSApp/audio/hit-2.mp3").play();
        } else {
            new Audio("../../../static/FSApp/audio/hit-3.mp3").play();
        }
    }
    if (parseInt(data["hp"]) <= 0){
        clearInterval(updateInterval);
        // endOfGame()
        setTimeout(endOfGame, 100);
    }
}


function endOfGame(){
    document.getElementById("frame").removeAttribute("onclick");

    $.ajax({
        url: `get_end_of_game?gameId=${gameId}`,
        method: "GET",
        dataType: "json",
        success: function(data) {
            for (let i = 0; i < bgMusic.length; i++) {
                bgMusic[i].pause();
            }

            document.getElementById("end-of-game").classList.remove("hidden");
            document.getElementById("start-game-buttons").classList.remove("hidden");
            let audio_string;
            if (data["current"]){
                audio_string = "../../../static/FSApp/audio/new_record.mp3"
                document.getElementById("end-record-time").innerText = "Good job setting a new record!";
            } else {
                audio_string = "../../../static/FSApp/audio/game_over.mp3";
                document.getElementById("end-record-time").innerText = `Your record is: ${data["record"]}`;
            }

            if (audioAllowed){
                new Audio(audio_string).play();
            }
        },
        error: function (error) {
            console.error("Error in AJAX request update game state:", error);
        }
    })
}


function clickedFrame(event) {
    let elapsed_time = timeSinceStart();

    let container = event.currentTarget;

    let rect = container.getBoundingClientRect();

    let x = ((event.clientX - rect.left) / rect.width) * 100;
    let y = ((event.clientY - rect.top) / rect.height) * 100;

    // console.log(`Offset X/Y: ${x}, ${y}`);
    
    let response = {
        "gameId": gameId,
        "x": x,
        "y": y,
        "elapsedTime": elapsed_time
    };


    $.ajax({
        url: "receive_click",
        method: "POST",
        dataType: "json",
        data: response,
    })
}


function createTarget(targetId, x, y, typeId) {
    let target = document.createElement("img");
    target.classList.add("game-target");

    target.style.left = "" + x + "%";
    target.style.top = "" + y + "%";

    const versions = ["l", "r"];
    // const ants = ["1-l"];
    let index = getRndInteger(0, versions.length);

    target.src = `../../../static/FSApp/img/ant${typeId+1}-${versions[index]}.png`;

    // target.style.width = "" + 10 + "%";
    // target.style.height = "" + 10 + "%";

    target.style.transform = "translate(-50%, -50%)";

    target.id = targetId;
    return target;
}


function toggleBgSound(){
    let checkbox = document.getElementById("bg-audio-box");

    for(let i = 0; i < bgMusic.length; i++){
        bgMusic[i].muted = !checkbox.checked;
    }
}

function toggleAudio() {
    audioAllowed = !audioAllowed;

    document.getElementById("bg-audio-box").checked = audioAllowed;

    toggleBgSound();


}


document.getElementById('start-game-buttons').querySelectorAll("button").forEach(function(button) {
    button.onclick = clickedStartGame;
});

document.getElementById("bg-audio-box").onclick = toggleBgSound;
document.getElementById("audio-box").onclick = toggleAudio;