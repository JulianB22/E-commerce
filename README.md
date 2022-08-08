This is a data exploration activity about orders coming from fake partners in an ecommerce app. 

Fake partners are the stores that are not integrated directly with the app so orders are charged to the customer upon delivery. 

When the products_total is lower than purchase_total_price we call them under-authorized orders, otherwise is a correctly authorized order. 

This data exploration will help the ecommerce company move away from charge-on-delivery to an authorize-and-capture model by undertanding the price fluctuation of past orders to know the risk of doing so.

The following six questions are answered:

What percent of orders are under-authorized?

What percent of orders would be correctly authorized w/ incremental authorisation (+20%) on the amount at checkout?

Are there differences when split by country?

For the remainder of orders that would be outside of incremental auth what values would be necessary to capture the remaining amount?

Which stores are the most problematic in terms of orders and monetary value?

For under-auth orders is there a correlation between the difference in the prices and the cancellation of the order? In other words: Is an order more likely to be cancelled as the price difference increases?
