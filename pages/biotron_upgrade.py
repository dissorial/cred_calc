import streamlit as st
import math
from utils import userInput_number, one_cycle_vp, daily_gain, gain_over_time, one_cycle_cc


class Biotron:
    def __init__(self, cost, container):
        st.info('`BIOTRON`')
        self.fst_cap = userInput_number(
            'Command cap/day', 1, 10, 6, 1, 'bio_fst_cap', retInt=True)

        self.cost = cost
        self.container = container
        with container.expander('Biotron activity', expanded=False):
            self.activity = userInput_number('Cycles per day', 0, math.floor(
                self.fst_cap), math.floor(self.fst_cap), 1, 'bio_activity', retInt=True)

            self.activity_days = userInput_number(
                'Number of days', 1, 50, 2, 1, 'bio_activity_days', retInt=True)

# ! VP--------------------------------------------------------
        with st.expander('SETTINGS: VP GAINS', expanded=False):
            self.fst_rate = (userInput_number(
                '!fight/!steal/!taunt success rate', 25.0, 100.0, 50.0, 2.5, 'bio_success_rate')/100)

            self.fight_vp = (userInput_number(
                '!fight VP', 1, 300, 100, 5, 'bio_fightVP'))

            self.steal_vp = userInput_number(
                '!steal VP', 1, 300, 100, 5, 'bio_stealVP')

            self.tauntCall_vp = userInput_number(
                '!taunt #arena VP', 0, 300, 0, 5, 'bio_tcVP')

            self.tauntRespond_vp = userInput_number(
                '#taunt response VP', 1, 300, 100, 5, 'bio_trVP')

            self.vp_mp = userInput_number(
                'VP multiplier (%)', 0, 300, 0, 5, 'bio_vp_mp', retInt=True)

            self.one_cycle_vp = one_cycle_vp(
                self.fight_vp, self.steal_vp, self.tauntCall_vp, self.tauntRespond_vp, self.fst_rate, self.vp_mp)

            self.daily_vp = daily_gain(self.one_cycle_vp, self.activity)

            self.vp_over_time = gain_over_time(
                self.one_cycle_vp, self.activity, self.activity_days)
# ! VP--------------------------------------------------------

# & CC--------------------------------------------------------
        with st.expander('SETTINGS: CC GAINS', expanded=False):
            self.fight_cc = userInput_number(
                '!fight CC', 1, 200, 60, 5, 'bio_fight_cc')

            self.steal_cc = userInput_number(
                '!steal CC', 1, 200, 60, 5, 'bio_steal_cc')

            self.tauntCall_cc = userInput_number(
                '!taunt #arena CC', 1, 100, 30, 5, 'bio_tc_cc')

            self.tauntRespond_cc = userInput_number(
                '#taunt response CC', 1, 100, 30, 5, 'bio_tr_cc')

            self.cc_mp = int(userInput_number(
                'Cyber Credit +%', 0, 100, 25, 5, 'bio_cc_mp'))

            base_gain = self.fight_cc+self.steal_cc+self.tauntCall_cc+self.tauntRespond_cc

            self.one_cycle_cc = one_cycle_cc(base_gain, self.cc_mp)

            self.daily_cc = daily_gain(self.one_cycle_cc, self.activity)

            self.cc_over_time = gain_over_time(
                self.one_cycle_cc, self.activity, self.activity_days)
# & CC--------------------------------------------------------
