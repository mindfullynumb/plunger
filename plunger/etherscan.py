# This file is part of Plunger.
#
# Copyright (C) 2017 reverendus
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import requests
from lxml import html

from plunger.transaction import Transaction


class Etherscan:
    def __init__(self, chain):
        if chain == "ethlive":
            self.url = "etherscan.io"
        elif chain == "kovan":
            self.url = "kovan.etherscan.io"
        else:
            #TODO for unit testing only, let's find a better solution afterwards
            self.url = "unknown.etherscan.io"

    def list_pending_txs(self, address) -> list:
        page = requests.get(f"https://{self.url}/txsPending?a={address}")
        tree = html.fromstring(page.content)
        tx_ids = tree.xpath('//table[contains(@class,"table")]//td[1]/span[@class="address-tag"]/a/text()')
        return list(map(self.tx_details, tx_ids))

    def tx_details(self, tx_id) -> Transaction:
        page = requests.get(f"https://{self.url}/tx/{tx_id}")
        tree = html.fromstring(page.content)
        nonce = int(tree.xpath('//span[contains(@title,"The transaction nonce")]/text()')[0].strip())
        return Transaction(tx_hash=tx_id, nonce=nonce)
