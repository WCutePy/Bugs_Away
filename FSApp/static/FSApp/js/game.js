
let gameId;
let updateInterval;
let serverStartTime;
let clientStartTime;
let serverTimeOffset;

let clicked = null;

let intervalTime = 25;


function getRndInteger(min, max) {
    return Math.floor(Math.random() * (max - min) ) + min;
}


function timeSinceStart(){
    return new Date() - clientStartTime;
}


function clickedStartGame(event){
    this.classList.add("hidden");
    document.getElementById('timer-wrapper').classList.toggle("hidden");

    $.ajax({
        url: "start_game",
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
    // on success calls updateGameState
    $.ajax({
        url: "get_game_state",
        method: "GET",
        dataType: "json",
        success: function(data) {
            updateGameState(data);

            // requestAnimationFrame(requestGameState);
        },
        error: function (error) {
            console.error("Error in AJAX request update game state:", error);
        }
    })
    updateStopWatch();
}


function updateGameState(data) {
    const container = document.getElementById("frame");

    const targets = data["targets"];

    const existingTargets = Array.from(container.getElementsByClassName("game-target")); // change into get children if slow

    existingTargets.forEach(existingTarget => {
        const targetId = existingTarget.id;
        const matchingData = targets.find(
            dataTarget => "target" + dataTarget[2] == targetId);

        if (!matchingData) {
            existingTarget.remove();
        } else {
            existingTarget.style.left = "" + matchingData[0] + "%";
            existingTarget.style.top = "" + matchingData[1] + "%";
        }
    });

    targets.forEach(newTargetData => {
        const existingTarget = existingTargets.find(
            target => target.id == "target" + newTargetData[2]);

        if (!existingTarget) {
            const newTarget = createTarget("target" + newTargetData[2], newTargetData[0], newTargetData[1]);
            container.appendChild(newTarget);
        } 
    });

    document.getElementById("hp-display").innerHTML = data["hp"];
    document.getElementById("kill-display").innerHTML = data["kills"];
    
    if (parseInt(data["hp"]) <= 0){
        endOfGame()
    }
}


function endOfGame(){
    clearInterval(updateInterval);

    $.ajax({
        url: "get_end_of_game",
        method: "GET",
        dataType: "json",
        success: function(data) {
            document.getElementById("end-of-game").classList.remove("hidden");
            document.getElementById("end-record-time").innerText = data["record"];

        },
        error: function (error) {
            console.error("Error in AJAX request update game state:", error);
        }
    })
}


function clickedFrame(event) {
    let clicked_id = null;
    let elapsed_time = timeSinceStart();

    if (clicked != null){
        clicked_id = clicked.id;
        clicked = null;
    }

    let container = event.currentTarget;

    let rect = container.getBoundingClientRect();

    let x = ((event.clientX - rect.left) / rect.width) * 100;
    let y = ((event.clientY - rect.top) / rect.height) * 100;

    // console.log(`Offset X/Y: ${x}, ${y}`);
    
    let response = {
        "gameId": gameId,
        "x": x,
        "y": y,
        "hitTarget": clicked_id,
        "elapsedTime": elapsed_time
    };


    $.ajax({
        url: "receive_click",
        method: "POST",
        dataType: "json",
        data: response,
    })
}

function clickedTarget(event) {
    // console.log("hit target: " +this.id);
    clicked = this;
}


// function createTarget(targetId, x, y) {
//     let target = document.createElement("div");
//     target.classList.add("game-target");
//     target.style.left = "" + x + "%";
//     target.style.top = "" + y + "%";
//     target.style.transform = "translate(-50%, -50%)";
//
//     target.onclick = clickedTarget;
//
//     target.id = targetId;
//     return target;
// }


function createTarget(targetId, x, y) {
    let target = document.createElement("img");
    target.classList.add("game-target");

    target.style.left = "" + x + "%";
    target.style.top = "" + y + "%";

    const ants = ["1-l", "1-r", "2-l", "2-r", "3-l", "3-r"];
    // const ants = ["1-l"];
    let index = getRndInteger(0, ants.length);
    console.log(`spawning ${index}`);
    let ant = ants[index];
    target.src = `../../../static/FSApp/img/ant${ant}.png`;

    // target.style.width = "" + 10 + "%";
    // target.style.height = "" + 10 + "%";

    target.style.transform = "translate(-50%, -50%)";

    target.onclick = clickedTarget;

    target.id = targetId;
    return target;
}


document.getElementById("frame").onclick = clickedFrame;
document.getElementById("start-game").onclick = clickedStartGame;
