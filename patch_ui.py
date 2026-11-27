import io, sys

p = 'src/ui.js'
s = io.open(p, encoding='utf-8').read()
orig = s
n = 0

def rep(old, new, label):
    global s, n
    if s.count(old) != 1:
        print('FAIL', label, 'count=', s.count(old)); sys.exit(1)
    s = s.replace(old, new, 1); n += 1
    print('ok', label)

# 1. GPC international listing
rep("""  { sym: 'PGC/USD', name: 'Pilgrim Coin', cls: 'Native', price: 12.84, chg24: 2.31, vol: 4.4e6, dp: 4 }""",
"""  { sym: 'PGC/USD', name: 'Pilgrim Coin', cls: 'Native', price: 12.84, chg24: 2.31, vol: 4.4e6, dp: 4 },
  { sym: 'GPC/USD', name: 'Global Pilgrim Coin (International)', cls: 'International', price: 3.4120, chg24: 1.07, vol: 2.6e7, dp: 4 }""", 'gpc market')

# 2. renderTrading additions
rep("""  const mb = document.getElementById('marketBody');""",
"""  const csw = document.getElementById('contSwitch');
  if (csw) csw.classList.toggle('on', !!S.settings.continuous);
  const dsw = document.getElementById('destSwitch');
  if (dsw) dsw.classList.toggle('on', !!S.settings.profitToMain);
  const dw = document.getElementById('dirWin');
  if (dw && document.activeElement !== dw) dw.value = S.settings.dirWindow || 6;
  set('dirWinLbl', (S.settings.dirWindow || 6) + 's rise = BUY \\u00b7 ' + (S.settings.dirWindow || 6) + 's fall = SELL');

  const e = S.earnings || { realised: 0, trades: 0, wins: 0, losses: 0 };
  set('termAcct', (S.clients[0] && S.clients[0].account) || (S.bank ? '70' + '0000000' : '\\u2014'));
  set('termEarn', usd(e.realised || 0));
  set('termTrades', (e.trades || 0) + ' trades');
  set('termMain', usd(w.main));
  set('termClock', stamp(new Date()));

  renderCandlePanel('candleTabs', 'candleCanvas', 'candleStats', 'candleHint');

  const mb = document.getElementById('marketBody');""", 'renderTrading extras')

# 3. renderView + renderAll wiring
rep("""    wallets: renderWallets, bank: renderBank, payouts: renderPayouts, clients: renderClients,
    network: renderNetwork, nodes: renderNodes, settings: renderSettings, audit: renderAudit""",
"""    wallets: renderWallets, bank: renderBank, payouts: renderPayouts, clients: renderClients,
    terminal: renderTerminal, integrations: renderIntegrations,
    network: renderNetwork, nodes: renderNodes, settings: renderSettings, audit: renderAudit""", 'renderView map')

rep("""  renderPayouts();
  renderClients();""",
"""  renderPayouts();
  renderClients();
  renderTerminal();
  renderIntegrations();""", 'renderAll map')

# 4. renderClients extras
rep("""    set('clientCount', S.clients.length + ' account' + (S.clients.length === 1 ? '' : 's'));
  }
}""",
"""    set('clientCount', S.clients.length + ' account' + (S.clients.length === 1 ? '' : 's'));
  }
  const sel = document.getElementById('cbClient');
  if (sel) sel.innerHTML = S.clients.length
    ? S.clients.map(c => `<option value="${esc(c.account)}">${esc(c.account)} \\u00b7 ${esc(c.holder)} \\u00b7 ${usd(c.balance)}</option>`).join('')
    : '<option value="">no client accounts</option>';
  const bs = document.getElementById('cbBank');
  if (bs && !bs.dataset.loaded) {
    bs.innerHTML = BANK_DIRECTORY.map(b => `<option>${esc(b.name)}</option>`).join('');
    bs.dataset.loaded = '1';
  }
}""", 'renderClients extras')

# 5. change-account button in client row
rep("""          <button class="btn-sm" onclick="clientProfile('${c.account}')">Edit Profile</button>""",
"""          <button class="btn-sm" onclick="clientProfile('${c.account}')">Edit Profile</button>
          <button class="btn-sm" onclick="clientChangeAccount('${c.account}')">Change Account No.</button>""", 'client row button')

# 6. renderBank extras
rep("""  set('rcHint', last ? last.serial : 'none issued');
}""",
"""  set('rcHint', last ? last.serial : 'none issued');
  const ib = document.getElementById('ibTo');
  if (ib) ib.innerHTML = ['main', 'trading', 'profit', 'micro', 'macro', 'cscs']
    .map(k => `<option value="${k}">${WALLET_LABELS[k]}</option>`).join('');
  const bd = document.getElementById('bankDirBody');
  if (bd) bd.innerHTML = BANK_DIRECTORY.map(b =>
    `<tr><td>${esc(b.name)}</td><td class="mono">${esc(b.code)}</td><td><span class="chip ${b.type === 'Global Pilgrim' ? 'ok' : 'info'}">${esc(b.type)}</span></td></tr>`).join('');
  set('cbnState', (S.bank && S.bank.licenceStatus) || 'APPLICATION PENDING');
}""", 'renderBank extras')

# 7. renderSettings licence
rep("""  const tp = document.getElementById('robotTp'); if (tp) tp.value = st.tp;
}""",
"""  const tp = document.getElementById('robotTp'); if (tp) tp.value = st.tp;
  set('licState', (S.bank && S.bank.licenceStatus) || 'APPLICATION PENDING');
  set('tmState', (S.bank && S.bank.trademarkStatus) || 'FILED \\u2014 NOT YET REGISTERED');
}""", 'renderSettings licence')

# 8. openAddClient -> real 10-digit
rep("""    const account = 'GP' + String(Math.floor(10000000 + Math.random() * 89999999));""",
"""    const account = gpAccountNo();""", 'openAddClient account')

io.open(p, 'w', encoding='utf-8').write(s)
print('WROTE', p, len(orig), '->', len(s), 'replacements', n)
