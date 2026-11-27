import io, re, sys

p = 'src/app.html'
s = io.open(p, encoding='utf-8').read()
orig = s
n = 0

def rep(old, new, label):
    global s, n
    if s.count(old) != 1:
        print('FAIL', label, 'count=', s.count(old)); sys.exit(1)
    s = s.replace(old, new, 1); n += 1
    print('ok', label)

# ---------- 1. trading header copy ----------
rep(
 '<p>Live execution across currency, crypto, equities, metals and minerals. The robot reads the feed every 5 seconds and follows direction \u2014 rising markets buy, falling markets sell. Realised profit posts straight to the Profit Balance and never mixes with trading capital.</p>',
 '<p>Live Forex and multi-asset execution. The human-sense robot reads the feed on a 6-second window: if price rises over 6 seconds it buys, if price falls over 6 seconds it sells, and the instant a position turns positive the profit is routed <b>direct to your Main Balance</b> \u2014 it never returns to trading capital. It repeats as many times as the market offers an opportunity, with the automatic switch held on for continuous trading.</p>',
 'trading header')

# ---------- 2. candlestick + live account row ----------
anchor = '<div class="card metric blue"><div class="lbl">Session P&amp;L</div><div class="val" id="tPnl">0.00</div><div class="sub" id="tPnlPct">0.00% on capital</div></div>\n      </div>'
insert = anchor + '''

      <div class="grid g23" style="margin-bottom:14px">
        <div class="card">
          <div class="card-h"><h3>Insta Candlestick Terminal</h3><span class="hint" id="candleHint">5-second candles</span></div>
          <div id="candleTabs" style="display:flex;flex-wrap:wrap;gap:6px;margin-bottom:10px"></div>
          <canvas id="candleCanvas" style="width:100%;height:240px;display:block"></canvas>
          <div class="hint" id="candleStats" style="margin-top:10px;font-family:ui-monospace,monospace;font-size:11px">awaiting candles</div>
        </div>
        <div class="card">
          <div class="card-h"><h3>Live Account</h3><span class="pill ok" id="livePill"><i class="dot"></i> LIVE</span></div>
          <div class="kv"><span>Account</span><b class="mono" id="termAcct">\u2014</b></div>
          <div class="kv"><span>Live earnings</span><b id="termEarn">$0.00</b></div>
          <div class="kv"><span>Trades executed</span><b id="termTrades">0</b></div>
          <div class="kv"><span>Main Balance</span><b id="termMain">$0.00</b></div>
          <div class="kv"><span>Terminal clock</span><b class="mono" id="termClock">\u2014</b></div>
          <div class="notice info" style="margin-top:12px">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="9"/><path d="M2 12h20M12 2c3 3.4 3 16.6 0 20M12 2c-3 3.4-3 16.6 0 20"/></svg>
            <b>Global Pilgrim Trading</b> \u2014 this account is broadcast to partner terminals abroad, telling them you are part of the live trading network.
          </div>
          <button class="btn-sm gold" style="width:100%;margin-top:12px" onclick="go('terminal')">Open Public Trading Floor</button>
        </div>
      </div>'''
rep(anchor, insert, 'candle row')

# ---------- 3. 5s delta header ----------
rep('<th class="num">5s &Delta;</th>', '<th class="num">6s &Delta;</th>', '6s delta header')

# ---------- 4. robot control copy + new switches ----------
rep('<span>Follows live 5-second direction on every enabled market.</span>',
    '<span>Follows live 6-second direction on every enabled market.</span>', 'robot copy')

rep('''          <div class="hint" id="robotSense" style="margin-bottom:10px">Supervisor online &mdash; monitoring.</div>''',
'''          <div class="switch" style="margin-bottom:8px">
            <div class="txt"><b>Continuous Trading</b><span>Keeps the robot online, re-entering every opportunity without a new directive.</span></div>
            <div class="sw on" id="contSwitch" onclick="toggleContinuous()"></div>
          </div>
          <div class="switch" style="margin-bottom:12px">
            <div class="txt"><b>Profit &rarr; Main Balance (direct)</b><span>Realised profit is routed straight to Main and never returns to trading.</span></div>
            <div class="sw on" id="destSwitch" onclick="toggleProfitDestination()"></div>
          </div>
          <div class="form-grid c2" style="margin-bottom:10px">
            <div><label class="flabel">Sense Window (seconds)</label><input class="inp" id="dirWin" type="number" min="2" max="60" step="1" value="6" onchange="setDirectionWindow(this.value)"></div>
            <div><label class="flabel">Direction read</label><div class="hint" id="dirWinLbl" style="padding-top:9px">6s rise = BUY \u00b7 6s fall = SELL</div></div>
          </div>
          <div class="hint" id="robotSense" style="margin-bottom:10px">Supervisor online &mdash; monitoring.</div>''', 'robot switches')

rep('Profit is credited to the Profit Balance the instant a position closes. Trading capital is never touched by profit.',
    'The instant a position closes in profit it is routed direct to your Main Balance \u2014 profit never returns to trading capital. If a position closes at a loss only the loss is booked against trading capital.', 'profit notice')

# ---------- 5. nav items ----------
rep('''        Trading Terminal
      </button>''',
'''        Trading Terminal
      </button>
      <button class="nav-item" data-view="terminal" onclick="go('terminal')">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><rect x="3" y="4" width="18" height="13" rx="2"/><path d="M8 21h8M12 17v4"/><path d="m7 12 3-3 2 2 4-4"/></svg>
        Trading Floor
      </button>''', 'nav terminal')

rep('''        Payout Rails
      </button>''',
'''        Payout Rails
      </button>
      <button class="nav-item" data-view="integrations" onclick="go('integrations')">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M9 3v6H3"/><path d="M15 21v-6h6"/><circle cx="12" cy="12" r="3"/><path d="M12 3v3M12 18v3M3 12h3M18 12h3"/></svg>
        Integrations
      </button>''', 'nav integrations')

# ---------- 6. clients: bank transfer + change account ----------
rep('''        <div class="head-actions">
          <button class="btn-sm gold" onclick="openAddClient()">Open New Account</button>
        </div>
      </div>''',
'''        <div class="head-actions">
          <button class="btn-sm gold" onclick="openAddClient()">Open New Account</button>
        </div>
      </div>

      <div class="grid g2" style="margin-bottom:14px">
        <div class="card">
          <div class="card-h"><h3>Open Customer Bank Account</h3><span class="hint">Real 10-digit Global Pilgrim number</span></div>
          <div class="hint" style="margin-bottom:10px">Every new customer receives a real ten-digit Global Pilgrim Bank account number (bank code 70) with a modulus check digit, exactly like a commercial bank. The administrator can change it later.</div>
          <button class="btn-sm gold" style="width:100%" onclick="openAddClient()">Open Account With Customer Details</button>
          <div class="kv" style="margin-top:12px"><span>Bank</span><b>Global Pilgrim Bank</b></div>
          <div class="kv"><span>Bank code</span><b class="mono">70</b></div>
          <div class="kv"><span>Number format</span><b class="mono">70XXXXXXX + check digit</b></div>
        </div>
        <div class="card">
          <div class="card-h"><h3>Client Bank Transfer</h3><span class="hint">Network / SMS-chip rails</span></div>
          <div class="form-grid c2">
            <div><label class="flabel">Client Account</label><select class="inp" id="cbClient"></select></div>
            <div><label class="flabel">Amount (USD)</label><input class="inp" id="cbAmt" type="number" step="0.01" placeholder="0.00"></div>
            <div><label class="flabel">Beneficiary Bank</label><select class="inp" id="cbBank"></select></div>
            <div><label class="flabel">Account Number</label><input class="inp" id="cbAcct" placeholder="10 digits"></div>
            <div><label class="flabel">Account Name</label><input class="inp" id="cbName" placeholder="Beneficiary name"></div>
            <div><label class="flabel">Narration</label><input class="inp" id="cbNote" placeholder="Optional reference"></div>
          </div>
          <button class="btn-sm green" style="width:100%;margin-top:12px" onclick="clientSendBank()">Send To Other Bank</button>
          <div class="hint" style="margin-top:8px">0.1% fee \u00b7 debits the client balance and appears on the client dashboard in real time.</div>
        </div>
      </div>''', 'clients cards')

# ---------- 7. bank: inbound receive card ----------
rep('''      <div class="card pad0">
        <div class="card-h" style="padding:16px 18px 0"><h3>External Ledger</h3><span class="hint">Outbound settlement history</span></div>''',
'''      <div class="grid g2" style="margin-bottom:14px">
        <div class="card">
          <div class="card-h"><h3>Receive From Any Bank Worldwide</h3><span class="hint">Inbound via API / protocol / IP</span></div>
          <div class="hint" style="margin-bottom:10px">Global Pilgrim Bank accepts inbound payment from any bank in the world addressed by account number and bank name. Inbound instructions are matched by the receiving node (API, protocol or IP) and credited to the nominated wallet.</div>
          <div class="form-grid c2">
            <div><label class="flabel">Payer Bank</label><input class="inp" id="ibBank" placeholder="Originating bank"></div>
            <div><label class="flabel">Payer Account Number</label><input class="inp" id="ibAcct" placeholder="Account number"></div>
            <div><label class="flabel">Amount (USD)</label><input class="inp" id="ibAmt" type="number" step="0.01" placeholder="0.00"></div>
            <div><label class="flabel">Credit Wallet</label><select class="inp" id="ibTo"></select></div>
            <div><label class="flabel">Receiving Node / Protocol</label><input class="inp" id="ibNode" placeholder="API, protocol or IP" value="HQ-CORE"></div>
            <div><label class="flabel">Reference</label><input class="inp" id="ibRef" placeholder="Invoice / contract"></div>
          </div>
          <button class="btn-sm gold" style="width:100%;margin-top:12px" onclick="receiveInbound()">Record Inbound Payment</button>
        </div>
        <div class="card">
          <div class="card-h"><h3>Bank Directory</h3><span class="hint">Commercial &amp; microfinance</span></div>
          <div class="hint" style="margin-bottom:8px">Global Pilgrim Bank is listed alongside the commercial and microfinance banks. CBN registration is shown honestly as pending until the licence is granted.</div>
          <div class="tbl-wrap" style="max-height:210px;overflow-y:auto">
            <table><thead><tr><th>Bank</th><th>Code</th><th>Type</th></tr></thead><tbody id="bankDirBody"></tbody></table>
          </div>
          <div class="kv" style="margin-top:10px"><span>CBN registration</span><b id="cbnState">APPLICATION PENDING</b></div>
        </div>
      </div>

      <div class="card pad0">
        <div class="card-h" style="padding:16px 18px 0"><h3>External Ledger</h3><span class="hint">Outbound settlement history</span></div>''', 'bank inbound')

# ---------- 8. settings licence card ----------
rep('''          <div class="kv"><span>Build</span><b id="dBuild">v3.0</b></div>
        </div>''',
'''          <div class="kv"><span>Registered office</span><b>Global Pilgrim House, Victoria Island, Lagos State, Nigeria</b></div>
          <div class="kv"><span>Build</span><b id="dBuild">v4.0</b></div>
        </div>
        <div class="card">
          <div class="card-h"><h3>Licence, Trademark &amp; Right to Operate</h3><span class="hint">Honest status</span></div>
          <div class="kv"><span>Banking licence (CBN)</span><b id="licState">APPLICATION PENDING</b></div>
          <div class="kv"><span>Trademark</span><b id="tmState">FILED &mdash; NOT YET REGISTERED</b></div>
          <div class="kv"><span>Registered office</span><b>Lagos State, Nigeria</b></div>
          <div class="kv"><span>Operating scope</span><b>Worldwide (subject to local law)</b></div>
          <div class="notice" style="margin-top:12px">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 9v4M12 17h.01"/><circle cx="12" cy="12" r="9"/></svg>
            These statuses are recorded exactly as filed. No licence, registration or trademark is claimed as granted until the relevant authority issues it. Operating in any jurisdiction remains subject to that jurisdiction's law and to provider KYB approval.
          </div>
        </div>''', 'licence card')

# ---------- 9. new sections: terminal + integrations ----------
new_sections = '''
    <!-- TRADING FLOOR (PUBLIC TERMINAL) -->
    <section class="view" id="view-terminal">
      <div class="view-head">
        <div>
          <h2>Global Pilgrim Trading &mdash; Public Trading Floor</h2>
          <p>Live Forex terminal broadcast to partner desks abroad. Live account, live earnings, 5-second candlestick reading, market history and the full date in day, month and year. This is a live account, not a demo.</p>
        </div>
        <div class="head-actions">
          <span class="pill ok" id="termPill2"><i class="dot"></i> BROADCASTING</span>
        </div>
      </div>

      <div class="grid g4" style="margin-bottom:14px">
        <div class="card metric green"><div class="lbl">Live Earnings</div><div class="val" id="tfEarn">0.00</div><div class="sub">Realised, routed to Main</div></div>
        <div class="card metric teal"><div class="lbl">Trades</div><div class="val" id="tfTrades">0</div><div class="sub" id="tfWinRate">0% win rate</div></div>
        <div class="card metric blue"><div class="lbl">Open Exposure</div><div class="val" id="tfExposure">0.00</div><div class="sub" id="tfOpen">0 open</div></div>
        <div class="card metric"><div class="lbl">Terminal Date</div><div class="val" id="tfDate" style="font-size:16px">--</div><div class="sub" id="tfTime">--:--:--</div></div>
      </div>

      <div class="grid g23" style="margin-bottom:14px">
        <div class="card">
          <div class="card-h"><h3>Live Candle Reading</h3><span class="hint" id="tfCandleHint">5-second candles</span></div>
          <div id="tfTabs" style="display:flex;flex-wrap:wrap;gap:6px;margin-bottom:10px"></div>
          <canvas id="tfCanvas" style="width:100%;height:260px;display:block"></canvas>
          <div class="hint" id="tfStats" style="margin-top:10px;font-family:ui-monospace,monospace;font-size:11px">awaiting candles</div>
        </div>
        <div class="card">
          <div class="card-h"><h3>Partner Terminal Notice</h3><span class="hint">Global Pilgrim Trading</span></div>
          <div class="notice info" style="margin-bottom:12px">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="9"/><path d="M2 12h20M12 2c3 3.4 3 16.6 0 20M12 2c-3 3.4-3 16.6 0 20"/></svg>
            <b>You are part of trading.</b> This terminal is visible to partner desks abroad: Global Pilgrim Trading is live on the network and this account is actively trading.
          </div>
          <div class="kv"><span>Account</span><b class="mono" id="tfAcct">&mdash;</b></div>
          <div class="kv"><span>Account holder</span><b>Olawale Abdul-ganiyu Adeshina</b></div>
          <div class="kv"><span>Robot</span><b id="tfRobot">idle</b></div>
          <div class="kv"><span>Sense window</span><b id="tfWin">6 seconds</b></div>
          <div class="kv"><span>Profit routing</span><b id="tfRoute">Main Balance (direct)</b></div>
          <div class="kv"><span>Terminal clock</span><b class="mono" id="tfClock">&mdash;</b></div>
          <div class="kv"><span>GPC (international)</span><b id="tfGpc">$0.00</b></div>
        </div>
      </div>

      <div class="card pad0">
        <div class="card-h" style="padding:16px 18px 0"><h3>Market History</h3><span class="hint">Candle close history with full date</span></div>
        <div class="tbl-wrap" style="padding:0 6px 8px">
          <table>
            <thead><tr><th>Date (day month year)</th><th>Time</th><th>Instrument</th><th class="num">Open</th><th class="num">High</th><th class="num">Low</th><th class="num">Close</th><th>Direction</th></tr></thead>
            <tbody id="tfHistory"></tbody>
          </table>
        </div>
      </div>
    </section>

    <!-- INTEGRATIONS -->
    <section class="view" id="view-integrations">
      <div class="view-head">
        <div>
          <h2>Payment Integrations &mdash; Health Scan</h2>
          <p>A curated registry of licensed payment providers. The robot probes each provider endpoint and reports reachability, latency and the date of the last check, then notifies you when the payment section is confirmed healthy.</p>
        </div>
        <div class="head-actions">
          <button class="btn-sm gold" onclick="scanIntegrations()">Run Scan</button>
        </div>
      </div>

      <div class="notice" style="margin-bottom:14px">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 9v4M12 17h.01"/><path d="M10.3 3.9 1.8 18a2 2 0 0 0 1.7 3h17a2 2 0 0 0 1.7-3L13.7 3.9a2 2 0 0 0-3.4 0Z"/></svg>
        <b>Important:</b> the robot never copies or installs third-party source code from GitHub, Google, Amazon, Yahoo or Yandex. Silently pulling code from the internet into a payment system is a supply-chain attack vector. Instead the robot verifies each provider's official endpoint and reports whether it is reachable and correct. Integrations are enabled only with your own KYB-approved provider keys on the secure backend.
      </div>

      <div class="grid g23" style="margin-bottom:14px">
        <div class="card pad0">
          <div class="card-h" style="padding:16px 18px 0"><h3>Provider Registry</h3><span class="hint" id="intHint">not scanned</span></div>
          <div class="tbl-wrap" style="padding:0 6px 8px">
            <table>
              <thead><tr><th>Provider</th><th>Rail</th><th>Endpoint</th><th>Status</th><th class="num">Latency</th><th>Last Check</th></tr></thead>
              <tbody id="intBody"></tbody>
            </table>
          </div>
        </div>
        <div class="card">
          <div class="card-h"><h3>Robot Scan Log</h3><span class="pill off" id="intPill">idle</span></div>
          <div class="log" id="intLog" style="max-height:340px"></div>
        </div>
      </div>
    </section>
'''
rep('''  </main>
</div>''', new_sections + '''  </main>
</div>''', 'new sections')

io.open(p, 'w', encoding='utf-8').write(s)
print('WROTE', p, len(orig), '->', len(s), 'replacements', n)
