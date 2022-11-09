# Brand New Day quotes

[🇬🇧 English](#brand-new-day-quotes) | [🇳🇱 Nederlands](#brand-new-day-koersen)

API Docs: https://bnd.properchaos.nl/docs

This project delivers quotes from [BrandNewDay.nl](https://brandnewday.nl) funds in a structured manner, with support for [PortfolioPerformance](https://www.portfolio-performance.info/en/).
You can either self-host this application, or you can use the publicly available endpoint.

The minimum version of PortfolioPerformance that is compatible with this project is 0.45.0.

## Using the public endpoint in PortfolioPerformance
To use the endpoint in PortfolioPerformance for `Historical Quotes`, use the following configuration.
For `Latest Quote`, use the `(same as historical quotes)` option.

| Setting | Value |
|-|-|
| Provider  | JSON  |
| Feed URL  | `https://bnd.properchaos.nl/quotes/bnd-wereld-indexfonds-hedged?page={PAGE}`  |
| Path to Date | `$.[*].Date` |
| Path to Close | `$.[*].Close` |

You can replace `bnd-wereld-indexfonds-hedged` in the Feed URL with any of the fund names you can find [here](https://bnd.properchaos.nl/funds) (use the fund names, ignore the numbers).

## Self-hosting
To self-host this project, use the `Dockerfile`:

```
$ git clone git@github.com:StevenReitsma/bnd-quotes.git
$ cd bnd-quotes
$ docker build --tag bnd-quotes .
$ docker run -it -p 80:80 bnd-quotes
```

You can then access the API at `http://localhost/docs`.




# Brand New Day koersen
API documentatie: https://bnd.properchaos.nl/docs

Dit project zorgt ervoor dat [PortfolioPerformance](https://www.portfolio-performance.info/en/) de koersen van [BrandNewDay.nl](https://brandnewday.nl) fondsen op de juiste manier kan importeren.
Je kunt deze applicatie zelf hosten, of het publieke endpoint gebruiken.

Je hebt minimaal versie 0.45.0 van PortfolioPerformance nodig.

## Het publieke endpoint gebruiken in PortfolioPerformance
Gebruik onderstaande instellingen bij `Historical Quotes` om het publieke endpoint in PortfolioPerformance te gebruiken.
Voor `Latest Quote` moet je de `(same as historical quotes)` optie gebruiken.

| Instelling | Waarde |
|-|-|
| Provider  | JSON  |
| Feed URL  | `https://bnd.properchaos.nl/quotes/bnd-wereld-indexfonds-hedged?page={PAGE}`  |
| Path to Date | `$.[*].Date` |
| Path to Close | `$.[*].Close` |

Je kunt `bnd-wereld-indexfonds-hedged` in de Feed URL vervangen met de naam van elk ander fonds. [Hier](https://bnd.properchaos.nl/funds) vind je een lijst van alle fondsen (gebruik alleen de naam van het fonds, de getallen kun je negeren).

## Zelf hosten
Om de applicatie zelf te draaien gebruik je de `Dockerfile`:

```
$ git clone git@github.com:StevenReitsma/bnd-quotes.git
$ cd bnd-quotes
$ docker build --tag bnd-quotes .
$ docker run -it -p 80:80 bnd-quotes
```

Je kunt de API dan benaderen via `http://localhost/docs`.

## Disclaimer

This project is not affiliated, associated, authorized, endorsed by, or in any way officially connected with Brand New Day, or any of its subsidiaries or its affiliates. The official Brand New Day website can be found at https://brandnewday.nl.
