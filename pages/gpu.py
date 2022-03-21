import streamlit as st


def app():
    st.title("My App")
    st.markdown('## GPU')
    a, b = st.columns([1, 3])
    base = 50
    if 'activity' not in st.session_state:
        st.session_state.activity = 250

    def activity_log():
        st.session_state.activity += 0
    with b:
        with st.expander('Settings', expanded=True):
            level_input = st.number_input(
                label='Level to attain', min_value=1, max_value=100, step=1, value=27)

            daily_limit = st.number_input(
                'Daily limit', min_value=100, max_value=3000, value=1000, step=50)

            increment = st.number_input(
                'Increment for each level', min_value=1, max_value=100, value=2, step=1)

            user_activity = st.slider('Daily user activity',
                                      min_value=0, max_value=int(daily_limit), key='activity', step=50, on_change=activity_log())
            st.write(st.session_state.activity)
    ms_needed = 0
    for i in range(level_input):
        base += increment
        ms_needed += base
    try:
        days_to_level = round(ms_needed/user_activity, ndigits=2)
    except ZeroDivisionError:
        st.error('Daily user activity must be greater than 0')
        st.stop()
    words_needed = ms_needed//8
    words_per_day = round(words_needed/days_to_level, ndigits=0)
    with a:
        with st.expander('Outcome', expanded=True):
            st.info('{} MS needed = {} words'.format(
                ms_needed, words_needed))
            st.info('{} days to attain level {}'.format(
                days_to_level, level_input))
            st.info('Requires ~{} words a day'.format(int(words_per_day)))

# if __name__ == '__main__':
#     app()
