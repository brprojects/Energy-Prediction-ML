# Spanish Energy Demand and Price Prediction with ML

## Data Collection

- Daily Spanish Gas Prices (GDAES_D+1) 2019-2024 - https://www.mibgas.es/en - https://www.mibgas.es/en/file-access
- Hourly Weather Data for Madrid, Barcelona, Seville, Bilboa, Valencia 2019-2024 - https://www.visualcrossing.com/weather/weather-data-services
- Hourly energy consumption and generation 2019-2024 - https://newtransparency.entsoe.eu/ or https://transparency.entsoe.eu/
- Another source for hourly consumption and generation data - https://www.esios.ree.es/en/generation-and-consumption?date=22-11-2024


- Kaggle dataset 2014-2018 https://www.kaggle.com/datasets/nicholasjhana/energy-consumption-generation-prices-and-weather?resource=download
    - Model on this kaggle data - https://www.kaggle.com/code/dimitriosroussis/electricity-price-forecasting-with-dnns-eda


- https://www.omie.es/en/file-access-list?parents%5B0%5D=/&parents%5B1%5D=Day-ahead%20Market&parents%5B2%5D=3.%20Curves&dir=Monthly%20files%20with%20aggregate%20supply%20and%20demand%20curves%20of%20Day-ahead%20market%20including%20bid%20units&realdir=curva_pbc_uof

## Background

### Spain's Day-Ahead Energy Market

In Spain, the Day-Ahead Market (DAM) sets electricity prices for the following day, with results published at 12:00 PM CET the day before the scheduled delivery. The process begins when market participants—electricity producers, consumers, and traders—submit their hourly price and quantity bids for each hour of the next day, from 00:00 to 23:00. These bids represent the minimum price at which producers are willing to sell and the maximum price at which consumers are willing to buy.

The seller bids are ranked from lowest to highest to form a "bid stack", and contrarily consumers' bids are ranked from highest to lowest. The market operator (OMIE in Spain's case) matches the bids, starting from the lowest seller bid and highest consumer bid, until the buying and selling prices meet. Any consumer bids below this price or seller bids above this price are forgetten about. This sets the marginal price—the highest price needed to meet the demand for each hour. This marginal price is applied uniformly across all producers and consumers for that hour. Renewable energy sources like wind and solar often have lower bids due to their low production costs, while gas and coal plants typically set the marginal price when renewable generation is insufficient.

Price transparency is ensured, and the final Day-Ahead Price is published on OMIE’s website. The market also includes an Intraday Market, where participants can adjust their positions after the Day-Ahead results. If consumers fail to secure sufficient energy in the DAM or if their energy needs change, they can use the intraday market to purchase additional electricity. Similarly, producers can sell any surplus they may have or adjust their commitments to match their real-time production capabilities. Prices are influenced by supply, demand, and the availability of generation sources, ensuring efficient electricity trading.

### Benefits of accurately predicting energy demand and price


model the consumer and seller bid stacks 