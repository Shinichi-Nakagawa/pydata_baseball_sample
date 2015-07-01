#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Shinichi Nakagawa'


class RetroSheetUtil(object):

    # at batとevent codeの対応表
    # http://www.retrosheet.org/datause.txt
    BATTING_EVENT = {
        20: ('S', ),
        21: ('DGR', 'D'),
        22: ('T', ),
        23: ('HR', ),
    }

    ATBAT_NAMES = {
        'S': 'single',
        'D': 'double',
        'DGR': 'ground rule double',
        'T': 'triple',
        'HR': 'home run'
    }

    def __init__(self):
        pass

    @classmethod
    def parse_event_tx(cls, event_tx):
        """
        event text
        :param event_tx: event text by Retrosheet
        :return: event text list
        """
        _tx = event_tx
        return _tx.split('/')

    @classmethod
    def get_atbat(cls, event_tx, event_cd, battedball_cd):
        """
        get at bat
        :param event_tx: event text by Retrosheet
        :param event_cd: event code by Retrosheet
        :param battedball_cd: battedball code by Retrosheet
        :return: batted ball
            {
                'event': 'S'
                'position': '8',
                'battedball': 'linedrive',
            }
        """
        atbat = {
            'event': None,
            'position': None,
            'battedball': None
        }
        # イベントコードをみて、打球が飛んだ場合のみ処理(三振とか四球は無視)
        int_event_cd = int(event_cd)
        if int_event_cd not in cls.BATTING_EVENT.keys():
            return atbat
        # event textをparse
        event_tx_list = cls.parse_event_tx(event_tx)
        for prefix in cls.BATTING_EVENT.get(int_event_cd):
            if event_tx_list[0].startswith(prefix):
                atbat['event'] = prefix
                atbat['battedball'] = battedball_cd
                if prefix in ('HR', 'DGR'):
                    for event_tx in event_tx_list:
                        if event_tx.isdigit():
                            atbat['position'] = event_tx
                            return atbat
                else:
                    atbat['position'] = event_tx_list[0].replace(prefix, '')
                return atbat


import unittest


class TestRetroSheetUtil(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get_atbat(self):

        # single
        self.assertEqual(
            RetroSheetUtil.get_atbat('S9/G.1-3', '20', 'G'),
            {'event': 'S', 'position': '9', 'battedball': 'G'}
        )

        # duble
        self.assertEqual(
            RetroSheetUtil.get_atbat('D57/G', 21, 'G'),
            {'event': 'D', 'position': '57', 'battedball': 'G'}
        )

        # ground rule duble
        self.assertEqual(
            RetroSheetUtil.get_atbat('DGR/9/F', '21', 'F'),
            {'event': 'DGR', 'position': '9', 'battedball': 'F'}
        )

        # ground rule duble(fan interference)
        self.assertEqual(
            RetroSheetUtil.get_atbat('DGR/FINT/7/L-.1-3', '21', 'L'),
            {'event': 'DGR', 'position': '7', 'battedball': 'L'}
        )

        # triple
        self.assertEqual(
            RetroSheetUtil.get_atbat('T9/L', '22', 'L'),
            {'event': 'T', 'position': '9', 'battedball': 'L'}
        )

        # home run
        self.assertEqual(
            RetroSheetUtil.get_atbat('HR/89/F.1-H', '23', 'F'),
            {'event': 'HR', 'position': '89', 'battedball': 'F'}
        )

        #

if __name__ == '__main__':
    unittest.main()
