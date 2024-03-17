let current = null;
let awaiting = null;

const waitingElement = document.getElementById("waiting");
const replayRequestText = document.getElementById("replay-request-text");





function clickedGameButton(gameId) {
        awaiting = gameId;
        if (current === gameId){
            return
        }

        for (let i = 0; i < 3; i++) {
            $(`#plot-${i + 1}`).html("");
        }
        replayRequestText.classList.replace("visible", "invisible");

        waitingElement.classList.replace("invisible", "visible");

        $.ajax({
            url: `personal_game_data/?game_id=${gameId}`,
            type: 'GET',
            dataType: 'json',
            success: function(response) {
                if (gameId !== awaiting){
                    return
                }

                waitingElement.classList.replace("visible", "invisible");

                current = gameId;

                $(`#replay`).html("");

                const plots = response.plots;
                for (let i = 0; i < plots.length; i++) {
                    $(`#plot-${i + 1}`).html(plots[i]);
                }

                replayRequestText.classList.replace("invisible", "visible");


            },
            error: function(error) {
                console.error('Error fetching dot plot:', error);
            }
        });
    }


function getReplay(gameId) {
    replayRequestText.classList.replace("visible", "invisible");

    waitingElement.classList.replace("invisible", "visible");

    $.ajax({
        url: `get_replay/?game_id=${current}`,
        type: 'GET',
        dataType: 'json',
        success: function(response) {

            const replay = response.replay;
            $(`#replay`).html(replay);

            waitingElement.classList.replace("visible", "invisible");
        },
        error: function(error) {
            console.error('Error fetching replay:', error);
        }
    });
}