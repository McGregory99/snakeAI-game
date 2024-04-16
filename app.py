import streamlit as st

from agent import train, Agent, SnakeGameAI

st.set_page_config(page_title='SNAKE AI GAME',
        page_icon=":snake", 
        layout='centered', 
        initial_sidebar_state='expanded')
    
def set_display():
    sidebar = st.sidebar
    btn_compute = sidebar.button("COMPUTE", on_click=main)
    
    # TODO: CUADRADO EN EL MEDIOO PARA MOSTRAR LA ST.PYPLOT. WWITH ST.EMTY()?
    # TODO: PUNTUACI'ON ARRIBA
    # TODO: TIEMPO ARRIBA
    # TODO: BOTON DE STOP
    
def main():
    set_display()
    
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record_score = 0
    agent = Agent()
    game = SnakeGameAI()
    while True:
        # get the current state
        state_old = agent.get_state(game)

        # get move based on the current state
        final_move = agent.get_action(state_old)

        # hacer el movimiento y obtener nuevo estado
        reward, game_over, score, fig = game.play_step(final_move)
        st.pyplot(fig)
        # TODO: REFRESH THE FIGURE
        state_new = agent.get_state(game)

        # train short memory
        agent.train_short_memory(state_old, final_move, reward, state_new, game_over)

        # remember
        agent.remember(state_old, final_move, reward, state_new, game_over)

        if game_over:
            # train long memory and plot result
            game.reset()
            agent.num_games += 1
            agent.train_long_memory()

            if score > record_score:
                record_score = score
                agent.model.save()
            
            print(f"\n\nGame {agent.num_games} \nScore {score} \nRecord {record_score}")
            
            #plot_scores.append(score)
            #total_score += score
            #mean_score = total_score/agent.num_games
            #plot_mean_scores.append(mean_score)
            #if agent.num_games%50==0:
            #    print("IMAGE SAVED")
            #    plot(plot_scores, plot_mean_scores, agent.num_games)

if __name__ == '__main__':
    set_display()
