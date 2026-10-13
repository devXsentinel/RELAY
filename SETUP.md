# ⚡ Quick Setup & User Guide

> **Get up and running with RELAY GUI in under 60 seconds. Zero installation, zero dependencies, 100% offline.**

---

## 📋 Requirements
- **Python 3.8+** (Standard installation from [python.org](https://www.python.org/)).
- **Zero Dependencies**: No `pip install` needed. Uses only standard library modules.

---

## 🚀 Scenario 1: Computers on the Same Network / Wi-Fi
If all computers are already connected to the same Wi-Fi, Ethernet, or office network:

### Computer 1:
```bash
python relay_gui.py ALICE
```

### Computer 2:
```bash
python relay_gui.py BOB
```

**That's it!** Both computers will automatically discover each other in under 1 second.

---

## 🏕️ Scenario 2: 100% Offline (No Internet, No Router)
If you are in a disaster zone, wilderness expedition, or off-grid room with **zero internet and no Wi-Fi router**:

### Step 1 (Host Laptop):
1. Launch RELAY GUI:
   ```bash
   python relay_gui.py ALICE
   ```
2. Click the yellow **`⚡ SIGNAL / AP`** button in the top bar.
3. Turn on the Mobile Hotspot switch (set the hotspot name to **`RELAY`** or **`RELAY-MESH`**).

### Step 2 (Other Laptops — 50m to 200m away):
1. Turn your Wi-Fi card **ON**.
2. Launch RELAY GUI:
   ```bash
   python relay_gui.py BOB
   ```
3. **You don't need to do anything else!** The background scanner automatically detects the `RELAY` signal, connects in the background, and ALICE appears in your **PEERS** sidebar.

> [!NOTE]
> Windows Mobile Hotspot works **100% offline** with zero internet or SIM card required. It simply broadcasts an ad-hoc radio signal from your laptop's Wi-Fi antenna.

---

## 💬 How to Send Messages

### 1. Broadcast to Everyone (Default Mode)
- The **`TO:`** field is already set to **`ALL`** by default.
- Simply type your message into the text box and press **Enter** (or click **SEND**).
- Every computer within radio range receives and displays the message:
  ```text
  📢 ALL (ALICE) [🔒]
  Base Camp setup complete. All units report in.
  ```
- Intermediate computers automatically forward the packet across the mesh up to **10 hops**!

### 2. Private 1-to-1 Encrypted Chat
- Click any name in the **`PEERS`** sidebar (e.g. `● BOB`).
- The **`TO:`** field changes to `BOB`.
- Type your message and press **Enter**.
- Only BOB can decrypt and read the message.
- Once BOB receives it, a green delivery confirmation appears on your screen:
  ```text
  ✓ Done → BOB: "Message text"
  ```

---

## 🔒 Optional: Password-Protected Team Mesh
To isolate your communications onto a private cryptographic channel, pass a shared secret as the 2nd argument:

```bash
# Alice:
python relay_gui.py ALICE BravoTeam2026

# Bob:
python relay_gui.py BOB BravoTeam2026
```

Both computers will display matching lock fingerprints in the footer (e.g. `🔒#8E1F03`). Nodes without this passphrase cannot decrypt messages or forge packets.

---

## 📱 Running on Android (Phones & Tablets)
1. Install **[Pydroid 3](https://play.google.com/store/apps/details?id=ru.iiec.pydroid3)** from Google Play.
2. Transfer `relay_gui.py` to your phone's storage.
3. Open `relay_gui.py` inside Pydroid 3 and tap **Run**.
4. The interface automatically adapts to mobile with fullscreen mode and a hamburger drawer (`☰`).

---

## 🔧 Quick Troubleshooting Tips
1. **Windows Firewall Prompt:** When launched for the first time, click **Allow** on Private Networks if Windows Defender asks for UDP socket permissions.
2. **Wi-Fi Not Finding Signal:** Click the **`SCAN / AUTO`** button in the sidebar to force an immediate re-scan of nearby radio signals.
3. **Interface Priority:** If both Ethernet and Wi-Fi are connected at once, unplug the unused cable so all multicast packets route through the Wi-Fi antenna.
