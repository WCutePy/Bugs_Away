

def apply_default_layout(fig):
    default_layout = dict(
        uirevision='True',
        margin=dict(l=20, r=20, t=30, b=20),

        title=dict(
            font_color="white",
            x=0.5,
            xanchor="center",
        ),

        xaxis_fixedrange=True,
        yaxis_fixedrange=True,

        font=dict(
            color="white",
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        modebar=dict(
            bgcolor='rgba(0,0,0,0)',
        ),

        dragmode=False,
        clickmode="none",
    )
    fig.update_layout(**default_layout)
    fig.update_traces(
        marker=dict(
            color="rgb(59, 130, 246)",
        )
    )