# Brand New Day quotes

API Docs: https://bnd.properchaos.nl/docs

This project delivers quotes from [BrandNewDay.nl](https://brandnewday.nl) funds in a structured manner, with support for [PortfolioPerformance](https://www.portfolio-performance.info/en/).
You can either self-host this application, or you can use the publicly available endpoint.

## Using the public endpoint in PortfolioPerformance
To use the endpoint in PortfolioPerformance, use the following configuration:

| Setting | Value |
|-|-|
| Provider  | JSON  |
| Feed URL  | `https://bnd.properchaos.nl/quotes/bnd-wereld-indexfonds-hedged?page={PAGE}`  |
| Path to Date | `$.[*].Date` |
| Path to Close | `$.[*].Close` |

You can replace `bnd-wereld-indexfonds-hedged` with any of the fund names you can find [here](https://bnd.properchaos.nl/funds).
The `?page={PAGE}` part makes sure PortfolioPerformance retrieves the entire history of quotes, not just the last 60 days.

## Self-hosting
To self-host this project, use the `Dockerfile`:

```
$ git clone git@github.com:StevenReitsma/bnd-quotes.git
$ cd bnd-quotes
$ docker build --tag bnd-quotes .
$ docker run -it -p 8080:8080 bnd-quotes
```

You can then access the API at `http://localhost:8080/docs`.

## Disclaimer

This project is not affiliated, associated, authorized, endorsed by, or in any way officially connected with Brand New Day, or any of its subsidiaries or its affiliates. The official Brand New Day website can be found at https://brandnewday.nl.
