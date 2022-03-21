import streamlit as st
import math
import altair as alt


def userInput_number(label, min, max, val, step, key, retInt=False):
    res = st.number_input(label=label, min_value=min,
                          max_value=max, value=val, step=step, key=key)
    if retInt:
        return int(res)
    else:
        return res


def one_cycle_vp(fight_vp, steal_vp, tauntCall_vp, tauntRespond_vp, fst_rate, vp_mp):
    multiplier = 1+(vp_mp/100)
    res = fst_rate*(fight_vp+steal_vp+tauntCall_vp)+tauntRespond_vp
    if vp_mp == 0:
        return res
    else:
        return res*multiplier


def one_cycle_cc(default_cycle_gainCC, multiplier):
    if multiplier == 0:
        return default_cycle_gainCC
    else:
        return default_cycle_gainCC*(1+(multiplier/100))


def daily_gain(gain_per_cycle, cycles_per_day):
    return int(gain_per_cycle*cycles_per_day)


def gain_over_time(gain_per_cycle, num_cycles, num_days):
    return int(gain_per_cycle*num_cycles*num_days)


def days_to_whitelist(whitelist_price, cc_per_day):
    return int(whitelist_price/cc_per_day)


def days_to_next(cost, activity, cycle_gain):
    return math.ceil(cost/(activity*cycle_gain))


def get_barh_chart(data, y_axis, x_axis, w, h, t):
    chart_data = alt.Chart(data).mark_bar().encode(
        y=alt.Y(y_axis, axis=None),
        x=alt.X(x_axis, sort='y', axis=alt.Axis(
            labelAngle=0, ticks=False, title='')),
        color=alt.Color(x_axis, legend=None)
    ).properties(width=w, height=h, title=t)

    chart_labels = chart_data.mark_text(
        align='center', baseline='middle', dx=0, dy=-7, color="#FFFFFF").encode(text=y_axis)
    chart = (chart_data+chart_labels).configure_view(
        strokeOpacity=0
    ).configure_axisBottom(domainOpacity=0)

    return chart
