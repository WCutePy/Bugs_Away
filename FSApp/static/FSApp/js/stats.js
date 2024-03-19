let current = null;
let awaiting = null;

const waitingElement = document.getElementById("waiting");
const replayRequestText = document.getElementById("replay-request-text");
const dotplotMenu = document.getElementById("dotplot-menu")




function clickedGameButton(gameId) {
        awaiting = gameId;
        if (current === gameId){
            return
        }

        for (let i = 0; i < 10; i++) {
            $(`#plot-${i + 1}`).html("");
        }
        $(`#replay`).html("");

        replayRequestText.classList.replace("visible", "invisible");
        dotplotMenu.classList.replace("visible", "invisible");
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

                const plots = response.plots;
                for (let i = 0; i < plots.length; i++) {
                    $(`#plot-${i + 1}`).html(plots[i]);
                }

                // let titleDate = $(`#plot-1`).find('.gtitle').children().first();
                // console.log(titleDate)
                // let date = new Date(titleDate.textContent).toLocaleDateString();
                // titleDate.innerHTML = "hello";

                replayRequestText.classList.replace("invisible", "visible");
                dotplotMenu.classList.replace("invisible", "visible");

            },
            error: function(error) {
                console.error('Error fetching dot plot:', error);
            }
        });
    }


function getReplay() {
    replayRequestText.classList.replace("visible", "invisible");

    waitingElement.classList.replace("invisible", "visible");

    const gameId = current;

    $.ajax({
        url: `get_replay/?game_id=${gameId}`,
        type: 'GET',
        dataType: 'json',
        success: function(response) {
            if (gameId !== current){
                console.log(`returning! gameId: ${gameId} current: ${current}`);
                return
            }
            console.log(`performing! gameId: ${gameId} current: ${current}`);
            const replay = response.replay;
            $(`#replay`).html(replay);

            waitingElement.classList.replace("visible", "invisible");

            if (gameId !== current){
                $(`#replay`).html("");
            }
        },
        error: function(error) {
            console.error('Error fetching replay:', error);
        }
    });
}


function togglePlot(radioButton) {
    let option = radioButton.value;
    console.log(option);
    if (option === '1') {
        document.getElementById('plot-2').classList.remove('hidden');
        document.getElementById('plot-3').classList.add('hidden');
    } else if (option === '2') {
        document.getElementById('plot-3').classList.remove('hidden');
        document.getElementById('plot-2').classList.add('hidden');
    }
}
