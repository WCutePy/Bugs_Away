let current = null;
let awaiting = null;


function clickedGameButton(gameId) {
        awaiting = gameId;
        if (current === gameId){
            return
        }

        // Make an AJAX request to get the dot plot
        $.ajax({
            url: `personal_game_data/?game_id=${gameId}`,
            type: 'GET',
            dataType: 'json',
            success: function(response) {
                if (gameId !== awaiting){
                    return
                }

                current = gameId;

                const plots = response.plots;
                for (let i = 0; i < plots.length; i++) {
                    $(`#plot-${i + 1}`).html(plots[i]);
                }




            },
            error: function(error) {
                console.error('Error fetching dot plot:', error);
            }
        });
    }

