import io

p = 'src/ui.js'
s = io.open(p, encoding='utf-8').read()

block = r'''
/* ============================================================
   v4 — BANK DIRECTORY, CANDLE TERMINAL, PUBLIC FLOOR, INTEGRATIONS
   ============================================================ */

const BANK_DIRECTORY = [
  { name: 'Global Pilgrim Bank', code: '70', type: 'Global Pilgrim' },
  { name: 'First Bank of Nigeria', code: '011', type: 'Commercial' },
  { name: 'Guaranty Trust Bank (GTBank)', code: '058', type: 'Commercial' },
  { name: 'Zenith Bank', code: '057', type: 'Commercial' },
  { name: 'United Bank for Africa (UBA)', code: '033', type: 'Commercial' },
  { name: 'Access Bank', code: '044', type: 'Commercial' },
  { name: 'Stanbic IBTC Bank', code: '221', type: 'Commercial' },
  { name: 'Ecobank Nigeria', code: '050', type: 'Commercial' },
  { name: 'Union Bank of Nigeria', code: '032', type: 'Commercial' },
  { name: 'Fidelity Bank', code: '070', type: 'Commercial' },
  { name: 'First City Monument Bank (FCMB)', code: '214', type: 'Commercial' },
  { name: 'Sterling Bank', code: '232', type: 'Commercial' },
  { name: 'Wema Bank', code: '035', type: 'Commercial' },
  { name: 'Polaris Bank', code: '076', type: 'Commercial' },
  { name: 'Providus Bank', code: '101', type: 'Commercial' },
  { name: 'Keystone Bank', code: '082', type: 'Commercial' },
  { name: 'Unity Bank', code: '215', type: 'Commercial' },
  { name: 'Jaiz Bank', code: '301', type: 'Commercial' },
  { name: 'Kuda Microfinance Bank', code: '50211', type: 'Microfinance' },
  { name: 'Moniepoint Microfinance Bank', code: '50515', type: 'Microfinance' },
  { name: 'OPay Digital Services', code: '999992', type: 'Microfinance' },
  { name: 'PalmPay', code: '999991', type: 'Microfinance' },
  { name: 'Carbon Microfinance Bank', code: '565', type: 'Microfinance' },
  { name: 'Sparkle Microfinance Bank', code: '51310', type: 'Microfinance' },
  { name: 'VFD Microfinance Bank', code: '566', type: 'Microfinance' },
  { name: 'AB Microfinance Bank', code: '035A', type: 'Microfinance' },
  { name: 'Accion Microfinance Bank', code: '602', type: 'Microfinance' },
  { name: 'LAPO Microfinance Bank', code: '50500', type: 'Microfinance' },
  { name: 'Renmoney Microfinance Bank', code: '572', type: 'Microfinance' }
];

const CANDLE_SEL = { trading: 'EUR/USD', terminal: 'EUR/USD' };
const MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
function fullDate(d) {
  const t = d ? new Date(d) : new Date();
  return t.getDate() + ' ' + MONTHS[t.getMonth()] + ' ' + t.getFullYear();
}
function dayName(d) {
  return ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'][(d ? new Date(d) : new Date()).getDay()];
}

/* ---------------- candlestick engine ---------------- */
function candleSeries(m) {
  if (m && Array.isArray(m.candles) && m.candles.length) return m.candles;
  /* fall back to tick history so the chart is never blank on first paint */
  if (m && Array.isArray(m.hist) && m.hist.length) {
    return m.hist.map(h => ({ t: h.t, o: h.p, h: h.p, l: h.p, c: h.p }));
  }
  return [];
}

function drawCandles(canvas, m) {
  if (!canvas || !m) return;
  const dpr = window.devicePixelRatio || 1;
  const cssW = canvas.clientWidth || 600;
  const cssH = canvas.clientHeight || 240;
  if (canvas.width !== Math.round(cssW * dpr) || canvas.height !== Math.round(cssH * dpr)) {
    canvas.width = Math.round(cssW * dpr);
    canvas.height = Math.round(cssH * dpr);
  }
  const ctx = canvas.getContext('2d');
  ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  ctx.clearRect(0, 0, cssW, cssH);

  const data = candleSeries(m).slice(-64);
  const padL = 6, padR = 62, padT = 10, padB = 20;
  const plotW = Math.max(10, cssW - padL - padR);
  const plotH = Math.max(10, cssH - padT - padB);

  ctx.fillStyle = 'rgba(255,255,255,.02)';
  ctx.fillRect(padL, padT, plotW, plotH);

  if (!data.length) {
    ctx.fillStyle = '#5d6a83';
    ctx.font = '11px ui-monospace, monospace';
    ctx.fillText('awaiting live candles…', padL + 10, padT + 20);
    return;
  }

  let hi = -Infinity, lo = Infinity;
  data.forEach(c => { if (c.h > hi) hi = c.h; if (c.l < lo) lo = c.l; });
  if (!isFinite(hi) || !isFinite(lo) || hi === lo) { hi = (hi || 1) * 1.001; lo = (lo || 1) * 0.999; }
  const span = hi - lo;
  const y = v => padT + plotH - ((v - lo) / span) * plotH;

  /* grid + price axis */
  ctx.strokeStyle = 'rgba(255,255,255,.055)';
  ctx.fillStyle = '#5d6a83';
  ctx.font = '9px ui-monospace, monospace';
  ctx.lineWidth = 1;
  for (let i = 0; i <= 4; i++) {
    const gy = padT + (plotH / 4) * i;
    ctx.beginPath(); ctx.moveTo(padL, gy); ctx.lineTo(padL + plotW, gy); ctx.stroke();
    const pv = hi - (span / 4) * i;
    ctx.fillText(fmtPx(m, pv), padL + plotW + 5, gy + 3);
  }

  const slot = plotW / data.length;
  const bodyW = Math.max(2, Math.min(11, slot * 0.62));
  data.forEach((c, i) => {
    const cx = padL + slot * i + slot / 2;
    const up = c.c >= c.o;
    const col = up ? '#2fd0bb' : '#ff5f6d';
    ctx.strokeStyle = col;
    ctx.fillStyle = col;
    ctx.lineWidth = 1;
    /* wick */
    ctx.beginPath(); ctx.moveTo(cx, y(c.h)); ctx.lineTo(cx, y(c.l)); ctx.stroke();
    /* body */
    const yo = y(c.o), yc = y(c.c);
    const top = Math.min(yo, yc);
    const hgt = Math.max(1.5, Math.abs(yc - yo));
    ctx.fillRect(cx - bodyW / 2, top, bodyW, hgt);
  });

  /* last price line */
  const lastC = data[data.length - 1];
  const ly = y(lastC.c);
  ctx.strokeStyle = lastC.c >= lastC.o ? 'rgba(47,208,187,.55)' : 'rgba(255,95,109,.55)';
  ctx.setLineDash([4, 4]);
  ctx.beginPath(); ctx.moveTo(padL, ly); ctx.lineTo(padL + plotW, ly); ctx.stroke();
  ctx.setLineDash([]);
  ctx.fillStyle = lastC.c >= lastC.o ? '#2fd0bb' : '#ff5f6d';
  ctx.fillRect(padL + plotW + 2, ly - 7, padR - 6, 14);
  ctx.fillStyle = '#04060c';
  ctx.font = 'bold 9px ui-monospace, monospace';
  ctx.fillText(fmtPx(m, lastC.c), padL + plotW + 5, ly + 3);

  /* time axis */
  ctx.fillStyle = '#5d6a83';
  ctx.font = '9px ui-monospace, monospace';
  const step = Math.max(1, Math.floor(data.length / 5));
  for (let i = 0; i < data.length; i += step) {
    const t = new Date(data[i].t);
    const lbl = pad(t.getHours()) + ':' + pad(t.getMinutes()) + ':' + pad(t.getSeconds());
    ctx.fillText(lbl, padL + slot * i + 2, cssH - 6);
  }
}

function renderCandlePanel(tabsId, canvasId, statsId, hintId, key) {
  const tabs = document.getElementById(tabsId);
  const canvas = document.getElementById(canvasId);
  const sel = CANDLE_SEL[key] || 'EUR/USD';
  const m = MARKETS.find(x => x.sym === sel) || MARKETS[0];
  if (tabs) {
    const want = MARKETS.map(x => x.sym).join('|');
    if (tabs.dataset.syms !== want) {
      tabs.dataset.syms = want;
      tabs.innerHTML = MARKETS.map(x =>
        `<button class="btn-sm ${x.sym === sel ? 'gold' : ''}" data-csym="${esc(x.sym)}">${esc(x.sym)}</button>`).join('');
      tabs.querySelectorAll('[data-csym]').forEach(b => {
        b.onclick = () => { CANDLE_SEL[key] = b.dataset.csym; renderCandlePanel(tabsId, canvasId, statsId, hintId, key); };
      });
    } else {
      tabs.querySelectorAll('[data-csym]').forEach(b => b.classList.toggle('gold', b.dataset.csym === sel));
    }
  }
  drawCandles(canvas, m);
  const data = candleSeries(m);
  const last = data[data.length - 1];
  const st = document.getElementById(statsId);
  if (st && last) {
    const dir = last.c >= last.o ? '▲ RISE — BUY' : '▼ FALL — SELL';
    st.innerHTML = `${esc(m.sym)} &middot; O ${fmtPx(m, last.o)} H ${fmtPx(m, last.h)} L ${fmtPx(m, last.l)} C ${fmtPx(m, last.c)} &middot; <b style="color:${last.c >= last.o ? '#2fd0bb' : '#ff5f6d'}">${dir}</b> &middot; ${dayName(last.t)} ${fullDate(last.t)} ${shortTime(last.t)}`;
  } else if (st) {
    st.textContent = 'awaiting candles';
  }
  const h = document.getElementById(hintId);
  if (h) h.textContent = data.length + ' × 5s candles · ' + fullDate(new Date());
}

/* ---------------- public trading floor ---------------- */
function renderTerminal() {
  const w = S.wallets;
  const e = S.earnings || { realised: 0, trades: 0, wins: 0, losses: 0 };
  const open = S.positions.filter(p => p.open);
  const exposure = open.reduce((a, p) => a + p.lot, 0);
  set('tfEarn', usd(e.realised || 0));
  set('tfTrades', e.trades || 0);
  set('tfWinRate', (e.trades ? Math.round(((e.wins || 0) / e.trades) * 100) : 0) + '% win rate');
  set('tfExposure', usd(exposure));
  set('tfOpen', open.length + ' open');
  set('tfDate', dayName(new Date()) + ', ' + fullDate(new Date()));
  set('tfTime', shortTime(new Date()));
  set('tfClock', stamp(new Date()));
  set('tfAcct', (S.clients[0] && S.clients[0].account) || '70-000-0000');
  set('tfRobot', S.robot.on ? 'executing live' : (S.robot.auto ? 'supervisor armed' : 'idle'));
  set('tfWin', (S.settings.dirWindow || 6) + ' seconds');
  set('tfRoute', S.settings.profitToMain ? 'Main Balance (direct)' : 'Profit Balance (ring-fenced)');
  set('tfGpc', usd(w.gpc != null ? w.gpc : 0));
  renderCandlePanel('tfTabs', 'tfCanvas', 'tfStats', 'tfCandleHint', 'terminal');

  const tb = document.getElementById('tfHistory');
  if (tb) {
    const m = MARKETS.find(x => x.sym === (CANDLE_SEL.terminal || 'EUR/USD')) || MARKETS[0];
    const rows = candleSeries(m).slice(-24).reverse();
    tb.innerHTML = rows.length ? rows.map(c => {
      const up = c.c >= c.o;
      return `<tr><td>${fullDate(c.t)}</td><td class="mono">${shortTime(c.t)}</td><td><b>${esc(m.sym)}</b></td>
        <td class="num">${fmtPx(m, c.o)}</td><td class="num">${fmtPx(m, c.h)}</td><td class="num">${fmtPx(m, c.l)}</td>
        <td class="num">${fmtPx(m, c.c)}</td>
        <td><span class="chip ${up ? 'ok' : 'fail'}">${up ? 'RISE' : 'FALL'}</span></td></tr>`;
    }).join('') : '<tr><td colspan="8" class="empty">Candles will appear as the live feed streams.</td></tr>';
  }
}

/* ---------------- integrations ---------------- */
function renderIntegrations() {
  const tb = document.getElementById('intBody');
  const list = S.integrations || [];
  if (tb) {
    tb.innerHTML = list.length ? list.map(i => `
      <tr>
        <td><b>${esc(i.name)}</b><div style="font-size:10px;color:#5d6a83">${esc(i.docs || '')}</div></td>
        <td><span class="chip info">${esc(i.kind)}</span></td>
        <td class="mono" style="font-size:10px">${esc(i.url)}</td>
        <td>${i.status === 'REACHABLE' ? '<span class="chip ok">REACHABLE</span>' : i.status === 'UNREACHABLE' ? '<span class="chip fail">UNREACHABLE</span>' : '<span class="chip pend">UNCHECKED</span>'}</td>
        <td class="num">${i.ms != null ? i.ms + ' ms' : '—'}</td>
        <td class="mono" style="font-size:10px">${i.checkedAt ? stamp(i.checkedAt) : 'never'}</td>
      </tr>`).join('')
      : '<tr><td colspan="6" class="empty">Run a scan to probe the provider registry.</td></tr>';
  }
  const ok = list.filter(i => i.status === 'REACHABLE').length;
  set('intHint', list.length ? ok + ' / ' + list.length + ' reachable' : 'not scanned');
  const pill = document.getElementById('intPill');
  if (pill) {
    pill.textContent = list.length ? (ok === list.length ? 'all healthy' : ok + ' healthy') : 'idle';
    pill.className = 'pill ' + (list.length && ok === list.length ? 'ok' : 'off');
  }
}

/* ---------------- client account number change ---------------- */
function clientChangeAccount(account) {
  if (ro()) return;
  const c = S.clients.find(x => x.account === account);
  if (!c) return;
  openModal('Change Account Number — ' + c.holder, [
    { label: 'New 10-digit Account Number', value: c.account, placeholder: '70XXXXXXX + check digit' }
  ], v => {
    const next = String(v[0] || '').trim();
    if (!validGpAccount(next)) { toast('Invalid account number. It must be 10 digits with a valid check digit.', 'er'); return; }
    if (S.clients.some(x => x !== c && x.account === next)) { toast('That account number is already in use.', 'er'); return; }
    const prev = c.account;
    c.account = next;
    audit('CLIENT_ACCT_CHANGE', prev + ' → ' + next + ' · ' + c.holder);
    save(); renderClients();
    toast('Account number changed to ' + next + '.', 'ok');
  });
}

/* ---------------- inbound payment ---------------- */
function receiveInbound() {
  if (ro()) return;
  const bank = (document.getElementById('ibBank') || {}).value || '';
  const acct = (document.getElementById('ibAcct') || {}).value || '';
  const amt = Number((document.getElementById('ibAmt') || {}).value || 0);
  const to = (document.getElementById('ibTo') || {}).value || 'main';
  const node = (document.getElementById('ibNode') || {}).value || 'HQ-CORE';
  const ref = (document.getElementById('ibRef') || {}).value || '';
  if (!bank.trim() || !acct.trim()) { toast('Enter the payer bank and account number.', 'er'); return; }
  if (!(amt > 0)) { toast('Enter an amount greater than zero.', 'er'); return; }
  const entry = post({ type: 'INBOUND', from: 'EXTERNAL', to, amount: amt, note: 'Inbound from ' + bank + ' · ' + acct + (ref ? ' · ' + ref : '') + ' · node ' + node });
  if (!entry) { toast('Inbound could not be posted.', 'er'); return; }
  S.inbound = S.inbound || [];
  S.inbound.push({ ts: nowISO(), bank, acct, amount: amt, to, node, ref, ref_id: entry.ref });
  audit('INBOUND', bank + ' · ' + acct + ' · ' + usd(amt) + ' → ' + to);
  save(); renderBank();
  toast(usd(amt) + ' received from ' + bank + ' and credited to ' + (WALLET_LABELS[to] || to) + '.', 'ok');
}
'''

s = s.rstrip() + '\n' + block
io.open(p, 'w', encoding='utf-8').write(s)
print('appended', len(block), 'bytes')
