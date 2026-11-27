# Global Pilgrim — v4.0.0 build plan

## Trading engine (6-second human sense)
- [x] 6-second direction window driving BUY on rise / SELL on fall
- [x] Profit routed direct to Main Balance, never back to trading capital
- [x] Continuous trading switch (stays online, re-enters every opportunity)
- [x] Profit destination switch + sense-window control
- [x] Margin guard so exposure cannot run away from capital

## Insta terminal
- [x] 5-second candlestick canvas on the trading page
- [x] Instrument tabs + OHLC readout with day/month/year
- [x] Public Trading Floor view (live account, live earnings, market history)
- [x] Global Pilgrim Trading partner-terminal broadcast notice
- [x] GPC international coin listed and priced

## Banking
- [x] Real 10-digit Global Pilgrim account numbers with check digit
- [x] Admin can change a client account number (validated, unique)
- [x] Admin opens customer bank accounts with customer details
- [x] Client dashboard shows real balance and can send to other banks
- [x] Inbound receive-from-any-bank flow
- [x] Bank directory: commercial + microfinance + Global Pilgrim + First Bank
- [x] CBN registration shown as APPLICATION PENDING (honest)

## Integrations
- [x] Curated provider registry + reachability scan + scan log
- [x] Explicit refusal to auto-copy third-party code (documented in UI)

## Licence / ownership
- [x] Licence, trademark, registered office card with honest statuses

## Verification
- [x] node --check on all sources
- [x] All 13 views render with zero JS errors (admin + client)
- [x] Profit → Main verified live
- [x] Client transfer + inbound verified
- [x] Read-only seal blocks new posting paths
- [x] Backup taken before deploy
- [x] Deploy
