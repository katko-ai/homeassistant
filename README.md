# Katko.ai Infrastructure Radar — Home Assistant Custom Component 📡

[![HACS Validation](https://github.com/katko-ai/homeassistant/actions/workflows/hacs.yml/badge.svg)](https://github.com/katko-ai/homeassistant/actions)
[![HACS Default](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://hacs.xyz/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Official Home Assistant integration for **Katko.ai — The Global Infrastructure Radar**. This integration tracks real-time telecommunication network failures, power grid blackouts, water service interruptions, and official emergency alerts across 26 countries directly into your Home Assistant instance.

---

## 🚀 Installation via HACS (Home Assistant Community Store)

1. Open **HACS** in your Home Assistant sidebar -> **Integrations**.
2. Click the top-right `...` menu -> **Custom repositories**.
3. Paste repository URL: `https://github.com/katko-ai/homeassistant` and select Category: **Integration**.
4. Click **Download** and restart Home Assistant.
5. Go to **Settings** -> **Devices & Services** -> **Add Integration** -> Search for **Katko.ai Infrastructure Radar**.

---

## 📊 Sensors & Entities Provided

Each configured location creates 5 dedicated sensors with rich attributes:

| Entity ID | Sensor Name | State / Values | Key Attributes |
| :--- | :--- | :--- | :--- |
| `sensor.katko_active_disruptions_<location>` | Active Disruptions | Integer count (e.g. `0`, `3`) | List of active outages, operator names, categories |
| `sensor.katko_highest_severity_<location>` | Highest Severity | `none`, `minor`, `medium`, `major`, `critical` | Dynamic icons & alert rankings |
| `sensor.katko_telecom_outages_<location>` | Telecom Outages | Integer count | Telia, Elisa, DNA, Telenor, Vodafone, Orange, etc. |
| `sensor.katko_electricity_outages_<location>` | Power Grid Outages | Integer count | Fingrid, Caruna, ERCOT, CAISO, NYISO, etc. |
| `sensor.katko_subscription_tier_<location>` | Subscription Status | `community`, `plus`, `pro` | Update interval, webhook status, multi-location limits |

---

## ⚡ Automation Blueprints & Examples

### Example 1: Graceful Server / NAS Shutdown on Critical Outage
Automatically shut down home servers or NAS storage before UPS battery backup depletes when a critical grid failure is detected:

```yaml
alias: "Katko.ai: Graceful Server Shutdown on Grid Outage"
trigger:
  - platform: numeric_state
    entity_id: sensor.katko_active_disruptions_home
    above: 0
condition:
  - condition: state
    entity_id: sensor.katko_highest_severity_home
    state: "critical"
action:
  - service: notify.notify
    data:
      title: "🚨 Katko.ai - Critical Outage Detected!"
      message: "Infrastructure failure detected in your area. Shutting down NAS & servers..."
  - service: hassio.host_shutdown
```

### Example 2: Cottage Power Outage Freeze Warning
Receive instant mobile notifications if power fails at your cottage so you can protect heating systems and water pipes:

```yaml
alias: "Katko.ai: Cottage Power Outage Frost Warning"
trigger:
  - platform: numeric_state
    entity_id: sensor.katko_electricity_outages_cottage
    above: 0
action:
  - service: notify.mobile_app_phone
    data:
      title: "🥶 Cottage Power Outage Alert!"
      message: "Katko.ai detected a power grid outage at your cottage coordinates. Check heating & pipes."
```

---

## 🌐 Supported Countries

This integration tracks live infrastructure across 26 countries:
`Finland (FI)`, `Sweden (SE)`, `Norway (NO)`, `Denmark (DK)`, `Germany (DE)`, `France (FR)`, `Italy (IT)`, `Spain (ES)`, `United Kingdom (UK)`, `Ireland (IE)`, `Netherlands (NL)`, `Belgium (BE)`, `Portugal (PT)`, `Estonia (EE)`, `Latvia (LV)`, `Lithuania (LT)`, `Poland (PL)`, `Austria (AT)`, `Switzerland (CH)`, `Greece (GR)`, `Romania (RO)`, `Czech Republic (CZ)`, `Hungary (HU)`, `Slovakia (SK)`, `Ukraine (UA)`, `United States (US)`.

---

## 🔗 Links & Resources

* **Website & Live Radar:** [https://katko.ai](https://katko.ai)
* **Home Assistant Documentation:** [https://katko.ai/home-assistant](https://katko.ai/home-assistant)
* **Issue Tracker:** [https://github.com/katko-ai/homeassistant/issues](https://github.com/katko-ai/homeassistant/issues)

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
