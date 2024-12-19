# Spanish Energy Demand and Price Prediction with ML

## Data Collection

- Daily Spanish Gas Prices (GDAES_D+1) 2019-2024 - https://www.mibgas.es/en - https://www.mibgas.es/en/file-access
- Hourly Weather Data for Madrid, Barcelona, Seville, Bilboa, Valencia 2019-2024 - https://www.visualcrossing.com/weather/weather-data-services
- Hourly energy consumption and generation 2019-2024 - https://newtransparency.entsoe.eu/ or https://transparency.entsoe.eu/
- Another source for hourly consumption and generation data - https://www.esios.ree.es/en/generation-and-consumption?date=22-11-2024


- Kaggle dataset 2014-2018 https://www.kaggle.com/datasets/nicholasjhana/energy-consumption-generation-prices-and-weather?resource=download
    - Model on this kaggle data - https://www.kaggle.com/code/dimitriosroussis/electricity-price-forecasting-with-dnns-eda


- map of power plants around the world (can be used to get location of wind and solar plants in spain) - https://datasets.wri.org/datasets/global-power-plant-database?map=eyJ2aWV3U3RhdGUiOnsibG9uZ2l0dWRlIjowLCJsYXRpdHVkZSI6MCwiem9vbSI6MywicGl0Y2giOjAsImJlYXJpbmciOjAsInBhZGRpbmciOnsidG9wIjowLCJib3R0b20iOjAsImxlZnQiOjAsInJpZ2h0IjowfX0sImJhc2VtYXAiOiJsaWdodCIsImJvdW5kYXJpZXMiOmZhbHNlLCJsYWJlbHMiOiJkYXJrIiwiYWN0aXZlTGF5ZXJHcm91cHMiOlt7ImRhdGFzZXRJZCI6IjUzNjIzZGZkLTNkZjYtNGYxNS1hMDkxLTY3NDU3Y2RiNTcxZiIsImxheWVycyI6WyIyYTY5NDI4OS1mZWM5LTRiZmUtYTZkMi01NmMzODY0ZWMzNDkiXX1dLCJib3VuZHMiOnsiYmJveCI6bnVsbCwib3B0aW9ucyI6e319LCJsYXllcnNQYXJzZWQiOltbIjJhNjk0Mjg5LWZlYzktNGJmZS1hNmQyLTU2YzM4NjRlYzM0OSIseyJ2aXNpYmlsaXR5Ijp0cnVlLCJhY3RpdmUiOnRydWUsIm9wYWNpdHkiOjEsInpJbmRleCI6MTF9XV19

- Spanish population density data - https://data.humdata.org/dataset/worldpop-population-density-for-spain

Any missing data (of which there was very little) was filled using linear interpolation

## Background

### Spain's Day-Ahead Energy Market

In Spain, the Day-Ahead Market (DAM) sets electricity prices for the following day, with results published at 12:00 PM CET the day before the scheduled delivery. The process begins when market participants—electricity producers, consumers, and traders—submit their hourly price and quantity bids for each hour of the next day, from 00:00 to 23:00. These bids represent the minimum price at which producers are willing to sell and the maximum price at which consumers are willing to buy.

The seller bids are ranked from lowest to highest to form a "bid stack", and contrarily consumers' bids are ranked from highest to lowest. The market operator (OMIE in Spain's case) matches the bids, starting from the lowest seller bid and highest consumer bid, until the buying and selling prices meet. Any consumer bids below this price or seller bids above this price are forgetten about. This sets the marginal price—the highest price needed to meet the demand for each hour. This marginal price is applied uniformly across all producers and consumers for that hour. Renewable energy sources like wind and solar often have lower bids due to their low production costs, while gas and coal plants typically set the marginal price when renewable generation is insufficient.

<img src="./images/energy_bid-stack.png" alt="Bid Stack Example" width="500"/>

An example of a bid stack is shown in the figure above. Historical bid stacks for every hour are available [here](https://www.omie.es/en/file-access-list?parents%5B0%5D=/&parents%5B1%5D=Day-ahead%20Market&parents%5B2%5D=3.%20Curves&dir=Monthly%20files%20with%20aggregate%20supply%20and%20demand%20curves%20of%20Day-ahead%20market%20including%20bid%20units&realdir=curva_pbc_uof). These could be extremely interesting to analyse for a future project, such as creating a Reinforcement Learning agent to maximise generator profits by bidding strategically or
minimise the consumer clearing price for affordable energy.

Price transparency is ensured, and the final Day-Ahead Price is published on OMIE’s website. The market also includes an Intraday Market, where participants can adjust their positions after the Day-Ahead results. If consumers fail to secure sufficient energy in the DAM or if their energy needs change, they can use the intraday market to purchase additional electricity. Similarly, producers can sell any surplus they may have or adjust their commitments to match their real-time production capabilities. Prices are influenced by supply, demand, and the availability of generation sources, ensuring efficient electricity trading.



### Benefits of accurately predicting energy demand and price


model the consumer and seller bid stacks 


## Energy Demand Prediction

### Requirements

- Predict the energy demand for each hour in the following day (00:00 - 23:00) at 12:00 on the previous day, so as to be useful for the Day Ahead Market.
- Not using energy cost as a parameter.

### Benchmark - Seasonal ARIMA

The aim of the SARIMA model is to use linear time series analysis to create an energy demand prediction from which to benchmark the performance of the more complex ML models.

The complete work can be found in : [SARIMA Jupyter Notebook](SARIMA_demand.ipynb)

**Summary:**

- A SARIMA model extends ARIMA to include seasonality, which can be effective for regular, repeating patterns like weekly energy demand.
- SARIMA Parameters: (p, d, q) × (P, D, Q, s).
    - Non-Seasonal: 
        - p: Auto-Regressive order
        - d: Differencing order for stationarity
        - q: Moving Average order
    - Seasonal: 
        - P: Seasonal Auto-Regressive order
        - D: Seasonal Differencing order
        - Q: Seasonal Moving Average order
        - s: Seasonal period (168 for weekly seasonality in this model)
- Stationarity Testing:
    - Stationarity required for SARIMA to function correctly.
    - Applied Augmented Dickey-Fuller (ADF) test and got that trend differencing (d = 1) and seasonal differencing (D = 1) needed to achieve stationarity.
- Parameter Estimation:
    - ACF (Autocorrelation Function) and PACF (Partial ACF) plots used to estimate initial parameters: p = 3, q = 50, P = 1, Q = 6.
    - Refined parameters by minimizing Akaike Information Criterion (AIC):
        - Final parameters: (p, d, q, P, D, Q, s) = (2, 1, 3, 1, 1, 1, 168).

Model Fit and Residuals:

Residuals largely follow a normal distribution with slightly fat tails.
Extreme values/outliers (e.g., public holidays) not fully captured.
Prediction Approach:

Rolling forecast methodology:
Trained on 500 preceding data points.
Forecasts up to 36 hours ahead for day-ahead energy market.
New SARIMA model fit every 30 days in test range.
Benchmark Role:

Provides a baseline for comparison with more complex ML models.
Simplicity prioritized, excluding external predictors like weather or holidays.

<img src="./images/SARIMA_residuals.png" alt="SARIMA Residuals" width="500"/>

RMSE : 2161.1438366925386
MAE : 1575.876012516152

<img src="./images/previous_week_residuals.png" alt="Previous Week Residuals" width="500"/>

RMSE : 1822.592475434879
MAE : 1207.4430783242258
