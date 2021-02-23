![hacs_badge](https://img.shields.io/badge/hacs-custom-orange.svg) [![BuyMeCoffee][buymecoffeebedge]][buymecoffee]

# Instagram Sensor Component

![logo.jpg](logo.png)

Custom component to get full name, posts, followers, following from Instagram for Home Assistant

# Installation

## HACS

- Have [HACS](https://hacs.xyz/) installed, this will allow you to easily update.

- Add https://github.com/hudsonbrendon/sensor.instagram as a custom repository with Type: Integration
- Click Install under "Instagram" integration.
- Restart Home-Assistant.

## Manual

- Copy directory custom_components/instagram to your <config dir>/custom_components directory.
- Configure.
- Restart Home-Assistant.

# Configuration

```yaml
- platform: instagram
  account: your-instagram-account
```

# Debugging

```yaml
logger:
  default: info
  logs:
    custom_components.instagram: debug
```

[buymecoffee]: https://www.buymeacoffee.com/hudsonbrendon
[buymecoffeebedge]: https://camo.githubusercontent.com/cd005dca0ef55d7725912ec03a936d3a7c8de5b5/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f6275792532306d6525323061253230636f666665652d646f6e6174652d79656c6c6f772e737667
