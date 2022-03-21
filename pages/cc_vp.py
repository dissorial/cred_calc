import streamlit as st
from pages.base import Base
from biotron_upgrade import Biotron
from electrox_upgrade import Electrox
from polyzer_upgrade import Polyzer
from neuronic_upgrade import Neuronic
from utils import days_to_whitelist, days_to_next, get_barh_chart
import pandas as pd


def app():
    a, b, c, d, e, f = st.columns(6)

# ~ WHITELIST PRICE
    with st.sidebar:
        wl_price = st.number_input(
            'Whitelist price', min_value=1, max_value=30000, value=10500, step=500, key='wl_price')

# ~ UPGRADE PRICES
    with st.sidebar:
        with st.expander('Upgrade prices', expanded=False):
            bio_cost = st.number_input(
                'Biotron', 500, 1500, 900, 50, key='bio_cost')
            ele_cost = st.number_input(
                'Electrox', 500, 2500, 1500, 50, key='ele_cost')
            poly_cost = st.number_input(
                'Polyzer', 1500, 4500, 3000, 100, key='poly_cost')
            neuro_cost = st.number_input(
                'Neuronic', 3000, 6000, 4500, 100, key='neuro_cost')

        activity_container = st.sidebar.container()

# ! NO UPGRADE
    with a:
        no_upgrade = Base(activity_container)
        def_wl = days_to_whitelist(wl_price, no_upgrade.daily_cc)
        canBuy_biotron = st.container()

# ! BIOTRON
    with b:
        biotron = Biotron(bio_cost, activity_container)
        bio_wl = days_to_whitelist(wl_price, biotron.daily_cc)
        base_to_bio = days_to_next(
            biotron.cost, no_upgrade.activity, no_upgrade.one_cycle_cc)
        canBuy_biotron.write(
            '`Can buy biotron in {} day(s)`'.format(base_to_bio))

        canBuy_electrox = st.container()

# ! ELECTROX
    with c:
        electrox = Electrox(ele_cost, activity_container)
        ele_wl = days_to_whitelist(wl_price, electrox.daily_cc)
        bio_to_ele = days_to_next(
            electrox.cost, biotron.activity, biotron.one_cycle_cc)

        canBuy_electrox.write(
            '`Can buy electrox in {} day(s)`'.format(bio_to_ele))
        canBuy_polzer = st.container()

# ! POLYZER
    with d:
        polyzer = Polyzer(poly_cost, activity_container)
        poly_wl = days_to_whitelist(wl_price, polyzer.daily_cc)

        ele_to_poly = days_to_next(
            polyzer.cost, electrox.activity, electrox.one_cycle_cc)

        canBuy_polzer.write(
            '`Can buy polyzer in {} day(s)`'.format(ele_to_poly))
        canBuy_neuronic = st.container()

# ! NEURONIC
    with e:
        neuronic = Neuronic(neuro_cost, activity_container)
        neuro_wl = days_to_whitelist(wl_price, neuronic.daily_cc)

        poly_to_neuro = days_to_next(
            neuronic.cost, polyzer.activity, polyzer.one_cycle_cc)

        canBuy_neuronic.write(
            '`Can buy neuronic in {} day(s)`'.format(poly_to_neuro))

        st.write('`Days to WL w/ all upgrades: {}`'.format(
            base_to_bio+bio_to_ele+ele_to_poly+poly_to_neuro+neuro_wl))

# & CHART DATAFRAME
    all_data = {
        'Upgrades': ['Base', 'Biotron', 'Electrox', 'Polyzer', 'Neuronic'],
        'CC cycle': [no_upgrade.one_cycle_cc, biotron.one_cycle_cc, electrox.one_cycle_cc, polyzer.one_cycle_cc, neuronic.one_cycle_cc],
        'CC daily': [no_upgrade.daily_cc, biotron.daily_cc, electrox.daily_cc, polyzer.daily_cc, neuronic.daily_cc],
        'Days to whitelist': [def_wl, bio_wl, ele_wl, poly_wl, neuro_wl],
        'CC over time': [no_upgrade.cc_over_time, biotron.cc_over_time, electrox.cc_over_time, polyzer.cc_over_time, neuronic.cc_over_time],
        'VP cycle': [no_upgrade.one_cycle_vp, biotron.one_cycle_vp, electrox.one_cycle_vp, polyzer.one_cycle_vp, neuronic.one_cycle_vp],
        'VP daily': [no_upgrade.daily_vp, biotron.daily_vp, electrox.daily_vp, polyzer.daily_vp, neuronic.daily_vp],
        'VP over time': [no_upgrade.vp_over_time, biotron.vp_over_time, electrox.vp_over_time, polyzer.vp_over_time, neuronic.vp_over_time]
    }

    all_df = pd.DataFrame(all_data)

# & VICTORY POINTS ONE CYCLE CHART
    ch_cycleVP = get_barh_chart(
        all_df, 'VP cycle', 'Upgrades', 350, 350, 'ONE CYCLE')

# & VICTORY POINTS DAILY CHART
    ch_dailyVP = get_barh_chart(
        all_df, 'VP daily', 'Upgrades', 350, 350, 'DAILY GAIN')

# & VICTORY POINTS OVER TIME CHART
    ch_overTimeVP = get_barh_chart(
        all_df, 'VP over time', 'Upgrades', 350, 350, 'GAIN OVER TIME')

# & CYBER CREDITS ONE CYCLE CHART
    ch_cycleCC = get_barh_chart(
        all_df, 'CC cycle', 'Upgrades', 350, 350, 'ONE CYCLE')

# & CYBER CREDITS DAILY CHART
    ch_dailyCC = get_barh_chart(
        all_df, 'CC daily', 'Upgrades', 350, 350, 'DAILY GAIN')

# & CYBER CREDITS OVER TIME CHART
    ch_overTimeCC = get_barh_chart(
        all_df, 'CC over time', 'Upgrades', 350, 350, 'GAIN OVER TIME')

# & TIME TO WHITELIST CHART
    ch_wl = get_barh_chart(all_df, 'Days to whitelist',
                           'Upgrades', 250, 300, 'DAYS TO WHITELIST')

# & DISPLAYING CHARTTS

# * CYBER CREDIT CHARTS
    with st.expander('CYBER CREDIT CHARTS'):
        one, two, three = st.columns(3)

# ? CYBER CREDITS: ONE CYCLE GAIN
        with one:
            st.altair_chart(ch_cycleCC)
            st.markdown(
                '`DEFAULT —— ASSUMING {}% CC MULTIPLIER`'.format(no_upgrade.cc_mp))
            st.markdown(
                '`BIOTRON —— ASSUMING {}% CC MULTIPLIER`'.format(biotron.cc_mp))
            st.markdown(
                '`ELECTROX —— ASSUMING {}% CC MULTIPLIER`'.format(electrox.cc_mp))
            st.markdown(
                '`POLYZER —— ASSUMING {}% CC MULTIPLIER`'.format(polyzer.cc_mp))
            st.markdown(
                '`NEURONIC —— ASSUMING {}% CC MULTIPLIER`'.format(neuronic.cc_mp))

# ? CYBER CREDITS: DAILY GAIN
        with two:
            st.altair_chart(ch_dailyCC)
            st.markdown(
                '`DEFAULT —— ASSUMING {} CYCLES COMPLETED`'.format(no_upgrade.activity))
            st.markdown(
                '`BIOTRON —— ASSUMING {} CYCLES COMPLETED`'.format(biotron.activity))
            st.markdown(
                '`ELECTROX —— ASSUMING {} CYCLES COMPLETED`'.format(electrox.activity))
            st.markdown(
                '`POLYZER —— ASSUMING {} CYCLES COMPLETED`'.format(polyzer.activity))
            st.markdown(
                '`NEURONIC —— ASSUMING {} CYCLES COMPLETED`'.format(neuronic.activity))

# ? CYBER CREDITS: GAIN OVER TIME
        with three:
            st.altair_chart(ch_overTimeCC)
            st.markdown(
                '`DEFAULT —— ASSUMING {} CYCLES OVER {} DAY(S)`'.format(no_upgrade.activity, no_upgrade.activity_days))
            st.markdown(
                '`BIOTRON —— ASSUMING {} CYCLES OVER {} DAY(S)`'.format(biotron.activity, biotron.activity_days))
            st.markdown(
                '`ELECTROX —— ASSUMING {} CYCLES OVER {} DAY(S)`'.format(electrox.activity, electrox.activity_days))
            st.markdown(
                '`POLYZER —— ASSUMING {} CYCLES OVER {} DAY(S)`'.format(polyzer.activity, polyzer.activity_days))
            st.markdown(
                '`NEURONIC —— ASSUMING {} CYCLES OVER {} DAY(S)`'.format(neuronic.activity, neuronic.activity_days))

# * VICTORY POINT CHARTS
    with st.expander('VICTORY POINT CHARTS'):
        raz, dva, tri = st.columns(3)

# ? VICTORY POINTS: ONE CYCLE GAIN
        with raz:
            st.altair_chart(ch_cycleVP)
            st.markdown(
                '`DEFAULT —— ASSUMING {}% VP MULTIPLIER`'.format(no_upgrade.vp_mp))
            st.markdown(
                '`BIOTRON —— ASSUMING {}% VP MULTIPLIER`'.format(biotron.vp_mp))
            st.markdown(
                '`ELECTROX —— ASSUMING {}% VP MULTIPLIER`'.format(electrox.vp_mp))
            st.markdown(
                '`POLYZER —— ASSUMING {}% VP MULTIPLIER`'.format(polyzer.vp_mp))
            st.markdown(
                '`NEURONIC —— ASSUMING {}% VP MULTIPLIER`'.format(neuronic.vp_mp))

# ? VICTORY POINTS: DAILY GAIN
        with dva:
            st.altair_chart(ch_dailyVP)
            st.markdown(
                '`DEFAULT —— ASSUMING {} CYCLES COMPLETED`'.format(no_upgrade.activity))
            st.markdown(
                '`BIOTRON —— ASSUMING {} CYCLES COMPLETED`'.format(biotron.activity))
            st.markdown(
                '`ELECTROX —— ASSUMING {} CYCLES COMPLETED`'.format(electrox.activity))
            st.markdown(
                '`POLYZER —— ASSUMING {} CYCLES COMPLETED`'.format(polyzer.activity))
            st.markdown(
                '`NEURONIC —— ASSUMING {} CYCLES COMPLETED`'.format(neuronic.activity))

# ? VICTORY POINTS: GAIN OVER TIME
        with tri:
            st.altair_chart(ch_overTimeVP)
            st.markdown(
                '`DEFAULT —— ASSUMING {} CYCLES OVER {} DAY(S)`'.format(no_upgrade.activity, no_upgrade.activity_days))
            st.markdown(
                '`Biotron —— ASSUMING {} CYCLES OVER {} DAY(S)`'.format(biotron.activity, biotron.activity_days))
            st.markdown(
                '`ELECTROX —— ASSUMING {} CYCLES OVER {} DAY(S)`'.format(electrox.activity, electrox.activity_days))
            st.markdown(
                '`POLYZER —— ASSUMING {} CYCLES OVER {} DAY(S)`'.format(polyzer.activity, polyzer.activity_days))
            st.markdown(
                '`NEURONIC —— ASSUMING {} CYCLES OVER {} DAY(S)`'.format(neuronic.activity, neuronic.activity_days))

# ^ WHITELIST CHART
    with f:
        st.altair_chart(ch_wl)
