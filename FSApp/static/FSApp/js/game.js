
let gameId;
let gameUpdater;

let clicked = null;
let targetn = 0;


function getRndInteger(min, max) {
    return Math.floor(Math.random() * (max - min) ) + min;
}


function clickedStartGame(event){
    this.classList.add("invisible");

    $.ajax({
        url: "start_game",
        method: "GET",
        dataType: "json",
        success: function (data) {
            gameId = data["gameId"];
            requestGameState();
            gameUpdater = setInterval(requestGameState, 100);
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
        data: {"gameId": gameId},
        success: function(data) {
            updateGameState(data);

            // requestAnimationFrame(requestGameState);
        },
        error: function (error) {
            console.error("Error in AJAX request update game state:", error);
        }
    })
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
            console.log("removing!");
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
}


function clickedFrame(event) {
    console.log( `Offset X/Y: ${event.offsetX}, ${event.offsetY}`);
    let response = {
        "gameId": gameId,
        "x": event.offsetX,
        "y": event.offsetY,
        "hitTarget": null
    };
    if (clicked != null){
        response["hitTarget"] = clicked.id;
        clicked = null;
    }

    $.ajax({
        url: "process_click",
        method: "GET",
        dataType: "json",
        data: response,
        // success: function (data) {
        
        // },
        error: function (error) {
            console.error("Error in AJAX clicked frame:", error);
        }
    })
}

function clickedTarget(event) {
    console.log("hit target: " +this.id);
    clicked = this;
}


function createTarget(targetId, x, y) {
    let target = document.createElement("div");
    target.classList.add("game-target");
    target.style.left = "" + x + "%";
    target.style.top = "" + y + "%";

    target.onclick = clickedTarget;

    target.id = targetId;
    return target;
}

// function createTarget(targetId, x, y) {
//     let target = document.createElement("img");
//     target.classList.add("game-target");

//     target.style.left = "" + x + "%";
//     target.style.top = "" + y + "%";
//     target.src = "../../../static/FSApp/img/donut.jpg";

//     target.style.width = "" + 10 + "%";
//     target.style.height = "" + 10 + "%";

//     target.onclick = clickedTarget;

//     target.id = targetId;
//     return target;
// }

document.getElementById("frame").onclick = clickedFrame;
document.getElementById("start-game").onclick = clickedStartGame;
